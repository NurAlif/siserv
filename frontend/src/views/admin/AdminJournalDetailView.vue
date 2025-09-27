<template>
  <main id="admin-journal-detail-view" class="fade-in">
    <!-- Header -->
    <div class="mb-6">
      <router-link :to="`/admin/student/${studentId}`" class="text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-100 font-medium flex items-center gap-2 mb-4">
         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        Back to Student Details
      </router-link>
    </div>
    
    <!-- Loading and Error States -->
    <div v-if="adminStore.isLoading" class="text-center py-10">
      <p class="text-gray-500 dark:text-gray-400">Loading journal...</p>
    </div>
    <div v-else-if="adminStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
      <p>{{ adminStore.error }}</p>
    </div>

    <div v-else-if="journal" class="space-y-6">
       <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ journal.title || 'Journal Entry' }}</h2>
          <div class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(journal.journal_date) }}</div>
        </div>
        <div v-if="journal.writing_phase === 'completed'" class="mt-2 inline-block bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 text-xs font-bold px-2 py-1 rounded-full">
          Completed
        </div>
      </div>
      
      <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Outline</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap">{{ journal.outline_content || 'No outline was created.' }}</p>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Content</h3>
        <p class="text-base text-gray-800 dark:text-gray-200 whitespace-pre-wrap leading-relaxed">{{ journal.content }}</p>
      </div>

    </div>
  </main>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAdminStore } from '../../stores/adminStore';
import { format, parseISO } from 'date-fns';

const route = useRoute();
const adminStore = useAdminStore();
const studentId = route.params.studentId;
const journalDate = route.params.journalDate;

const journal = computed(() => adminStore.currentStudentJournal);

onMounted(() => {
  if (studentId && journalDate) {
    adminStore.fetchSingleStudentJournal(studentId, journalDate);
  }
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = parseISO(dateString);
  return format(date, 'MMMM d, yyyy');
};
</script>
