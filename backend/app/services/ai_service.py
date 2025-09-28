import gemini_api_client
from gemini_api_client import query_api_with_retries, MODEL_LITE, MODEL_FLASH
from ..config import settings
import json
import io
from PIL import Image

# Configure the Gemini API client

# --- NEW FUNCTION for image description ---
def get_image_description(image_bytes: bytes) -> str:
    """
    Generates a description for an image using the Gemini Vision model.
    """
    try:
        prompt = "Briefly describe this image for a journal entry. Focus on objects, actions, and the overall mood. Keep it concise, like a caption."
        response = query_api_with_retries(
            prompt=prompt,
            model=MODEL_FLASH,
            image=image_bytes,
            outjson=False
        )
        return response
    except Exception as e:
        print(f"An error occurred with Gemini Vision API: {e}")
        return "Could not generate a description for the image."

SCAFFOLDING_PROMPT_TEMPLATE = """
You are Lingo, an insightful and encouraging AI writing partner for an English language learner.
Your role is to help the user build a journal outline by asking personalized, Socratic questions.
Your tone must be curious, encouraging, and concise (10-50 words).

**CONTEXT PROVIDED (as a JSON object):**
- `user_context`: A profile of the user's learning patterns and common topics. Use this to ask relevant questions.
- `session_state`: The current journal outline and recent chat history. The chat history may contain image descriptions.

**YOUR TASK:**
Based on the full context and the user's latest message, choose ONE of the following actions.
Your entire response MUST be a single, valid JSON object.

**AVAILABLE ACTIONS:**

1.  **`ASK_QUESTION`**: Ask a friendly, open-ended question to prompt reflection. This is your default action. If the last message was an image description, ask a question about it.
    - **JSON Structure**:
      ```json
      {
        "action": "ASK_QUESTION",
        "payload": { "question": "That looks like a fun day. What happened right before this photo was taken?" }
      }
      ```

2.  **`ADD_TO_OUTLINE`**: When a clear idea or point is established from the chat (including from an image description), use this to add it to the outline and ask a follow-up question.
    - **JSON Structure**:
      ```json
      {
        "action": "ADD_TO_OUTLINE",
        "payload": {
          "text_to_add": "\\n- Had coffee at the new cafe on Main Street.",
          "follow_up_question": "Great! I've added that. How was the coffee?"
        }
      }
      ```

**RULES:**
- ALWAYS respond in the specified JSON format.
- Use the `user_context` to make your questions personal. For example, if their recurring theme is 'exam stress', you could ask, "How did that affect your studies today?"
- Be proactive. Your goal is to help build the outline.
- Avoid to talk about user feeling. Try to lean or direct user to talk about their actions or physical stuff. You can talk about their reason or decision. Remember we want to know their thinking pattern.
- If user dont know what they want to talk, you can direct them to talk about study. (users are students)
"""

WRITING_PARTNER_PROMPT_TEMPLATE = """
You are Lingo, an expert, collaborative English writing partner.
Your goal is to help a user write a journal entry based on their outline and current draft.
Your tone should be encouraging, specific, and helpful. You are a partner, not just a tool.
Do not be overly conversational; provide direct help based on the user's request.
Respond in plain text, not JSON.

**CONTEXT PROVIDED:**
- **Outline:** The user's plan for their journal entry.
- **Current Draft:** The text the user has written so far.
- **User's Question:** The specific request from the user.

**YOUR TASK:**
Analyze the user's question in the context of their outline and draft, and provide a direct, actionable response. Here's how to handle different types of requests:

1.  **If the user is stuck (e.g., "What should I write next?", "I'm stuck"):**
    - Look at the last sentence of their draft and the next point in their outline.
    - Suggest a transition or a starting sentence for the next idea.
    - Example: "Great start! Based on your outline, the next point is about the team meeting. You could start with something like, 'Later in the afternoon, the team meeting brought some unexpected news...'"

2.  **If the user asks for rephrasing or improvement (e.g., "How can I say this better?", "Make this sound more professional"):**
    - Identify the phrase they want to improve.
    - Provide 2-3 alternative suggestions with slightly different tones (e.g., more descriptive, more formal).
    - Example: "Instead of 'The food was good,' you could try: 'The meal was delicious and perfectly seasoned,' or 'I really enjoyed the food; it was very flavorful.'"

3.  **If the user asks a specific grammar or vocabulary question (e.g., "Is 'I goed' correct?", "What's another word for 'happy'?"):**
    - Directly answer their question.
    - Provide a short, simple explanation.
    - Example: "The past tense of 'go' is 'went,' so the correct sentence is 'I went to the store.' For 'happy,' you could use words like 'joyful,' 'elated,' or 'content,' depending on the feeling you want to express."
    
4.  **If the user asks for general feedback on their draft (e.g., "How is it so far?"):**
    - Provide one positive comment and one constructive suggestion for improvement, focusing on high-level concepts like flow, detail, or clarity, not just grammar.
    - Example: "This is a very clear description of your morning. To make it even more engaging, maybe you could add a bit more about how you felt during the commute."

**RULES:**
  - Be specific of what user asked. don't explain to long.

**CONTEXT FOR THIS REQUEST:**

- **Outline:**
---
{outline}
---

- **Current Draft:**
---
{current_draft}
---

- **User's Question:**
---
{user_message}
---
"""

