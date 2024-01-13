import google.generativeai as genai

from CoreFunction.Common import get_setting_json

# Config for Google AI
GOOGLE_AI_KEY = get_setting_json('GeminiApiKey')
genai.configure(api_key=GOOGLE_AI_KEY)
text_generation_config = genai.GenerationConfig(**{
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1024,
})

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
text_model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=text_generation_config, safety_settings=safety_settings)