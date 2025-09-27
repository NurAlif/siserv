<template>
  <div v-if="authStore.isAuthenticated" :class="containerClass">
    <header v-if="!isWriterView" class="flex justify-between items-center mb-6 flex-shrink-0">
      <div class="flex items-center gap-3">
         <router-link to="/" class="hidden sm:flex items-center gap-3">
           <div class="bg-indigo-600 p-2 rounded-lg">
              <!-- Book Icon -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="text-white" fill="currentColor" viewBox="0 0 256 256"><path d="M208,24H88A48.05,48.05,0,0,0,40,72V208a48.05,48.05,0,0,0,48,48H208a8,8,0,0,0,8-8V32A8,8,0,0,0,208,24ZM88,240a32,32,0,0,1,0-64H200V240ZM200,40v96H88a32,32,0,0,1,0-64h8V40Z"></path></svg>
           </div>
           <h1 class="text-2xl font-bold text-indigo-600 dark:text-indigo-400">LingoJourn</h1>
         </router-link>
         <!-- Navigation Link to Learning Hub -->
         <!-- <nav class="ml-6">
           <router-link to="/learning-hub" class="text-sm font-semibold text-gray-600 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors">Learning Hub</router-link>
         </nav> -->
         <nav class="flex items-center gap-4">
           <router-link to="/learning-hub" class="text-sm font-semibold text-gray-600 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors">Learning Hub</router-link>
           <!-- Admin Link (Conditional) -->
           <router-link v-if="authStore.isAdmin" to="/admin" class="text-sm font-semibold text-gray-600 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors">Admin</router-link>
         </nav>
      </div>
      <div id="user-profile" class="flex items-center gap-4">
         <span class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ authStore.user?.username }}</span>
         <!-- Dark Mode Toggle -->
         <button @click="uiStore.toggleDarkMode()" title="Toggle Dark Mode" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
            <svg v-if="uiStore.isDarkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="text-yellow-400" viewBox="0 0 256 256"><path d="M128,80a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,80Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,160ZM208,128a8,8,0,0,1-8,8H184a8,8,0,0,1,0-16h16A8,8,0,0,1,208,128ZM128,48a8,8,0,0,1-8,8V72a8,8,0,0,1-16,0V56a8,8,0,0,1,8-8A8,8,0,0,1,128,48ZM72,120H56a8,8,0,0,0,0,16H72a8,8,0,0,0,0-16Zm109.66,58.34a8,8,0,0,0,5.65-2.34l11.32-11.32a8,8,0,0,0-11.32-11.32l-11.32,11.32a8,8,0,0,0,5.67,13.66ZM74.34,74.34l-11.32-11.32a8,8,0,1,0-11.32,11.32l11.32,11.32a8,8,0,0,0,11.32-11.32ZM181.66,74.34a8,8,0,0,0-11.32,0L159,85.66a8,8,0,0,0,11.32,11.32l11.32-11.32A8,8,0,0,0,181.66,74.34ZM85.66,159,74.34,170.34a8,8,0,0,0,11.32,11.32l11.32-11.32a8,8,0,1,0-11.32-11.32ZM128,208a8,8,0,0,1,8-8v16a8,8,0,0,1,0,16V200A8,8,0,0,1,128,208Z"></path></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="text-gray-600 dark:text-gray-300" viewBox="0 0 256 256"><path d="M216,144a88.08,88.08,0,0,1-88,88,88,88,0,0,1,0-176,87.27,87.27,0,0,1,64,24,8,8,0,0,1-11.31,11.31A71.32,71.32,0,0,0,128,72a72,72,0,0,0,0,144,71.32,71.32,0,0,0,52.69-21.31,8,8,0,0,1,11.31,11.31A87.27,87.27,0,0,1,216,144Z"></path></svg>
         </button>
         <button @click="authStore.logout()" title="Logout" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
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
import { useRoute } from 'vue-router';
import { useAuthStore } from './stores/authStore';
import { useUiStore } from './stores/uiStore';

const authStore = useAuthStore();
const uiStore = useUiStore();
const route = useRoute();

const isWriterView = computed(() => route.name === 'Writer');

const containerClass = computed(() => {
  if (isWriterView.value) {
    // For WriterView, use a full-height flex container for the immersive layout.
    return 'h-full flex flex-col';
  }
  // For all other views, use the original centered, padded layout.
  return 'max-w-4xl mx-auto p-4 md:p-6';
});

onMounted(() => {
  uiStore.initTheme();
});
</script>
