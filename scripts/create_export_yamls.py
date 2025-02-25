"""
A script to create export yamls for user collections. Export files
for groups of run collections and a single file for the chained
collections alone are generated separately.

Copying of the data is done separately, i.e., the `transfer=None` option
is used in `butler.export`.
"""
import os
from collections import defaultdict
import numpy as np
import pandas as pd
import lsst.daf.butler as daf_butler
from repo_tools import export_chained_collections

repo = "embargo"
col_prefix = "u/lsstccs"
file_prefix = col_prefix.replace("/", "_")
butler = daf_butler.Butler(repo)
dest_dir = "./export_yamls"

# The number of export yaml groups should be chosen to partition the
# dataset references into memory-friendly sized imports.
num_groups = 100  # This was used for the u/lsstccs collections in embargo

# Find chained collections and write the export file.
chained_cols = sorted(set(butler.registry.queryCollections(
    f"{col_prefix}/*", collectionTypes=[daf_butler.CollectionType.CHAINED])))
export_file = f"{file_prefix}_chained_collections.yaml"
with butler.export(directory=dest_dir, filename=export_file,
                   transfer=None) as exporter:
    for collection in chained_cols:
        exporter.saveCollection(collection)

# Find the run collections.
run_cols = sorted([_ for _ in set(butler.registry.queryCollections(
    f"{col_prefix}/*", collectionTypes=[daf_butler.CollectionType.RUN]))])

# Group the collections to limit the in-memory size while importing.
# Save both the run collections and dataset references.
indexes = np.linspace(0, len(run_cols) + 1, num_groups, dtype=int)
for i, (imin, imax) in enumerate(zip(indexes[:-1], indexes[1:])):
    export_file = f"{file_prefix}_run_collections_{i:03d}.yaml"
    print(export_file, end=" ", flush=True)
    with butler.export(directory=dest_dir, filename=export_file,
                       transfer=None) as exporter:
        refs = set()
        for collection in run_cols[imin:imax]:
            for ref_iter in butler.registry.queryDatasets(
                    "*", collections=collection).byParentDatasetType():
                refs = refs.union(set(_ for _ in ref_iter))
            exporter.saveCollection(collection)
        print(len(refs), flush=True)
        exporter.saveDatasets(refs)
