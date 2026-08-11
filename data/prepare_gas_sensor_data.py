#!/usr/bin/env python3
"""Turn the UCI Gas Sensor Array Drift Dataset into a workshop-ready CSV.

Source : UCI ML Repository #270/#224 (CC BY 4.0)
         https://archive.ics.uci.edu/dataset/270/gas+sensor+array+drift+dataset
Cite   : Vergara, A. (2012). Gas Sensor Array Drift Dataset. UCI Machine Learning
         Repository. https://doi.org/10.24432/C5RP6W

The raw files are libsvm-style (`<class> 1:v 2:v … 128:v`), one per batch — not
something a non-programmer can open. This writes a tidy CSV with named columns.

    python3 prepare_gas_sensor_data.py --raw /path/to/Dataset [--full]

CLASS→GAS MAPPING: the official one, re-checked against the data.
UCI states "1: Ethanol; 2: Ethylene; 3: Ammonia; 4: Acetaldehyde; 5: Acetone;
6: Toluene". `--verify` confirms it by matching each class's 10-batch count vector
against the published per-gas counts, and refuses to write if it ever stops holding.

Cautionary note (a real mistake made while building this): an earlier pass read the
per-gas count table through an HTML→markdown summarizer, which reordered the table's
columns. Matching against those mis-ordered columns "proved" a different mapping and
made the official documentation look wrong. The table's columns actually follow the
gas order used in the dataset description (Ammonia, Acetaldehyde, Acetone, Ethylene,
Ethanol, Toluene); with that order everything agrees with UCI. Verify against the raw
source, not a summary of it.
"""
import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

# UCI official mapping, re-verified against the published counts; see --verify
GAS = {1: "Ethanol", 2: "Ethylene", 3: "Ammonia",
       4: "Acetaldehyde", 5: "Acetone", 6: "Toluene"}
GAS_KO = {"Acetone": "아세톤", "Acetaldehyde": "아세트알데하이드", "Ethanol": "에탄올",
          "Ethylene": "에틸렌", "Ammonia": "암모니아", "Toluene": "톨루엔"}
# UCI batch table: batch -> month IDs covered (36 months total)
MONTHS = {1: "1-2", 2: "3,4,8-10", 3: "11-13", 4: "14-15", 5: "16",
          6: "17-20", 7: "21", 8: "22-23", 9: "24,30", 10: "36"}
# published per-gas counts per batch. COLUMN ORDER = the gas order used in the
# dataset description ("Ammonia, Acetaldehyde, Acetone, Ethylene, Ethanol, Toluene"),
# NOT the order an HTML summarizer may report. Getting this wrong flips the mapping.
UCI_TABLE = {
    1: [83, 30, 70, 98, 90, 74], 2: [100, 109, 532, 334, 164, 5],
    3: [216, 240, 275, 490, 365, 0], 4: [12, 30, 12, 43, 64, 0],
    5: [20, 46, 63, 40, 28, 0], 6: [110, 29, 606, 574, 514, 467],
    7: [360, 744, 630, 662, 649, 568], 8: [40, 33, 143, 30, 30, 18],
    9: [100, 75, 78, 55, 61, 101], 10: [600] * 6,
}
UCI_COLS = ["Ammonia", "Acetaldehyde", "Acetone", "Ethylene", "Ethanol", "Toluene"]

# 8 features per sensor. k=1,2 are the steady-state pair (ΔR and its normalized
# ratio) and k=3..8 the EMA transients — the raw UCI page documents that split and
# the data agrees (k=1 ~1e4 magnitude; k=3..5 always positive = rising portion,
# k=6..8 always negative = decaying portion, checked over batch1 × 16 sensors).
# The raw page says only "three different values for α" WITHOUT naming them; the
# 0.001/0.01/0.1 figures circulate in secondary sources and are NOT verified here,
# so the columns are numbered rather than labelled with an α we cannot confirm.
FEATS = ["dR", "dR_norm", "ema_rise_1", "ema_rise_2", "ema_rise_3",
         "ema_decay_1", "ema_decay_2", "ema_decay_3"]


def read_batches(raw):
    data = {}
    for b in range(1, 11):
        f = raw / f"batch{b}.dat"
        if not f.exists():
            sys.exit(f"missing {f} — unzip the UCI Dataset.zip first")
        rows = []
        for line in f.open():
            parts = line.split()
            feats = {}
            for p in parts[1:]:
                i, v = p.split(":")
                feats[int(i)] = float(v)
            if len(feats) != 128:
                sys.exit(f"batch{b}: expected 128 features, got {len(feats)}")
            rows.append((int(float(parts[0])), feats))
        data[b] = rows
    return data


def verify_mapping(data):
    """Each class's 10-batch count vector must match exactly one UCI table column."""
    ok = True
    for cls in range(1, 7):
        got = [Counter(c for c, _ in data[b])[cls] for b in range(1, 11)]
        hits = [UCI_COLS[j] for j in range(6)
                if [UCI_TABLE[b][j] for b in range(1, 11)] == got]
        mark = "OK " if hits == [GAS[cls]] else "!! "
        if hits != [GAS[cls]]:
            ok = False
        print(f"  {mark}class {cls}: counts {got} -> {hits or 'no match'}", file=sys.stderr)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="Dataset", help="folder holding batch1..10.dat")
    ap.add_argument("--out", default="gas_sensor_drift.csv")
    ap.add_argument("--full", action="store_true",
                    help="write all 128 features (default: 32 steady-state columns)")
    ap.add_argument("--verify", action="store_true", help="only run the mapping check")
    args = ap.parse_args()

    data = read_batches(Path(args.raw))
    print("class->gas verification:", file=sys.stderr)
    if not verify_mapping(data):
        sys.exit("ERROR: class->gas mapping no longer matches the published counts — "
                 "do not ship mislabelled gases.")
    if args.verify:
        return

    keep = range(8) if args.full else range(2)          # dR, dR_norm only by default
    header = ["batch", "months", "gas", "gas_ko", "gas_no"]
    for s in range(1, 17):
        header += [f"S{s:02d}_{FEATS[k]}" for k in keep]

    n = 0
    with open(args.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for b in range(1, 11):
            for cls, feats in data[b]:
                row = [b, MONTHS[b], GAS[cls], GAS_KO[GAS[cls]], cls]
                for s in range(1, 17):
                    base = (s - 1) * 8
                    row += [feats[base + k + 1] for k in keep]
                w.writerow(row)
                n += 1
    size = Path(args.out).stat().st_size / 1e6
    print(f"wrote {args.out}: {n:,} rows x {len(header)} cols ({size:.1f} MB)")


if __name__ == "__main__":
    main()
