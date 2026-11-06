from lab6_search import Retriever,show_hits
records=[
 {"id":"handbook:assessment","text":"Late coursework normally has a penalty. Illness may qualify for an extension when a medical certificate is provided before the deadline."},
 {"id":"handbook:contact","text":"Send an extension request to the course coordinator and keep the response."},
]
print("QUERY Can I submit late if I was ill?")
show_hits(Retriever(records).search("Can I submit late if I was ill?"))
