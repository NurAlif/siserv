<template>
  <button @click="$emit('open-notifications')" title="View Notifications" class="relative p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
    <!-- Bell Icon -->
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="text-gray-600 dark:text-gray-300" viewBox="0 0 256 256">
      <path d="M224,176v-0.12a88.1,88.1,0,0,0-72-87.81V72a40,40,0,0,0-80,0v16.07A88.1,88.1,0,0,0,0,175.88V176a16,16,0,0,0,16,16H59.21a48,48,0,0,0,93.58,0H192a16,16,0,0,0,16-16ZM40,176a72.08,72.08,0,0,1,72-72h0.12a72.08,72.08,0,0,1,71.87,72Z"></path>
    </svg>
    <!-- Notification Dot -->
    <span v-if="notificationCount > 0" class="absolute top-1.5 right-1.5 flex h-3 w-3">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
    </span>
  </button>
</template>

<script setup>
defineProps({
  notificationCount: {
    type: Number,
    default: 0,
  },
});

defineEmits(['open-notifications']);
</script>
