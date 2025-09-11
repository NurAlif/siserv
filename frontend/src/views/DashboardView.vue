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
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 256 256"><path d="M229.66,117.66l-48-48A8,8,0,0,0,176,64a8.07,8.07,0,0,0-5.66,2.34L128,108.69,85.66,66.34A8,8,0,0,0,72,64a8.07,8.07,0,0,0-5.66,2.34l-48,48A8,8,0,0,0,16,128a8.07,8.07,0,0,0,2.34,5.66L92.69,208,49.82,250.82A8,8,0,0,0,56,256a8.12,8.12,0,0,0,5.17-1.82L128,187.33l66.83,66.83A8,8,0,0,0,200,256a8,8,0,0,0,6.18-2.82L250.34,133.66A8,8,0,0,0,248,128,8.07,8.07,0,0,0,229.66,117.66ZM128,169.31,46.34,87.66l40-40L128,89.31Zm81.66-81.65L168,129.31,126.34,87.66l40-40Z"></path></svg>
          <div>
            <div class="font-bold text-lg">12 Day Streak</div>
            <p class="text-sm">Keep it up!</p>
          </div>
        </div>
      </div>
    </div>

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
import JournalCard from '../components/JournalCard.vue';

const authStore = useAuthStore();
const journalStore = useJournalStore();

// Fetch journals when the component is first mounted
onMounted(() => {
  journalStore.fetchJournals();
});
</script>

