
from openai import OpenAI
import os

#Load API key from environment variable
client= OpenAI(
    api_key="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"
)

#context-aware prompt

messages= [
    {"role": "system", "content": "you are a helpful python assistant."},
    {"role": "user", "content": "What is Python"},
    {"role": "assistant", "content": "Pyhton is a..."}
]

#Call OpenAI API
response= client.chat.completions.create(
    model= "gpt-4.1-mini",
    messages=messages
)

#Print the response
#print(response.choices[0].message["content"])
print(response.choices[0].message.content)