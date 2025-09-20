<template>
  <div class="absolute inset-0 h-full overflow-y-auto">
    <div class="p-6">
      <div class="bg-indigo-50 dark:bg-indigo-900/50 p-4 rounded-lg mb-4">
        <h3 class="font-bold text-indigo-800 dark:text-indigo-200">Phase 1: Let's build an outline!</h3>
        <p class="text-sm text-indigo-700 dark:text-indigo-300 mt-1">Answer the questions, chat with the AI, or write your own key points below. The goal is to create a simple plan for your journal entry.</p>
      </div>
      <div class="mb-4 space-y-2 text-sm text-gray-600 dark:text-gray-300">
          <p><strong>Guiding questions:</strong></p>
          <ul class="list-disc list-inside bg-gray-50 dark:bg-gray-700/50 p-3 rounded-md">
              <li>What was the most memorable part of your day?</li>
              <li>Did you learn or try something new?</li>
              <li>How are you feeling right now?</li>
          </ul>
      </div>
      <textarea 
        :value="outlineContent"
        @input="$emit('update:outlineContent', $event.target.value)"
        placeholder="Write down your main ideas or key points here..." 
        class="w-full h-48 p-4 border rounded-lg ...">
      </textarea>
    </div>
    
    <div v-show="isChatActive" class="p-6 border-t border-gray-200 dark:border-gray-700">
        <slot name="chat"></slot> </div>
  </div>
</template>

<script setup>
defineProps({
  outlineContent: String,
  isChatActive: Boolean,
});
defineEmits(['update:outlineContent']);
</script>