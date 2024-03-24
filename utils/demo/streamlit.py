import streamlit as st
import pandas as pd
from datetime import datetime
import os

def journal_app():
    # Check if the CSV file exists
    if os.path.isfile('journal_entries.csv'):
        # Load the data into the DataFrame
        journal_df = pd.read_csv('journal_entries.csv')
    else:
        # Create an empty DataFrame to store the journal entries
        journal_df = pd.DataFrame(columns=['Timestamp', 'Text Input', 'Response Needed', 'Completed'])

    # Add a toggle to show/hide the table
    show_table = st.sidebar.checkbox("Show Journal Entries")

    # Text input for the journal entry
    text_input = st.text_input("Enter your journal entry:")

    # Checkbox for response needed
    response_needed = st.checkbox("Response Needed")

    # Button to submit the journal entry
    if st.button("Submit"):
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add the entry to the DataFrame
        journal_df = journal_df.append({'Timestamp': timestamp,
                                        'Text Input': text_input,
                                        'Response Needed': response_needed,
                                        'Completed': False}, ignore_index=True)
        st.success("Journal entry submitted successfully!")

        # Save the journal entries as a CSV file
        journal_df.to_csv('journal_entries.csv', index=False)

    # Show the table if the toggle is enabled
    if show_table:
        st.subheader("Journal Entries")
        st.dataframe(journal_df)

# Call the function
# journal_app()