<template>
  <div class="p-4 rounded-lg flex justify-between items-start gap-4" :class="[cardColorClasses.bg, { 'opacity-60': isApplied }]">
    <div class="flex-grow">
      <p class="font-semibold" :class="cardColorClasses.text">
        {{ feedbackItem.error_type }}
      </p>
      <p class="text-sm mt-2">
        Incorrect phrase: 
        <span class="line-through text-red-600 bg-red-100 dark:bg-red-900/50 dark:text-red-300 px-1 rounded">"{{ feedbackItem.incorrect_phrase }}"</span>
      </p>
      <p class="text-sm mt-1">
        Suggestion: 
        <span class="font-semibold text-green-700 bg-green-100 dark:bg-green-900/50 dark:text-green-300 px-1 rounded">"{{ feedbackItem.suggestion }}"</span>
      </p>
      <p class="text-xs text-gray-700 dark:text-gray-300 mt-2 bg-gray-100 dark:bg-gray-700/50 p-2 rounded">
        <strong>Explanation:</strong> {{ feedbackItem.explanation }}
      </p>
    </div>
    <div class="flex-shrink-0">
        <button 
          @click="$emit('apply-suggestion', feedbackItem)" 
          :disabled="isApplied"
          class="bg-white dark:bg-gray-600 text-sm font-semibold px-3 py-1 rounded-md border border-gray-300 dark:border-gray-500 text-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-500 disabled:bg-gray-100 disabled:cursor-not-allowed disabled:text-gray-400 dark:disabled:bg-gray-800 dark:disabled:text-gray-500 transition-colors flex items-center gap-1.5"
        >
          <svg v-if="!isApplied" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"></path></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm45.66-125.66a8,8,0,0,1,0,11.32L133.31,144l-22.34,22.34a8,8,0,0,1-11.32-11.32L122,132.69,99.66,110.34a8,8,0,0,1,11.32-11.32L132,121.31l22.34-22.34A8,8,0,0,1,173.66,90.34Z"></path></svg>
          {{ isApplied ? 'Applied' : 'Apply' }}
        </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  feedbackItem: {
    type: Object,
    required: true,
  },
  isApplied: {
    type: Boolean,
    default: false
  }
});

defineEmits(['apply-suggestion']);

// Dynamically change card colors for better visual grouping of feedback
const cardColorClasses = computed(() => {
  const type = props.feedbackItem.error_type.toLowerCase();
  if (type.includes('grammar')) {
    return { bg: 'bg-blue-50 dark:bg-blue-900/50', text: 'text-blue-800 dark:text-blue-200' };
  }
  if (type.includes('vocabulary') || type.includes('phrasing')) {
    return { bg: 'bg-purple-50 dark:bg-purple-900/50', text: 'text-purple-800 dark:text-purple-200' };
  }
  if (type.includes('cohesion') || type.includes('style')) {
      return { bg: 'bg-yellow-50 dark:bg-yellow-900/50', text: 'text-yellow-800 dark:text-yellow-200'};
  }
  return { bg: 'bg-gray-100 dark:bg-gray-700', text: 'text-gray-800 dark:text-gray-200' }; // Default color
});
</script>
