<template>
  <main id="admin-dashboard-view" class="p-4 md:p-6 fade-in">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Admin Dashboard</h2>
      <p class="text-gray-500 dark:text-gray-400">Overview of class progress and statistics.</p>
    </div>

    <!-- Loading and Error States -->
    <div v-if="adminStore.isLoading" class="text-center py-10">
      <p class="text-gray-500 dark:text-gray-400">Loading analytics...</p>
    </div>
    <div v-else-if="adminStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
      <p>{{ adminStore.error }}</p>
    </div>

    <div v-else-if="adminStore.classAnalytics">
      <!-- Stat Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <AdminStatCard title="Total Students" :value="adminStore.classAnalytics.total_students" />
        <AdminStatCard title="Total Journal Entries" :value="adminStore.classAnalytics.total_journals" />
        <AdminStatCard title="Total Errors Logged" :value="adminStore.classAnalytics.total_errors" />
        <AdminStatCard title="Avg Errors per Journal" :value="adminStore.classAnalytics.avg_errors_per_journal.toFixed(2)" />
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Error Distribution Chart -->
        <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 class="font-semibold text-gray-800 dark:text-gray-200 mb-2">Class Error Distribution</h3>
          <div class="relative h-80">
            <ErrorDistributionChart :chart-data="adminStore.classAnalytics?.error_distribution" />
          </div>
        </div>

        <!-- Error Trend Chart -->
        <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 class="font-semibold text-gray-800 dark:text-gray-200 mb-2">Class Error Trend (Last 30 Days)</h3>
          <div class="relative h-80">
            <ErrorTrendChart :chart-data="adminStore.classAnalytics?.error_trend" />
          </div>
        </div>
      </div>

      <!-- Student Table -->
      <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">Students</h3>
        <StudentTable :students="adminStore.students" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAdminStore } from '../../stores/adminStore';
import AdminStatCard from '../../components/admin/AdminStatCard.vue';
import ErrorDistributionChart from '../../components/admin/ErrorDistributionChart.vue';
import ErrorTrendChart from '../../components/admin/ErrorTrendChart.vue';
import StudentTable from '../../components/admin/StudentTable.vue';

const adminStore = useAdminStore();

onMounted(() => {
  adminStore.fetchClassAnalytics();
  adminStore.fetchAllStudents();
});
</script>

