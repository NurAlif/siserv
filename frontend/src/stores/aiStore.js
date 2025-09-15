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

    async chatWithAI(date, message) {
      this.isLoading = true;
      this.error = null;
      const journalStore = useJournalStore();
      
      // Optimistically add the user's message
      const userMessage = {
        id: `temp-${Date.now()}`, // A temporary ID for Vue's :key binding
        sender: 'user',
        message_type: 'conversation',
        message_text: message,
      };
      journalStore.addChatMessageOptimistically(date, userMessage);
      
      try {
        // This POST request triggers the backend logic
        await apiClient.post(`/ai/chat/${date}`, { message });

        // CRITICAL STEP: This fetches the updated journal, including
        // any outline changes made by the AI agent on the backend.
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
