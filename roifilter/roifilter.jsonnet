// This is a main entry point for configuring a wire-cell CLI job to
// simulate protoDUNE-SP.  It is simplest signal-only simulation with
// one set of nominal field response function.  It excludes noise.
// The kinematics are a mixture of Ar39 "blips" and some ideal,
// straight-line MIP tracks.
//
// Output is a Python numpy .npz file.
local g = import 'pgraph.jsonnet';
local f = import 'pgrapher/common/funcs.jsonnet';
local wc = import 'wirecell.jsonnet';
local io = import 'pgrapher/common/fileio.jsonnet';
local tools_maker = import 'pgrapher/common/tools.jsonnet';
local params = import 'pgrapher/experiment/pdsp/simparams.jsonnet';
local tools_orig = tools_maker(params);
local tools = tools_orig {
//   anodes : [tools_orig.anodes[0],tools_orig.anodes[1]],
};
local sim_maker = import 'pgrapher/experiment/pdsp/sim.jsonnet';
local sim = sim_maker(params, tools);
local stubby = {
  tail: wc.point(1000.0, 3.0, 100.0, wc.mm),
  head: wc.point(1100.0, 3.0, 200.0, wc.mm),
};
// Something close to APA 0 (smallest Y,Z)
local close0 = {
  tail: wc.point(-3.000, 3.0, 1.000, wc.m),
  head: wc.point(-3.000, 3.0, 2.000, wc.m),
};
local parallel = {
  tail: wc.point(-1.000, 3.0, 1.000, wc.m),
  head: wc.point(-1.000, 3.0, 2.000, wc.m),
};
local apa6 = {
  tail: wc.point(0.5, 4, 2.4, wc.m),
  head: wc.point(3.5, 2, 4.5, wc.m),
};
local cathpier = {
  tail: wc.point(-113, 585, 409, wc.cm),
  head: wc.point( 118,  24, 269, wc.cm),
};
local tracklist = [
  {
    time: 0 * wc.us, 
    charge: -2500, // 5000 e/mm
    ray: parallel,
  },
  {
    time: 0 * wc.us,
    charge: -2500, // 5000 e/mm
    ray: cathpier,
  },
  {
    time: 0 * wc.us,
    charge: -7500, // 15000 e/mm
    ray: apa6,
  },
];
local output = 'wct-sim-ideal-sig.npz';
//local depos = g.join_sources(g.pnode({type:"DepoMerger", name:"BlipTrackJoiner"}, nin=2, nout=1),
//                             [sim.ar39(), sim.tracks(tracklist)]);
local depos = sim.tracks(tracklist, step=0.5 * wc.mm);
//local deposio = io.numpy.depos(output);
local drifter = sim.drifter;
local bagger = sim.make_bagger();
// signal plus noise pipelines
//local sn_pipes = sim.signal_pipelines;
local sn_pipes = sim.splusn_pipelines;
local multimagnify = import 'pgrapher/experiment/pdsp/multimagnify.jsonnet';
local magoutput = 'protodune-sim-check.root';
// please remove the root file before you generate a new one
// local rootfile_creation_depos = g.pnode({
//   type: 'RootfileCreation_depos',
//   name: 'origmag',
//   data: {
//     output_filename: magoutput,
//     root_file_mode: 'RECREATE',
//   },
// }, nin=1, nout=1);
local multi_magnify = multimagnify('orig', tools, magoutput);
local magnify_pipes = multi_magnify.magnify_pipelines;
local multi_magnify2 = multimagnify('raw', tools, magoutput);
local magnify_pipes2 = multi_magnify2.magnify_pipelines;
local multi_magnify3 = multimagnify('gauss', tools, magoutput);
local magnify_pipes3 = multi_magnify3.magnify_pipelines;
local multi_magnify4 = multimagnify('wiener', tools, magoutput);
local magnify_pipes4 = multi_magnify4.magnify_pipelines;
local multi_magnify5 = multimagnify('threshold', tools, magoutput);
local magnify_pipes5 = multi_magnify5.magnifysummaries_pipelines;
local multi_magnify6 = multimagnify('roi', tools, magoutput);
local magnify_pipes6 = multi_magnify6.magnify_pipelines;
local perfect = import 'pgrapher/experiment/pdsp/chndb-base.jsonnet';
local chndb = [{
  type: 'OmniChannelNoiseDB',
  name: 'ocndbperfect%d' % n,
  data: perfect(params, tools.anodes[n], tools.field, n),
  uses: [tools.anodes[n], tools.field],  // pnode extension
} for n in std.range(0, std.length(tools.anodes) - 1)];
//local chndb_maker = import 'pgrapher/experiment/pdsp/chndb.jsonnet';
//local noise_epoch = "perfect";
//local noise_epoch = "after";
//local chndb_pipes = [chndb_maker(params, tools.anodes[n], tools.fields[n]).wct(noise_epoch)
//                for n in std.range(0, std.length(tools.anodes)-1)];
local nf_maker = import 'pgrapher/experiment/pdsp/nf.jsonnet';
// local nf_pipes = [nf_maker(params, tools.anodes[n], chndb_pipes[n]) for n in std.range(0, std.length(tools.anodes)-1)];
local nf_pipes = [nf_maker(params, tools.anodes[n], chndb[n], n, name='nf%d' % n) for n in std.range(0, std.length(tools.anodes) - 1)];
local sp_maker = import 'pgrapher/experiment/pdsp/sp.jsonnet';
local sp = sp_maker(params, tools);
local sp_pipes = [sp.make_sigproc(a) for a in tools.anodes];
//local parallel_pipes = [g.pipeline([sn_pipes[n], magnify_pipes[n],
//                                nf_pipes[n], magnify_pipes2[n] ], "parallel_pipe_%d"%n)
//                    for n in std.range(0, std.length(tools.anodes)-1)];
local roi_filter = [g.pnode({
type: 'RegionOfInterestFilter',  //parameter to configure the node (type and name pair should be unique)
name: 'roi_filter%d' % n,
data: {
  roi_tag: 'roi%d' % n
}, 
}, nin=1, nout=1, uses=[]),
for n in std.range(0, std.length(tools.anodes) - 1) //tools.anodes sono le linee parallele del grafico
];

