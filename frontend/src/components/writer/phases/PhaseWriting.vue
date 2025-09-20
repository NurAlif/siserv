<template>
  <div class="h-full flex flex-col p-6 gap-4">
    <!-- Banner -->
    <div class="flex-shrink-0 bg-green-50 dark:bg-green-900/50 p-4 rounded-lg">
      <h3 class="font-bold text-green-800 dark:text-green-200">Phase 2: Write your draft</h3>
      <p class="text-sm text-green-700 dark:text-green-300 mt-1">
        Use your outline to write your journal entry. Your writing partner, Lingo, is here to help if you get stuck.
      </p>
    </div>

    <!-- Mobile View Switcher -->
    <div class="md:hidden flex-shrink-0 flex border border-gray-300 dark:border-gray-600 rounded-lg p-1 bg-gray-100 dark:bg-gray-900">
      <button 
        @click="mobileView = 'writer'" 
        :class="['flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out', mobileView === 'writer' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 dark:text-gray-300']">
        📝 Writer
      </button>
      <button 
        @click="mobileView = 'partner'" 
        :class="['flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out', mobileView === 'partner' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 dark:text-gray-300']">
        🤖 Partner
      </button>
    </div>

    <!-- Main Grid for Desktop -->
    <div class="flex-grow overflow-hidden grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Left Column: Outline + Writer -->
      <div class="flex flex-col gap-4 min-h-0" :class="{ 'hidden md:flex': mobileView !== 'writer' }">
        <!-- Outline Section -->
        <div class="flex-shrink-0 bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border dark:border-gray-700">
          <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Outline</h4>
          <div class="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap max-h-24 overflow-y-auto">
            {{ outlineContent || "No outline was created." }}
          </div>
        </div>
        <!-- Writing Area -->
        <textarea
          :value="content"
          @input="$emit('update:content', $event.target.value)"
          class="flex-grow w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
        ></textarea>
      </div>

      <!-- Right Column: Partner Sidebar -->
      <div class="flex flex-col min-h-0" :class="{ 'hidden md:flex': mobileView !== 'partner' }">
        <!-- Chat Slot -->
        <slot name="chat"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  content: String,
  outlineContent: String,
});

defineEmits(['update:content']);

// New state for mobile tab view, local to this component
const mobileView = ref('writer'); // 'writer' or 'partner'
</script>
