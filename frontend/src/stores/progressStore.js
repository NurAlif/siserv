import { defineStore } from 'pinia';
import apiClient from '../services/api';

export const useProgressStore = defineStore('progress', {
  state: () => ({
    summary: null,
    topics: [],
    currentTopicDetails: null,
    isLoading: false,
    error: null,
  }),
  actions: {
    async fetchProgressSummary() {
      this.isLoading = true;
      this.error = null;
      this.summary = null;
      try {
        const response = await apiClient.get('/progress/summary');
        this.summary = response.data;
      } catch (err) {
        this.error = 'Failed to load progress summary.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchTopics() {
      this.isLoading = true;
      this.error = null;
      this.topics = [];
      try {
        const response = await apiClient.get('/progress/topics');
        this.topics = response.data;
      } catch (err) {
        this.error = 'Failed to load learning topics.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchTopicDetails(topicId) {
      this.isLoading = true;
      this.error = null;
      this.currentTopicDetails = null;
      try {
        const response = await apiClient.get(`/progress/topics/${topicId}`);
        this.currentTopicDetails = response.data;
      } catch (err) {
        this.error = `Failed to load details for topic ${topicId}.`;
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});

