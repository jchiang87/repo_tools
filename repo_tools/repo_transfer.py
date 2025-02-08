import subprocess
import lsst.daf.butler


__all__ = ['export_chained_collections']


def mc_cp(chained_collection, src, dest):
    """Use `mc cp --recursive` command line tool to copy from src to dest."""
    command = (f"mc cp --recursive {src}/{chained_collection}/ "
               f"{dest}/{chained_collection}")
    subprocess.check_call(command, shell=True)


def export_chained_collections(butler, chains, src_dir, dest_dir,
                               export_file, collection_prefix=None,
                               do_copy=True):
    with butler.export(directory=dest_dir, filename=export_file,
                       transfer=None) as exporter:
        for chained_collection in chains:
            print(chained_collection)
            # Use `mc cp` tooling to copy to/from datastores.
            if do_copy:
                mc_cp(chained_collection, src_dir, dest_dir)
            # Get collections in chain, with optional selection on prefix.
            collections = [
                _ for _ in
                butler.registry.getCollectionChain(chained_collection)
                if (collection_prefix is None or
                    _.startswith(collection_prefix))
            ]
            for collection in collections:
                print("  ", collection, end=" ")
                refs = set()
                for ref_iter in butler.registry.queryDatasets(
                        '*', collections=collection).byParentDatasetType():
                    refs = refs.union(set(_ for _ in ref_iter))
                exporter.saveCollection(collection)
            print(len(refs), flush=True)
            exporter.saveDatasets(refs)
            exporter.saveCollection(chained_collection)


if __name__ == '__main__':
    user = "lsstccs"
    repo = "embargo"
    butler = daf_butler.Butler(repo)
    collection_prefix = f"u/{user}"
    #dest_directory = "/sdf/data/rubin/repo/main_20210215"
    dest_directory = "./repo_test"
    # Get list of chained collections:
    chains = sorted(butler.registry.queryCollections(
        f"{collection_prefix}*",
        collectionTypes=daf_butler.CollectionType.CHAINED))
