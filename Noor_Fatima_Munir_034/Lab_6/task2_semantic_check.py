import json
from task2_chunks import load_docs,records
from lab6_search import Retriever,show_hits

queries=["I missed the deadline due to illness","I lost my login credentials","Can I pay tuition in installments?"]
recs=records(load_docs(),"sentence")
for backend in ["tfidf","embedding"]:
    print("BACKEND",backend)
    try:
        retriever=Retriever(recs,backend)
    except (ImportError,OSError) as error:
        print("NOT RUN",backend,type(error).__name__,str(error)[:160])
        continue
    print("MODEL LOAD",retriever.model_load_seconds)
    for query in queries:
        print("QUERY",query)
        show_hits(retriever.search(query))
