import google.generativeai as genai
from sqlalchemy.orm import Session, joinedload
import json
from datetime import datetime

from .. import models, database
from ..config import settings

# Configure the Gemini API client
try:
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    model = None

def _call_gemini_api(prompt):
    """A helper to safely call the Gemini API and parse JSON."""
    if not model:
        raise ConnectionError("Generative AI model is not configured.")
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error calling Gemini API or parsing JSON: {e}")
        return None

def get_thematic_summary(text: str) -> str:
    """Generates a thematic summary of the journal entry."""
    prompt = f"Summarize the key events, topics, and overall sentiment of this journal entry in a few sentences.\n\n---\n{text}\n---"
    if not model:
        return "Summary generation unavailable."
    response = model.generate_content(prompt)
    return response.text.strip()

def get_cognitive_patterns(summary: str) -> dict:
    """Extracts cognitive patterns from the summary."""
    prompt = f"""
From the summary below, identify recurring themes, the user's decision-making style (e.g., logical, emotional, cautious), and any expressed problems or challenges.
Format the output as a valid JSON object with keys: "recurring_themes" (list of strings), "decision_style" (string), "recent_sentiments" (string).

Summary:
---
{summary}
---
"""
    return _call_gemini_api(prompt)

def get_linguistic_patterns(text: str) -> dict:
    """Extracts linguistic patterns from the user's text."""
    prompt = f"""
Analyze this text from an English learner. Identify up to 3 common error types (e.g., 'Verb Tense'), assess the vocabulary level (Beginner, Intermediate, Advanced), and find one example of a linguistic strength (e.g., 'Good use of adjectives').
Format as a valid JSON object with keys: "common_errors" (list of dicts with "type" and "example"), "vocabulary_level" (string), "strength" (string).

Text:
---
{text}
---
"""
    return _call_gemini_api(prompt)

def process_journal(journal_id: int, user_id: int):
    """
    The main function for the asynchronous context agent.
    Fetches a completed journal, analyzes it, and updates the user's context profile.
    """
    db = next(database.get_db())
    try:
        journal = db.query(models.Journal).options(
            joinedload(models.Journal.chat_messages)
        ).filter(models.Journal.id == journal_id).first()

        if not journal:
            print(f"Context Agent: Journal with id {journal_id} not found.")
            return

        full_text = journal.content + "\n\nChat History:\n" + "\n".join(
            [f"{msg.sender.name}: {msg.message_text}" for msg in journal.chat_messages]
        )

        # Step 1: Thematic Summary
        summary = get_thematic_summary(full_text)

        # Steps 2 & 3: Cognitive and Linguistic Extraction
        cognitive_insights = get_cognitive_patterns(summary)
        linguistic_insights = get_linguistic_patterns(journal.content)

        # Step 4: Consolidation
        profile = db.query(models.UserContextProfile).filter(models.UserContextProfile.user_id == user_id).first()
        if not profile:
            profile = models.UserContextProfile(user_id=user_id, profile_data={})
            db.add(profile)

        # Merge new insights. A simple overwrite is robust for this structure.
        updated_profile_data = {
            "linguistic_profile": linguistic_insights or {},
            "cognitive_profile": cognitive_insights or {}
        }
        profile.profile_data = updated_profile_data
        profile.last_updated = datetime.utcnow()

        db.commit()
        print(f"Context Agent: Successfully processed journal {journal_id} for user {user_id}.")

    except Exception as e:
        print(f"Context Agent: An error occurred during processing: {e}")
        db.rollback()
    finally:
        db.close()
