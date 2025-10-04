<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex justify-center items-center p-4 transition-opacity duration-300" @click.self="close">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg w-full max-w-2xl max-h-[90vh] flex flex-col transform transition-transform duration-300 scale-95" :class="{ 'scale-100': show }">
      <!-- Modal Header -->
      <header class="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center flex-shrink-0">
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">All Notifications</h2>
        <button @click="close" title="Close" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="text-gray-600 dark:text-gray-300" fill="currentColor" viewBox="0 0 256 256"><path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"></path></svg>
        </button>
      </header>
      
      <!-- Modal Content -->
      <main class="flex-grow overflow-y-auto p-4 custom-scrollbar">
        <div v-if="notificationStore.isLoadingHistory" class="text-center py-10 text-gray-500 dark:text-gray-400">
          Loading history...
        </div>
        <div v-else-if="notificationStore.notificationHistory.length === 0" class="text-center py-10 text-gray-500 dark:text-gray-400">
            No notifications found.
        </div>
        <ul v-else class="space-y-2">
          <li v-for="item in notificationStore.notificationHistory" :key="item.notification.id">
            <div 
              @click="handleClick(item)" 
              class="block p-3 rounded-lg transition-colors"
              :class="getItemClasses(item)"
            >
              <div class="flex justify-between items-start">
                <div>
                    <p class="font-semibold text-gray-800 dark:text-gray-200">{{ item.notification.title }}</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{{ item.notification.content.substring(0, 100) }}...</p>
                </div>
                <div class="flex-shrink-0 ml-4 flex items-center gap-2">
                   <span class="px-2 py-0.5 text-xs font-semibold rounded-full" :class="getStatusClass(item)">
                        {{ getStatusText(item) }}
                    </span>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </main>
    </div>
  </div>
</template>

<script setup>
import { useNotificationStore } from '../stores/notificationStore';

const props = defineProps({
  show: Boolean,
});

const emit = defineEmits(['close', 'view-notification']);

const notificationStore = useNotificationStore();

const close = () => {
  emit('close');
};

const canViewNotification = (item) => {
    // Only announcements are re-viewable from the list.
    return item.notification.notification_type === 'announcement';
};

const handleClick = (item) => {
    if (canViewNotification(item)) {
        emit('view-notification', item.notification);
    }
};

const getItemClasses = (item) => {
    if (canViewNotification(item)) {
        return 'hover:bg-gray-100 dark:hover:bg-gray-700/50 cursor-pointer';
    }
    return 'cursor-not-allowed opacity-70';
};

const getStatusText = (item) => {
    if (!item.is_seen) {
        return 'New';
    }
    if (item.notification.notification_type === 'survey') {
        return item.is_completed ? 'Completed' : 'Pending';
    }
    return 'Viewed';
};

const getStatusClass = (item) => {
    if (!item.is_seen) {
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300'; // New
    }
    if (item.notification.notification_type === 'survey' && item.is_completed) {
        return 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300'; // Completed
    }
    return 'bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-200'; // Viewed / Pending
};

</script>

