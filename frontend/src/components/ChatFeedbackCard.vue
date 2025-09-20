<template>
  <div class="bg-teal-50 dark:bg-teal-900/50 border-l-4 border-teal-400 dark:border-teal-600 p-3 rounded-r-lg max-w-xs break-words">
    <p class="text-xs font-bold text-teal-700 dark:text-teal-200 mb-2">Quick Correction!</p>
    <div v-if="feedbackData" class="space-y-1 text-sm">
      <p class="text-gray-800 dark:text-gray-200">
        You wrote: 
        <span class="line-through text-red-600 bg-red-100 dark:bg-red-900/50 dark:text-red-300 px-1 rounded">"{{ feedbackData.incorrect_phrase }}"</span>
      </p>
      <p class="text-gray-800 dark:text-gray-200">
        A better way is: 
        <span class="font-semibold text-green-700 bg-green-100 dark:bg-green-900/50 dark:text-green-300 px-1 rounded">"{{ feedbackData.suggestion }}"</span>
      </p>
      <p class="text-xs text-gray-600 dark:text-gray-400 mt-2 pt-2 border-t border-teal-200 dark:border-teal-800">
        {{ feedbackData.explanation }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
});

const feedbackData = ref(null);

onMounted(() => {
  try {
    // The message_text for feedback messages is a JSON string
    feedbackData.value = JSON.parse(props.message.message_text);
  } catch (e) {
    console.error("Failed to parse chat feedback JSON:", e);
    feedbackData.value = null;
  }
});
</script>
