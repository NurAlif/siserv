import { defineStore } from 'pinia';
import apiClient from '../services/api';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    activeNotifications: [],
    notificationHistory: [],
    isLoading: false,
    isLoadingHistory: false,
    error: null,
    hasManuallyOpened: false,
    showHistoryModal: false,
  }),
  getters: {
    notificationCount: (state) => state.activeNotifications.length,
    hasNotifications: (state) => state.activeNotifications.length > 0,
    shouldShowModal: (state) => state.hasNotifications && !state.hasManuallyOpened,
  },
  actions: {
    async fetchActiveNotifications() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/notifications/active');
        this.activeNotifications = response.data;
      } catch (err) {
        this.error = 'Failed to load notifications.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchNotificationHistory() {
      this.isLoadingHistory = true;
      this.error = null;
      try {
        const response = await apiClient.get('/notifications/history');
        this.notificationHistory = response.data;
      } catch (err) {
        this.error = 'Failed to load notification history.';
        console.error(err);
      } finally {
        this.isLoadingHistory = false;
      }
    },

    async markAsSeen(notificationId) {
      try {
        await apiClient.post(`/notifications/seen/${notificationId}`);
        this.removeNotificationById(notificationId);
      } catch (err) {
        console.error('Failed to mark notification as seen:', err);
      }
    },

    async submitSurvey(payload) {
      this.isLoading = true;
      this.error = null;
      try {
        await apiClient.post('/notifications/responses', payload);
        this.removeNotificationById(payload.notification_id);
      } catch (err) {
        this.error = 'Failed to submit survey.';
        console.error(err);
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    userOpenedNotifications() {
      this.hasManuallyOpened = true;
      this.showHistoryModal = true;
      this.fetchNotificationHistory();
    },

    closeHistoryModal() {
      this.showHistoryModal = false;
    },
    
    resetManualOpenState() {
      this.hasManuallyOpened = false;
      this.showHistoryModal = false;
    },

    removeNotificationById(notificationId) {
      const index = this.activeNotifications.findIndex(n => n.id === notificationId);
      if (index !== -1) {
        this.activeNotifications.splice(index, 1);
      }
    },
  },
});

