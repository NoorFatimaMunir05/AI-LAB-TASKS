from guided_chatbot import build_bot,reply

bot=build_bot("tfidf")
for question in ["How do I reset my password?","reset forgotten account","", "volcano geology"]:
    print("QUESTION:",repr(question))
    print("RESPONSE:",reply(bot,question))
