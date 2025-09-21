<template>
  <div v-if="feedbackData" class="border-l-4 p-3 rounded-r-lg max-w-xs break-words" :class="cardClasses">
    
    <!-- Case 1: A correction was found -->
    <div v-if="feedbackData.status !== 'no_errors'">
      <p class="text-xs font-bold mb-2" :class="textColor">Quick Correction!</p>
      <div class="space-y-1 text-sm">
        <p class="text-gray-800 dark:text-gray-200">
          You wrote: 
          <span class="line-through text-red-600 bg-red-100 dark:bg-red-900/50 dark:text-red-300 px-1 rounded">"{{ feedbackData.incorrect_phrase }}"</span>
        </p>
        <p class="text-gray-800 dark:text-gray-200">
          A better way is: 
          <span class="font-semibold text-green-700 bg-green-100 dark:bg-green-900/50 dark:text-green-300 px-1 rounded">"{{ feedbackData.suggestion }}"</span>
        </p>
        <p class="text-xs text-gray-700 dark:text-gray-300 mt-3 bg-white dark:bg-gray-700/50 p-2 rounded">
          <strong>Why:</strong> {{ feedbackData.explanation }}
        </p>
      </div>
    </div>

    <!-- Case 2: No errors were found -->
    <div v-else class="flex items-center gap-2">
       <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="flex-shrink-0" :class="textColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm45.66-125.66a8,8,0,0,1,0,11.32L133.31,144l-22.34,22.34a8,8,0,0,1-11.32-11.32L122,132.69,99.66,110.34a8,8,0,0,1,11.32-11.32L132,121.31l22.34-22.34A8,8,0,0,1,173.66,90.34Z"></path></svg>
      <p class="text-sm font-semibold" :class="textColor">Looking good! No corrections found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
});

const feedbackData = ref(null);

onMounted(() => {
  try {
    feedbackData.value = JSON.parse(props.message.message_text);
  } catch (e) {
    console.error("Failed to parse chat feedback JSON:", e);
    feedbackData.value = null;
  }
});

// Computed properties for dynamic styling based on feedback type
const cardClasses = computed(() => {
  if (feedbackData.value?.status === 'no_errors') {
    return 'bg-green-50 dark:bg-green-900/50 border-green-400 dark:border-green-600';
  }
  return 'bg-teal-50 dark:bg-teal-900/50 border-teal-400 dark:border-teal-600';
});

const textColor = computed(() => {
  if (feedbackData.value?.status === 'no_errors') {
    return 'text-green-700 dark:text-green-200';
  }
  return 'text-teal-700 dark:text-teal-200';
});

</script>

