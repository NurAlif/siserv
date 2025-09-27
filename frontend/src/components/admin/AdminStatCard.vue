<template>
  <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
    <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ title }}</h4>
    <p class="text-3xl font-bold text-gray-900 dark:text-gray-100 mt-1">{{ value }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
});
</script>
