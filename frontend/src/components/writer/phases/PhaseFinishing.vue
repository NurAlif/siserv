<template>
  <div class="absolute inset-0 h-full overflow-y-auto p-6">
    <div class="bg-rose-50 dark:bg-rose-900/50 p-4 rounded-lg mb-4">
      <h3 class="font-bold text-rose-800 dark:text-rose-200">Phase 3: Polish your writing</h3>
      <p class="text-sm text-rose-700 dark:text-rose-300 mt-1">
        Review the AI's suggestions below to improve your grammar, vocabulary, and style. Your original text is highlighted with suggestions.
      </p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="md:col-span-2">
        <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Corrected Text</h4>
        <div 
          v-html="highlightedContent" 
          class="w-full h-96 p-4 border border-gray-300 dark:border-gray-600 rounded-lg overflow-y-auto bg-gray-50 dark:bg-gray-700/50 whitespace-pre-wrap">
        </div>
      </div>
      <div class="md:col-span-1">
        <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Suggestions</h4>
        <div id="ai-feedback-section" class="space-y-3">
          <div v-if="aiStore.isLoading" class="text-center py-4">
            <p class="text-gray-500 dark:text-gray-400 animate-pulse">Analyzing your text...</p>
          </div>
          <div v-else-if="aiStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
            <p>{{ aiStore.error }}</p>
          </div>
          <div v-else-if="aiStore.feedback.length > 0">
            <AIFeedbackCard 
              v-for="(item, index) in aiStore.feedback"
              :key="index"
              :feedback-item="item"
              :is-applied="appliedSuggestions.includes(item.incorrect_phrase)"
              @apply-suggestion="$emit('apply-suggestion', item)"
            />
          </div>
          <div v-else class="text-center py-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <p class="text-gray-600 dark:text-gray-300 font-semibold">Great job!</p>
            <p class="text-gray-500 dark:text-gray-400">The AI didn't find any specific errors to correct.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// This component re-uses the AIFeedbackCard you already have.
import AIFeedbackCard from '../../AIFeedbackCard.vue';

defineProps({
  highlightedContent: String,
  aiStore: Object, // Pass the whole store object for simplicity
  appliedSuggestions: Array,
});

defineEmits(['apply-suggestion']);
</script>
