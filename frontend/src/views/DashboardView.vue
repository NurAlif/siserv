<template>
  <main id="dashboard-view" class="fade-in">
    <!-- Modal for showing a SINGLE notification (announcement or survey) -->
    <NotificationModal
      v-if="notificationToView"
      :notification="notificationToView"
      :is-loading="notificationStore.isLoading"
      @close="handleModalClose"
      @submit="handleSurveySubmit"
    />

    <!-- Modal for showing the list of ALL notifications -->
    <NotificationListModal 
        :show="notificationStore.showHistoryModal"
        @close="notificationStore.closeHistoryModal()"
        @view-notification="handleViewNotificationFromList"
    />

    <div class="bg-white dark:bg-gray-800 p-3 sm:p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-6">
      <div class="flex flex-row justify-between items-center gap-2">
        <div class="flex-grow">
          <h2 class="text-sm sm:text-xl font-bold text-gray-900 dark:text-gray-100 truncate">Welcome Back, {{ authStore.user?.username }}!</h2>
          <p class="text-gray-500 dark:text-gray-400 text-sm">Ready to practice your English today?</p>
        </div>
        <div class="flex-col sm:flex-row flex-shrink-0 flex items-center gap-2 sm:gap-3 bg-orange-100 dark:bg-orange-900/50 text-orange-700 dark:text-orange-300 p-2 sm:p-3 rounded-lg">
          <!-- Fire Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-flame-icon lucide-flame"><path d="M12 3q1 4 4 6.5t3 5.5a1 1 0 0 1-14 0 5 5 0 0 1 1-3 1 1 0 0 0 5 0c0-2-1.5-3-1.5-5q0-2 2.5-4"/></svg>
          <div>
            <div class="font-bold text-sm sm:text-xm sm:text-base whitespace-nowrap">{{ progressStore.streak }} Day Streak</div>
            <p class="text-sm sm:text-sm hidden sm:block">Keep it up!</p>
          </div>
        </div>
      </div>
    </div>

    <!-- View Controls -->
    <div class="flex flex-row justify-between items-center mb-4 gap-4">
      <div class="flex items-center gap-1 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
        <button 
          @click="viewMode = 'list'" 
          :class="viewMode === 'list' ? 'bg-white dark:bg-gray-800 shadow text-indigo-600' : 'text-gray-500 dark:text-gray-400'" 
          class="px-3 py-1 text-sm font-semibold rounded-md transition-all flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M224,88H32a8,8,0,0,0-8,8v64a8,8,0,0,0,8,8H224a8,8,0,0,0,8-8V96A8,8,0,0,0,224,88Zm-8,64H40V104H216v48ZM32,48H224a8,8,0,0,0,0-16H32a8,8,0,0,0,0,16Zm0,160H224a8,8,0,0,0,0-16H32a8,8,0,0,0,0,16Z"></path></svg>
          List
        </button>
        <button 
          @click="viewMode = 'calendar'" 
          :class="viewMode === 'calendar' ? 'bg-white dark:bg-gray-800 shadow text-indigo-600' : 'text-gray-500 dark:text-gray-400'" 
          class="px-3 py-1 text-sm font-semibold rounded-md transition-all flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32Zm0,16V80H48V48ZM48,208V96H208V208Z"></path></svg>
          Calendar
        </button>
      </div>
      <router-link
      to="/writer"
      class="bg-indigo-600 text-white font-semibold px-3 py-1 md:px-4 md:py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-1 md:gap-2 text-sm md:text-base"
      >
        <!-- Small icon for mobile -->
        <svg class="md:hidden" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path></svg>
        <!-- Larger icon for desktop -->
        <svg class="hidden md:block" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path></svg>
        
        <!-- Short text for mobile -->
        <span class="md:hidden">New Entry</span>
        <!-- Longer text for desktop -->
        <span class="hidden md:inline">New Entry for Today</span>
      </router-link>
    </div>

    <!-- Loading and Error States -->
    <div v-if="journalStore.isLoading" class="text-center py-10">
      <p class="text-gray-500 dark:text-gray-400">Loading your journals...</p>
    </div>
    <div v-else-if="journalStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
      <p>{{ journalStore.error }}</p>
    </div>

    <!-- Conditional Views -->
    <template v-else>
      <!-- List View -->
      <div v-if="viewMode === 'list'">
        <div v-if="journalStore.journals.length > 0" id="journal-list" class="space-y-4">
          <JournalCard
            v-for="journal in journalStore.journals"
            :key="journal.id"
            :journal="journal"
          />
        </div>
        <div v-else class="text-center py-10 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <h4 class="font-semibold text-lg text-gray-800 dark:text-gray-200">No entries yet!</h4>
            <p class="text-gray-500 dark:text-gray-400">Click "New Entry for Today" to start your first journal.</p>
        </div>
      </div>
      <!-- Calendar View -->
      <JournalCalendarView v-else-if="viewMode === 'calendar'" :journals="journalStore.journals" />
    </template>
  </main>
</template>

<script setup>
import { onMounted, ref, watch, onUnmounted } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useJournalStore } from '../stores/journalStore';
import { useProgressStore } from '../stores/progressStore';
import { useNotificationStore } from '../stores/notificationStore';
import JournalCard from '../components/JournalCard.vue';
import JournalCalendarView from '../components/JournalCalendarView.vue';
import NotificationModal from '../components/NotificationModal.vue';
import NotificationListModal from '../components/NotificationListModal.vue';


const authStore = useAuthStore();
const journalStore = useJournalStore();
const progressStore = useProgressStore();
const notificationStore = useNotificationStore();

const viewMode = ref('list');
const notificationToView = ref(null); // This will hold the notification for the single modal

// This watcher is the core of the sequential display logic
watch(
  () => notificationStore.activeNotifications,
  (active) => {
    // If there are active notifications and the user hasn't manually opened the history list...
    if (active.length > 0 && notificationStore.shouldShowModal) {
      // ...show the first one in the queue.
      notificationToView.value = active[0];
    } else {
      // Otherwise, there's nothing to show, so close the modal.
      notificationToView.value = null;
    }
  },
  { immediate: true, deep: true } // deep is important for array changes
);


// This function is called when a notification is selected from the history list
const handleViewNotificationFromList = (notification) => {
    notificationStore.closeHistoryModal(); // Close the list modal
    // Need a small delay for the modals to transition smoothly
    setTimeout(() => {
        notificationToView.value = notification;
    }, 200);
};

const handleModalClose = async () => {
  const notif = notificationToView.value;
  if (notif && notif.notification_type === 'announcement') {
    // This action will remove the notification from the active list if it's new
    await notificationStore.markAsSeen(notif.id);
  } else {
    // If it's a survey or the user just closes an old announcement
    notificationToView.value = null; 
  }
  // The watcher will automatically show the next notification if one exists
};


const handleSurveySubmit = async (payload) => {
  // This action will remove the notification from the active list
  await notificationStore.submitSurvey(payload);
  // The watcher will automatically show the next notification or close the modal
};

onMounted(() => {
  journalStore.fetchJournals();
  progressStore.fetchStreak();
  // Fetch active (new) notifications if the list is empty
  if (notificationStore.notificationCount === 0) {
      notificationStore.fetchActiveNotifications();
  }
});

onUnmounted(() => {
    // Reset the state when leaving the dashboard to allow modals on next visit
    notificationStore.resetManualOpenState();
});
</script>

