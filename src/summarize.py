import requests
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Get Google Gemini API Key from Environment Variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
if not GEMINI_API_KEY:
    raise ValueError("❌ Error: GEMINI_API_KEY is not set. Please configure it.")

# ✅ Use the correct model endpoint
GEMINI_MODEL = "gemini-1.5-pro"

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

def chunk_code(code, max_length=500):
    """Splits code into smaller chunks for processing."""
    words = code.split()
    chunks = []
    while words:
        chunk, words = words[:max_length], words[max_length:]
        chunks.append(" ".join(chunk))
    return chunks

def call_gemini_api(prompt):
    """Send a request to the Google Gemini AI API."""
    try:
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(GEMINI_URL, json=data, timeout=15)

        # ✅ Debugging: Print API Response
        print(f"🔍 API Response Status: {response.status_code}")
        print(f"📝 API Response Text: {response.text}")

        if response.status_code == 200:
            try:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            except (IndexError, KeyError):
                return "⚠️ API Response Format Error: Unexpected data structure."

        if response.status_code == 401:
            return "❌ API Error 401: Invalid API Key. Please check your Gemini API key."

        if response.status_code == 429:
            return "❌ API Error 429: Too many requests. Try again later."

        if response.status_code == 404:
            return f"❌ API Error 404: Model {GEMINI_MODEL} is not found. Please check the correct model version."

        return f"❌ API Error {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return "❌ API Error: Request timed out. Try again later."
    except requests.exceptions.ConnectionError:
        return "❌ API Error: Failed to connect to Google Gemini API."
    except Exception as e:
        return f"❌ Unexpected API Error: {str(e)}"

def summarize_code_gemini(code):
    """Send code to Google Gemini AI API for explanation-based summarization."""
    prompt = f"Explain the following code snippet in simple terms:\n\n{code}\n\nSummary:"
    return call_gemini_api(prompt)
