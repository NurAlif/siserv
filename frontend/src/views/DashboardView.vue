<template>
  <main id="dashboard-view" class="fade-in">
    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Welcome Back, {{ authStore.user?.username }}!</h2>
          <p class="text-gray-500 dark:text-gray-400">Ready to practice your English today?</p>
        </div>
        <div class="flex items-center gap-3 bg-orange-100 dark:bg-orange-900/50 text-orange-700 dark:text-orange-300 p-3 rounded-lg">
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

    <!-- View Controls -->
    <div class="flex flex-col sm:flex-row justify-between items-center mb-4 gap-4">
      <div class="flex items-center gap-1 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
        <button 
          @click="viewMode = 'list'" 
          :class="viewMode === 'list' ? 'bg-white dark:bg-gray-800 shadow text-indigo-600' : 'text-gray-500 dark:text-gray-400'" 
          class="px-3 py-1 text-sm font-semibold rounded-md transition-all flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M224,88H32a8,8,0,0,0-8,8v64a8,8,0,0,0,8,8H224a8,8,0,0,0,8-8V96A8,8,0,0,0,224,88Zm-8,64H40V104H216v48ZM32,48H224a8,8,0,0,0,0-16H32a8,8,0,0,0,0,16Zm0,160H224a8,8,0,0,0,0-16H32a8,8,0,0,0,0,16Z"></path></svg>
          List
        </button>
        <button 
          @click="viewMode = 'calendar'" 
          :class="viewMode === 'calendar' ? 'bg-white dark:bg-gray-800 shadow text-indigo-600' : 'text-gray-500 dark:text-gray-400'" 
          class="px-3 py-1 text-sm font-semibold rounded-md transition-all flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32Zm0,16V80H48V48ZM48,208V96H208V208Z"></path></svg>
          Calendar
        </button>
      </div>
      <router-link
        to="/writer"
        class="bg-indigo-600 text-white font-semibold px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path></svg>
        New Entry for Today
      </router-link>
    </div>

    <!-- Loading and Error States -->
    <div v-if="journalStore.isLoading" class="text-center py-10">
      <p class="text-gray-500 dark:text-gray-400">Loading your journals...</p>
    </div>
    <div v-else-if="journalStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
      <p>{{ journalStore.error }}</p>
    </div>

    <!-- Conditional Views -->
    <template v-else>
      <!-- List View -->
      <div v-if="viewMode === 'list'">
        <div v-if="journalStore.journals.length > 0" id="journal-list" class="space-y-4">
          <JournalCard
            v-for="journal in journalStore.journals"
            :key="journal.id"
            :journal="journal"
          />
        </div>
        <div v-else class="text-center py-10 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <h4 class="font-semibold text-lg text-gray-800 dark:text-gray-200">No entries yet!</h4>
            <p class="text-gray-500 dark:text-gray-400">Click "New Entry for Today" to start your first journal.</p>
        </div>
      </div>
      <!-- Calendar View -->
      <JournalCalendarView v-else-if="viewMode === 'calendar'" :journals="journalStore.journals" />
    </template>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useJournalStore } from '../stores/journalStore';
import { useProgressStore } from '../stores/progressStore';
import JournalCard from '../components/JournalCard.vue';
import JournalCalendarView from '../components/JournalCalendarView.vue';

const authStore = useAuthStore();
const journalStore = useJournalStore();
const progressStore = useProgressStore();

const viewMode = ref('list'); // 'list' or 'calendar'

onMounted(() => {
  journalStore.fetchJournals();
  progressStore.fetchStreak();
});
</script>
