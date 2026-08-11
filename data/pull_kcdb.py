#!/usr/bin/env python3
"""Pull CMC records from the BIPM KCDB public API (no credentials needed).

    python3 pull_kcdb.py                        # KRISS chemistry/biology -> csv + json
    python3 pull_kcdb.py --countries KR JP DE   # several NMIs
    python3 pull_kcdb.py --category 4           # Gases only (see --list-categories)
    python3 pull_kcdb.py --analyte lead         # one analyte, all countries
    python3 pull_kcdb.py --list-categories

Spec: https://www.bipm.org/api/kcdb/v3/api-docs
Required body fields: metrologyAreaLabel (QM = chemistry), page, pageSize, showTable.
"""
import argparse
import csv
import json
import sys
import time
import urllib.request

BASE = "https://www.bipm.org/api/kcdb"
SEARCH = f"{BASE}/cmc/searchData/chemistryAndBiology"

FLAT = ["kcdbCode", "nmiCode", "countryValue", "categoryValue", "subCategoryValue",
        "analyteValue", "analyteMatrix", "quantityValue",
        "cmc_low", "cmc_high", "cmc_unit", "unc_low", "unc_high", "unc_unit",
        "uncertaintyMode", "coverageFactor", "confidenceLevel", "mechanism",
        "publicationDate", "status"]


def post(url, body, tries=3):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as f:
                return json.load(f)
        except Exception as ex:
            if t == tries - 1:
                raise
            print(f"  retry {t + 1}: {ex}", file=sys.stderr)
            time.sleep(2)


def get(path):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=60) as f:
        return json.load(f)


def pull(criteria, cap=6000):
    """Paginate a search. Politeness sleep between pages — this is a public service."""
    out, page, total = [], 0, None
    while True:
        body = dict(criteria, page=page, pageSize=100, showTable=True)
        d = post(SEARCH, body)
        total = d["totalElements"]
        out += d["data"]
        print(f"  page {page}: {len(out)}/{total}", file=sys.stderr)
        if not d["data"] or len(out) >= min(total, cap):
            break
        page += 1
        time.sleep(0.3)
    return out, total


def flatten(r):
    c = r.get("cmc") or {}
    u = r.get("cmcUncertainty") or {}
    row = {k: r.get(k) for k in FLAT if k in r}
    row.update(cmc_low=c.get("lowerLimit"), cmc_high=c.get("upperLimit"), cmc_unit=c.get("unit"),
               unc_low=u.get("lowerLimit"), unc_high=u.get("upperLimit"), unc_unit=u.get("unit"))
    return [row.get(k) for k in FLAT]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--countries", nargs="*", default=["KR"])
    ap.add_argument("--category", help="categoryLabel, e.g. 4 = Gases")
    ap.add_argument("--analyte", help="analyteLabel, e.g. lead (ignores --countries)")
    ap.add_argument("--out", default="kcdb_cmc")
    ap.add_argument("--list-categories", action="store_true")
    args = ap.parse_args()

    if args.list_categories:
        d = get("/referenceData/category")
        key = next(k for k, v in d.items() if isinstance(v, list))
        for r in d[key]:
            print(f"  {r['label']:>3}  {r['value']}")
        return

    crit = {"metrologyAreaLabel": "QM"}
    if args.analyte:
        crit["analyteLabel"] = args.analyte
    elif args.countries:
        crit["countries"] = args.countries
    if args.category:
        crit["categoryLabel"] = args.category
    print(f"criteria: {crit}", file=sys.stderr)

    rows, total = pull(crit)
    with open(f"{args.out}.json", "w") as f:
        json.dump(rows, f, ensure_ascii=False)
    with open(f"{args.out}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(FLAT)
        for r in rows:
            w.writerow(flatten(r))
    print(f"wrote {args.out}.csv / .json — {len(rows)} of {total} records")


if __name__ == "__main__":
    main()
