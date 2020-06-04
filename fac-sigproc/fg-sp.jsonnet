local g = import 'pgraph.jsonnet';
local wc = import 'wirecell.jsonnet';
local hydra = import 'hydra.jsonnet';


function(params, tools, anode, override = {}) {

    local fansel = g.pnode({
    type: 'ChannelSplitter',
    name: 'fgsp_fansel_%s'%anode.name,
    data: {
        anodes: [wc.tn(a) for a in tools.anodes],
        tag_rules: [{
        frame: {
            '.*': 'raw%d' % ind,
        },
        } for ind in std.range(0, 2)],
    },
    }, nin=1, nout=3, uses=tools.anodes),

    local fanout = g.pnode({
        type:'FrameFanout',
        name:'fgsp_fanout_%s'%anode.name,
        data:{
            multiplicity:3,
            tags: [],
        }}, nin=1, nout=3),

    local roi_init_maker = import 'roi-init.jsonnet',
    local roi_init_0 = roi_init_maker(params, tools, anode, 0),
    local roi_init_1 = roi_init_maker(params, tools, anode, 1),
    local roi_init_2 = roi_init_maker(params, tools, anode, 2),

    local mp = hydra({
        type: 'ROIMultiPlane',
        name: 'mp_%s_'%anode.name,
        data: {
            tag: "raw%d"%anode.data.ident,
            intypes: ["roi_init_%d"%iplane for iplane in std.range(0, 2)],
            outtypes: ["mp3_%d"%iplane for iplane in std.range(0, 2)],
            },
        }, tags = ['raw%d'%anode.data.ident for iplane in std.range(0, 2)],
        types = ["mp3_%d"%iplane for iplane in std.range(0, 2)],
        nin = 3, nout = 3, uses=[anode]),


    local roi_final_maker = import 'roi-dnn.jsonnet',
    local roi_final_0 = roi_final_maker(params, tools, anode, 0),
    local roi_final_1 = roi_final_maker(params, tools, anode, 1),
    local roi_final_2 = roi_final_maker(params, tools, anode, 2),


    local fanin = g.pnode({
    type: 'FrameFanin',
    name: 'fgsp_sigmerge_%s'%anode.name,
    data: {
        multiplicity: 3,
        tags: [],
        tag_rules: [{
        trace: {
            ['gauss%d' % ind]: 'gauss%d' % ind,
        },
        } for ind in std.range(0, 2)],
    },
    }, nin=3, nout=1),

    fgsp : g.intern(innodes=[fanout],
        outnodes=[fanin],
        centernodes=[
            roi_init_0, roi_init_1, roi_init_2,
            mp,
            roi_final_0, roi_final_1, roi_final_2
            ],
        edges=
        [
            g.edge(fanout, roi_init_0, 0, 0),
            g.edge(fanout, roi_init_1, 1, 0),
            g.edge(fanout, roi_init_2, 2, 0),

            g.edge(roi_init_0, mp, 0, 0),
            g.edge(roi_init_1, mp, 0, 1),
            g.edge(roi_init_2, mp, 0, 2),
            
            g.edge(roi_init_0, roi_final_0, 1, 0),
            g.edge(roi_init_0, roi_final_0, 2, 2),
            g.edge(mp, roi_final_0, 0, 1),
            
            g.edge(roi_init_1, roi_final_1, 1, 0),
            g.edge(roi_init_1, roi_final_1, 2, 2),
            g.edge(mp, roi_final_1, 1, 1),
            
            g.edge(roi_init_2, roi_final_2, 1, 0),
            g.edge(roi_init_2, roi_final_2, 2, 2),
            g.edge(mp, roi_final_2, 2, 1),
            
            g.edge(roi_final_0, fanin, 0, 0),
            g.edge(roi_final_1, fanin, 0, 1),
            g.edge(roi_final_2, fanin, 0, 2),
        ],
        name='fgsp_%s_'%anode.name),
}.fgsp