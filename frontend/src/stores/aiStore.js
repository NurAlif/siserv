import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { useJournalStore } from './journalStore';

export const useAiStore = defineStore('ai', {
  state: () => ({
    feedback: [],
    isLoading: false,
    error: null,
    conceptualFeedback: null,
    isConceptualLoading: false,
  }),
  actions: {
    async getFeedback(date, text) {
      this.isLoading = true;
      this.error = null;
      this.feedback = []; // Clear previous feedback before fetching new results
      try {
        // According to the API docs, the endpoint is /api/ai/feedback/{journal_date}
        const response = await apiClient.post(`/ai/feedback/${date}`, { text });
        
        // The response body is expected to be an object like { "feedback": [...] }
        this.feedback = response.data.feedback || [];
      } catch (err) {
        this.error = 'An error occurred while getting AI feedback. Please try again.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async getConceptualFeedback(date, text) {
      this.isConceptualLoading = true;
      this.error = null;
      this.conceptualFeedback = null; // Clear previous feedback
      try {
        const response = await apiClient.post(`/ai/conceptual-feedback/${date}`, { text });
        this.conceptualFeedback = response.data.feedback_text;
      } catch (err) {
        this.error = 'An error occurred while getting high-level feedback.';
        console.error(err);
      } finally {
        this.isConceptualLoading = false;
      }
    },

    // --- REWORKED and FIXED Action: Chat with the AI ---
    async chatWithAI(date, message) {
      this.isLoading = true;
      this.error = null;
      const journalStore = useJournalStore();
      
      // --- FIX: Optimistic UI Update ---
      // 1. Create a temporary message object for the user's input to display it immediately.
      const userMessage = {
        id: `temp-${Date.now()}`, // A temporary ID for Vue's :key binding
        sender: 'user',
        message_type: 'conversation',
        message_text: message,
      };

      // 2. Add this temporary message to the local state so the UI updates instantly.
      journalStore.addChatMessageOptimistically(date, userMessage);
      
      try {
        // 3. Make the actual API call to the backend.
        await apiClient.post(`/ai/chat/${date}`, { message });

        // 4. After the API call succeeds, fetch the updated journal from the server.
        // This will replace the optimistic update with the final, correct data from the database,
        // including the AI's response and the user's message with its permanent ID.
        await journalStore.fetchJournalByDate(date, true); // force refresh

      } catch (err) {
        this.error = 'An error occurred during the chat. Please try again.';
        console.error(err);
        // NOTE: In a production app, you might want to add logic here to remove
        // the optimistic message if the API call fails.
      } finally {
        this.isLoading = false;
      }
    },
  },
});
