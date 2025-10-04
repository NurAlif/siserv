<template>
  <div v-if="authStore.isAuthenticated" :class="containerClass">
    <header v-if="!isWriterView" class="flex justify-between items-center mb-6 flex-shrink-0">
      <div class="flex items-center gap-3">
         <router-link to="/" class="flex items-center gap-3">
           <div class="bg-indigo-600 p-2 rounded-lg">
              <!-- Book Icon -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="text-white" fill="currentColor" viewBox="0 0 256 256"><path d="M208,24H88A48.05,48.05,0,0,0,40,72V208a48.05,48.05,0,0,0,48,48H208a8,8,0,0,0,8-8V32A8,8,0,0,0,208,24ZM88,240a32,32,0,0,1,0-64H200V240ZM200,40v96H88a32,32,0,0,1,0-64h8V40Z"></path></svg>
           </div>
           <h1 class="hidden sm:flex text-2xl font-bold text-indigo-600 dark:text-indigo-400">LingoJourn</h1>
         </router-link>
         <!-- Navigation Link to Learning Hub -->
         <nav class="flex items-center gap-4">
           <router-link to="/learning-hub" class="text-sm font-semibold text-gray-600 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors">Learning Hub</router-link>
           <!-- Admin Link (Conditional) -->
           <router-link v-if="authStore.isAdmin" to="/admin" class="text-sm font-semibold text-gray-600 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors">Admin</router-link>
         </nav>
      </div>
      <div id="user-profile" class="flex items-center gap-4">
         <span class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ authStore.user?.username }}</span>
         <NotificationBell 
            :notification-count="notificationStore.notificationCount"
            @open-notifications="handleOpenNotifications"
         />
         <!-- Dark Mode Toggle -->
          <Moon />
         <button @click="uiStore.toggleDarkMode()" title="Toggle Dark Mode" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
            <svg v-if="uiStore.isDarkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun-icon lucide-sun text-yellow-400"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon-icon lucide-moon text-gray-600"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/></svg>
         </button>
         <button @click="handleLogout" title="Logout" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
            <!-- SignOut Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="text-gray-600 dark:text-gray-300" viewBox="0 0 256 256"><path d="M112,216a8,8,0,0,1-8,8H48a16,16,0,0,1-16-16V48A16,16,0,0,1,48,32h56a8,8,0,0,1,0,16H48V208h56A8,8,0,0,1,112,216Zm109.66-93.66-48-48a8,8,0,0,0-11.32,11.32L196.69,120H104a8,8,0,0,0,0,16h92.69l-34.35,34.34a8,8,0,0,0,11.32,11.32l48-48a8,8,0,0,0,0-11.32Z"></path></svg>
         </button>
      </div>
    </header>
    <router-view class="flex-grow overflow-hidden" />
  </div>
  <div v-else class="h-full">
    <router-view class="h-full"/>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from './stores/authStore';
import { useUiStore } from './stores/uiStore';
import { useNotificationStore } from './stores/notificationStore';
import NotificationBell from './components/NotificationBell.vue';

const authStore = useAuthStore();
const uiStore = useUiStore();
const notificationStore = useNotificationStore();
const route = useRoute();
const router = useRouter();

const isWriterView = computed(() => route.name === 'Writer');
const isAdminView = computed(() => route.path.startsWith('/admin'));

const containerClass = computed(() => {
  if (isWriterView.value) {
    // For WriterView, use a full-height flex container for the immersive layout.
    return 'h-full flex flex-col';
  }
  if (isAdminView.value) {
    // For Admin views, use a wider container to accommodate large tables.
    return 'max-w-screen-xl mx-auto p-4 md:p-6';
  }
  // For all other views, use the original centered, padded layout.
  return 'max-w-4xl mx-auto p-4 md:p-6';
});

// Handle bell click
const handleOpenNotifications = () => {
  // This action now handles showing the history modal and fetching data
  notificationStore.userOpenedNotifications();
  
  // Navigate to dashboard if not already there, so the modal can be displayed
  if (route.name !== 'Dashboard') {
    router.push('/');
  }
};

const handleLogout = () => {
    notificationStore.resetManualOpenState();
    authStore.logout();
};

onMounted(() => {
  uiStore.initTheme();
  // Fetch notifications when the app loads for an authenticated user
  if (authStore.isAuthenticated) {
    notificationStore.fetchActiveNotifications();
  }
});
</script>

