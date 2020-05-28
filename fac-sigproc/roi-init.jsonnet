// This roi init block for signal processing

local g = import 'pgraph.jsonnet';
local wc = import 'wirecell.jsonnet';

local spfilt = import 'pgrapher/experiment/pdsp/sp-filters.jsonnet';

local hf_tight_filters = ["Wiener_tight_U", "Wiener_tight_V", "Wiener_tight_W"];
local lf_tight_filters = ["ROI_tight_lf", "ROI_tight_lf", "ROI_tight_lf"];
local lf_tighter_filters = ["ROI_tighter_lf", "ROI_tighter_lf", "ROI_tighter_lf"];

function(params, tools, anode, iplane=0, override = {}) {

    local pc = tools.perchanresp_nameuses,

    local unpacker_in = g.pnode({
            type: 'TensorSetUnpacker',
            name: 'unpacker_in_%s_'%anode.name+'%d'%iplane,
            data: {
                tags: ['raw%d' % anode.data.ident, 'raw%d' % anode.data.ident, 'raw%d' % anode.data.ident, 'raw%d' % anode.data.ident],
                types: ['waveform', 'channels', 'bad:cmm_range', 'bad:cmm_channel'],
            },
        }, nin=1, nout=4),

    local packer_init = g.pnode({
            type: 'TensorPacker',
            name: 'packer_init_%s_'%anode.name+'%d'%iplane,
            data: {
                multiplicity: 2
            },
        }, nin=2, nout=1),

    local decon_init = g.pnode({
        type: 'Decon2DResponse',
        name: 'decon_init_%s_'%anode.name+'%d'%iplane,
        data: {
            anode: wc.tn(anode),
            per_chan_resp: pc.name,
            field_response: wc.tn(tools.field),
            tag: "raw%d"%anode.data.ident,
            },
            }, nin=1, nout=1, uses=[anode, tools.field] + pc.uses + spfilt),

    local unpacker_init = g.pnode({
            type: 'TensorSetUnpacker',
            name: 'unpacker_init_%s_'%anode.name+'%d'%iplane,
            data: {
                tags: ['raw%d' % anode.data.ident, 'raw%d' % anode.data.ident],
                types: ['waveform', 'channels'],
            },
        }, nin=1, nout=2),

    local packer_tight = g.pnode({
            type: 'TensorPacker',
            name: 'packer_tight_%s_'%anode.name+'%d'%iplane,
            data: {
                multiplicity: 4
            },
        }, nin=4, nout=1),

    local decon_tight = g.pnode({
        type: 'Decon2DFilter',
        name: 'decon_tight0_%s_'%anode.name+'%d'%iplane,
        data: {
            tag: "raw%d"%anode.data.ident,
            filters: [
                "HfFilter:%s"%hf_tight_filters[iplane],
                "LfFilter:%s"%lf_tight_filters[iplane],
            ],
            },
            }, nin=1, nout=1, uses=[] + spfilt),

    make_roi_init() :: g.intern(innodes=[unpacker_in,],
        outnodes=[decon_tight,],
        centernodes=[packer_init,decon_init,unpacker_init,packer_tight,],
        edges=
        [
            g.edge(unpacker_in, packer_init, 0, 0),
            g.edge(unpacker_in, packer_init, 1, 1),
            g.edge(packer_init, decon_init, 0, 0),
            g.edge(decon_init, unpacker_init, 0, 0),
            g.edge(unpacker_init, packer_tight, 0, 0),
            g.edge(unpacker_init, packer_tight, 1, 1),
            g.edge(unpacker_in, packer_tight, 2, 2),
            g.edge(unpacker_in, packer_tight, 3, 3),
            g.edge(packer_tight, decon_tight, 0, 0),
        ],
        name='roi_init_%s_'%anode.name+'%d'%iplane),
}
