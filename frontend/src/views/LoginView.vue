<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
    <main class="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-indigo-600 dark:text-indigo-400">LingoJourn</h1>
        <p class="text-gray-500 dark:text-gray-400">Log in to continue your journey</p>
      </div>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="text-sm font-medium text-gray-700 dark:text-gray-300">Username or Student ID</label>
          <input
            v-model="username"
            type="text"
            id="username"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="yourname or 412..."
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
      <div class="text-center text-sm text-gray-600 dark:text-gray-400">
        <p>
          Don't have an account? 
          <router-link to="/signup" class="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
            Sign Up
          </router-link>
        </p>
        <!-- Button to open the user manual -->
        <p class="mt-4">
            Need help? 
            <button @click="showManualModal = true" class="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
                View User Manual
            </button>
        </p>
      </div>
    </main>

    <!-- Modal for the user manual -->
    <ManualModal 
        :show="showManualModal" 
        title="LingoJourn User Manual"
        :content="participantManualContent"
        @close="showManualModal = false" 
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/authStore';
import ManualModal from '../components/ManualModal.vue'; // Import the new modal component

const authStore = useAuthStore();
const username = ref('');
const password = ref('');

const showManualModal = ref(false); // State to control the modal's visibility

const handleLogin = () => {
  authStore.login({ username: username.value, password: password.value });
};

// The content for the participant manual is stored here as an HTML string.
// I've added images with loading="lazy" to illustrate key features.
const participantManualContent = `
<h1>LingoJourn User Manual</h1>
<p>Welcome to LingoJourn, your personal AI-powered partner for improving your English through journaling! This guide will walk you through all the features of the app.</p>
<hr />
<h2>1. Getting Started</h2>
<h3>Creating Your Account</h3>
<p>To use LingoJourn, you must first create an account.</p>
<ol>
    <li>Click on the <strong>Sign Up</strong> link on the login page.</li>
        <img src="https://ipa.parasyst.com/static/images/login.png" alt="login" loading="lazy">
        <br/>
    <li>Fill in your details: Real Name, Student ID, Username, Email, and a secure Password.</li>
        <img src="https://ipa.parasyst.com/static/images/signup.png" alt="sign up" loading="lazy">
        <br/>
    <li><strong>Important</strong>: Your Student ID and Email must be pre-approved by your teacher/administrator to register successfully.</li>
        <img src="https://ipa.parasyst.com/static/images/signup_login.png" alt="login" loading="lazy">
        <br/>
    <li>Once you sign up, you'll be redirected to the login page.</li>
</ol>
<h3>Logging In</h3>
<p>Enter the Username and Password you created during signup to access your dashboard.</p>
<hr />
<h2>2. Your Dashboard</h2>
<p>The dashboard is your central hub. Here you can see your writing streak, a snapshot of your learning progress, access past journals, or start a new entry.</p>
  <img src="https://ipa.parasyst.com/static/images/dashboard.png" alt="Dashboard Overview" loading="lazy">
  <br/>
<hr />
<h2>3. The Four-Phase Writing Process</h2>
<p>Every journal entry follows a structured four-phase process designed to maximize your learning. It guides you from planning to a final, polished piece.</p>
  <img src="https://placehold.co/600x120/e2e8f0/4a5568?text=1.+Scaffolding+→+2.+Writing+→+3.+Evaluation+→+4.+Completed" alt="Writing Phases" loading="lazy">
  <br/>
<h3>Phase 1: Scaffolding (Outline)</h3>
<p>This is the planning stage. The goal is to create a simple outline for your journal entry. You can write freely or chat with your AI partner, Lingo, for ideas.</p>
  <img src="https://ipa.parasyst.com/static/images/scaffolding.png" alt="scaffolding" loading="lazy">
  <br/>
<h3>Phase 2: Writing (Draft)</h3>
<p>Now it's time to write your full journal entry using your outline as a guide. Your AI Writing Partner is available to help if you get stuck.</p>
  <img src="https://ipa.parasyst.com/static/images/writing.png" alt="Writing" loading="lazy">
  <br/>
<h3>Phase 3: Evaluation (Feedback)</h3>
<p>In this phase, Lingo analyzes your complete draft and provides detailed feedback on grammar, vocabulary, and phrasing. You can apply the suggestions with a single click.</p>
  <img src="https://ipa.parasyst.com/static/images/Evaluation.png" alt="Evaluation" loading="lazy">
  <br/>
<h3>Phase 4: Completed</h3>
<p>Congratulations! You've finished your journal entry. Your final text is saved, and all the learning points have been added to your <strong>Learning Hub</strong> for future review.</p>
  <img src="https://ipa.parasyst.com/static/images/finished.png" alt="finished" loading="lazy">
  <br/>
<hr />
`;
</script>
