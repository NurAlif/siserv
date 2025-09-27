<template>
  <main id="admin-dashboard-view" class="p-4 md:p-6 fade-in">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-6">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Admin Dashboard</h2>
          <p class="text-gray-500 dark:text-gray-400">Overview of class progress and statistics.</p>
        </div>
        <div class="flex items-center gap-3">
          <!-- Button to open the admin manual -->
          <button @click="showManualModal = true" class="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 font-semibold px-4 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24a8,8,0,0,0-8,8V64a8,8,0,0,0,16,0V32A8,8,0,0,0,128,24Zm0,176a8,8,0,0,0-8,8v32a8,8,0,0,0,16,0V208A8,8,0,0,0,128,200Zm88-88H192a8,8,0,0,0,0,16h24a8,8,0,0,0,0-16ZM40,120H64a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16Zm151.78-63.78a8,8,0,0,0-11.32,0L158.11,78.59a8,8,0,0,0,11.31,11.31l22.35-22.34a8,8,0,0,0,0-11.32ZM78.59,158.11,56.24,180.46a8,8,0,0,0,11.32,11.32l22.34-22.35a8,8,0,0,0-11.31-11.31Zm11.31-68.2L67.54,67.54a8,8,0,0,0-11.32,11.32l22.35,22.34a8,8,0,0,0,11.31-11.31ZM128,72a56,56,0,1,0,56,56A56.06,56.06,0,0,0,128,72Zm0,96a40,40,0,1,1,40-40A40,40,0,0,1,128,168Z"></path></svg>
            Admin Manual
          </button>
          <router-link
            to="/admin/manage-students"
            class="bg-indigo-600 text-white font-semibold px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path></svg>
            Manage Whitelist
          </router-link>
        </div>
      </div>
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
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Error Distribution Chart -->
          <div class="relative h-80 mb-16">
            <ErrorDistributionChart title="Class Error Distribution" :chart-raw-data="adminStore.classAnalytics.error_distribution" />
          </div>

        <!-- Error Trend Chart -->
          <div class="relative h-80 mb-16">
            <ErrorTrendChart title="Class Error Trend" :chart-raw-data="adminStore.classAnalytics.error_trend" />
          </div>
      </div>
      <!-- Student Table -->
      <div>
        <StudentTable :students="adminStore.students" />
      </div>
    </div>
     <!-- Modal for the admin manual -->
    <ManualModal 
        :show="showManualModal" 
        title="LingoJourn Administrator Manual"
        :content="adminManualContent"
        @close="showManualModal = false" 
    />
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAdminStore } from '../../stores/adminStore';
import AdminStatCard from '../../components/admin/AdminStatCard.vue';
import ErrorDistributionChart from '../../components/admin/ErrorDistributionChart.vue';
import ErrorTrendChart from '../../components/admin/ErrorTrendChart.vue';
import StudentTable from '../../components/admin/StudentTable.vue';
import ManualModal from '../../components/ManualModal.vue'; // Import the new modal component

const adminStore = useAdminStore();
const showManualModal = ref(false); // State to control the modal's visibility

onMounted(() => {
  adminStore.fetchClassAnalytics();
  adminStore.fetchAllStudents();
});

// The content for the admin manual is stored here as an HTML string.
// I've added an image with loading="lazy" to illustrate a key feature.
const adminManualContent = `
<h1>LingoJourn Administrator Manual</h1>
<p>Welcome, Administrator! This guide provides an overview of the tools available to you for managing students and monitoring class-wide progress.</p>
<hr>
<h2>1. The Admin Dashboard</h2>
<p>This is your main view, providing a high-level summary of your class's activity.</p>
<h3>Key Analytics & Charts</h3>
<p>The dashboard gives you a live look at class-wide statistics and charts showing common error types and performance trends over time. This helps you quickly identify topics the whole class may be struggling with.</p>
  <img src="https://ipa.parasyst.com/static/images/admin_dashboard.png" alt="login" loading="lazy">
  <br/>
<h3>Student List</h3>
<p>The table at the bottom of the dashboard lists all registered students with a summary of their activity. You can click "View" on any student to see their detailed profile.</p>
  <img src="https://ipa.parasyst.com/static/images/students_admin.png" alt="login" loading="lazy">
  <br/>
<hr>
<h2>2. Managing Student Access</h2>
<p>You control who can register for LingoJourn via the student whitelist. From the Admin Dashboard, click the <strong>Manage Whitelist</strong> button.</p>
<h3>Adding a Student</h3>
<ol>
    <li>On the "Manage Student Whitelist" page, enter the student's <strong>Student ID</strong> and <strong>Email Address</strong> into the form.</li>
    <li>Click the "Add Student" button. The student will now be able to create an account.</li>
</ol>
<h3>Removing a Student</h3>
<p>In the whitelist table, find the student you wish to remove and click the "Remove" button. This prevents them from registering (it does not delete an existing account).</p>
<hr>
<h2>3. Monitoring & Reviewing Student Work</h2>
<p>To see how a specific student is doing, click "View" from the main student list on the dashboard. This will take you to their individual detail page, where you can see their personal analytics and a list of all their journal entries.</p>
  <img src="https://ipa.parasyst.com/static/images/students_admin.png" alt="login" loading="lazy">
  <br/>
  <img src="https://ipa.parasyst.com/static/images/admin_journal_entry.png" alt="login" loading="lazy">
  <br/>
<p>Clicking on any journal entry allows you to read the student's final, corrected text, giving you direct insight into their writing process and progress.</p>
  <img src="https://ipa.parasyst.com/static/images/journal_entry.png" alt="login" loading="lazy">
  <br/>
`;
</script>

