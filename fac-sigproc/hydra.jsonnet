local g = import 'pgraph.jsonnet';
local wc = import 'wirecell.jsonnet';

function (inode, tags, types, nin=1, nout=1, uses = []) { 
    local packer = g.pnode({
            type: 'TensorPacker',
            name: 'packer_%s'%inode.type+'_%s'%inode.name,
            data: {
                multiplicity: nin
            },
        }, nin=nin, nout=1),

    local worker = g.pnode(inode,
            nin=nin, nout=nout, uses=uses),

    local unpacker = g.pnode({
            type: 'TensorSetUnpacker',
            name: 'unpacker_%s'%inode.type+'_%s'%inode.name,
            data: {
                tags: tags,
                types: types,
            },
        }, nin=1, nout=nout),
    hydra : g.intern(innodes=[packer],
            outnodes=[unpacker],
            centernodes=[worker],
            edges=
            [
                g.edge(packer, worker, 0, 0),
                g.edge(worker, unpacker, 0, 0),
            ],
            name='hydra_%s'%inode.type+'_%s'%inode.name)
}.hydra