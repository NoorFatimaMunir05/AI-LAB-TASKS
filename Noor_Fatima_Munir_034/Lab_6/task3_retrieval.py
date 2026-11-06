import argparse
import csv
import json
import time
from pathlib import Path
from lab6_search import Retriever
from task2_chunks import load_docs,records

def load_queries():
    return json.loads(Path("queries.json").read_text(encoding="utf-8"))

def evaluate(engine,queries,strategy,backend,record_rows):
    hits=[];rr=[];elapsed=[]
    for question in queries:
        beginning=time.perf_counter()
        matches=engine.search(question["query"],3)
        elapsed.append(time.perf_counter()-beginning)
        relevant_rank=None
        for rank,(rec,score) in enumerate(matches,1):
            relevant=bool(question["evidence"] and rec["source_id"]==question["source_id"] and question["evidence"] in rec["text"])
            if relevant and relevant_rank is None: relevant_rank=rank
            row={"strategy":strategy,"backend":backend,"split":question["split"],"question_id":question["id"],"query":question["query"],"expected_source":question["source_id"] or "NONE","rank":rank,"chunk_id":rec["id"],"source":rec["source_id"],"source_path":rec["source_path"],"start":rec["start"],"end":rec["end"],"score":f"{score:.6f}","relevant":int(relevant),"evidence":rec["text"]}
            record_rows.append(row)
            print("TOP3",backend,strategy,question["split"],question["id"],rank,rec["id"],f"score={score:.4f}",f"offsets={rec['start']}:{rec['end']}","relevant="+str(relevant))
            print("EVIDENCE",rec["text"])
        if not matches:
            print("NO CANDIDATE",backend,strategy,question["id"])
        if question["evidence"]:
            hits.append(int(relevant_rank is not None))
            rr.append(1/relevant_rank if relevant_rank else 0.)
        else:
            print("UNANSWERABLE",question["id"],"top-ranked chunk is not automatically an answer")
    return {"hit3":sum(hits)/len(hits) if hits else None,"mrr3":sum(rr)/len(rr) if rr else None,"search_seconds":sum(elapsed),"query_count":len(queries)}

def run(backends=("tfidf","embedding")):
    docs=load_docs()
    queries=load_queries()
    assert len(docs)>=5 and sum(bool(x["evidence"]) for x in queries)>=8
    dev=[q for q in queries if q["split"]=="development"]
    test=[q for q in queries if q["split"]=="test"]
    unsupported=[q for q in queries if q["split"]=="unanswerable"]
    assert len(dev)==4 and len(test)==4 and len(unsupported)==2
    combos={}
    rows=[]
    model=None;load_secs=0.0
    if "embedding" in backends:
        try:
            from sentence_transformers import SentenceTransformer
            begin=time.perf_counter()
            model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",device="cpu")
            load_secs=time.perf_counter()-begin
            print("MODEL LOAD SECONDS",f"{load_secs:.6f}")
            print("MODEL VERSION",model.__class__.__name__,"TOKEN LIMIT",model.max_seq_length)
        except (ImportError,OSError) as error:
            print("EMBEDDING NOT RUN",type(error).__name__,str(error)[:160])
            backends=tuple(b for b in backends if b!="embedding")
    for backend in backends:
        for strategy in ("window0","window10","sentence"):
            recs=records(docs,strategy)
            engine=Retriever(recs,backend,model=model)
            nwords=sum(len(r["text"].split()) for r in recs)
            if backend=="embedding":
                lengths=engine.check_length([r["text"] for r in recs])
                print("TOKEN AUDIT",backend,strategy,"MAX",max(lengths),"LIMIT",engine.model.max_seq_length,"MIN",min(lengths))
            else:
                print("TOKEN AUDIT",backend,strategy,"MODEL TOKEN LENGTH NOT APPLICABLE")
            print("CONFIG",backend,strategy,"CHUNKS",len(recs),"WORDS INDEXED",nwords,"ENCODE/INDEX SEC",f"{engine.index_seconds:.6f}")
            d=evaluate(engine,dev,strategy,backend,rows)
            combos[(backend,strategy)]={"engine":engine,"dev":d,"num_chunks":len(recs)}
            print("DEV METRICS",backend,strategy,d)
    if not combos:
        raise RuntimeError("No search backend ran")
    pick=max(combos,key=lambda key:(combos[key]["dev"]["hit3"],combos[key]["dev"]["mrr3"],-combos[key]["num_chunks"]))
    print("SELECTED USING DEVELOPMENT ONLY",pick)
    summary={}
    for (backend,strategy),data in combos.items():
        e=data["engine"]
        held=evaluate(e,test,strategy,backend,rows)
        noanswer=evaluate(e,unsupported,strategy,backend,rows)
        summary[f"{backend}:{strategy}"]={"development":data["dev"],"held_out":held,"unanswerable":noanswer,"chunks":data["num_chunks"],"encoding_seconds":e.index_seconds,"model_load_seconds":load_secs if backend=="embedding" else 0.0}
        print("HELD OUT METRICS",backend,strategy,held)
    Path("retrieval_summary.json").write_text(json.dumps({"selected_development_only":list(pick),"results":summary},indent=2),encoding="utf-8")
    with open("retrieval_log.csv","w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=["strategy","backend","split","question_id","query","expected_source","rank","chunk_id","source","source_path","start","end","score","relevant","evidence"])
        writer.writeheader();writer.writerows(rows)
    print("EXPORTED retrieval_log.csv and retrieval_summary.json")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--backend",choices=["both","tfidf","embedding"],default="both")
    args=parser.parse_args()
    run(("tfidf","embedding") if args.backend=="both" else (args.backend,))
