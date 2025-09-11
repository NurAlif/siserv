<template>
  <div v-if="authStore.isAuthenticated">
    <div id="app-container" class="max-w-4xl mx-auto p-4 md:p-6">
      <header class="flex justify-between items-center mb-6">
        <div class="flex items-center gap-3">
           <div class="bg-indigo-600 p-2 rounded-lg">
              <!-- Book Icon -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="text-white" fill="currentColor" viewBox="0 0 256 256"><path d="M208,24H88A48.05,48.05,0,0,0,40,72V208a48.05,48.05,0,0,0,48,48H208a8,8,0,0,0,8-8V32A8,8,0,0,0,208,24ZM88,240a32,32,0,0,1,0-64H200V240ZM200,40v96H88a32,32,0,0,1,0-64h8V40Z"></path></svg>
           </div>
           <h1 class="text-2xl font-bold text-indigo-600">LingoJourn</h1>
        </div>
        <div id="user-profile" class="flex items-center gap-3">
           <span class="text-sm font-medium">{{ authStore.user?.username }}</span>
           <button @click="authStore.logout()" title="Logout" class="p-2 rounded-full hover:bg-gray-200 transition-colors">
              <!-- SignOut Icon -->
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="text-gray-600" viewBox="0 0 256 256"><path d="M112,216a8,8,0,0,1-8,8H48a16,16,0,0,1-16-16V48A16,16,0,0,1,48,32h56a8,8,0,0,1,0,16H48V208h56A8,8,0,0,1,112,216Zm109.66-93.66-48-48a8,8,0,0,0-11.32,11.32L196.69,120H104a8,8,0,0,0,0,16h92.69l-34.35,34.34a8,8,0,0,0,11.32,11.32l48-48a8,8,0,0,0,0-11.32Z"></path></svg>
           </button>
        </div>
      </header>
      <router-view />
    </div>
  </div>
  <div v-else>
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/authStore';
const authStore = useAuthStore();
</script>

