import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { format, parseISO } from 'date-fns';
import { useRouter } from 'vue-router';

export const useJournalStore = defineStore('journal', {
  state: () => ({
    journals: [],
    isLoading: false,
    error: null,
  }),
  getters: {
    getJournalByDate: (state) => (date) => {
      return state.journals.find(j => j.journal_date === date);
    }
  },
  actions: {
    // --- Existing actions ---
    async fetchJournals() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/journals/');
        // The API returns journal_date as a string like "2025-09-10"
        // We'll format it for display later, but store as is.
        this.journals = response.data;
      } catch (err) {
        this.error = 'Failed to load journal entries.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    async fetchJournalByDate(date, forceRefresh = false) {
        // Check if we already have it and are not forcing a refresh
        const existing = this.getJournalByDate(date);
        if (existing && !forceRefresh) {
            return existing;
        }

        // If not, fetch it from the API
        this.isLoading = true;
        this.error = null;
       try {
            const response = await apiClient.get(`/journals/${date}`);
            
            // If it already exists, update it. Otherwise, add it.
            const index = this.journals.findIndex(j => j.journal_date === date);
            if (index !== -1) {
                // FIXED: Use splice to ensure reactivity
                this.journals.splice(index, 1, response.data);
            } else {
                this.journals.push(response.data);
            }
            return response.data;
        } catch (err) {
            this.error = 'Failed to load journal entry.';
            console.error(err);
            return null; // Return null on failure
        } finally {
            this.isLoading = false;
        }
    },

    // --- New Action: Create a journal entry ---
    async createJournal(content) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.post('/journals/', { content });
        // Add the new journal to the front of our local list
        this.journals.unshift(response.data);
        return response.data; // Return the created journal
      } catch (err) {
        this.error = 'Failed to create journal entry.';
        console.error(err);
        return null;
      } finally {
        this.isLoading = false;
      }
    },

    async updateJournal(date, payload) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.put(`/journals/${date}`, payload);
        // Find and update the journal in our local list
        const index = this.journals.findIndex(j => j.journal_date === date);
        if (index !== -1) {
          this.journals[index] = response.data;
        }
        return response.data;
      } catch (err) {
        this.error = 'Failed to update journal entry.';
        console.error(err);
        return null;
      } finally {
        this.isLoading = false;
      }
    },
    
    async updateJournalPhase(date, phase) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.put(`/journals/${date}/phase`, { phase });
        const index = this.journals.findIndex(j => j.journal_date === date);
        if (index !== -1) {
          this.journals[index] = response.data;
        }
        return response.data;
      } catch (err) {
        this.error = 'Failed to update journal phase.';
        console.error(err);
        return null;
      } finally {
        this.isLoading = false;
      }
    },

    addChatMessageOptimistically(date, message) {
      const journal = this.getJournalByDate(date);
      if (journal) {
        // Ensure the chat_messages array exists before pushing to it.
        if (!journal.chat_messages) {
          journal.chat_messages = [];
        }
        journal.chat_messages.push(message);
      }
    },

    updateLocalJournal(updatedJournal) {
      if (!updatedJournal || !updatedJournal.journal_date) return;
      
      const index = this.journals.findIndex(j => j.journal_date === updatedJournal.journal_date);
      if (index !== -1) {
        // Use splice for reactivity
        this.journals.splice(index, 1, updatedJournal);
      } else {
        // If it's a new journal not yet in the list (should be rare for updates)
        this.journals.unshift(updatedJournal);
      }
    },

    // --- New Action: Directly set a journal's content ---
    // This allows other stores (like the AI store) to update content reactively
    setJournalContent(date, newContent) {
      const index = this.journals.findIndex(j => j.journal_date === date);
      if (index !== -1) {
        this.journals[index].content = newContent;
      }
    },

    formatDisplayDate(dateString) {
      if (!dateString) return '';
      // parseISO handles the 'YYYY-MM-DD' format
      const date = parseISO(dateString);
      return format(date, 'MMMM d, yyyy');
    }
  },
});