local sn_pipe = [
  g.pipeline([
               sn_pipes[n],
               magnify_pipes[n],
             ],
             'sn_pipe_%d' % n)
  for n in std.range(0, std.length(tools.anodes) - 1)];

local nfsp_pipe = [
  g.pipeline([
               nf_pipes[n],
               magnify_pipes2[n],
               sp_pipes[n],
               magnify_pipes3[n],
               magnify_pipes4[n],
               magnify_pipes5[n],
             ],
             'nfsp_pipe_%d' % n)
  for n in std.range(0, std.length(tools.anodes) - 1)];

local roifilter_pipe = [
  g.pipeline([
               roi_filter[n],
               magnify_pipes6[n],
             ],
             'roifilter_pipe_%d' % n)
  for n in std.range(0, std.length(tools.anodes) - 1)];

local frame_fanout = [g.pnode({
    type:'FrameFanout',
    name:'frame_fanout-%d'%n,
    data:{
        multiplicity:2,
        tag_rules: [  // example in gen/test/test_fans.jsonnet
          {
            frame: {
              '.*': 'orig%d' % n,
            },
          }
        ],
    }}, nin=1, nout=2) for n in std.range(0, std.length(tools.anodes) - 1)];

local frame_fanin = [g.pnode({
    type: 'FrameFanin',
    name: 'frame_fanin-%d'%n,
    data: {
        multiplicity: 2, 
        tags: [],
    }}, nin=2, nout=1) for n in std.range(0, std.length(tools.anodes) - 1)];

local nfsp_roifilter = [g.intern(innodes=[frame_fanout[n]], centernodes=[nfsp_pipe[n], roifilter_pipe[n]], outnodes=[frame_fanin[n],],
                     edges = [
                       g.edge(frame_fanout[n], nfsp_pipe[n], 0, 0),
                       g.edge(frame_fanout[n], roifilter_pipe[n], 1, 0),
                       g.edge(nfsp_pipe[n], frame_fanin[n], 0, 0),
                       g.edge(roifilter_pipe[n], frame_fanin[n], 0, 1),]) for n in std.range(0, std.length(tools.anodes) - 1)];

local parallel_pipes = [
  g.pipeline([
               sn_pipe[n],
               nfsp_roifilter[n],
             ],
             'roifilter_pipe_%d' % n)
  for n in std.range(0, std.length(tools.anodes) - 1)];

local outtags = ['raw%d' % n for n in std.range(0, std.length(tools.anodes) - 1)];
local parallel_graph = f.fanpipe('DepoSetFanout', parallel_pipes, 'FrameFanin', 'sn_mag_nf', outtags);
//local frameio = io.numpy.frames(output);
local sink = sim.frame_sink;
// local graph = g.pipeline([depos, rootfile_creation_depos, drifter, bagger, parallel_graph, sink]);
local graph = g.pipeline([depos, drifter, bagger, parallel_graph, sink]);
local app = {
  type: 'Pgrapher',
  data: {
    edges: g.edges(graph),
  },
};
local cmdline = {
    type: "wire-cell",
    data: {
        plugins: ["WireCellGen", "WireCellPgraph", "WireCellSio", "WireCellSigProc", "WireCellRoot"],
        apps: ["Pgrapher"]
    }
};
// Finally, the configuration sequence which is emitted.
[cmdline] + g.uses(graph) + [app]
