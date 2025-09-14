<template>
  <main id="dashboard-view" class="fade-in">
    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 class="text-xl font-bold">Welcome Back, {{ authStore.user?.username }}!</h2>
          <p class="text-gray-500">Ready to practice your English today?</p>
        </div>
        <div class="flex items-center gap-3 bg-orange-100 text-orange-700 p-3 rounded-lg">
          <!-- Fire Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 256 256">
            <path d="M221.5,145.45C221.5,184.12,190,224,150,224s-72-39.88-72-78.55c0-20.93,12.35-46,29.9-71.55,14.28-20.81,28.2-38,33.43-45.11a8,8,0,0,1,13.34,0c5.23,7.07,19.15,24.3,33.43,45.11C209.15,99.44,221.5,124.52,221.5,145.45ZM152,80a16,16,0,1,0-16,16A16,16,0,0,0,152,80Z"></path>
          </svg>
          <div>
            <div class="font-bold text-lg">{{ progressStore.streak }} Day Streak</div>
            <p class="text-sm">Keep it up!</p>
          </div>
        </div>
      </div>
    </div>

    <!-- New Progress Summary Card -->
    <ProgressSummaryCard 
      :summary="progressStore.summary"
      :is-loading="progressStore.isLoading"
      :error="progressStore.error"
    />

    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold">Your Journal Entries</h3>
      <router-link
        to="/writer"
        class="bg-indigo-600 text-white font-semibold px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
      >
        <!-- Plus Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path></svg>
        New Entry
      </router-link>
    </div>

    <!-- Loading and Error States -->
    <div v-if="journalStore.isLoading" class="text-center py-10">
      <p class="text-gray-500">Loading your journals...</p>
    </div>
    <div v-else-if="journalStore.error" class="bg-red-50 text-red-700 p-4 rounded-lg">
      <p>{{ journalStore.error }}</p>
    </div>

    <!-- Journal List -->
    <div v-else-if="journalStore.journals.length > 0" id="journal-list" class="space-y-4">
       <JournalCard
         v-for="journal in journalStore.journals"
         :key="journal.id"
         :journal="journal"
       />
    </div>
    <div v-else class="text-center py-10 bg-white rounded-xl border border-gray-200">
        <h4 class="font-semibold text-lg">No entries yet!</h4>
        <p class="text-gray-500">Click "New Entry" to start your first journal.</p>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useJournalStore } from '../stores/journalStore';
import { useProgressStore } from '../stores/progressStore'; // Import progress store
import JournalCard from '../components/JournalCard.vue';
import ProgressSummaryCard from '../components/ProgressSummaryCard.vue'; // Import new component

const authStore = useAuthStore();
const journalStore = useJournalStore();
const progressStore = useProgressStore(); // Instantiate progress store

// Fetch data when the component is first mounted
onMounted(() => {
  journalStore.fetchJournals();
  progressStore.fetchProgressSummary();
  progressStore.fetchStreak(); // Fetch streak data
});
</script>
