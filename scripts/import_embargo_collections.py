"""
Example script to import embargo rack collections to /repo/main.
"""
import os
import glob
import datetime
import lsst.daf.butler as daf_butler

repo_path = '/sdf/data/rubin/repo/main_20210215'

butler = daf_butler.Butler("/sdf/data/rubin/repo/main_20210215", writeable=True)

export_files = sorted(glob.glob("export_yamls/u_lsstccs_run*.yaml"))
export_files = ['export_yamls/u_lsstccs_chained_collections.yaml']

for item in export_files:
    export_file = os.path.abspath(item)
    assert os.path.isfile(export_file)
    print(datetime.datetime.now(), export_file, flush=True)
    butler.import_(directory=repo_path,
                   filename=export_file,
                   transfer=None,
                   record_validation_info=True)
