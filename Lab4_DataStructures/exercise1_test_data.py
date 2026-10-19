from Student_Specific_Inputs import *
from collections import defaultdict


CATEGORIES = ["TEMPERATURE", "VOLTAGE", "CURRENT", "PRESSURE", "SPEED"]
ABBR = {"TEMPERATURE": "TEMP", "VOLTAGE": "VOLT", "CURRENT": "CURR", "PRESSURE": "PRES", "SPEED": "SPD"}


def letter_positions(text):
    """Alphabetical position (A=1 ... Z=26) of every letter in text."""
    return [ord(c) - ord("a") + 1 for c in text.lower() if c.isalpha()]


def tag(src):
    """Madrigal_T1 -> T1 (short label for the one-line output)."""
    return src.rsplit("_", 1)[1]


def show(number, label, text):
    print(f"{number}. {label}: {text}")


positions = letter_positions(FAVORITE_ARTIST)
value = lambda i: SEED_NUM + positions[i % len(positions)]

# ---------------- generate data ----------------
sources = [f"{LAST_NAME}_T{n}" for n in range(1, 6)]
records = [(src, cat, value(i)) for i, (src, cat) in enumerate(zip(sources, CATEGORIES))]
records.append((sources[0], "TEMPERATURE", value(5)))   # multiple measurements:
records.append((sources[1], "VOLTAGE", value(6)))       # two categories
records.append(records[0])                              # repeated record

# ---------------- process data ----------------
organized = defaultdict(list)                  # {(source, category): [values]}
for src, cat, val in records:
    organized[(src, cat)].append(val)

unique_records = set(records)
seen, repeated = set(), []
for rec in records:
    if rec in seen:
        repeated.append(rec)
    seen.add(rec)

by_category = defaultdict(list)
for _, cat, val in records:
    by_category[cat].append(val)
cat_avg = {c: round(sum(v) / len(v), 1) for c, v in by_category.items()}

source_totals = defaultdict(int)               # duplicates removed
for src, _, val in unique_records:
    source_totals[src] += val

ordered_cats = sorted(cat_avg.items(), key=lambda kv: kv[1], reverse=True)
ordered_srcs = sorted(source_totals.items(), key=lambda kv: kv[1], reverse=True)
all_vals = [r[2] for r in unique_records]

# ---------------- output ----------------
print(f"Inputs: {LAST_NAME} | SEED_NUM={SEED_NUM} | {FAVORITE_ARTIST} | letter positions={positions}")
print(f"Key: T1-T5 = {LAST_NAME}_T1-T5 | TEMP/VOLT/CURR/PRES/SPD = the 5 categories\n")

show(1, "Generated Test Data",
     " ".join(f"{tag(s)}{ABBR[c]}={v}" for s, c, v in records))
show(2, "Organized Test Data",
     " ".join(f"{tag(s)}{ABBR[c]}{vals}".replace(" ", "") for (s, c), vals in organized.items()))
show(3, "Repeated/Distinct Data",
     f"Repeated={tag(repeated[0][0])}{ABBR[repeated[0][1]]}={repeated[0][2]} | "
     f"Distinct={len(unique_records)} of {len(records)} records")
show(4, "Numerical/Categorical Summaries",
     "Avg " + " ".join(f"{ABBR[c]}={a}" for c, a in cat_avg.items()))
show(5, "Processed Results",
     "Source totals (no duplicates) " + " ".join(f"{tag(s)}={t}" for s, t in sorted(source_totals.items())))
show(6, "Ordered Results",
     "Avg high-low " + ">".join(ABBR[c] for c, _ in ordered_cats)
     + " | Totals high-low " + ">".join(tag(s) for s, _ in ordered_srcs))
show(7, "Final Summary",
     f"{len(records)} records, {len(unique_records)} distinct, {len(repeated)} repeated | "
     f"max={max(all_vals)} min={min(all_vals)} mean={round(sum(all_vals) / len(all_vals), 1)}")
