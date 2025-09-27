import { defineStore } from 'pinia';
import apiClient from '../services/api';

export const useAdminStore = defineStore('admin', {
  state: () => ({
    students: [],
    studentDetails: null,
    studentJournals: [],
    currentStudentJournal: null,
    classAnalytics: null, // This will hold all dashboard data
    isLoading: false,
    isLoadingJournals: false,
    error: null,
    whitelist: [], // New state for student whitelist
    isLoadingWhitelist: false, // New loading state
  }),
  actions: {
    async fetchAllStudents() {
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
        this.classAnalytics = null;
        try {
            // Fetch all data points for the dashboard
            const distributionRes = await apiClient.get('/admin/analytics/error-distribution');
            const trendRes = await apiClient.get('/admin/analytics/error-trend');
            
            // For stats, we can aggregate from the full student list
            const studentsRes = await apiClient.get('/admin/students');
            const studentsData = studentsRes.data;

            const total_students = studentsData.length;
            const total_journals = studentsData.reduce((sum, student) => sum + student.journal_count, 0);
            const total_errors = studentsData.reduce((sum, student) => sum + student.total_errors, 0);
            const avg_errors_per_journal = total_journals > 0 ? total_errors / total_journals : 0;
            
            // Combine all data into the classAnalytics object
            this.classAnalytics = {
              total_students,
              total_journals,
              total_errors,
              avg_errors_per_journal,
              error_distribution: distributionRes.data,
              error_trend: trendRes.data,
            };

        } catch (err) {
            this.error = 'Failed to load class analytics.';
            console.error(err);
        } finally {
            this.isLoading = false;
        }
    },

    async fetchStudentJournals(studentId) {
      this.isLoadingJournals = true;
      this.error = null;
      this.studentJournals = []; 
      try {
        const response = await apiClient.get(`/admin/students/${studentId}/journals`);
        this.studentJournals = response.data;
      } catch (err) {
        this.error = `Failed to load journals for student ${studentId}.`;
        console.error(err);
      } finally {
        this.isLoadingJournals = false;
      }
    },
    
    async fetchSingleStudentJournal(studentId, journalDate) {
      this.isLoading = true;
      this.error = null;
      this.currentStudentJournal = null;
      try {
        const response = await apiClient.get(`/admin/students/${studentId}/journals/${journalDate}`);
        this.currentStudentJournal = response.data;
      } catch (err) {
        this.error = `Failed to load journal for date ${journalDate}.`;
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    // --- NEW ACTIONS for Whitelist Management ---
    async fetchWhitelist() {
      this.isLoadingWhitelist = true;
      this.error = null;
      try {
        const response = await apiClient.get('/admin/whitelist');
        this.whitelist = response.data;
      } catch (err) {
        this.error = 'Failed to load student whitelist.';
        console.error(err);
      } finally {
        this.isLoadingWhitelist = false;
      }
    },

    async addStudentToWhitelist(studentData) {
      // Clear previous errors before a new attempt
      this.error = null;
      try {
        const response = await apiClient.post('/admin/whitelist', studentData);
        this.whitelist.push(response.data);
        // Sort the list after adding
        this.whitelist.sort((a, b) => a.student_id.localeCompare(b.student_id));
        return { success: true };
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to add student.';
        console.error(err);
        return { success: false, error: this.error };
      }
    },

    async removeStudentFromWhitelist(studentId) {
      this.error = null;
      try {
        await apiClient.delete(`/admin/whitelist/${studentId}`);
        this.whitelist = this.whitelist.filter(s => s.student_id !== studentId);
        return { success: true };
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to remove student.';
        console.error(err);
        return { success: false, error: this.error };
      }
    },
  },
});
