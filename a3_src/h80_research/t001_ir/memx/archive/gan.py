import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the generator function with a prompt
def generate(prompt):
    # Add a prompt to encourage the generator to respond in a specific way
    prompt_text = f"Generate a response to the following prompt:\n{prompt}\n\nResponse:"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    # Return only the generated response text, excluding the prompt
    return response.choices[0].text.replace(prompt_text, "").strip()

# Define the discriminator function with prompts for good and bad output
def discriminate(prompt, output):
    # Add prompts to make it clear what constitutes "good" or "bad" output
    prompt_text = f"Classify the following output as either good or bad:\nPrompt: {prompt}\nOutput: {output}\n\n1. Good\n2. Bad\n\nSelection:"
    input_text = f"{prompt} {output}"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.0,
    )
    
    label = response.choices[0].text.strip()
    
    # Return True for "good" output and False for "bad" output
    return label == "1"
