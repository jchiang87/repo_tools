import sys

log_file = sys.argv[1]

scale_factor = {"KiB": 1024,
                "MiB": 1024**2,
                "GiB": 1024**3,
                "TiB": 1024**4}

total = 0
with open(log_file) as fobj:
    for line in fobj:
        if not line.strip():
            continue
        tokens = line.strip().split('\t')
        unit = tokens[0][-3:]
        if unit not in scale_factor:
            continue
        value = float(tokens[0][:-3])
        total += value*scale_factor[unit]
print(total/scale_factor['TiB'], 'TiB')

