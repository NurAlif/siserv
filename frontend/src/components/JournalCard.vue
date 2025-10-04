<template>
  <router-link
    :to="`/writer/${journal.journal_date}`"
    class="bg-white dark:bg-gray-800 p-3 sm:p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 hover:border-indigo-400 dark:hover:border-indigo-500 transition-colors cursor-pointer flex items-start gap-3 sm:gap-4"
    :class="{ 'border-green-400 dark:border-green-600': journal.writing_phase === 'completed' }"
  >
    <!-- Image Thumbnail -->
    <div v-if="thumbnailUrl" class="w-20 h-20 sm:w-24 sm:h-24 bg-gray-100 dark:bg-gray-700 rounded-md flex items-center justify-center flex-shrink-0 overflow-hidden">
      <img :src="thumbnailUrl" alt="Journal thumbnail" class="w-full h-full object-cover">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="text-gray-400 dark:text-gray-500" viewBox="0 0 256 256"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM48,48H208V157.38l-19.52-19.52a16,16,0,0,0-22.62,0L144,160,99.51,115.51a16,16,0,0,0-22.62,0L48,144.38ZM208,208H48V172.69l36.49-36.5,44.49,44.49a16,16,0,0,0,22.62,0L176,159.31l32,32V208Zm-40-88a12,12,0,1,1,12-12A12,12,0,0,1,168,120Z"></path></svg>
    </div>
    <div class="flex-grow overflow-hidden pt-1">
      <div class="flex items-center gap-2">
        <h4 class="font-bold text-md text-gray-800 dark:text-gray-200 truncate">{{ journal.title || 'Journal Entry' }}</h4>
        <div v-if="journal.is_late" class="flex-shrink-0 bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 text-xs font-bold px-2 py-0.5 rounded-full">
          Late
        </div>
        <div v-if="journal.writing_phase === 'completed'" class="flex-shrink-0 bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 text-xs font-bold px-2 py-0.5 rounded-full">
          Completed
        </div>
      </div>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ journalStore.formatDisplayDate(journal.journal_date) }}</p>
      <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed overflow-hidden" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">{{ snippet }}</p>
    </div>
    <!-- Caret Icon -->
    <div class="self-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="text-gray-400 dark:text-gray-500" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';
import { useJournalStore } from '../stores/journalStore';
import apiClient from '../services/api';

const journalStore = useJournalStore();

const props = defineProps({
  journal: {
    type: Object,
    required: true,
  },
});

const thumbnailUrl = computed(() => {
  if (props.journal.images && props.journal.images.length > 0) {
    // Get the last uploaded image to use as the thumbnail
    const lastImage = props.journal.images[props.journal.images.length - 1];
    const path = lastImage.file_path;
    if (!path) return null;
    const baseUrl = (apiClient.defaults.baseURL || '').replace('/api', '');
    return `${baseUrl}${path}`;
  }
  return null;
});


// Create a snippet from the full content
const snippet = computed(() => {
  if (!props.journal.content) {
    return 'No content yet...';
  }
  // Truncate the content to 120 characters
  if (props.journal.content.length > 120) {
    return props.journal.content.substring(0, 120) + '...';
  }
  return props.journal.content;
});
</script>
