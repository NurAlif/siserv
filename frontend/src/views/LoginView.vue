<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
    <main class="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-indigo-600 dark:text-indigo-400">LingoJourn</h1>
        <p class="text-gray-500 dark:text-gray-400">Log in to continue your journey</p>
      </div>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="text-sm font-medium text-gray-700 dark:text-gray-300">Username or Email</label>
          <input
            v-model="username"
            type="text"
            id="username"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="yourname"
          />
        </div>
        <div>
          <label for="password" class="text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="••••••••"
          />
        </div>
        <div v-if="authStore.error" class="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/50 p-3 rounded-lg">
          {{ authStore.error }}
        </div>
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="w-full py-2 px-4 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-400 dark:disabled:bg-indigo-800 transition-colors"
        >
          {{ authStore.isLoading ? 'Logging in...' : 'Log In' }}
        </button>
      </form>
      <p class="text-center text-sm text-gray-600 dark:text-gray-400">
        Don't have an account? 
        <router-link to="/signup" class="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
          Sign Up
        </router-link>
      </p>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();
const username = ref('');
const password = ref('');

const handleLogin = () => {
  authStore.login({ username: username.value, password: password.value });
};
</script>
