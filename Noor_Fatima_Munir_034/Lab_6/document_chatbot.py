import json
from pathlib import Path
from lab6_search import Retriever
from task2_chunks import load_docs,records

def selected():
    config=json.loads(Path("retrieval_summary.json").read_text(encoding="utf-8"))
    return config["selected_development_only"]

def start():
    backend,strategy=selected()
    retriever=Retriever(records(load_docs(),strategy),backend)
    print("Document assistant: sourced evidence suggestions, not automatic policy decisions.")
    print("Backend",backend,"strategy",strategy,"type exit to stop")
    while True:
        try: query=input("Question: ")
        except (EOFError,KeyboardInterrupt):break
        if query.strip().lower()=="exit":break
        if not query.strip():
            print("Please enter a question.")
            continue
        hits=retriever.search(query,3)
        if not hits:
            print("No supported passage found. Please contact the relevant office.")
            continue
        print("These are candidate passages; none is automatically confirmed as an answer.")
        for index,(rec,score) in enumerate(hits,1):
            print(index,rec["id"],f"score={score:.4f}",f"source={rec['source_path']}",f"offsets={rec['start']}:{rec['end']}")
            print(rec["text"])
        try: confirm=input("Does any passage answer your question? Enter its number or n: ").strip().lower()
        except (EOFError,KeyboardInterrupt):break
        if confirm in ("1","2","3") and int(confirm)<=len(hits):
            record=hits[int(confirm)-1][0]
            print("Confirmed evidence only:",record["text"],f"[source: {record['source_path']}, offset {record['start']}:{record['end']}]")
        else:
            print("No supported answer confirmed. Ask a member of staff.")

if __name__=="__main__":
    start()
