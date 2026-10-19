from Student_Specific_Inputs import *
from collections import defaultdict


SUBJECTS = ["PROGRAMMING", "MATHEMATICS", "ELECTRONICS", "PHYSICS", "ENGLISH"]
ABBR = {"PROGRAMMING": "PROG", "MATHEMATICS": "MATH", "ELECTRONICS": "ELEC", "PHYSICS": "PHYS", "ENGLISH": "ENGL"}


def letter_positions(text):
    return [ord(c) - ord("a") + 1 for c in text.lower() if c.isalpha()]


def make_score(index):
    """Score from 60 to 100 built from SEED_NUM and artist letter positions."""
    return 60 + (SEED_NUM * 3 + positions[index % len(positions)] * 7 + index) % 41


def categorize(score):
    if score >= 90:
        return "EXC"      # Excellent
    if score >= 85:
        return "VG"       # Very Good
    if score >= 75:
        return "GOOD"
    return "PASS"         # 60-74


def tag(name):
    return name.rsplit("_", 1)[1]


def show(number, label, text):
    print(f"{number}. {label}: {text}")


positions = letter_positions(FAVORITE_ARTIST)

# ---------------- generate data ----------------
students = [f"{LAST_NAME}_S{n}" for n in range(1, 6)]
records = []
for i, (stu, subj) in enumerate([(s, j) for s in students for j in SUBJECTS]):
    records.append((stu, subj, make_score(i)))
records[7] = (records[7][0], records[7][1], None)    # incomplete record (missing score)
records.append(records[0])                           # repeated student-subject record

# ---------------- process data ----------------
organized = defaultdict(dict)                        # {subject: {student: score}} first occurrence kept
seen, repeated, incomplete = set(), [], []
for stu, subj, score in records:
    if (stu, subj) in seen:
        repeated.append((stu, subj, score))
        continue
    seen.add((stu, subj))
    if score is None:
        incomplete.append((stu, subj))
    else:
        organized[subj][stu] = score

valid = {(stu, subj): sc for subj, d in organized.items() for stu, sc in d.items()}
cat_count = defaultdict(int)
for sc in valid.values():
    cat_count[categorize(sc)] += 1

stu_scores, subj_scores = defaultdict(list), defaultdict(list)
for (stu, subj), sc in valid.items():
    stu_scores[stu].append(sc)
    subj_scores[subj].append(sc)
stu_avg = {s: round(sum(v) / len(v), 1) for s, v in stu_scores.items()}
subj_avg = {s: round(sum(v) / len(v), 1) for s, v in subj_scores.items()}

ranked_stu = sorted(stu_avg.items(), key=lambda kv: kv[1], reverse=True)
ranked_subj = sorted(subj_avg.items(), key=lambda kv: kv[1], reverse=True)
all_scores = list(valid.values())

# ---------------- output ----------------
print(f"Inputs: {LAST_NAME} | SEED_NUM={SEED_NUM} | {FAVORITE_ARTIST} | letter positions={positions}")
print(f"Key: S1-S5 = {LAST_NAME}_S1-S5 | subject order = PROG,MATH,ELEC,PHYS,ENGL | -- = missing")
print("Item 1: one group per student (S1..S5), '+' = repeated record | Item 2: one group per subject\n")

by_student = defaultdict(list)
for stu, subj, sc in records[:25]:
    by_student[stu].append("--" if sc is None else str(sc))
show(1, "Generated Performance Records",
     "|".join(",".join(v) for v in by_student.values())
     + f" +{tag(records[25][0])}{ABBR[records[25][1]]}:{records[25][2]}")
show(2, "Organized Student/Subject Data",
     "|".join(",".join(map(str, d.values())) for d in organized.values()))
show(3, "Repeated/Incomplete Records",
     f"Repeated={tag(repeated[0][0])}-{ABBR[repeated[0][1]]} | "
     f"Incomplete={tag(incomplete[0][0])}-{ABBR[incomplete[0][1]]}")
show(4, "Performance Categories",
     " ".join(f"{k}={cat_count[k]}" for k in ["EXC", "VG", "GOOD", "PASS"]) + f" ({len(valid)} valid scores)")
show(5, "Student and Subject Summaries",
     "Stu=" + ",".join(str(a) for a in stu_avg.values()) + " Sub=" + ",".join(str(a) for a in subj_avg.values()))
show(6, "Ordered Results",
     "Students " + ">".join(tag(s) for s, _ in ranked_stu) + " | Subjects " + ">".join(ABBR[s] for s, _ in ranked_subj))
print()
show("FINAL", "Student Performance Report",
     f"{len(records)} rec, {len(repeated)} rep, {len(incomplete)} inc | "
     f"avg={round(sum(all_scores) / len(all_scores), 1)} | top={tag(ranked_stu[0][0])} | "
     f"best={ABBR[ranked_subj[0][0]]} | weakest={ABBR[ranked_subj[-1][0]]}")
