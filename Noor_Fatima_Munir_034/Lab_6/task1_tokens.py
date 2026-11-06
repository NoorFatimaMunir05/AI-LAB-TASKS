import re

def whitespace(text):
    return text.split()

def word_like(text):
    return re.findall(r"\b\w+\b", text, flags=re.UNICODE)

samples = [
    "Hello, world!",
    "I can't submit late!",
    "student@example.com",
    "CS4944",
    "",
    "میں اردو پڑھتا ہوں",
]

def run():
    for sample in samples:
        a = whitespace(sample)
        b = word_like(sample)
        print("TEXT:",repr(sample))
        print("WHITESPACE:",a,"COUNT:",len(a))
        print("UNICODE WORD-LIKE:",b,"COUNT:",len(b))
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        for sample in [samples[0],samples[1]]:
            ids = model.tokenizer(sample, truncation=False)["input_ids"]
            print("MODEL TOKENS:",repr(sample),ids,"COUNT:",len(ids))
    except (ImportError,OSError) as error:
        print("MODEL TOKENIZER NOT RUN:",type(error).__name__,str(error)[:150])

if __name__ == "__main__":
    run()
