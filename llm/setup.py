from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
import os

def get_llm():
    return ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.5,
        safety_settings={
            HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        }
    )