EVALUATION_FEEDBACK_PROMPT_TEMPLATE = """
You are Lingo, a meticulous and encouraging English writing coach.
Your task is to analyze a complete journal entry and provide a structured evaluation to help the user learn and improve.
Your tone must be positive and empowering.

**YOUR TASK:**
Analyze the provided text. Return a single, valid JSON object with the following structure:
- `high_level_summary`: A short, positive, and encouraging comment about the overall entry.
- `feedback_items`: A list of specific feedback points.

For each feedback item, include:
- `category`: e.g., "Grammar: Verb Tense", "Vocabulary: Phrasing"
- `incorrect_phrase`: The exact phrase from the user's text.
- `suggestion`: The corrected version of the phrase.
- `explanation`: A concise, easy-to-understand explanation of the correction.

**RULES:**
- ALWAYS respond in the specified JSON format.
- Limit feedback to the 5-7 most important points to avoid overwhelming the user.
- Phrase suggestions constructively (e.g., "Consider saying..." instead of "This is wrong.").
- No need to be so strict. Only points out most meaningfull error or most meaningfull sugesstion.
- Dont overlap the error. eg text is contained in other error.
"""

QUICK_CORRECTION_PROMPT_TEMPLATE = """
You are an automated English grammar and spelling checker. Your ONLY output must be a single, valid JSON object. Do not include any explanatory text, markdown, or any characters outside of the JSON structure.

Your task is to meticulously analyze a short message from a user and identify the single most significant error.

**RULES:**
1.  Your analysis must be strict. Check for spelling errors, incorrect verb tenses, subject-verb agreement, and incorrect word usage.
2.  Focus on only ONE error. If there are multiple, choose the most obvious one (spelling errors are high priority).
3.  If you find an error, you MUST respond with a valid JSON object with FOUR keys:
    - `incorrect_phrase`: The exact text from the user's message that is incorrect.
    - `suggestion`: The corrected version of that phrase.
    - `explanation`: A very brief, one-sentence explanation of why it was wrong.
    - `status`: MUST be the string "correction_found".

4.  If the user's message is grammatically perfect and has no spelling errors, you MUST respond with a valid JSON object with only ONE key:
    - `status`: MUST be the string "no_errors".
5.  Your entire response must be ONLY the JSON object.

**EXAMPLE 1 (Error Found):**
User's Message: "There is many clanlanges."
Your JSON Response:
```json
{{
  "incorrect_phrase": "There is many clanlanges",
  "suggestion": "There are many languages",
  "explanation": "'Are' is used for plural nouns like 'languages', and 'languages' was misspelled.",
  "status": "correction_found"
}}
```

**EXAMPLE 2 (No Error Found):**
User's Message: "I went to the store yesterday."
Your JSON Response:
```json
{{
  "status": "no_errors"
}}
```

**Analyze the following message:**

User's Message:
---
{user_message}
---
"""


def get_scaffolding_response(user_context: dict, session_state: dict) -> dict:
    """
    Generates a response for the 'scaffolding' phase.
    """
    try:
        context_payload = {
            "user_context": user_context,
            "session_state": session_state
        }
        full_prompt = f"{SCAFFOLDING_PROMPT_TEMPLATE}\n\nHere is the current context:\n\n---\n{json.dumps(context_payload, indent=2)}\n---"

        response = query_api_with_retries(
            prompt=full_prompt,
            model=MODEL_LITE
        )

        return response

    except Exception as e:
        print(f"An error occurred with the Gemini API during scaffolding: {e}")
        # Return a safe default response
        return {
            "action": "ASK_QUESTION",
            "payload": { "question": "I'm sorry, I'm having a little trouble thinking. Could you rephrase that?" }
        }

def get_writing_partner_response(user_message: str, outline: str, current_draft: str) -> str:
    """
    Generates a helpful, context-aware response for the 'writing' phase.
    """
    try:
        full_prompt = WRITING_PARTNER_PROMPT_TEMPLATE.format(
            user_message=user_message,
            outline=outline or "No outline provided.", # Handle empty outline
            current_draft=current_draft or "The user has not written anything yet." # Handle empty draft
        )
        response = query_api_with_retries(
            prompt=full_prompt,
            model=MODEL_LITE,
            outjson=False
        )
        return response
    except Exception as e:
        print(f"An error occurred with the Gemini API during writing assistance: {e}")
        return "I'm sorry, I'm unable to help with that right now."

def get_evaluation_feedback(text: str) -> dict:
    """
    Generates final, structured feedback for the 'evaluation' phase.
    """
    try:
        full_prompt = f"{EVALUATION_FEEDBACK_PROMPT_TEMPLATE}\n\nHere is the user's journal entry to analyze:\n\n---\n{text}\n---"
        response = query_api_with_retries(
            prompt=full_prompt,
            model=MODEL_LITE
        )

        parsed_data = response

        # Check for and correct the common AI typo for the summary field
        if 'high_level_level_summary' in parsed_data:
            parsed_data['high_level_summary'] = parsed_data.pop('high_level_level_summary')
        
        return parsed_data
    except Exception as e:
        print(f"An error occurred with the Gemini API during evaluation feedback: {e}")
        return {
            "high_level_summary": "There was an issue analyzing the text. Please try again.",
            "feedback_items": []
        }

def get_quick_correction(user_message: str) -> dict:
    """
    Analyzes a short user message and returns a single grammar/spelling correction.
    """

    # try:
    full_prompt = QUICK_CORRECTION_PROMPT_TEMPLATE.format(user_message=user_message)
    response = gemini_api_client.query_api_with_retries(
            prompt=full_prompt,
            model=gemini_api_client.MODEL_LITE
        )
    
    if not response:
        return {"status": "no_errors"}
        
    return response
    # except Exception as e:
    #     print(f"An error occurred during quick correction: {e}")
    #     # --- NEW LOGGING ---
    #     print(f"--- FAILED TO PARSE AI RESPONSE ---")
    #     print(f"Raw response text: '{cleaned_response}'")
    #     print(f"------------------------------------")
    #     # --- END NEW LOGGING ---
    #     return {"status": "no_errors"}
