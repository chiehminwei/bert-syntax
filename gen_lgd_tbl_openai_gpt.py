import sys
from collections import *

files=[("base","results/lgd_results_base.txt"),("large","results/lgd_results_large.txt")]
if "no_split" in sys.argv:
    files.append(("openai_gpt", "results/lgd_results_openai_gpt_no_split.txt"))
else:
    files.append(("openai_gpt", "results/lgd_results_openai_gpt.txt"))

by_model={}
conditions=set()
nskipped=0
for title,fname in files:
    lines = open(fname)
    results=defaultdict(Counter)
    by_model[title]=results
    skipped = set()
    for line in lines:
        if line.startswith("Better speed"): continue
        if line.startswith("skipping"):
            skipped.add(line.split()[1])
            #next(lines) # no need to skip, skipped in testing
            nskipped += 1
            continue
        assert (line.strip().split()[0] in ['True','False']),line
        res,c1,_ = line.split(None, 2)
        conditions.add(c1)
        results[c1][res]+=1

print("skipped:",nskipped,len(skipped),skipped)

print("condition & base & large & openai_gpt & count bert & count openai_gpt \\\\")
for cond in conditions:
    rb = by_model['base'][cond]
    rl = by_model['large'][cond]
    ro = by_model['openai_gpt'][cond]
    sb = "%.2f" % (rb['True']/(rb['True']+rb['False']))
    sl = "%.2f" % (rl['True']/(rl['True']+rl['False']))
    so = "%.2f" % (ro['True']/(ro['True']+ro['False']))
    print(" & ".join(map(str,[cond, sb, sl, so, sum(rb.values()), sum(ro.values())])),"\\\\")

