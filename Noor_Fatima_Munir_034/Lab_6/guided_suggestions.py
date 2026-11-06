import argparse
from guided_chatbot import build_bot
parser=argparse.ArgumentParser()
parser.add_argument("--backend",choices=["tfidf","embedding"],default="tfidf")
parser.add_argument("--query",default="assignment upload")
args=parser.parse_args()
engine=build_bot(args.backend)
print("QUERY",repr(args.query))
for record,score in engine.search(args.query,k=3):
    if args.backend=="embedding" or score>0:
        print(record["question"],f"score={score:.4f}")
