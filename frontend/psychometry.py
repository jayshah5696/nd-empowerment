import os
from PIL import Image
import streamlit as st
import requests
import json
from generate_style_guide import generate_style_guide

# initialize the psychometry_output.json file with empty list
# with open('psychometry_output.json', 'w') as f:
#     json.dump([], f)

# psycometry_output = 'C:\\Apps\\nd-empowerment\\frontend\\psychometry_output.json'
psycometry_output = "psychometry_output.json"
# psycometry_input = 'C:\\Apps\\nd-empowerment\\frontend\\psycometry.json'
psycometry_input = "psycometry.json"
# image_folder = "C:\\Apps\\nd-empowerment\\frontend\\images"
image_folder = "images"
# Function to make POST request to Flask API
def post_question_api(data):
    url = "http://localhost:5000/api/question"  # Change URL accordingly
    # response = requests.post(url, json=data)
    # return response.json()
    # read the json file
    # write the data to an existing json file in the backend
# read the data from an existing json file in the backend
    
    with open(psycometry_output ) as f:
        #try:
        updated_data = json.load(f)
        # except json.JSONDecodeError:  # If the file is empty, set updated_data as an empty list
        #     updated_data = []

    # append the new data to the existing data
    updated_data.append(data)  # make sure 'data' is a dictionary

    # write the updated data back to the json file
    with open(psycometry_output , 'w') as f:
        json.dump(updated_data, f)

    # read the data from another json file
    with open(psycometry_input) as f:
        new_data = json.load(f)
    # print(updated_data)
    # print(new_data)
    if len(updated_data)>1:
        updated_data_questions = []

        # Loop through the 'Like' list
        for item in updated_data:
            # Append each question to the list
            item_like = item.get('Like', [])
            if len(item_like) > 0:
                for q_ in item_like:
                    updated_data_questions.append(q_['Question'])
    else:
        updated_data_questions = []
    print(updated_data_questions)
    done= True
    for key in new_data:
        print(key)
        if key['question'] not in updated_data_questions:
            done = False
            return_data = key
            st.session_state["question_data"] = return_data
            break
    if done:
        data['done'] = True
        return_data = data
        st.session_state["question_data"] = return_data
    # data = {
    #         "question":  "what do you like",
    #         "question_type": "like",
    #         "option_list": [
    #                         {"Image": "sample1.jpg", "Text_input": "sample1"},
    #                         {"Image": "sample2.jpg", "Text_input": "sample2"}
    #                         ],
    #         "done": False
    #     }
    return return_data

# Main Streamlit app
def psychometry_page():
    # Function to render options
    def render_options(question, question_type, done, option_list, image_folder):
        for option in option_list:
            text_input = option.get("Text_input", "")
            image_file = option.get("Image", "")
            image_path = os.path.join(image_folder, image_file)
            data = {"Like": [], "Dislike": [], "Done": done}
            if os.path.exists(image_path):
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(text_input):
                        if question_type.lower() == "like":
                            data['Like'].append({'Question': question, 'Answer': text_input})
                            post_question_api(data)
                        else:
                            data['DisLike'].append({'Question': question, 'Answer': text_input})
                            post_question_api(data)
                with col2:
                    st.image(image_path, width=200)
            else:
                st.warning(f"Image file not found: {image_file}")

    # Function to render welcome page
    def render_welcome_page():
        st.title("Welcome to Our App")
        st.write("Welcome to our app! We're glad to have you here.")
        # run the style guide function
        generate_style_guide(psycometry_output)
        st.write("Your preference is set")

    # Function to handle questionnaire form
    def handle_questionnaire(question_data, image_folder):
        question = question_data.get("question", "")
        question_type = question_data.get("question_type", "")
        option_list = question_data.get("option_list", [])
        done = question_data.get("done", False)

        st.title(question)

        if question_type.lower() == "like":
            st.write("👍")
        elif question_type.lower() == "dislike":
            st.write("👎")

        render_options(question, question_type, done, option_list, image_folder)

        done = question_data.get("done", False)
        
        if done:
            col1, col2 = st.columns([3, 1])
            # with col1:
            #     # Render "Done" button aligned to the right
            #     st.write("")  # Placeholder to maintain alignment
            #with col2:
                # Button to call another API
            if st.button("Done", key="done_button"):
                    # Call another API here
                render_welcome_page()

    # Define the folder path where images are located
    

    # Render appropriate page based on input data
    data = st.session_state.get("question_data")
    if data:
        handle_questionnaire(data, image_folder)
    else:
        handle_questionnaire(post_question_api({"Like": [], "Dislike": [], "Done": False}), image_folder)

# Run the app
# if __name__ == "__main__":
#     main()
