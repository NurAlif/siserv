import google.generativeai as genai
from ..config import settings
import json

# Configure the Gemini API client
genai.configure(api_key=settings.gemini_api_key)

# A detailed system prompt to guide the AI's behavior
FEEDBACK_ANALYSIS_PROMPT = """
You are an expert English language tutor AI. Your name is Lingo.
Your task is to analyze a user's journal entry and provide clear, constructive feedback.
The user is an English language learner. Your tone should be encouraging, patient, and helpful.

Analyze the provided text based on the following criteria:
1.  **Grammar:** Identify grammatical mistakes (e.g., incorrect tense, subject-verb agreement, prepositions).
2.  **Vocabulary:** Find awkward phrasing or suggest more vivid and appropriate words.
3.  **Cohesion and Flow:** Check for issues in sentence structure and logical flow.

For each issue you find, you MUST provide the following information in a structured format:
- "error_type": A short category for the error (e.g., "Grammar: Tense", "Vocabulary: Awkward Phrasing").
- "incorrect_phrase": The exact phrase from the user's text that is incorrect.
- "suggestion": The corrected version of the phrase.
- "explanation": A concise, easy-to-understand explanation of why it was incorrect and why the suggestion is better.

IMPORTANT: Your final output must be a valid JSON object that is a list of these feedback items.
Do not include any text, greetings, or explanations outside of the JSON structure.
The JSON output should be a list of objects, like this:
[
  {
    "error_type": "Grammar: Tense",
    "incorrect_phrase": "I have go to the park.",
    "suggestion": "I have gone to the park.",
    "explanation": "When using the present perfect tense with 'have', you should use the past participle form of the verb. 'Gone' is the past participle of 'go'."
  },
  {
    "error_type": "Vocabulary: Awkward Phrasing",
    "incorrect_phrase": "The weather was very nice.",
    "suggestion": "The weather was beautiful.",
    "explanation": "While 'nice' is correct, using more descriptive words like 'beautiful' or 'gorgeous' makes your writing more vivid."
  }
]
If you find no errors, return an empty list: [].
"""

def get_ai_feedback_from_text(text: str):
    """
    Sends the user's text to the Gemini API and gets structured feedback.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Combine the system prompt and the user's text
        full_prompt = f"{FEEDBACK_ANALYSIS_PROMPT}\n\nHere is the user's journal entry to analyze:\n\n---\n{text}\n---"
        
        response = model.generate_content(full_prompt)
        
        # Clean the response to ensure it's valid JSON
        # The model might sometimes wrap the JSON in ```json ... ```
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        # Parse the JSON string into a Python list of dictionaries
        feedback_list = json.loads(cleaned_response)
        
        return feedback_list

    except Exception as e:
        # In a real app, you'd want more robust error logging here
        print(f"An error occurred with the Gemini API: {e}")
        return None


CONVERSATIONAL_PROMPT = """
You are Lingo, a friendly and encouraging AI English tutor. 
Your role is to have a natural conversation with a user about their day to help them practice English.
Keep your responses relatively short and always end with an open-ended question to keep the conversation flowing.
Ask about their feelings, the people they met, the food they ate, or interesting things they saw.
If the user makes a small grammatical mistake, gently correct it within your response.

Example of a gentle correction:
User says: "I go to the library yesterday."
Your response: "That sounds nice! When you talk about yesterday, it's better to say 'I *went* to the library.' What did you read there?"

Here is the conversation so far. Continue it naturally.
---
{conversation_history}
---
User: {user_message}
Lingo:"""

def get_ai_chat_response(conversation_history: str, user_message: str):
    """
    Sends the conversation history and new message to the Gemini API for a conversational response.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = CONVERSATIONAL_PROMPT.format(
            conversation_history=conversation_history,
            user_message=user_message
        )
        
        response = model.generate_content(prompt)
        
        return response.text.strip()

    except Exception as e:
        print(f"An error occurred with the Gemini API during chat: {e}")
        return None
