<template>
  <router-link
    :to="`/writer/${journal.journal_date}`"
    class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 hover:border-indigo-400 transition-colors cursor-pointer flex items-start gap-4"
  >
    <!-- Image Placeholder -->
    <div class="w-24 h-[70px] bg-gray-100 rounded-md flex items-center justify-center flex-shrink-0">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="text-gray-400" viewBox="0 0 256 256"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM48,48H208V157.38l-19.52-19.52a16,16,0,0,0-22.62,0L144,160,99.51,115.51a16,16,0,0,0-22.62,0L48,144.38ZM208,208H48V172.69l36.49-36.5,44.49,44.49a16,16,0,0,0,22.62,0L176,159.31l32,32V208Zm-40-88a12,12,0,1,1,12-12A12,12,0,0,1,168,120Z"></path></svg>
    </div>
    <div class="flex-grow overflow-hidden">
      <h4 class="font-bold text-md truncate">{{ journal.title || 'Journal Entry' }}</h4>
      <p class="text-sm text-gray-500 mb-2">{{ journalStore.formatDisplayDate(journal.journal_date) }}</p>
      <p class="text-sm text-gray-600 leading-relaxed">{{ snippet }}</p>
    </div>
    <!-- Caret Icon -->
    <div class="self-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="text-gray-400" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';
import { useJournalStore } from '../stores/journalStore';

const journalStore = useJournalStore();

const props = defineProps({
  journal: {
    type: Object,
    required: true,
  },
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

