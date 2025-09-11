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

    // --- New Action: Chat with the AI ---
    async chatWithAI(date, message) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.post(`/ai/chat/${date}`, { message });
        const { updated_journal_content } = response.data;
        
        // After getting the response, update the journal's content in the journalStore
        const journalStore = useJournalStore();
        journalStore.setJournalContent(date, updated_journal_content);

      } catch (err) {
        this.error = 'An error occurred during the chat. Please try again.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
