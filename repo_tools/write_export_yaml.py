"""
Create export yaml files for a parent chain and its linked run collections.
Tagged and calibration collections will need to be exported separately.
"""
import os
from pprint import pprint
from itertools import pairwise
import numpy as np
import lsst.daf.butler as daf_butler


__all__ = ["write_export_yaml", "export_chained_collection"]


def write_export_yaml(butler, collections, yaml_folder, outfile, verbose=True):
    if verbose:
        print("Processing collections:")
    refs = set()
    for collection in collections:
        print("  ", collection, flush=True)
        for ref_iter in butler.registry.queryDatasets(
            "*", collections=[collection]
        ).byParentDatasetType():
            refs = refs.union(set(_ for _ in ref_iter))
    refs = list(refs)
    if verbose:
        print("  # refs:", len(refs), flush=True)

    with butler.export(
        directory=yaml_folder, filename=outfile, transfer=None
    ) as exporter:
        exporter.saveDatasets(refs)
        for collection in collections:
            exporter.saveCollection(collection)


def export_chained_collection(repo, parent_chain, chain_id=None, ntranche=10,
                              yaml_folder="./export_yamls", verbose=True):
    butler = daf_butler.Butler(repo, collections=[parent_chain])
    if chain_id is None:
        chain_id = parent_chain.replace("/", "_")

    # Get list of run collections specific to this parent chain, assuming
    # the processing used the {parent_chain}/{timestamp} collection naming
    # convention.
    run_collections = butler.registry.queryCollections(
        f"{parent_chain}/20*", collectionTypes=[daf_butler.CollectionType.RUN]
    )
    num_collections = len(run_collections)
    if verbose:
        print(f"{num_collections} found:")
        pprint(run_collections)

    # Create export yaml files, partitioning the run collections into
    # at most ntranches.
    os.makedirs(yaml_folder, exist_ok=True)
    ntranche = min(num_collections, ntranche)
    indexes = np.linspace(0, num_collections, ntranche + 1, dtype=int)
    for i, (imin, imax) in enumerate(pairwise(indexes)):
        outfile = f"{chain_id}_{i:03d}_runs.yaml"
        write_export_yaml(butler, run_collections[imin:imax], yaml_folder,
                          outfile)

    # Export yaml for the parent chain.
    export_yaml_file = f"{chain_id}_parent.yaml"
    with butler.export(directory=yaml_folder, filename=export_yaml_file,
                       transfer=None) as exporter:
        exporter.saveCollection(parent_chain)

    return butler
