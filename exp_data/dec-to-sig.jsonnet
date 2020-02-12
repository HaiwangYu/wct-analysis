local reality = std.extVar('reality');
local raw_input_label = std.extVar('raw_input_label');  // eg "daq"
local engine = std.extVar('engine');


local wc = import 'wirecell.jsonnet';
local g = import 'pgraph.jsonnet';


local data_params = import 'pgrapher/experiment/pdsp/params.jsonnet';
local simu_params = import 'pgrapher/experiment/pdsp/simparams.jsonnet';
local params = if reality == 'data' then data_params else simu_params;


local tools_maker = import 'pgrapher/common/tools.jsonnet';
local tools_orig = tools_maker(params);
local tools = tools_orig {
  // anodes : [tools_orig.anodes[0]],
};


local sp_maker = import 'pgrapher/experiment/pdsp/sp.jsonnet';

// Collect the WC/LS input converters for use below.  Make sure the
// "name" argument matches what is used in the FHiCL that loads this
// file.  In particular if there is no ":" in the inputer then name
// must be the emtpy string.
local wcls_input = {
  adc_digits: g.pnode({
    type: 'wclsLazyFrameSource',
    name: 'adcs',
    data: {
      art_tag: raw_input_label,
      frame_tags: ['orig'],  // this is a WCT designator
    },
  }, nin=0, nout=1),

};

// local wcls_input = {
//   adc_digits: g.pnode({
//     type: 'wclsRawFrameSource',
//     name: 'adcs',
//     data: {
//       art_tag: raw_input_label,
//       frame_tags: ['orig'],  // this is a WCT designator
//     },
//   }, nin=0, nout=1),

// };

// Collect all the wc/ls output converters for use below.  Note the
// "name" MUST match what is used in theh "outputers" parameter in the
// FHiCL that loads this file.
local mega_anode = {
  type: 'MegaAnodePlane',
  name: 'meganodes',
  data: {
    anodes_tn: [wc.tn(anode) for anode in tools.anodes],
    // anodes_tn: [wc.tn(anode) for anode in [tools.anodes[0],]],
  },
};
local wcls_output = {
  // The noise filtered "ADC" values.  These are truncated for
  // art::Event but left as floats for the WCT SP.  Note, the tag
  // "raw" is somewhat historical as the output is not equivalent to
  // "raw data".
  nf_digits: g.pnode({
    type: 'wclsFrameSaver',
    name: 'nfsaver',
    data: {
      // anode: wc.tn(tools.anode),
      anode: wc.tn(mega_anode),
      digitize: true,  // true means save as RawDigit, else recob::Wire
      frame_tags: ['raw'],
      chanmaskmaps: ['bad'],
    },
  }, nin=1, nout=1, uses=[mega_anode]),


  // The output of signal processing.  Note, there are two signal
  // sets each created with its own filter.  The "gauss" one is best
  // for charge reconstruction, the "wiener" is best for S/N
  // separation.  Both are used in downstream WC code.
  sp_signals: g.pnode({
    type: 'wclsFrameSaver',
    name: 'spsaver',
    data: {
      // anode: wc.tn(tools.anode),
      anode: wc.tn(mega_anode),
      digitize: false,  // true means save as RawDigit, else recob::Wire
      frame_tags: ['gauss', 'wiener'],
      chanmaskmaps: [],
      nticks: params.daq.nticks,  // -1 means use LS det prop svc
    },
  }, nin=1, nout=1, uses=[mega_anode]),
};

local nanodes = std.length(tools.anodes);
local anode_iota = std.range(0, nanodes - 1);
// local nanodes = 1;
// local anode_iota = std.range(0, 0);

// local perfect = import 'chndb-perfect.jsonnet';
local base = import 'pgrapher/experiment/pdsp/chndb-base.jsonnet';
local chndb = [{
  type: 'OmniChannelNoiseDB',
  name: 'ocndbperfect%d' % n,
  // data: perfect(params, tools.anodes[n], tools.field, n),
  data: base(params, tools.anodes[n], tools.field, n),
  uses: [tools.anodes[n], tools.field],  // pnode extension
} for n in anode_iota];

local nf_maker = import 'pgrapher/experiment/pdsp/nf.jsonnet';
local nf_pipes = [nf_maker(params, tools.anodes[n], chndb[n], n, name='nf%d' % n) for n in anode_iota];

local sp = sp_maker(params, tools, { sparse: true, use_roi_debug_mode: false, use_multi_plane_protection: false });
local sp_pipes = [sp.make_sigproc(a) for a in tools.anodes];

local fansel = g.pnode({
  type: 'ChannelSplitter',
  name: 'peranode',
  data: {
    anodes: [wc.tn(a) for a in tools.anodes],
    tag_rules: [{
      frame: {
        '.*': 'orig%d' % ind,
      },
    } for ind in anode_iota],
  },
}, nin=1, nout=nanodes, uses=tools.anodes);

