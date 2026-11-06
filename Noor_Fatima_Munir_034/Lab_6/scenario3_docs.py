from lab6_search import Retriever,show_hits
records=[
 {"id":"docs:install","text":"Install the package with pip before importing the module."},
 {"id":"docs:errors","text":"If import fails check the virtual environment and package installation."},
 {"id":"docs:run","text":"Run the Python script in the folder containing its dependencies."},
]
print("QUERY module not found after starting python")
show_hits(Retriever(records).search("module not found after starting python"))
