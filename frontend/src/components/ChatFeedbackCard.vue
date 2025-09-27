<template>
  <div v-if="feedbackData && feedbackData.status !== 'no_errors'" class="border-l-4 p-3 rounded-r-lg max-w-xs break-words" :class="cardClasses">
    
    <p class="text-xs font-bold mb-2" :class="textColor">Quick Correction!</p>
    <div class="space-y-1 text-sm">
      <p class="text-gray-800 dark:text-gray-200">
        You wrote: 
        <span class="line-through text-red-600 bg-red-100 dark:bg-red-900/50 dark:text-red-300 px-1 rounded">"{{ feedbackData.incorrect_phrase }}"</span>
      </p>
      <p class="text-gray-800 dark:text-gray-200">
        The correct way is: 
        <span class="font-semibold text-green-700 bg-green-100 dark:bg-green-900/50 dark:text-green-300 px-1 rounded">"{{ feedbackData.suggestion }}"</span>
      </p>
      <p class="text-xs text-gray-700 dark:text-gray-300 mt-3 bg-white dark:bg-gray-700/50 p-2 rounded">
        <strong>Why:</strong> {{ feedbackData.explanation }}
      </p>
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

// Since the component no longer renders for 'no_errors', we can simplify the computed properties.
const cardClasses = computed(() => {
  return 'bg-teal-50 dark:bg-teal-900/50 border-teal-400 dark:border-teal-600';
});

const textColor = computed(() => {
  return 'text-teal-700 dark:text-teal-200';
});

</script>