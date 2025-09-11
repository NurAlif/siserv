<template>
  <div class="p-4 rounded-lg" :class="cardColorClasses.bg">
    <p class="font-semibold" :class="cardColorClasses.text">
      {{ feedbackItem.error_type }}
    </p>
    <p class="text-sm mt-2">
      Incorrect phrase: 
      <span class="line-through text-red-600 bg-red-100 px-1 rounded">"{{ feedbackItem.incorrect_phrase }}"</span>
    </p>
    <p class="text-sm mt-1">
      Suggestion: 
      <span class="font-semibold text-green-700 bg-green-100 px-1 rounded">"{{ feedbackItem.suggestion }}"</span>
    </p>
    <p class="text-xs text-gray-700 mt-2 bg-gray-100 p-2 rounded">
      <strong>Explanation:</strong> {{ feedbackItem.explanation }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  feedbackItem: {
    type: Object,
    required: true,
  },
});

// Dynamically change card colors for better visual grouping of feedback
const cardColorClasses = computed(() => {
  const type = props.feedbackItem.error_type.toLowerCase();
  if (type.includes('grammar')) {
    return { bg: 'bg-blue-50', text: 'text-blue-800' };
  }
  if (type.includes('vocabulary') || type.includes('phrasing')) {
    return { bg: 'bg-purple-50', text: 'text-purple-800' };
  }
  if (type.includes('cohesion') || type.includes('style')) {
      return { bg: 'bg-yellow-50', text: 'text-yellow-800'};
  }
  return { bg: 'bg-gray-100', text: 'text-gray-800' }; // Default color
});
</script>
