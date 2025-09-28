import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { format, parseISO } from 'date-fns';
import { useRouter } from 'vue-router';

export const useJournalStore = defineStore('journal', {
  state: () => ({
    journals: [],
    isLoading: false,
    error: null,
    isUploading: false, // New state for image uploads
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
        this.updateLocalJournal(response.data);
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
        this.updateLocalJournal(response.data);
        return response.data;
      } catch (err) {
        this.error = 'Failed to update journal phase.';
        console.error(err);
        return null;
      } finally {
        this.isLoading = false;
      }
    },

    // --- UPDATED ACTION for optimistic image uploading ---
    async uploadImage(date, file) {
      this.isUploading = true;
      this.error = null;
      
      // --- Optimistic UI Start ---
      const tempId = `temp-img-${Date.now()}`;
      const localUrl = URL.createObjectURL(file); // Create a local URL for the image preview

      const optimisticMessage = {
        id: tempId,
        sender: 'user',
        message_type: 'image',
        message_text: 'Uploading...', // Placeholder text
        timestamp: new Date().toISOString(), // Use current time for sorting
        image: {
          id: tempId,
          file_path: localUrl, // Use the local blob URL for immediate display
          ai_description: 'Generating description...'
        },
        isOptimistic: true // Flag to identify this temporary message if needed
      };
      
      // Add the optimistic message to the UI immediately
      this.addChatMessageOptimistically(date, optimisticMessage);
      // --- Optimistic UI End ---

      try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await apiClient.post(`/journals/${date}/images`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        
        // The response contains the updated journal, which replaces the optimistic one.
        this.updateLocalJournal(response.data);

      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to upload image.';
        console.error(err);
        // If upload fails, remove the optimistic message from the chat
        const journal = this.getJournalByDate(date);
        if (journal) {
          journal.chat_messages = journal.chat_messages.filter(m => m.id !== tempId);
        }
      } finally {
        this.isUploading = false;
        // Clean up the created blob URL to prevent memory leaks
        URL.revokeObjectURL(localUrl);
      }
    },

    addChatMessageOptimistically(date, message) {
      const journal = this.getJournalByDate(date);
      if (journal) {
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
        this.journals.splice(index, 1, updatedJournal);
      } else {
        this.journals.unshift(updatedJournal);
      }
    },

    setJournalContent(date, newContent) {
      const index = this.journals.findIndex(j => j.journal_date === date);
      if (index !== -1) {
        this.journals[index].content = newContent;
      }
    },

    formatDisplayDate(dateString) {
      if (!dateString) return '';
      const date = parseISO(dateString);
      return format(date, 'MMMM d, yyyy');
    }
  },
});
