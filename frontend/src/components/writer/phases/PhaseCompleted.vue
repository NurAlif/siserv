<template>
  <div class="absolute inset-0 h-full overflow-y-auto p-6 text-center">
    <div class="max-w-md mx-auto">
      <div class="bg-green-100 text-green-700 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 256 256">
          <path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"></path>
        </svg>
      </div>
      <h3 class="text-2xl font-bold mt-4 text-gray-900 dark:text-gray-100">Journal Completed!</h3>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Excellent work! You've finished this entry. All your learning points have been saved to your progress hub.
      </p>
      <div class="mt-6">
        <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg border dark:border-gray-700 text-left">
          <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Final Entry</h4>
          <div class="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">{{ content }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  content: String,
});
</script>
