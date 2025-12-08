
from openai import OpenAI
client = OpenAI(api_key="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")


# 2. Create the request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a..."}
    ]
)

# Extract the response
answer = response.choices[0].message.content

# Display the result
print(answer)


