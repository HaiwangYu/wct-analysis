// This roi init block for signal processing

local g = import 'pgraph.jsonnet';
local wc = import 'wirecell.jsonnet';
local hydra = import 'hydra.jsonnet';

local spfilt = import 'pgrapher/experiment/pdsp/sp-filters.jsonnet';

local hf_tight_filters = ["Wiener_tight_U", "Wiener_tight_V", "Wiener_tight_W"];
local lf_tight_filters = ["ROI_tight_lf", "ROI_tight_lf", "ROI_tight_lf"];
local lf_tighter_filters = ["ROI_tighter_lf", "ROI_tighter_lf", "ROI_tighter_lf"];

function(params, tools, anode, iplane=0, override = {}) {

    local pc = tools.perchanresp_nameuses,
    
    local decon_init = hydra({
        type: 'Decon2DResponse',
        name: 'decon_init_%s_'%anode.name+'%d'%iplane,
        data: {
            anode: wc.tn(anode),
            per_chan_resp: pc.name,
            field_response: wc.tn(tools.field),
            tag: "raw%d"%anode.data.ident,
            },
        }, tags = ['raw%d' % anode.data.ident,],
        types = ['waveform', ],
        nin = 2, nout = 1, uses=[anode, tools.field] + pc.uses + spfilt),
    
    local fanout_init = g.pnode({
            type: 'TensorFanout',
            name: 'fanout_init_%s_'%anode.name+'%d'%iplane,
            data: {
                multiplicity: 2,
            },
        }, nin=1, nout=2),

    local decon_tight = hydra({
        type: 'Decon2DFilter',
        name: 'decon_tight_%s_'%anode.name+'%d'%iplane,
        data: {
            tag: "raw%d"%anode.data.ident,
            out_type: "decon_tight",
            filters: [
                "HfFilter:%s"%hf_tight_filters[iplane],
                "LfFilter:%s"%lf_tight_filters[iplane],
            ],
            },
        }, tags = ['raw%d' % anode.data.ident,],
        types = ['decon_tight', ],
        nin = 1, nout = 1, uses=[anode, tools.field] + pc.uses + spfilt),
    
    local decon_tighter = hydra({
        type: 'Decon2DFilter',
        name: 'decon_tighter_%s_'%anode.name+'%d'%iplane,
        data: {
            tag: "raw%d"%anode.data.ident,
            out_type: "decon_tight",
            filters: [
                "HfFilter:%s"%hf_tight_filters[iplane],
                "LfFilter:%s"%lf_tighter_filters[iplane],
            ],
            },
        }, tags = ['raw%d' % anode.data.ident,],
        types = ['decon_tighter', ],
        nin = 1, nout = 1, uses=[anode, tools.field] + pc.uses + spfilt),
    
    local roi_th_tight = hydra({
        type: 'ROIThreshold',
        name: 'roi_th_tight_%s_'%anode.name+'%d'%iplane,
        data: {
            tag: "raw%d"%anode.data.ident,
            input0: "decon_tight",
            input1: "decon_tighter",
            cmm: "bad",
            },
        }, tags = ['raw%d' % anode.data.ident,'raw%d' % anode.data.ident,],
        types = ['roi_tight', 'rms'],
        nin = 4, nout = 2, uses=[anode]),
    
    local roi_refine = hydra({
        type: 'ROIRefine',
        name: 'roi_refine_%s_'%anode.name+'%d'%iplane,
        data: {
            tag: "raw%d"%anode.data.ident,
            },
        }, tags = ['raw%d' % anode.data.ident,],
        types = ['roi%d'%anode.data.ident,],
        nin = 2, nout = 1, uses=[anode]),

    local unpacker_in = g.pnode({
            type: 'TensorSetUnpacker',
            name: 'unpacker_in_%s_'%anode.name+'%d'%iplane,
            data: {
                tags: ['raw%d' % anode.data.ident, 'raw%d' % anode.data.ident, 'raw%d' % anode.data.ident, 'raw%d' % anode.data.ident],
                types: ['waveform', 'channels', 'bad:cmm_range', 'bad:cmm_channel'],
            },
        }, nin=1, nout=4),

    local packer_out = g.pnode({
            type: 'TensorPacker',
            name: 'packer_out_%s_'%anode.name+'%d'%iplane,
            data: {
                multiplicity: 1,
            },
        }, nin=1, nout=1),
    
    make_roi_init() :: g.intern(innodes=[unpacker_in],
        outnodes=[packer_out],
        centernodes=[decon_init, fanout_init, decon_tight, decon_tighter, roi_th_tight, roi_refine],
        edges=
        [
            g.edge(unpacker_in, decon_init, 0, 0),
            g.edge(unpacker_in, decon_init, 1, 1),
            g.edge(decon_init, fanout_init, 0, 0),
            g.edge(fanout_init, decon_tight, 0, 0),
            g.edge(fanout_init, decon_tighter, 1, 0),

            g.edge(unpacker_in, roi_th_tight, 2, 0),
            g.edge(unpacker_in, roi_th_tight, 3, 1),
            g.edge(decon_tight, roi_th_tight, 0, 2),
            g.edge(decon_tighter, roi_th_tight, 0, 3),

            g.edge(roi_th_tight, roi_refine, 0, 0),
            g.edge(roi_th_tight, roi_refine, 1, 1),
            g.edge(roi_refine, packer_out, 0, 0),
        ],
        name='roi_init_%s_'%anode.name+'%d'%iplane),
}
