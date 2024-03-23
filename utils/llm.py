from litellm import completion
from rich.pretty import pprint
import dotenv
dotenv.load_dotenv('.env')


def completion_llm(text,model='mistral/mistral-small-latest'):
    messages = [{ "content": text,"role": "user"}]
    response = completion(model=model, messages=messages)
    return response.choices[0].message.content


def chat_llm(input, model='mistral/mistral-small-latest'):
    messages = [{ "content": input,"role": "user"}]
    response = completion(model=model, messages=messages)
    # append response as a new message with role 'assistant'
    messages.append({ "content": response.choices[0].message.content, "role": "assistant"})
    return messages

    