<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
    <main class="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-indigo-600 dark:text-indigo-400">Create Your Account</h1>
        <p class="text-gray-500 dark:text-gray-400">Join LingoJourn to start your English learning journey</p>
      </div>
      <form @submit.prevent="handleSignup" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="realname" class="text-sm font-medium text-gray-700 dark:text-gray-300">Real Name</label>
            <input
              v-model="realname"
              type="text"
              id="realname"
              required
              class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              placeholder="John Doe"
            />
          </div>
          <div>
            <label for="student_id" class="text-sm font-medium text-gray-700 dark:text-gray-300">Student ID</label>
            <input
              v-model="student_id"
              type="text"
              id="student_id"
              required
              class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              placeholder="Your ID"
            />
          </div>
        </div>
        <div>
          <label for="username" class="text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
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
          <label for="email" class="text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="you@example.com"
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
        <div>
          <label for="confirmPassword" class="text-sm font-medium text-gray-700 dark:text-gray-300">Confirm Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            id="confirmPassword"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="••••••••"
          />
        </div>
         <div v-if="authStore.error || localError" class="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/50 p-3 rounded-lg">
          {{ authStore.error || localError }}
        </div>
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="w-full py-2 px-4 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-400 dark:disabled:bg-indigo-800 transition-colors"
        >
          {{ authStore.isLoading ? 'Creating Account...' : 'Sign Up' }}
        </button>
      </form>
       <p class="text-center text-sm text-gray-600 dark:text-gray-400">
        Already have an account?
        <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
          Log In
        </router-link>
      </p>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();
const router = useRouter();
const realname = ref('');
const student_id = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const localError = ref('');

const getGroupFromPort = () => {
  const port = window.location.port;
  if (port === '7779') {
    return 'CG';
  } else if (port === '7778') {
    return 'EG';
  }
  else{
    const hostname = window.location.hostname;
    if (hostname === 'ti.parasyst.com') {
      return 'CG';
    } else if (hostname === 'it.parasyst.com') {
      return 'EG';
    }
    return 'TEST';
  }
};

const handleSignup = async () => {
  localError.value = '';
  authStore.error = null;

  if (password.value !== confirmPassword.value) {
    localError.value = 'Passwords do not match.';
    return;
  }

  const group = getGroupFromPort(); 
  await authStore.signup({ 
    realname: realname.value,
    student_id: student_id.value,
    group: group,
    username: username.value, 
    email: email.value, 
    password: password.value 
  });

  if (!authStore.error) {
    // Redirect to the login page on successful signup
    router.push('/login');
  }
};
</script>
