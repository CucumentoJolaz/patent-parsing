from revChatGPT.V3 import Chatbot
chatbot = Chatbot(api_key="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")
# for data in chatbot.ask_stream("Hello world"):
#     print(data, end="", flush=True)

chatbot.ask("Hello world")