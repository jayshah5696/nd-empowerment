import streamlit as st
import pandas as pd
from datetime import datetime
import os
from litellm import completion
import dotenv
import ast
import json
dotenv.load_dotenv('../utils/.env')
import bentoml
from pydantic import BaseModel
from pathlib import Path
from audiorecorder import audiorecorder
from generate_answer import generate_markdown_using_style
style_guide_file_path = 'style_guide.json'
with open(style_guide_file_path, 'r') as file:
    style_guide = json.load(file)
# Access the environment variables
stt_api = os.getenv('stt_id')

class TranscribeRequest(BaseModel):
    audio_file: Path

class TranscribeResponse(BaseModel):
    segments: list
    word_segments: list

def transcribe_audio(request: TranscribeRequest) -> TranscribeResponse:
    with bentoml.SyncHTTPClient(stt_api) as client:
        result = client.transcribe(audio_file=request.audio_file)
    
    return TranscribeResponse(segments=result['segments'], word_segments=result['word_segments'])

def completion_llm(text,model='mistral/mistral-small-latest'):
    messages = [{ "content": text,"role": "user"}]
    response = completion(model=model, messages=messages)
    return response.choices[0].message.content

def response_llm_prompt(text_input):

    prompt = f""" Based on the user's query, determine if it requires a backend response or not.
    Questions and queries require a response, while log entries do not. 
    User query: {text_input} 
    Respond with only "true" or "false" (without quotes), or a JSON object in the format {{"result": true}} or {{"result": false}}. """
    response = completion_llm(prompt,model='mistral/mistral-medium-latest')
    # print(response)
    # print(type(response))
    try:
        response = json.loads(response)
    except:
        try:
            response = ast.literal_eval(response)
        except:
            response = {"result": False}

    return response['result']



def journal_app():
    # Check if the CSV file exists
    if os.path.isfile('journal_entries.csv'):
        journal_df = pd.read_csv('journal_entries.csv')
    else:
        # Create an empty DataFrame to store the journal entries
        journal_df = pd.DataFrame(columns=['Timestamp', 'Text Input', 'Response Needed', 'Completed'])
        journal_df.to_csv('journal_entries.csv', index=False)

    # Text input for the journal entry
    # text_input = st.text_input("Enter your journal entry:")
    audio_only = st.toggle("Audio Only", False)
    if audio_only:
        st.title("Audio Recorder")
        audio = audiorecorder("Click to record", "Click to stop recording")
        audio.export("audio.wav", format="wav")
        # with st.audio_recorder("user_audio.wav", format="wav", save_to_out=True, show_stop=True):
        #     st.write("Recording...")
        path = Path('audio.wav')
        result = transcribe_audio(TranscribeRequest(audio_file=path))
        text_input = result.segments[0]['text']
        text_input = st.text_input("Enter your journal entry:", value=text_input, key="journal_entry")

    else:
        text_input = st.text_input("Enter your journal entry:", value="", key="journal_entry")

        # Checkbox for response needed
    if text_input!="":
        #try:
        response_needed = response_llm_prompt(text_input)
    else:
        response_needed = False

    # Button to submit the journal entry
    if st.button("Submit") or text_input!="" or text_input is not None or text_input is not st.empty() :
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add the entry to the DataFrame
        # Create a new DataFrame for the new entry
        journal_df = pd.read_csv('journal_entries.csv')
        new_entry = pd.DataFrame({'Timestamp': [timestamp],
                                'Text Input': [text_input],
                                'Response Needed': [response_needed],
                                'Completed': [False]})
        if text_input not in journal_df['Text Input'].values:
            # Concatenate the new entry to the journal_df DataFrame
            journal_df = pd.concat([journal_df, new_entry], ignore_index=True)

        st.success("Journal entry submitted successfully!")

        # Save the journal entries as a CSV file
        journal_df.to_csv('journal_entries.csv', index=False)
        text_input = st.empty()
    # Add a toggle to show/hide the table
    show_table = st.checkbox("Show Journal Entries")
    # Show the table if the toggle is enabled
    if show_table:
        st.subheader("Journal Entries")
        journal_df = pd.read_csv('journal_entries.csv')
        st.dataframe(journal_df)

    if st.button("Clear Journal Entries"):
        journal_df = pd.DataFrame(columns=['Timestamp', 'Text Input', 'Response Needed', 'Completed'])
        journal_df.to_csv('journal_entries.csv', index=False)
        st.success("Journal entries cleared successfully!")
    if st.button("Execute on Journal Entries"):
        journal_df = pd.read_csv('journal_entries.csv')
        for index, row in journal_df.iterrows():
            if row['Completed'] == False:
                if row['Response Needed'] == True and row['Text Input'] is not None:
                    location = generate_markdown_using_style(row['Text Input'], style_guide)
                    # st.markdown(response)
                    journal_df.loc[index, 'Completed'] = True
                    # add markdown location
                    journal_df.loc[index, 'Location'] = location

        journal_df.to_csv('journal_entries.csv', index=False)
        st.success("Journal entries executed successfully!")

    # audio = mic_recorder(start_prompt="⏺️", stop_prompt="⏹️", key='recorder')
    


    

