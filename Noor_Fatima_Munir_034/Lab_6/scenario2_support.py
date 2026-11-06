from lab6_search import Retriever,show_hits
records=[
 {"id":"support:login","text":"Reset a forgotten password using the recovery link on the login page. If email is unavailable visit the IT desk."},
 {"id":"support:fees","text":"Ask the finance office for help with fee payment plans."},
 {"id":"support:upload","text":"Upload coursework through the learning portal."},
]
print("QUERY I cannot log in and forgot my password")
show_hits(Retriever(records).search("I cannot log in and forgot my password"))
