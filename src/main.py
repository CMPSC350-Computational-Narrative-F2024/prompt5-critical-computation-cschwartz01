# Code to generate "text"

#!/usr/bin/python

import os
import openai
from dotenv import dotenv_values

# Set up OpenAI credentials

CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG["KEY"] or os.environ["OPEN_AI_KEY"]
OPEN_AI_ORG = CONFIG["ORG"] or os.environ["OPEN_AI_ORG"]

openai.api_key = OPEN_AI_KEY
openai.organization = OPEN_AI_ORG

def load_file(filename: str = "") -> str:
    """Loads an arbitrary file name"""
    with open(filename, "r") as fh:
        return fh.read()
    
def main():

    # Load source file
    source_text = load_file("data/source.txt")

    # Create a chain of thought prompt to guide GPT through the analysis
    messages = [
        {"role": "system", "content": "You are a critical text analyst with a background in poetry and linguistic studies."},
        {"role": "user", "content": (
            "Read the following text and provide a chain of thought analysis 750 words or less in length that explains the significance of the use of specific words. " 
            "Look at the the repeating words, taking a numeric count of how many times the word appears in the text (for example, in the sentence 'The girl felt blue "
            "as she stood under the blue sky, looking across the blue water' would output that 'blue' was used 3 times) Take it step by step and " 
            "explain each part of your reasoning using quotes from the source text to support your claims. Do not stop mid-sentence or in the middle of a thought."
            "Ensure that the analysis reaches a complete and satisfying conclusion (that is a full and complete sentence) before the token limit or word count is reached. \n\n"
            f"Text: {source_text}\n\n"
            "Chain of Thought Analysis:"
        )}
    ]

    # Get the response from GPT
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000,
        temperature=0.3
    )

    # Extract and print the response
    analysis = response.choices[0].message.content
    print("Chain of Thought Analysis:\n", analysis)

    # Save the output to text.md
    with open('../writing/text.md', 'w') as f:
        f.write("# Chain of Thought Analysis\n\n")
        f.write(analysis)
    
if __name__ == "__main__":
    main()