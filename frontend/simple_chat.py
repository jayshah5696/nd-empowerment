import streamlit as st
from litellm import completion
import dotenv
dotenv.load_dotenv('../utils/.env')


# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
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


def simple_chat(mock_response=None):

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if mock_response:
                response = mock_response
                st.markdown(mock_response)
            # else:
            #     stream = client.chat.completions.create(
            #         model=st.session_state["openai_model"],
            #         messages=[
            #             {"role": m["role"], "content": m["content"]}
            #             for m in st.session_state.messages
            #         ],
            #         stream=True,
            #     )
            #     response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
