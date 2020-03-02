local reality = std.extVar('reality');
local engine = std.extVar('engine');


local wc = import 'wirecell.jsonnet';
local g = import 'pgraph.jsonnet';

local data_params = import 'pgrapher/experiment/pdsp/params.jsonnet';
local simu_params = import 'pgrapher/experiment/pdsp/simparams.jsonnet';
local params = if reality == 'data' then data_params else simu_params;


local tools_maker = import 'pgrapher/common/tools.jsonnet';
local tools_orig = tools_maker(params);
local tools = tools_orig {
  anodes : [tools_orig.anodes[0],tools_orig.anodes[1]],
  // anodes : [tools_orig.anodes[0]],
};

local nanodes = std.length(tools.anodes);
local anode_iota = std.range(0, nanodes - 1);
// local nanodes = 1;
// local anode_iota = std.range(0, 0);

local hio_source = [g.pnode({
      type: 'HDF5FrameSource',
      name: 'hio_source%d' % n,
      data: {
        anode: wc.tn(tools.anodes[n]),
        filelist: ["input/orig-%d.h5"%n],
        policy: "",
        sequence_max: 10,
      },  
    }, nin=1, nout=1, uses=[tools.anodes[n]]),
    for n in std.range(0, std.length(tools.anodes) - 1)
    ];

local hio_orig = [g.pnode({
      type: 'HDF5FrameTap',
      name: 'hio_orig%d' % n,
      data: {
        anode: wc.tn(tools.anodes[n]),
        trace_tags: ['orig%d' % n],
        filename: "out-%d.h5" % n,
        chunk: [0, 0], // ncol, nrow
        gzip: 2,
        high_throughput: false,
      },  
    }, nin=1, nout=1),
    for n in std.range(0, std.length(tools.anodes) - 1)
    ];

local pipelines = [
  g.pipeline([
              hio_source[n],
              hio_orig[n],
             ],
             'hio_pipe_%d' % n)
  for n in anode_iota
];

local fanin = g.pnode({
  type: 'FrameFanin',
  name: 'sigmerge',
  data: {
    multiplicity: nanodes,
    tags: [],
    tag_rules: [{
      trace: {
        ['gauss%d' % ind]: 'gauss%d' % ind,
        ['wiener%d' % ind]: 'wiener%d' % ind,
        ['threshold%d' % ind]: 'threshold%d' % ind,
      },
    } for ind in anode_iota],
  },
}, nin=nanodes, nout=1);

local fanpipe = g.intern(innodes=[],
                         outnodes=[fanin],
                         centernodes=pipelines,
                         edges=
                         [g.edge(pipelines[n], fanin, 0, n) for n in anode_iota],
                         name='fanpipe');


local sink = g.pnode({ type: 'DumpFrames' }, nin=1, nout=0);

local graph = g.pipeline([fanpipe, sink]);

local app = {
  type: engine,
  data: {
    edges: g.edges(graph),
  },
};


local cmdline = { 
    type: "wire-cell",
    data: {
        plugins: ["WireCellGen", "WireCellPgraph", "WireCellTbb", "WireCellHio"],
        apps: [engine]
    }   
};

// Finally, the configuration sequence
[cmdline] + g.uses(graph) + [app]
