import re, json
S="/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/"
pages=open(S+"thesis_lay.txt").read().split("\f")
HEAD=re.compile(r"^\d+\.\d+(\.\d+)*\s+[A-Z]")
def blocks(pg_from, pg_to):
    out=[]
    for pi in range(pg_from-1, pg_to):
        lines=[l.rstrip() for l in pages[pi].splitlines()]
        # drop page-number-only lines
        lines=[l for l in lines if not re.fullmatch(r"\s*(\d+|[ivx]+)\s*", l)]
        cur=[]
        page_blocks=[]
        for l in lines+[""]:
            if l.strip()=="":
                if cur: page_blocks.append(cur); cur=[]
            else: cur.append(l.strip())
        first=True
        for b in page_blocks:
            text=""
            for ln in b:
                text = text + ln if text.endswith("-") and not text.endswith(" -") else (text + " " + ln if text else ln)
            text=re.sub(r"\s+"," ",text)
            if first and out and out[-1]["t"]=="p" and text[:1].islower():
                out[-1]["x"]+=" "+text
            else:
                kind="h" if (len(b)==1 and HEAD.match(text) and len(text)<95 and not text.endswith(".")) else "p"
                out.append({"t":kind,"x":text,"pg":pi+1})
            first=False
    return out
if __name__=="__main__":
    import sys
    a,b=int(sys.argv[1]),int(sys.argv[2])
    bl=blocks(a,b)
    json.dump(bl,open(S+f"blocks_{a}_{b}.json","w"),indent=1)
    for i,x in enumerate(bl): print(i,x["t"],x["pg"],x["x"][:90])
