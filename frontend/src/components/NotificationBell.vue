<template>
  <button @click="$emit('open-notifications')" title="View Notifications" class="relative p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
    <!-- Bell Icon -->
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bell-icon lucide-bell text-gray-600 dark:text-gray-300"><path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>
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
