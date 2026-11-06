import json
import re
from pathlib import Path

def windows(text, size=40, overlap=0):
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Invalid size or overlap")
    spans = list(re.finditer(r"\S+",text))
    result = []
    for i in range(0,len(spans),size-overlap):
        part = spans[i:i+size]
        if not part:
            break
        result.append((part[0].start(),part[-1].end()))
        if i+size >= len(spans):
            break
    return result

def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("Invalid size")
    spans = list(re.finditer(r"[^.!?]+(?:[.!?]+|$)",text))
    output=[]
    current=[]
    words=0
    for span in spans:
        n = len(span.group().split())
        if not n:
            continue
        if n>size:
            if current:
                output.append((current[0].start(),current[-1].end()))
                current=[]; words=0
            for a,b in windows(span.group(),size,0):
                output.append((span.start()+a,span.start()+b))
            continue
        if current and words+n>size:
            output.append((current[0].start(),current[-1].end()))
            current=[];words=0
        current.append(span);words+=n
    if current:
        output.append((current[0].start(),current[-1].end()))
    return [(a,b) for a,b in output if text[a:b].strip()]

def load_docs(path="corpus.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def records(docs,strategy):
    all_records=[]
    for d in docs:
        text=d["text"]
        if strategy=="window0": spans=windows(text,40,0)
        elif strategy=="window10": spans=windows(text,40,10)
        elif strategy=="sentence": spans=sentence_chunks(text,40)
        else: raise ValueError("Invalid strategy")
        for index,(start,end) in enumerate(spans):
            rec={"id":f"{d['id']}:{strategy}:{index}","source_id":d['id'],"source_path":d['source'],"start":start,"end":end,"text":text[start:end].strip()}
            assert rec["text"]==text[start:end].strip()
            all_records.append(rec)
    return all_records

def stats(docs,queries,strategy):
    chunks=records(docs,strategy)
    count=sum(len(r["text"].split()) for r in chunks)
    original=sum(len(d["text"].split()) for d in docs)
    retained=sum(any(r["source_id"]==q["source_id"] and q["evidence"] in r["text"] for r in chunks) for q in queries if q["evidence"])
    return {"chunks":len(chunks),"sizes":[len(r["text"].split()) for r in chunks],"repeated_words":count-original,"evidence_coverage":f"{retained}/{sum(bool(q['evidence']) for q in queries)}"}

if __name__ == "__main__":
    docs=load_docs()
    queries=json.loads(Path("queries.json").read_text(encoding="utf-8"))
    for d in docs: print("DOCUMENT",d["id"],"WORDS",len(d["text"].split()))
    for strat in ["window0","window10","sentence"]:
        print("STRATEGY",strat,stats(docs,queries,strat))
    print("EMPTY",windows(""),sentence_chunks(""))
    print("SHORT",windows("small text"),sentence_chunks("small text"))
    try:
        windows("a b c",40,40)
    except ValueError as exc:
        print("INVALID OVERLAP",exc)
    print("LONG SENTENCE",sentence_chunks("word "*85,40))
    print("ABBREVIATION",sentence_chunks("Dr. Malik approved it. Students should ask first.",40))
