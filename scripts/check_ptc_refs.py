import numpy as np
import lsst.daf.butler as daf_butler

repo = "embargo"
collections = ["u/lsstccs/ptc_E748_w_2024_35",
               "u/lsstccs/ptc_E749_w_2024_35",
               "u/lsstccs/ptc_E1113_w_2024_35",
               "u/lsstccs/ptc_E1145_w_2024_35",
               "u/lsstccs/ptc_E1188_w_2024_35",
               "u/lsstccs/ptc_E1247_w_2024_35",
               "u/lsstccs/ptc_E1258_w_2024_35",
               "u/lsstccs/ptc_E1259_w_2024_35",
               "u/lsstccs/ptc_E1335_w_2024_35",
               "u/lsstccs/ptc_E1365_w_2024_35",
               "u/lsstccs/ptc_E1364_w_2024_35",
               "u/lsstccs/ptc_E1765_w_2024_35",
               "u/lsstccs/ptc_E1920_w_2024_35",
               "u/lsstccs/ptc_E1886_w_2024_35",
               "u/lsstccs/ptc_E1881_w_2024_35",
               "u/lsstccs/ptc_E2016_w_2024_35",
               "u/lsstccs/ptc_E2237_w_2024_35"
]
butler = daf_butler.Butler(repo)
for collection in collections:
    refs = list(set(butler.registry.queryDatasets(
        "ptc", collections=collection)))
    print(collection, len(refs))
    for index in np.random.randint(0, size=5, high=len(refs)):
        assert butler.getURI(refs[index]).exists()
