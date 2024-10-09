import openai

# Set up your API key
openai.api_key = ('sk-proj-UOIKxQAWr4YPFnvrFYN2n5y0l02NP2UkA2Uaf15zKVgoQw7j-l13surJVThRfFV9tg'
                  '-KKbd6A_T3BlbkFJ5CrU8ddyutxUvTT8mma1nECc8zlPehEK9_-kmJUpfASuMXYfOrFaUZSwnh7MFC_Yx9etSfWJEA')

# Function get question and return the chatGPT response
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message['content']

