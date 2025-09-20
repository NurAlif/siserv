<template>
  <router-link
    :to="`/learning-hub/topic/${topic.topic_id}`"
    class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 hover:border-indigo-400 dark:hover:border-indigo-500 transition-colors cursor-pointer flex justify-between items-center"
  >
    <div>
      <h4 class="font-bold text-md text-gray-800 dark:text-gray-200">{{ topic.topic_name }}</h4>
      <p class="text-sm text-gray-500 dark:text-gray-400">{{ topic.error_count }} unique error{{ topic.error_count > 1 ? 's' : '' }} logged</p>
    </div>
    <!-- Caret Icon -->
    <div class="self-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="text-gray-400 dark:text-gray-500" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  topic: {
    type: Object,
    required: true,
  },
});
</script>
