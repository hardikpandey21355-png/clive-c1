import openai

def get_paid_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message["content"]
