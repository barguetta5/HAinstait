import openai

# Set up your API key
openai.api_key = ('sk-proj-UOIKxQAWr4YPFnvrFYN2n5y0l02NP2UkA2Uaf15zKVgoQw7j-l13surJVThRfFV9tg'
                  '-KKbd6A_T3BlbkFJ5CrU8ddyutxUvTT8mma1nECc8zlPehEK9_-kmJUpfASuMXYfOrFaUZSwnh7MFC_Yx9etSfWJEA')

# Function to send a question to the model
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',  # or 'gpt-4' if you have access
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message['content']

# Example usage
# if __name__ == "__main__":
#     question = "What is the capital of France?"
#     answer = ask_openai(question)
#     print(f"Question: {question}\nAnswer: {answer}")

