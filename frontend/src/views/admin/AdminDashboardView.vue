<template>
  <main id="admin-dashboard-view" class="fade-in">
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
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-lightbulb-icon lucide-lightbulb text-gray-700 dark:text-gray-200"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>
            Admin Manual
          </button>
          <router-link
            to="/admin/manage-notifications"
            class="bg-indigo-600 text-white font-semibold px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bell-icon lucide-bell text-gray-100"><path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/></svg>
            Manage Notifications
          </router-link>
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

    <div v-else class="space-y-8">
       <!-- Class-wide Analytics -->
      <div v-if="adminStore.classAnalytics">
        <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">Class-wide Analytics</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <AdminStatCard title="Total Students" :value="adminStore.classAnalytics.total_students" />
          <AdminStatCard title="Total Journal Entries" :value="adminStore.classAnalytics.total_journals" />
          <AdminStatCard title="Total Errors Logged" :value="adminStore.classAnalytics.total_errors" />
          <AdminStatCard title="Avg Errors per Journal" :value="adminStore.classAnalytics.avg_errors_per_journal.toFixed(2)" />
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ErrorDistributionChart title="Class Error Distribution" :chart-raw-data="adminStore.classAnalytics.error_distribution" />
          <ErrorTrendChart title="Class Error Trend" :chart-raw-data="adminStore.classAnalytics.error_trend" />
        </div>
      </div>

      <!-- Daily Activity Section -->
      <div>
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4">
          <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200">
            Activity for {{ formattedSelectedDate }}
          </h3>
          <div class="flex items-center gap-2 mt-2 sm:mt-0">
            <button @click="changeDate(-1)" class="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M165.66,202.34a8,8,0,0,1-11.32,0L80,128l74.34-53.66a8,8,0,0,1,11.32,11.32L97.31,128l68.35,68.34A8,8,0,0,1,165.66,202.34Z"></path></svg>
            </button>
            <input 
                type="date" 
                v-model="selectedDate"
                class="bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
            <button @click="changeDate(1)" class="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed" :disabled="isToday">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M90.34,53.66a8,8,0,0,0-11.32,0l-80,80a8,8,0,0,0,0,11.32l80,80a8,8,0,0,0,11.32-11.32L17.31,128,90.34,53.66Z" transform="rotate(180 128 128)"></path></svg>
            </button>
          </div>
        </div>
        <div v-if="adminStore.isLoadingDailySummary" class="text-center py-10">
          <p class="text-gray-500 dark:text-gray-400">Loading summary for {{ formattedSelectedDate }}...</p>
        </div>
        <div v-else-if="adminStore.dailySummary.length > 0" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-1">
            <PhaseDistributionChart :journals="adminStore.dailySummary" />
          </div>
          <div class="lg:col-span-2">
            <DailyJournalTable :journals="adminStore.dailySummary" />
          </div>
        </div>
        <div v-else class="text-center py-10 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <h4 class="font-semibold text-lg text-gray-800 dark:text-gray-200">No Journals Submitted on this Day</h4>
          <p class="text-gray-500 dark:text-gray-400">Please select another date to view submissions.</p>
        </div>
      </div>

      <!-- Student Table -->
      <div>
        <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">All Students</h3>
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
import { ref, onMounted, computed, watch } from 'vue';
import { useAdminStore } from '../../stores/adminStore';
import AdminStatCard from '../../components/admin/AdminStatCard.vue';
import ErrorDistributionChart from '../../components/admin/ErrorDistributionChart.vue';
import ErrorTrendChart from '../../components/admin/ErrorTrendChart.vue';
import StudentTable from '../../components/admin/StudentTable.vue';
import ManualModal from '../../components/ManualModal.vue';
import PhaseDistributionChart from '../../components/admin/PhaseDistributionChart.vue';
import DailyJournalTable from '../../components/admin/DailyJournalTable.vue';

const adminStore = useAdminStore();
const showManualModal = ref(false);
const selectedDate = ref(new Date().toISOString().split('T')[0]); // YYYY-MM-DD format

onMounted(() => {
  adminStore.fetchClassAnalytics();
  adminStore.fetchAllStudents();
  adminStore.fetchDailySummary(selectedDate.value);
});

watch(selectedDate, (newDate) => {
  if (newDate) {
    adminStore.fetchDailySummary(newDate);
  }
});

const formattedSelectedDate = computed(() => {
  if (!selectedDate.value) return 'Select a Date';
  const [year, month, day] = selectedDate.value.split('-').map(Number);
  // Use UTC to prevent timezone off-by-one errors
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
});

const isToday = computed(() => {
    const today = new Date();
    // Get today's date in UTC
    const todayUTC = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()));
    
    // Get selected date in UTC
    const [year, month, day] = selectedDate.value.split('-').map(Number);
    const selectedUTC = new Date(Date.UTC(year, month - 1, day));
    
    return selectedUTC >= todayUTC;
});


const changeDate = (days) => {
    // Parse selected date string into UTC date object
    const [year, month, day] = selectedDate.value.split('-').map(Number);
    const currentDate = new Date(Date.UTC(year, month - 1, day));

    // Modify the UTC date
    currentDate.setUTCDate(currentDate.getUTCDate() + days);

    // Format back to YYYY-MM-DD string
    selectedDate.value = currentDate.toISOString().split('T')[0];
};

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
