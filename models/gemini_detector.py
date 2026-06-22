import google.generativeai as genai

from config import GEMINI_API_KEY

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
     "gemini-2.5-flash"
)


def detect_materials_with_gemini(image_path):

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
Analyze this image.

Identify all visible waste materials.

Return ONLY a comma separated list.

Example:

Plastic Bottle, Cardboard Box, Old Charger, Glass Jar

No explanation.
"""

    response = model.generate_content(
        [
            prompt,
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ]
    )

    text = response.text.strip()

    materials = [

        item.strip()

        for item in text.split(",")

        if item.strip()

    ]

    return materials