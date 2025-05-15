import os
import glob
import lsst.daf.butler as daf_butler

# The full path to the repo on disk, e.g., /global/cfs/cdirs/lsst/production/gen3/DC2-Run2.2i
dest_repo_path =
butler = daf_butler.Butler(dest_repo_path, writeable=True)

# Folder containing the export yaml files.
yaml_folder =

# Do parent collections last.
export_files = sorted(_ for _ in glob.glob(f"{yaml_folder}/*.yaml") if "parent" not in _)
export_files.extend(sorted(glob.glob(f"{yaml_folder}/*parent.yaml")))
for export_file in export_files:
    print(export_file, flush=True)
    butler.import_(directory=dest_repo_path,
                   filename=export_file,
                   transfer=None,
                   record_validation_info=True)
