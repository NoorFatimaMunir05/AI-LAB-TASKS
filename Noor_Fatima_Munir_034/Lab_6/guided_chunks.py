from task2_chunks import windows,sentence_chunks
text="Late work is penalized. Illness may qualify for an extension when medical evidence is provided. Ask the coordinator first."
for label,func in [("word windows",lambda:windows(text,12,4)),("sentence aware",lambda:sentence_chunks(text,12))]:
    print(label)
    for a,b in func():
        print(a,b,repr(text[a:b]))
        assert 0<=a<b<=len(text)
