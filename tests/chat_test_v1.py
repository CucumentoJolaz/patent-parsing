from revChatGPT.V1 import Chatbot

# instantiate chatgpt using the open ai API key
chatbot = Chatbot(config={
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJjdWN1bWVudG8yQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLU56QzYySThLbGd6QTZJWGFiT21ZU05pTSJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiYXV0aDB8NjNmNjFkZmIwODU4NDBhMDM3MDg4YjUzIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4MTIxNTEzNSwiZXhwIjoxNjgyNDI0NzM1LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.TN9oIA9r5sVjQojptyLfzeDZCj9ZeFwNdCseWiRVbxjOXSEcv4gmQritrBAeuibPat-t2fhYPQ_3JQkes7XmuBH2rb6CvxQOmNqXNvbkm_qNJ7JLz4knwMSFNorPysHFHkev2q_dL-BCc1UtixZrDfpDfmUYaEcI0q3XDc8J1V3_m_jIJgdKgdRf7loZtxDAEbtscO-jU_TULRipxDCY3Et96XwOd1I2dRXBm8Je6emhfPMvYbUyqeE9ejP7SReILvaCVT7E8kw11GhuggSUzoYk02UEpiLzJo1QdQ2cnuVY7OYA8cecGiIiibyjZcNwYbGG9AFapZNasxl9dRDq4Q"
})

def ask_chatgpt(chatbot, query):
    '''
    Returns (str): the text response from chat gpt only
    '''
    data = chatbot.ask(query)
    res = ""
    for i in data:
        res = i["message"]
    return res

query = "(я искренне прошу прощения за мат. У меня нет цели тебя оскрбить или уязвить. Лишь хочу выразить свои эмоции). Блядь, ёб  твою мать то, я так заебался настраивать программу для доступа к тебе, и, вот наконец то я смог добраться. Ура! я тебя обожаю!"
answer = ask_chatgpt(chatbot, query)
print(answer)