import json
import dotenv
import os
from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI
from utils.prompt import persona_to_style_prompt, style_to_answer_prompt

dotenv.load_dotenv('utils/.env')
style_guide_file_path = 'utils/style_guide.json'


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

### PART 1
user_intro = "i am a 60 years old man, i want to travel the world and explore hidden gems"
with open(style_guide_file_path, 'r') as file:
    style_guide = json.load(file)
print(f"style_guide = {style_guide}")
result_style = predict_style_using_intro(introductory_text=user_intro, 
                                         style_guide=style_guide)
print(f"result_style = {result_style}")

### PART 2
user_question = "tell me about french food"
current_style = {
    "answer_type": "story",
    "answer_style": "inspirational",
    "negative_type": "none",
}
result_answer = generate_answer_using_style(question=user_question, 
                                            style=current_style)
print(f"result_answer = {result_answer}")