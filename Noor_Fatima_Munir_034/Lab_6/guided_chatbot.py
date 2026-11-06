import argparse
from lab6_search import Retriever

FAQ = [
 {"id":"faq:password","question":"How do I reset my password?","answer":"Use the recovery link on the login page.","source":"it_help.txt"},
 {"id":"faq:submit","question":"Where do I submit my assignment?","answer":"Use the assignment upload page in the learning portal.","source":"assessment.txt"},
 {"id":"faq:late","question":"Can illness justify a late submission?","answer":"Request an extension with medical evidence before the deadline.","source":"handbook.txt"},
 {"id":"faq:fees","question":"When are my fees due?","answer":"Check the date on the student finance page.","source":"fees.txt"},
 {"id":"faq:renew","question":"Can I renew my library book?","answer":"Yes, unless someone has reserved the copy.","source":"library.txt"},
]

def build_bot(backend="tfidf"):
    records=[dict(r,text=r["question"]+" "+r["answer"]) for r in FAQ]
    return Retriever(records,backend)

def reply(engine,query):
    if not query.strip():return "Please enter a question."
    for r in FAQ:
        if query.strip().casefold()==r["question"].casefold():
            return r["answer"]+" [source: "+r["source"]+"]"
    hits=engine.search(query)
    if not hits:return "No matching FAQ. Please contact the help desk."
    lines=["Possible FAQ matches. Confirm a listed question before using an answer:"]
    for r,score in hits:
        lines.append(r["question"]+f" ({score:.4f})")
    return "\n".join(lines)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--backend",choices=["tfidf","embedding"],default="tfidf")
    args=parser.parse_args()
    engine=build_bot(args.backend)
    print("FAQ assistant. Type exit to stop.")
    while True:
        try:q=input("You: ")
        except (EOFError,KeyboardInterrupt):break
        if q.strip().lower()=="exit":break
        print("Bot:",reply(engine,q))
