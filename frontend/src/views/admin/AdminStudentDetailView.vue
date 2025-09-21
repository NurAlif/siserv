<template>
  <main id="admin-student-detail-view" class="fade-in">
    <!-- Header -->
    <div class="mb-6">
      <router-link to="/admin" class="text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-100 font-medium flex items-center gap-2 mb-4">
         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        Back to Admin Dashboard
      </router-link>
    </div>
    
    <!-- Loading and Error States -->
    <div v-if="adminStore.isLoading" class="text-center py-10">
      <p class="text-gray-500 dark:text-gray-400">Loading student details...</p>
    </div>
    <div v-else-if="adminStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
      <p>{{ adminStore.error }}</p>
    </div>

    <div v-else-if="adminStore.studentDetails" class="space-y-6">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ adminStore.studentDetails.username }}</h2>
        <p class="text-gray-500 dark:text-gray-400 mt-1">{{ adminStore.studentDetails.email }}</p>
      </div>

      <!-- Stat Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <AdminStatCard title="Total Journals" :value="adminStore.studentDetails.journal_count" />
        <AdminStatCard title="Total Errors" :value="adminStore.studentDetails.total_errors" />
        <AdminStatCard title="Last Active" :value="formatDate(adminStore.studentDetails.last_active)" />
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ErrorDistributionChart title="Student Error Distribution" :chart-raw-data="adminStore.studentDetails.error_distribution" />
        <ErrorTrendChart title="Student Error Trend" :chart-raw-data="adminStore.studentDetails.error_trend" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAdminStore } from '../../stores/adminStore';
import { formatDistanceToNow } from 'date-fns';
import AdminStatCard from '../../components/admin/AdminStatCard.vue';
import ErrorDistributionChart from '../../components/admin/ErrorDistributionChart.vue';
import ErrorTrendChart from '../../components/admin/ErrorTrendChart.vue';

const route = useRoute();
const adminStore = useAdminStore();
const studentId = route.params.id;

const loadDetails = () => {
  if (studentId) {
    adminStore.fetchStudentDetails(studentId);
  }
};

onMounted(loadDetails);

watch(() => route.params.id, (newId) => {
  if (newId) {
    loadDetails();
  }
});

const formatDate = (dateString) => {
  if (!dateString) return 'Never';
  return formatDistanceToNow(new Date(dateString), { addSuffix: true });
};
</script>
