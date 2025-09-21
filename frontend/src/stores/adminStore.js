import { defineStore } from 'pinia';
import apiClient from '../services/api';

export const useAdminStore = defineStore('admin', {
  state: () => ({
    students: [],
    studentDetails: null,
    classErrorDistribution: [],
    classErrorTrend: [],
    isLoading: false,
    error: null,
  }),
  actions: {
    async fetchStudents() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/admin/students');
        this.students = response.data;
      } catch (err) {
        this.error = 'Failed to load students.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchStudentDetails(studentId) {
      this.isLoading = true;
      this.error = null;
      this.studentDetails = null;
      try {
        const response = await apiClient.get(`/admin/students/${studentId}`);
        this.studentDetails = response.data;
      } catch (err) {
        this.error = `Failed to load details for student ${studentId}.`;
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchClassAnalytics() {
        this.isLoading = true;
        this.error = null;
        try {
            const [distributionRes, trendRes] = await Promise.all([
                apiClient.get('/admin/analytics/error-distribution'),
                apiClient.get('/admin/analytics/error-trend')
            ]);
            this.classErrorDistribution = distributionRes.data;
            this.classErrorTrend = trendRes.data;
        } catch (err) {
            this.error = 'Failed to load class analytics.';
            console.error(err);
        } finally {
            this.isLoading = false;
        }
    },
  },
});
