<template>
  <router-link
    :to="`/admin/student/${journal.user_id}/journal/${journal.journal_date}`"
    class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 hover:border-indigo-400 dark:hover:border-indigo-500 transition-colors cursor-pointer flex items-start gap-4"
    :class="{ 'border-green-400 dark:border-green-600': journal.writing_phase === 'completed' }"
  >
    <div class="flex-grow overflow-hidden">
      <div class="flex items-center gap-2">
        <h4 class="font-bold text-md text-gray-800 dark:text-gray-200 truncate">{{ journal.title || 'Journal Entry' }}</h4>
        <div v-if="journal.writing_phase === 'completed'" class="flex-shrink-0 bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 text-xs font-bold px-2 py-0.5 rounded-full">
          Completed
        </div>
      </div>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ formatDate(journal.journal_date) }}</p>
      <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{{ snippet }}</p>
    </div>
    <!-- Caret Icon -->
    <div class="self-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="text-gray-400 dark:text-gray-500" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';
import { format, parseISO } from 'date-fns';

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

const formatDate = (dateString) => {
  if (!dateString) return '';
  // parseISO handles the 'YYYY-MM-DD' format
  const date = parseISO(dateString);
  return format(date, 'MMMM d, yyyy');
};
</script>
