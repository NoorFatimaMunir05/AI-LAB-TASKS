from lab6_search import Retriever,show_hits
records=[
 {"id":"pw","text":"Recover a lost account password using the recovery link on the sign-in page."},
 {"id":"assignment","text":"Submit assignments through the online learning portal before the deadline."},
 {"id":"library","text":"A book renewal is allowed unless the copy has been reserved."},
]
try:
    engine=Retriever(records,"embedding")
except (ImportError,OSError) as error:
    print("EMBEDDING NOT RUN",type(error).__name__,str(error)[:150])
else:
    print("MODEL LOAD SECONDS",engine.model_load_seconds)
    for query in ["I forgot my login credentials", "How should I hand in my coursework?", "Can a book be renewed after another person reserves it?"]:
        print("QUERY",query)
        show_hits(engine.search(query))
