from repo_tools import export_chained_collection

repo = "dp1"
parent_chain = "LSSTComCam/runs/DRP/DP1/v29_0_0/DM-50260"

butler = export_chained_collection(repo, parent_chain)

