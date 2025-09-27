<template>
  <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
    <div class="flex justify-between items-start">
        <div>
            <p class="text-sm text-gray-800 dark:text-gray-200">
                Your phrase: 
                <span class="line-through text-red-600 bg-red-100 dark:bg-red-900/50 dark:text-red-300 px-1 rounded">"{{ error.incorrect_phrase }}"</span>
            </p>
            <p class="text-sm mt-1 text-gray-800 dark:text-gray-200">
                Suggestion: 
                <span class="font-semibold text-green-700 bg-green-100 dark:bg-green-900/50 dark:text-green-300 px-1 rounded">"{{ error.suggestion_text }}"</span>
            </p>
        </div>
        <div class="text-xs text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-700 px-2 py-1 rounded-md border dark:border-gray-600">
            Repeated: <span class="font-bold">{{ error.repetition_count }}</span> time{{ error.repetition_count > 1 ? 's' : ''}}
        </div>
    </div>
    <p class="text-xs text-gray-700 dark:text-gray-300 mt-3 bg-white dark:bg-gray-700 p-2 rounded border dark:border-gray-600">
      <strong>Explanation:</strong> {{ error.explanation_text }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  error: {
    type: Object,
    required: true,
  },
});
</script>
