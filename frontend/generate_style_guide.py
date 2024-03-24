import json
from rich.pretty import pprint
import ast
from prompt import system_prompt_initial as prompt
from journal import completion_llm


def generate_style_guide(location):
    # Load the JSON data
    with open(location) as f:
        data = json.load(f)

    # Initialize an empty list to hold the question-answer pairs
    qa_pairs = []

    # Iterate over each item in the data
    for item in data:
        # Iterate over each 'Like' in the item
        for like in item['Like']:
            # Extract the question and answer
            question = like['Question']
            answer = like['Answer']
            # Add the question-answer pair to the list
            qa_pairs.append((question, answer))

    # Print the question-answer pairs
    qa_list = []

    for pair in qa_pairs:
        qa_dict = {'Question': pair[0], 'Answer': pair[1]}
        qa_list.append(qa_dict)

    pprint(qa_list)

    response = completion_llm(prompt + f"\n messages {qa_list}", model="mistral/mistral-large-latest")
    pprint(ast.literal_eval(response))
    # save the json as style_guide.json
    with open('style_guide.json', 'w') as f:
        json.dump(ast.literal_eval(response), f)

    print("Style guide generated successfully!")

# # Example usage
# generate_style_guide('/Users/jshah/Documents/GitHub/nd-empowerment/frontend/psychometry_output.json')
