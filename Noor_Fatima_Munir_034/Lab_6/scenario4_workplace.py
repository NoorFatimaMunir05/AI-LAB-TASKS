from lab6_search import Retriever,show_hits
records=[
 {"id":"policy:staff","text":"Employees may request remote work with manager approval. Their normal timetable still applies."},
 {"id":"policy:contract","text":"Contractors can work remotely only when a signed contract permits it. Employee rules do not automatically apply."},
]
print("QUERY Can contractors work remotely?")
show_hits(Retriever(records).search("Can contractors work remotely?"))
