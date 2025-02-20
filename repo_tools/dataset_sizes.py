import os
from collections import defaultdict
import numpy as np
import pandas as pd
import lsst.daf.butler as daf_butler
import lsst.pipe.base as pipe_base


__all__ = ['get_dstype_map', 'get_dataset_sizes']


def get_dstype_map(qg_file):
    """
    Return a dictionary of dataset types, keyed by task, from a QuantumGraph.
    """
    qg = pipe_base.QuantumGraph.loadUri(qg_file)
    dsmap = defaultdict(set)
    for node in qg.graph.nodes:
        task = node.taskDef.label
        for output in node.quantum.outputs.keys():
            dstype = output.name
            dsmap[task].add(dstype)
    return dict(dsmap)


def get_dataset_sizes(butler, dsmap, limit=None, nsamp=None):
    """
    Extract mean, median, and maximum dataset sizes from a repo.
    """
    data = defaultdict(list)
    for task, dstypes in dsmap.items():
        for dstype in dstypes:
            print(task, dstype, flush=True)
            try:
                refs = butler.query_datasets(dstype, limit=limit)
            except daf_butler.EmptyQueryResultError:
                continue
            if None in (nsamp, limit) or nsamp > len(refs):
                target_refs = refs
            else:
                target_refs = np.random.choice(refs, replace=False, size=nsamp)
            sizes = [os.path.getsize(butler.getURI(ref).path)
                     for ref in target_refs]
            data['task'].append(task)
            data['dstype'].append(dstype)
            data['mean'].append(np.mean(sizes))
            data['median'].append(np.median(sizes))
            data['max'].append(np.max(sizes))
    return pd.DataFrame(data)
