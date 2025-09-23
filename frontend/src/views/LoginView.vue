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
const participantManualContent = `
<h1>LingoJourn User Manual</h1>
<p>Welcome to LingoJourn, your personal AI-powered partner for improving your English through journaling! This guide will walk you through all the features of the app.</p>
<hr />
<h2>1. Getting Started</h2>
<h3>Creating Your Account</h3>
<p>To use LingoJourn, you must first create an account.</p>
<ol>
    <li>Click on the <strong>Sign Up</strong> link on the login page.</li>
    <li>Fill in your details: Real Name, Student ID, Username, Email, and a secure Password.</li>
    <li><strong>Important</strong>: Your Student ID and Email must be pre-approved by your teacher/administrator to register successfully.</li>
    <li>Once you sign up, you'll be redirected to the login page.</li>
</ol>
<h3>Logging In</h3>
<p>Enter the Username and Password you created during signup to access your dashboard.</p>
<hr />
<h2>2. Your Dashboard</h2>
<p>The dashboard is your central hub. Here you can:</p>
<ul>
    <li><strong>See your writing streak</strong>: Keep writing every day to build your streak!</li>
    <li><strong>View your Learning Snapshot</strong>: Get a quick overview of your progress, including total errors logged and your top area for improvement.</li>
    <li><strong>Access past journals</strong>: All your previous entries are listed here. Click on any card to view or continue working on it.</li>
    <li><strong>Start a new entry</strong>: Click the "New Entry" button to begin your journal for the day.</li>
</ul>
<hr />
<h2>3. The Four-Phase Writing Process</h2>
<p>Every journal entry follows a structured four-phase process designed to maximize your learning.</p>
<h3>Phase 1: Scaffolding (Outline)</h3>
<p>This is the planning stage. The goal is to create a simple outline for your journal entry.</p>
<ul>
    <li><strong>Write freely</strong>: You can directly type your main ideas into the text area.</li>
    <li><strong>Chat with Lingo</strong>: If you're stuck, click "Chat with Lingo". Your AI partner will ask you guiding questions to help you brainstorm. As you discuss ideas, Lingo can automatically add them to your outline.</li>
    <li><strong>Quick Corrections</strong>: While chatting, you can enable the "Correct" toggle to get instant feedback on your messages.</li>
</ul>
<p>When your outline is ready, click <strong>Start Writing</strong>.</p>
<h3>Phase 2: Writing (Draft)</h3>
<p>Now it's time to write your full journal entry.</p>
<ul>
    <li><strong>Your Outline</strong>: Your outline is visible to guide you.</li>
    <li><strong>Writing Area</strong>: Write your draft in the main text area. Your work is saved automatically.</li>
    <li><strong>AI Writing Partner</strong>: The chat window is now your Writing Partner. If you need help, just ask! You can ask things like:
        <ul class="list-disc list-inside ml-6 mt-2">
            <li>"What should I write next?"</li>
            <li>"How can I say this better?"</li>
            <li>"What's another word for 'happy'?"</li>
        </ul>
    </li>
</ul>
<p>Once your draft is complete, click <strong>Evaluate Writing</strong>.</p>
<h3>Phase 3: Evaluation (Feedback)</h3>
<p>In this phase, Lingo analyzes your complete draft and provides detailed feedback.</p>
<ul>
    <li><strong>Corrected Text</strong>: You will see your original text with potential errors highlighted.</li>
    <li><strong>Suggestions List</strong>: On the right, you'll find a list of cards, each explaining an error and suggesting a correction. The feedback covers grammar, vocabulary, phrasing, and more.</li>
    <li><strong>Apply Suggestions</strong>: For each suggestion, you can click the "Apply" button to automatically fix the error in your text.</li>
    <li><strong>Mark as Complete</strong>: Once you have reviewed and applied all the suggestions, the "Mark as Complete" button will become active. Click it to finalize your entry.</li>
</ul>
<h3>Phase 4: Completed</h3>
<p>Congratulations! You've finished your journal entry for the day.</p>
<ul>
    <li>Your final, corrected text is saved.</li>
    <li>All the new errors and learning points from this session have been added to your <strong>Learning Hub</strong> for future review.</li>
</ul>
<hr />
<h2>4. The Learning Hub</h2>
<p>Accessible from the top navigation bar, the Learning Hub is your personalized progress tracker.</p>
<ul>
    <li><strong>Focus Areas</strong>: It lists all the error categories you've encountered (e.g., <code>Grammar: Verb Tense</code>).</li>
    <li><strong>Detailed Review</strong>: Click on any topic to see a full history of your mistakes in that area, including the incorrect phrase, the suggestion, and the explanation. This is a powerful tool to identify and work on your recurring challenges.</li>
</ul>
`;
</script>
