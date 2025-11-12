# backend_api/processing.py

# --- IMPORTS ---
import pypdf
import docx
import re
import requests.utils
from fastapi import UploadFile, HTTPException

# Import the new Google library
import google.generativeai as genai

# --- CONFIGURATION ---
# 1. This is the last API key you provided.
GEMINI_API_KEY = "AIzaSyBe1QPYAMoCjtY_HUXOrybIS5Uh2NJ0Raw" 

# 2. Configure the Google AI library
# This step is crucial and replaces the need to build the URL manually.
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not set.")

# --- ASYNC FUNCTION TO CALL GEMINI (NEW VERSION) ---
async def analyze_legal_text_with_gemini(text: str) -> str:
    """Sends text to Gemini API for analysis using the official library."""
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key is not configured in processing.py")

    # This prompt is the same as before
    prompt = f"""
    You are an expert legal assistant. Your task is to provide a clear and structured analysis of the following legal document.
    Please perform the following two actions and structure your response exactly as requested, using the specified markdown headers:

    ### Summary
    Provide a concise, easy-to-understand summary of the key arguments, findings, and conclusions in the text.

    ### Citations Found
    List every legal citation or case reference you find in the text, one per line. If no citations are present, you must explicitly write "No citations were found."
    ---
    Here is the document:
    {text}
    ---
    """
    
    try:
        # 1. Initialize the model (using the stable 'gemini-pro')
        # This is the standard, stable model that should work with your key.
        # Change it to this
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # 2. Call the API asynchronously
        response = await model.generate_content_async(prompt)
        
        # 3. Return the text directly
        return response.text
        
    except Exception as e:
        # This will give us a MUCH more useful error message than the 404
        print(f"---!!! GOOGLE LIBRARY ERROR !!!---")
        print(f"Error Type: {type(e)}")
        print(f"Error Details: {e}")
        print(f"---!!! END OF ERROR !!!---")
        # Pass the more specific error to the frontend
        raise HTTPException(status_code=500, detail=f"Error from Google AI: {str(e)}")


# --- PARSING AND FILE EXTRACTION (UNCHANGED) ---

def extract_and_hyperlink_citations(llm_response: str):
    """Parses the LLM response to separate summary and citations."""
    summary_match = re.search(r"### Summary\s*\n(.*?)\n### Citations Found", llm_response, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else "Summary could not be extracted."

    citations_match = re.search(r"### Citations Found\s*\n(.*?)$", llm_response, re.DOTALL)
    hyperlinks = []
    if citations_match:
        citations_text = citations_match.group(1).strip()
        if "No citations were found" not in citations_text:
            citations_list = [line.strip() for line in citations_text.split('\n') if line.strip()]
            for citation in citations_list:
                query = requests.utils.quote(citation)
                url = f"https://indiankanoon.org/search/?formInput={query}"
                hyperlinks.append({"citation_text": citation, "url": url})
    
    return summary, hyperlinks

def extract_text_from_file(file: UploadFile):
    """Extracts text from uploaded PDF or DOCX files."""
    text = ""
    if file.content_type == "application/pdf":
        reader = pypdf.PdfReader(file.file)
        for page in reader.pages:
            text += page.extract_text()
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file.file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        # Fallback for plain text files
        try:
            text = file.file.read().decode("utf-8")
        except Exception:
            raise HTTPException(status_code=400, detail="Unsupported file type or encoding.")
    return text