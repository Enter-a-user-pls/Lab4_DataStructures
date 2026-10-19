from Student_Specific_Inputs import *
from collections import defaultdict


PRODUCTS = ["NOTEBOOK", "PEN", "USB", "HEADPHONES", "CALCULATOR"]
ABBR = {"NOTEBOOK": "NB", "PEN": "PEN", "USB": "USB", "HEADPHONES": "HP", "CALCULATOR": "CALC"}
PRICES = {"NOTEBOOK": 45, "PEN": 15, "USB": 350, "HEADPHONES": 900, "CALCULATOR": 500}


def letter_positions(text):
    return [ord(c) - ord("a") + 1 for c in text.lower() if c.isalpha()]


def quantity(index):
    """Quantity from 1 to 9 using SEED_NUM and artist letter positions."""
    return 1 + (SEED_NUM + positions[index % len(positions)]) % 9


def tag(name):
    return name.rsplit("_", 1)[1]


def show(number, label, text):
    print(f"{number}. {label}: {text}")


positions = letter_positions(FAVORITE_ARTIST)

# ---------------- generate data ----------------
customers = [f"{LAST_NAME}_C{n}" for n in range(1, 6)]
transactions = []                                   # (id, customer, product, qty, value)
plan = [(c, PRODUCTS[i]) for i, c in enumerate(customers)]          # each customer, a different product
plan.append((customers[0], PRODUCTS[1]))                            # extra purchase by C1
plan.append((customers[1], PRODUCTS[1]))                            # extra purchase by C2
plan.append(plan[0])                                                # repeated customer-product purchase
for i, (cust, prod) in enumerate(plan):
    q = quantity(i)
    transactions.append((f"TX{i + 1}", cust, prod, q, q * PRICES[prod]))

# ---------------- process data ----------------
organized = defaultdict(list)                       # {customer: [(product, qty)]}
pair_ids = defaultdict(list)
cust_total, prod_total = defaultdict(int), defaultdict(int)
for tid, cust, prod, q, val in transactions:
    organized[cust].append((prod, q))
    pair_ids[(cust, prod)].append(tid)
    cust_total[cust] += val
    prod_total[prod] += val

repeated = {pair: ids for pair, ids in pair_ids.items() if len(ids) > 1}
grand_total = sum(t[4] for t in transactions)
units = sum(t[3] for t in transactions)
ranked_cust = sorted(cust_total.items(), key=lambda kv: kv[1], reverse=True)
ranked_prod = sorted(prod_total.items(), key=lambda kv: kv[1], reverse=True)

# ---------------- output ----------------
print(f"Inputs: {LAST_NAME} | SEED_NUM={SEED_NUM} | {FAVORITE_ARTIST} | letter positions={positions}")
print("Key: C1-C5 = customers | NB=NOTEBOOK HP=HEADPHONES CALC=CALCULATOR | "
      "Prices: " + " ".join(f"{ABBR[p]}={v}" for p, v in PRICES.items()))
print("Items 1 and 4 list transactions in order TX1, TX2, ... TX8 (customer, product, xquantity)\n")

show(1, "Generated Transaction Records",
     " ".join(f"{tag(t[1])}{ABBR[t[2]]}x{t[3]}" for t in transactions))
show(2, "Organized Transaction Data",
     " ".join(f"{tag(c)}[{','.join(f'{ABBR[p]}{q}' for p, q in items)}]" for c, items in organized.items()))
(rc, rp), rids = next(iter(repeated.items()))
show(3, "Repeated/Distinct Transactions",
     f"Repeated={tag(rc)}-{ABBR[rp]} ({'&'.join(rids)}) | Distinct pairs={len(pair_ids)} of {len(transactions)}")
show(4, "Transaction Values",
     " ".join(str(t[4]) for t in transactions) + f" | Total={grand_total}")
show(5, "Customer Summaries",
     "Spent " + " ".join(f"{tag(c)}={v}" for c, v in sorted(cust_total.items())))
show(6, "Product Summaries",
     "Revenue " + " ".join(f"{ABBR[p]}={v}" for p, v in prod_total.items()))
show(7, "Ordered Results",
     "Customers " + ">".join(tag(c) for c, _ in ranked_cust) + " | Products " + ">".join(ABBR[p] for p, _ in ranked_prod))
show(8, "Overall Transaction Summary",
     f"{len(transactions)} tx, {units} units, total={grand_total}, "
     f"avg={round(grand_total / len(transactions), 1)}, top cust={tag(ranked_cust[0][0])}, "
     f"top prod={ABBR[ranked_prod[0][0]]}")
