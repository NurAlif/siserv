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
      this.feedback = []; // Clear previous feedback
      this.conceptualFeedback = null;
      try {
        const response = await apiClient.post(`/ai/feedback/${date}`, { text });
        // The new response has a different structure
        this.feedback = response.data.feedback_items || [];
        this.conceptualFeedback = response.data.high_level_summary || null;
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
      
      // Optimistically add the user's message for perceived speed
      const userMessage = {
        id: `temp-${Date.now()}`,
        sender: 'user',
        message_type: 'conversation',
        message_text: message,
      };
      journalStore.addChatMessageOptimistically(date, userMessage);
      
      try {
        // The API now returns the complete, updated journal object
        const response = await apiClient.post(`/ai/chat/${date}`, { message });
        
        // **KEY CHANGE**: Update the entire journal state with the response from the API.
        // This is more robust than fetching again.
        journalStore.updateLocalJournal(response.data);

      } catch (err) {
        this.error = 'An error occurred during the chat. Please try again.';
        console.error(err);
        // NOTE: In a production app, you might want to remove the optimistic message on failure.
      } finally {
        this.isLoading = false;
      }
    },
  },
});
