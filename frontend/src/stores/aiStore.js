import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { useJournalStore } from './journalStore';

export const useAiStore = defineStore('ai', {
  state: () => ({
    feedback: [],
    isLoading: false,
    error: null,
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

    // --- REWORKED and FIXED Action: Chat with the AI ---
    async chatWithAI(date, message) {
      this.isLoading = true;
      this.error = null;
      const journalStore = useJournalStore();
      
      try {
        // REMOVED: The previous optimistic update was causing instability.
        // This simplified version ensures the API call is always made reliably.

        // 1. Make the actual API call.
        await apiClient.post(`/ai/chat/${date}`, { message });

        // 2. After the API call succeeds, fetch the updated journal from the server.
        // This will bring in both the user's new message and the AI's reply.
        await journalStore.fetchJournalByDate(date, true); // force refresh

      } catch (err) {
        this.error = 'An error occurred during the chat. Please try again.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});

