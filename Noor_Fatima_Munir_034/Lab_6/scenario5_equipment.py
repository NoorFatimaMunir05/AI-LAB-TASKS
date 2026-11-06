from lab6_search import Retriever,show_hits
records=[
 {"id":"equipment:printer","text":"If a printer produces blank pages check ink levels, run the cleaning utility and then print a test page."},
 {"id":"equipment:router","text":"If the router drops a connection check cables, power and restart it safely."},
]
print("QUERY printer blank paper after printing")
show_hits(Retriever(records).search("printer blank paper after printing"))