local magnify = import 'pgrapher/experiment/pdsp/multimagnify.jsonnet';
local magoutput = 'protodune-data-check.root';

local rootfile_creation_frames = g.pnode({
  type: 'RootfileCreation_frames',
  name: 'origmag',
  data: {
    output_filename: magoutput,
    root_file_mode: 'RECREATE',
  },
}, nin=1, nout=1);

local magnify_orig = magnify('orig', tools, magoutput);
local magnify_raw = magnify('raw', tools, magoutput);
local magnify_gauss = magnify('gauss', tools, magoutput);
local magnify_thr = magnify('threshold', tools, magoutput);

local magbr_orig = magnify_orig.magnify_pipelines;
local magbr_raw = magnify_raw.magnify_pipelines;
local magbr_gauss = magnify_gauss.magnify_pipelines;
local magbr_thr = magnify_thr.magnifysummaries_pipelines;

local rio_nf = [g.pnode({
      type: 'ExampleROOTAna',
      name: 'rio_nf_apa%d' % n,
      data: {
        output_filename: "data-%d.root" % n,
        anode: wc.tn(tools.anodes[n]),
      },  
    }, nin=1, nout=1),
    for n in std.range(0, std.length(tools.anodes) - 1)
    ];

local rio_sp = [g.pnode({
      type: 'ExampleROOTAna',
      name: 'rio_sp_apa%d' % n,
      data: {
        output_filename: "data-%d.root" % n,
        anode: wc.tn(tools.anodes[n]),
      },  
    }, nin=1, nout=1),
    for n in std.range(0, std.length(tools.anodes) - 1)
    ];

    
local npy_frame_saver = [g.pnode({
      type: 'NumpyFrameSaver',
      name: 'apa%d' % n,
      data: {
        frame_tags: ["gauss%d" % n, "threshold%d" % n, "wiener%d" % n],
        filename: "data-%d.npz" % n,
      },  
    }, nin=1, nout=1),
    for n in std.range(0, std.length(tools.anodes) - 1)
    ];

local hdf5_frame_saver = [g.pnode({
      type: 'HDF5FrameTap',
      name: 'apa%d' % n,
      data: {
        anode: wc.tn(tools.anodes[n]),
        trace_tags: ['orig%d' % n
        , 'raw%d' % n
        , 'loose_lf%d' % n
        , 'tight_lf%d' % n
        , 'cleanup_roi%d' % n
        , 'break_roi_1st%d' % n
        , 'break_roi_2nd%d' % n
        , 'shrink_roi%d' % n
        , 'extend_roi%d' % n
        , 'mp_roi%d' % n
        , 'gauss%d' % n],
        filename: "data-%d.h5" % n,
        // filename: "frame.h5",
        chunk: [0, 0], // ncol, nrow
        gzip: 2,
        high_throughput: true,
      },  
    }, nin=1, nout=1),
    for n in std.range(0, std.length(tools.anodes) - 1)
    ];

local pipelines = [
  g.pipeline([
                nf_pipes[n],
                // rio_nf[n],
                sp_pipes[n],
                // npy_frame_saver[n],
                rio_sp[n],
                hdf5_frame_saver[n],
             ],
             'nfsp_pipe_%d' % n)
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

local retagger = g.pnode({
  type: 'Retagger',
  data: {
    // Note: retagger keeps tag_rules in an array to be like frame
    // fanin/fanout but only uses first element.
    tag_rules: [{
      // Retagger also handles "frame" and "trace" like
      // fanin/fanout and also "merge" separately all traces
      // like gaussN to gauss.
      frame: {
        '.*': 'retagger',
      },
      merge: {
        'gauss\\d': 'gauss',
        'wiener\\d': 'wiener',
      },
    }],
  },
}, nin=1, nout=1);


local fanpipe = g.intern(innodes=[fansel],
                         outnodes=[fanin],
                         centernodes=pipelines,
                         edges=
                         [g.edge(fansel, pipelines[n], n, 0) for n in anode_iota] +
                         [g.edge(pipelines[n], fanin, 0, n) for n in anode_iota],
                         name='fanpipe');


local sink = g.pnode({ type: 'DumpFrames' }, nin=1, nout=0);

// local graph = g.pipeline([wcls_input.adc_digits, rootfile_creation_frames, fanpipe, retagger, wcls_output.sp_signals, sink]);
local graph = g.pipeline([wcls_input.adc_digits, fanpipe, retagger, wcls_output.sp_signals, sink]);

local app = {
  type: engine,
  data: {
    edges: g.edges(graph),
  },
};

// Finally, the configuration sequence
g.uses(graph) + [app]
