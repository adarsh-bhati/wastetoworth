from groq import Groq
from models.prompt_builder import build_prompt
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

def generate_project(materials):

    prompt = build_prompt(materials)

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.8

    )

    return response.choices[0].message.content