<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50">
    <main class="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-md border border-gray-200">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-indigo-600">Create Your Account</h1>
        <p class="text-gray-500">Join LingoJourn to start your English learning journey</p>
      </div>
      <form @submit.prevent="handleSignup" class="space-y-4">
        <div>
          <label for="username" class="text-sm font-medium text-gray-700">Username</label>
          <input
            v-model="username"
            type="text"
            id="username"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="yourname"
          />
        </div>
        <div>
          <label for="email" class="text-sm font-medium text-gray-700">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="you@example.com"
          />
        </div>
        <div>
          <label for="password" class="text-sm font-medium text-gray-700">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="••••••••"
          />
        </div>
         <div v-if="authStore.error" class="text-sm text-red-600 bg-red-50 p-3 rounded-lg">
          {{ authStore.error }}
        </div>
        <div v-if="successMessage" class="text-sm text-green-700 bg-green-50 p-3 rounded-lg">
          {{ successMessage }}
        </div>
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="w-full py-2 px-4 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300 transition-colors"
        >
          {{ authStore.isLoading ? 'Creating Account...' : 'Sign Up' }}
        </button>
      </form>
       <p class="text-center text-sm text-gray-600">
        Already have an account? 
        <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
          Log In
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
const email = ref('');
const password = ref('');
const successMessage = ref('');

const handleSignup = async () => {
  successMessage.value = '';
  await authStore.signup({ 
    username: username.value, 
    email: email.value, 
    password: password.value 
  });

  if (!authStore.error) {
    successMessage.value = 'Account created successfully! You can now log in.';
    // Clear form fields
    username.value = '';
    email.value = '';
    password.value = '';
  }
};
</script>
