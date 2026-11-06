try:
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",device="cpu")
    for label,text in [("short","Reset my password."),("long","password "*300),("course code","CS4944 email@example.com")]:
        ids=model.tokenizer(text,truncation=False)["input_ids"]
        print(label,"tokens",len(ids),"limit",model.max_seq_length,"fits",len(ids)<=model.max_seq_length)
except (ImportError,OSError) as error:
    print("MODEL TOKEN LIMIT TEST NOT RUN",type(error).__name__,str(error)[:150])
