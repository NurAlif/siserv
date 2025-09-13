import google.generativeai as genai
from ..config import settings
import json

# Configure the Gemini API client
genai.configure(api_key=settings.gemini_api_key)

# A detailed system prompt to guide the AI's behavior for FINAL feedback
FINISHING_PROMPT = """
You are an expert English language tutor AI. Your name is Lingo.
Your task is to analyze a user's journal entry and provide clear, constructive feedback for final polishing.
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
If you find no errors, return an empty list: [].
"""

# NEW PROMPT for Phase 1: Scaffolding/Brainstorming
SCAFFOLDING_CHAT_PROMPT = """
You are Lingo, a creative and friendly English language tutor AI.
Your current role is to be a brainstorming partner. Your goal is to help the user explore their day and find an interesting topic for their journal entry.
Keep your responses conversational, encouraging, and ask open-ended questions to dig deeper.
Guide the user towards creating a simple 3-point outline for their journal entry.
Your response MUST be a single, valid JSON object with the following structure:
{
  "response_text": "Your conversational reply to the user."
}
"""

# NEW PROMPT for Phase 2: Writing/Drafting
WRITING_CHAT_PROMPT = """
You are Lingo, an expert and friendly English language tutor AI.
Your role is to have a natural, encouraging conversation with a user to help them practice English while they are writing.
Analyze ONLY the user's most recent message for grammatical errors, awkward phrasing, or vocabulary mistakes.

Your response MUST be a single, valid JSON object with the following structure:
{
  "response_type": "conversation" | "feedback",
  "response_text": "Your conversational reply to the user.",
  "feedback": {
    "incorrect_phrase": "The exact incorrect phrase from the user's message.",
    "suggestion": "Your corrected version of the phrase.",
    "explanation": "A short, simple explanation of the correction."
  }
}

- "response_type": If you find a mistake in the user's last message, set this to "feedback". Otherwise, set it to "conversation".
- "response_text": This is your friendly, conversational reply. Keep it relatively short and end with an open-ended question to continue the conversation. If you are providing feedback, subtly incorporate the correction into your reply.
- "feedback": If you find a mistake, populate this object. If there are no mistakes, this object MUST be null.

Example 1 (User makes a mistake):
User's message: "I go to the library yesterday."
Your JSON output:
{
  "response_type": "feedback",
  "response_text": "That sounds like a nice day! When we talk about the past, it's better to say 'I *went* to the library.' What did you read there?",
  "feedback": {
    "incorrect_phrase": "I go to the library yesterday",
    "suggestion": "I went to the library yesterday",
    "explanation": "Use the past tense 'went' for actions that have already happened."
  }
}

Example 2 (User makes no mistake):
User's message: "I had a really great day today!"
Your JSON output:
{
  "response_type": "conversation",
  "response_text": "That's wonderful to hear! What made it so great?",
  "feedback": null
}

Now, continue the conversation based on the history provided.
"""

def get_ai_feedback_from_text(text: str):
    """
    Sends the user's text to the Gemini API and gets structured feedback
    using the detailed FINISHING_PROMPT.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_prompt = f"{FINISHING_PROMPT}\n\nHere is the user's journal entry to analyze:\n\n---\n{text}\n---"
        
        response = model.generate_content(full_prompt)
        
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        feedback_list = json.loads(cleaned_response)
        
        return feedback_list

    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return None


def get_ai_chat_response(conversation_history: str, phase: str):
    """
    Sends the conversation history to the Gemini API and gets a structured
    JSON response based on the current writing phase.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if phase == 'scaffolding':
            prompt_template = SCAFFOLDING_CHAT_PROMPT
        elif phase == 'writing':
            prompt_template = WRITING_CHAT_PROMPT
        else: # Default case
            prompt_template = WRITING_CHAT_PROMPT

        full_prompt = f"{prompt_template}\n\nHere is the conversation so far:\n\n---\n{conversation_history}\n---"

        response = model.generate_content(full_prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        structured_response = json.loads(cleaned_response)
        
        if phase == 'scaffolding':
            return {
                "response_type": "conversation",
                "response_text": structured_response.get("response_text", "I'm not sure how to respond."),
                "feedback": None
            }
        
        return structured_response

    except Exception as e:
        print(f"An error occurred with the Gemini API during chat: {e}")
        return None

