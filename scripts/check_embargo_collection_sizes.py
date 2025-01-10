import subprocess

bucket_name = "embargo/rubin-summit-users"
#top_folder = "u/jchiang"
#top_folder = "LSSTCam/calib"
top_folder = "u/lsstccs"

# List all sub-folders
subfolders = []
command = f"mc ls {bucket_name}/{top_folder}"
lines = subprocess.check_output(command, shell=True, encoding="utf-8").split('\n')
for item in lines:
    if not item:
        continue
    subfolders.append(item.split()[-1])

for subfolder in subfolders:
    command = f"mc du {bucket_name}/{top_folder}/{subfolder}"
    subprocess.check_call(command, shell=True, encoding="utf-8")
