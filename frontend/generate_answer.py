import json
import dotenv
import os
import base64
import uuid
from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI
from prompt import persona_to_style_prompt, style_to_answer_prompt, split_answer_to_visual_prompt
import image_gen

dotenv.load_dotenv('../utils/.env')
style_guide_file_path = '../utils/style_guide.json'


def predict_style_using_intro(introductory_text, style_guide):
    augmented_prompt = persona_to_style_prompt.format(user_text=introductory_text,
                                                      style_guide=style_guide)
    chat = ChatMistralAI(model="mistral-large-latest",
                         mistral_api_key=os.getenv("MISTRAL_API_KEY"))
    messages = [HumanMessage(content=augmented_prompt)]
    response = chat.invoke(messages)
    return response.content

def generate_answer_using_style(question, style):
    augmented_prompt = style_to_answer_prompt.format(question=question,
                                                     style=style)
    chat = ChatMistralAI(model="mistral-large-latest",
                         mistral_api_key=os.getenv("MISTRAL_API_KEY"))
    messages = [HumanMessage(content=augmented_prompt)]
    response = chat.invoke(messages)
    return response.content

def generate_markdown_using_style(question, style):
    # print(f"starting generate_markdown_using_style from - {os.getcwd()}")
    # get full text based on Question and Style
    full_answer = generate_answer_using_style(question, style)
    print(f"string_representation = {full_answer}")
    # generate multiprompts
    augmented_prompt = split_answer_to_visual_prompt.format(user_text=full_answer)
    chat = ChatMistralAI(model="mistral-large-latest",
                         mistral_api_key=os.getenv("MISTRAL_API_KEY"))
    messages = [HumanMessage(content=augmented_prompt)]
    response = chat.invoke(messages)
    # getting string format
    string_representation = response.content
    print(f"string_representation = {string_representation}")
    list_from_string = json.loads(string_representation)
    # creating markdown string
    main_markdown_string = """
    """
    main_markdown_string += f"""<p>{full_answer}</p>"""
    for current_prompt in list_from_string:
        file_name, file_b64 = image_gen.generate_image(current_prompt,
                                                       get_b64=True)
        base64_image = file_b64
        # below 3 lines are for preview in Ipython-nb
        # from IPython.display import Image, display
        # image_bytes = base64.b64decode(base64_image)
        # display(Image(image_bytes))
        main_markdown_string += f"""<p>{current_prompt}</p><img src="data:image/png;base64,{base64_image}" alt="{current_prompt}" width="300" height="300">"""

    # writing string to Markdown file
    uuid_value = uuid.uuid4()
    md_filename = f"output/{uuid_value}.md"
    # Write the Markdown string to the file
    with open(md_filename, "w") as file:
        file.write(main_markdown_string)
    return md_filename

# ### PART 1
# user_intro = "i am a 60 years old man, i want to travel the world and explore hidden gems"
# with open(style_guide_file_path, 'r') as file:
#     style_guide = json.load(file)
# # print(f"style_guide = {style_guide}")
# # result_style = predict_style_using_intro(introductory_text=user_intro, 
# #                                          style_guide=style_guide)
# # print(f"result_style = {result_style}")

# ### PART 2
# user_question = "tell me about french food"
# current_style = {
#     "answer_type": "story",
#     "answer_style": "inspirational",
#     "negative_type": "none",
# }
# # result_answer = generate_answer_using_style(question=user_question, 
# #                                             style=current_style)
# # print(f"result_answer = {result_answer}")

# ### PART 3
# # user_question = "tell me about french food"
# # current_style = {
# #     "answer_type": "story",
# #     "answer_style": "inspirational",
# #     "negative_type": "none",
# # }
# user_question = "tell me about california"
# current_style = {
#     "answer_type": "poem",
#     "answer_style": "analytical",
#     "negative_type": "none",
# }
# result_filename = generate_markdown_using_style(question=user_question,
#                                                 style=current_style)
# print(f"result_filename = {result_filename}")