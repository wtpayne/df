import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a function to generate likely options based on input text
def generate_options(text):
    prompt = f"You are an assistant for non verbal individuals. Please generate some likely sentences based on the following text received from a non-verbal individual:\n\n{text}\n\nOptions:"
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=100, n=5, stop=None, temperature=0.1)
    options = [option.text.strip() for option in response.choices]
    return options

# Define a function to generate a revised sentence based on user feedback
def generate_revised_sentence(text, feedback):
    prompt = f"You are an assistant for non verbal individuals. Please revise the following sentence based on the following feedback:\n\n{text}\n\nFeedback:\n\n{feedback}\n\nRevised sentence"
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=100, n=1, stop=None, temperature=0.1)
    revised_sentence = response.choices[0].text.strip()
    return revised_sentence

# Define the main function
def main():
    # Prompt the user for input
    text = input("Please enter a sentence or phrase: ")

    # Generate likely options and present them to the user
    options = generate_options(text)
    print("Here are some likely options:")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    
    # Allow the user to provide feedback and refine the sentence
    feedback = []
    while True:
        feedback.append(input("Please provide feedback or indicate if one of the options is satisfactory (enter 'done' to finish): "))
        if feedback[-1] == 'done':
            feedback.pop()
            break
        revised_sentence = generate_revised_sentence(text, feedback)
        print(f"Revised sentence: {revised_sentence}")
        time.sleep(1)  # Wait for 1 second to avoid rate limiting

    # Output the final version of the sentence
    final_sentence = generate_revised_sentence(text, feedback)
    print(f"Final sentence: {final_sentence}")

# Call the main function
if __name__ == "__main__":
    main()
