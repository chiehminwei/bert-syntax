import sys
from collections import *

files=[("base","results/marvin_results_base.txt"),("large","results/marvin_results_large.txt")]
if "no_split" in sys.argv:
    files.append(("openai_gpt", "results/marvin_results_openai_gpt_no_split.txt"))
else:
    files.append(("openai_gpt", "results/marvin_results_openai_gpt.txt"))


by_model={}
conditions=set()
for title,fname in files:
    lines = open(fname)
    results=defaultdict(Counter)
    by_model[title]=results
    skipped = set()
    for line in lines:
        if line.startswith("Better speed"): continue
        if line.startswith("skipping"):
            skipped.add(line.split()[1])
            next(lines)
            continue
        res,c1,c2,w1,w2,s = line.split(None, 5)
        c1 = c1.replace("inanim","anim")
        conditions.add(c1)
        results[c1][res]+=1

print("skipped:",skipped)

print("condition & base & large & openai_gpt & count bert & count openai_gpt \\\\")
for cond in conditions:
    rb = by_model['base'][cond]
    rl = by_model['large'][cond]
    ro = by_model['openai_gpt'][cond]
    if sum(ro.values())==0:
        so = "-"
    else:
        so = "%.2f" % (ro['True']/(ro['True']+ro['False']))
    sb = "%.2f" % (rb['True']/(rb['True']+rb['False']))
    sl = "%.2f" % (rl['True']/(rl['True']+rl['False']))
    print(" & ".join(map(str,[cond, sb, sl, so, sum(rb.values()), sum(ro.values())])),"\\\\")

    


