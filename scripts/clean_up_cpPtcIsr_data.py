import lsst.daf.butler as daf_butler

repo = "embargo"
chained_collection = "u/jchiang/cpPtcIsr_detector_clustering_E1003_w_2024_49"

command_template = "butler --log-level WARNING prune-datasets %(repo)s --purge %(run_collection)s --datasets %(dstype)s %(run_collection)s"

butler = daf_butler.Butler(repo, writeable=True)
run_collections = butler.registry.queryCollections(
    f"{chained_collection}/*",
    collectionTypes=[daf_butler.CollectionType.RUN])

dstype = 'cpPtcIsrExp'
for run_collection in run_collections:
    refs = list(set(butler.registry.queryDatasets(
        dstype, collections=[run_collection])))
    print(run_collection, len(refs))
    butler.pruneDatasets(refs, disassociate=True, unstore=True, purge=True)

