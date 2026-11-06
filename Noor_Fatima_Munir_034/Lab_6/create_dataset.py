import json
from pathlib import Path

docs=json.loads(Path("corpus.json").read_text(encoding="utf-8"))
queries=json.loads(Path("queries.json").read_text(encoding="utf-8"))
for d in docs:
    n=len(d["text"].split())
    assert 150<=n<=250,(d["id"],n)
    print("DOCUMENT",d["id"],"WORDS",n)
for q in queries:
    if q["evidence"]:
        source=next(d for d in docs if d["id"]==q["source_id"])
        assert q["evidence"] in source["text"]
print("ANSWERABLE",sum(bool(q["evidence"]) for q in queries),"UNANSWERABLE",sum(not bool(q["evidence"]) for q in queries))
