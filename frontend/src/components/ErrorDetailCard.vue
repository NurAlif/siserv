<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
    <div class="flex justify-between items-start">
        <div>
            <p class="text-sm">
                Your phrase: 
                <span class="line-through text-red-600 bg-red-100 px-1 rounded">"{{ error.incorrect_phrase }}"</span>
            </p>
            <p class="text-sm mt-1">
                Suggestion: 
                <span class="font-semibold text-green-700 bg-green-100 px-1 rounded">"{{ error.suggestion_text }}"</span>
            </p>
        </div>
        <div class="text-xs text-gray-500 bg-white px-2 py-1 rounded-md border">
            Repeated: <span class="font-bold">{{ error.repetition_count }}</span> time{{ error.repetition_count > 1 ? 's' : ''}}
        </div>
    </div>
    <p class="text-xs text-gray-700 mt-3 bg-white p-2 rounded border">
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