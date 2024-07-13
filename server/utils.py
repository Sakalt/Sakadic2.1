import openai
import json
from datetime import datetime

openai.api_key = 'your_openai_api_key'

def generate_sentence():
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Create a daily example sentence:",
        max_tokens=50
    )
    return response.choices[0].text.strip()

def save_sentence(sentence, filename='data/example_sentences.json'):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    example_sentence = {"time": current_time, "sentence": sentence}
    
    with open(filename, 'r+') as file:
        data = json.load(file)
        data.append(example_sentence)
        file.seek(0)
        json.dump(data, file, indent=4)

def load_example_sentences(filename='data/example_sentences.json'):
    with open(filename, 'r') as file:
        return json.load(file)
