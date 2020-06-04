
local g = import 'pgraph.jsonnet';
local wc = import 'wirecell.jsonnet';
local hydra = import 'hydra.jsonnet';

function(params, tools, anode, iplane=0, override = {}) {

    local roidnn = hydra({
        type: 'ROIDNN',
        name: 'roi_dnn_roidnn_%s_'%anode.name+'%d'%iplane,
        data: {
            tag: "raw%d"%anode.data.ident,
            intypes: ["decon_loose_%d"%iplane,"mp3_%d"%iplane, "decon_charge_%d"%iplane],
            outtypes: ["waveform"],
            },
        }, tags = ['raw%d' % anode.data.ident,],
        types = ["waveform"],
        nin = 3, nout = 1, uses=[anode]),
    
    local tt2f = g.pnode({
        type: 'TaggedTensorSetFrame',
        name: 'roi_dnn_tt2f_%s_'%anode.name+'%d'%iplane,
        data: {
            "tensors": [
                {"tag": "raw%d"%anode.data.ident},
            ],
        },  
        }, nin=1, nout=1),
    
    ret : g.intern(innodes=[roidnn,],
        outnodes=[tt2f],
        centernodes=[],
        edges=
        [
            g.edge(roidnn, tt2f, 0, 0),
        ],
        name='roi_dnn_%s_'%anode.name+'%d'%iplane,),
}.ret