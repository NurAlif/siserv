src/
  components/
   - AIFeedbackCard.vue
   - JournalCard.vue
  router/
   - index.js
  services/
   - api.js
  stores/
   - aiStore.js
   - authStore.js
   - journalStore.js
  views/
   - DashboardView.vue
   - LoginView.vue
   - WriterView.vue
 - App.vue
 - main.js
 - style.css
index.html







# src/components/AIFeedbackCard.vue
<template>
  <div class="p-4 rounded-lg" :class="cardColorClasses.bg">
    <p class="font-semibold" :class="cardColorClasses.text">
      {{ feedbackItem.error_type }}
    </p>
    <p class="text-sm mt-2">
      Incorrect phrase: 
      <span class="line-through text-red-600 bg-red-100 px-1 rounded">"{{ feedbackItem.incorrect_phrase }}"</span>
    </p>
    <p class="text-sm mt-1">
      Suggestion: 
      <span class="font-semibold text-green-700 bg-green-100 px-1 rounded">"{{ feedbackItem.suggestion }}"</span>
    </p>
    <p class="text-xs text-gray-700 mt-2 bg-gray-100 p-2 rounded">
      <strong>Explanation:</strong> {{ feedbackItem.explanation }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  feedbackItem: {
    type: Object,
    required: true,
  },
});

// Dynamically change card colors for better visual grouping of feedback
const cardColorClasses = computed(() => {
  const type = props.feedbackItem.error_type.toLowerCase();
  if (type.includes('grammar')) {
    return { bg: 'bg-blue-50', text: 'text-blue-800' };
  }
  if (type.includes('vocabulary') || type.includes('phrasing')) {
    return { bg: 'bg-purple-50', text: 'text-purple-800' };
  }
  if (type.includes('cohesion') || type.includes('style')) {
      return { bg: 'bg-yellow-50', text: 'text-yellow-800'};
  }
  return { bg: 'bg-gray-100', text: 'text-gray-800' }; // Default color
});
</script>

# /end of file/


# src/components/JournalCard.vue
<template>
  <router-link
    :to="`/writer/${journal.journal_date}`"
    class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 hover:border-indigo-400 transition-colors cursor-pointer flex items-start gap-4"
  >
    <!-- Image Placeholder -->
    <div class="w-24 h-[70px] bg-gray-100 rounded-md flex items-center justify-center flex-shrink-0">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="text-gray-400" viewBox="0 0 256 256"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM48,48H208V157.38l-19.52-19.52a16,16,0,0,0-22.62,0L144,160,99.51,115.51a16,16,0,0,0-22.62,0L48,144.38ZM208,208H48V172.69l36.49-36.5,44.49,44.49a16,16,0,0,0,22.62,0L176,159.31l32,32V208Zm-40-88a12,12,0,1,1,12-12A12,12,0,0,1,168,120Z"></path></svg>
    </div>
    <div class="flex-grow overflow-hidden">
      <h4 class="font-bold text-md truncate">{{ journal.title || 'Journal Entry' }}</h4>
      <p class="text-sm text-gray-500 mb-2">{{ journalStore.formatDisplayDate(journal.journal_date) }}</p>
      <p class="text-sm text-gray-600 leading-relaxed">{{ snippet }}</p>
    </div>
    <!-- Caret Icon -->
    <div class="self-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="text-gray-400" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';
import { useJournalStore } from '../stores/journalStore';

const journalStore = useJournalStore();

const props = defineProps({
  journal: {
    type: Object,
    required: true,
  },
});

// Create a snippet from the full content
const snippet = computed(() => {
  if (!props.journal.content) {
    return 'No content yet...';
  }
  // Truncate the content to 120 characters
  if (props.journal.content.length > 120) {
    return props.journal.content.substring(0, 120) + '...';
  }
  return props.journal.content;
});
</script>


# /end of file/


# src/router/index.js
<template>
  <router-link
    :to="`/writer/${journal.journal_date}`"
    class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 hover:border-indigo-400 transition-colors cursor-pointer flex items-start gap-4"
  >
    <!-- Image Placeholder -->
    <div class="w-24 h-[70px] bg-gray-100 rounded-md flex items-center justify-center flex-shrink-0">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="text-gray-400" viewBox="0 0 256 256"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM48,48H208V157.38l-19.52-19.52a16,16,0,0,0-22.62,0L144,160,99.51,115.51a16,16,0,0,0-22.62,0L48,144.38ZM208,208H48V172.69l36.49-36.5,44.49,44.49a16,16,0,0,0,22.62,0L176,159.31l32,32V208Zm-40-88a12,12,0,1,1,12-12A12,12,0,0,1,168,120Z"></path></svg>
    </div>
    <div class="flex-grow overflow-hidden">
      <h4 class="font-bold text-md truncate">{{ journal.title || 'Journal Entry' }}</h4>
      <p class="text-sm text-gray-500 mb-2">{{ journalStore.formatDisplayDate(journal.journal_date) }}</p>
      <p class="text-sm text-gray-600 leading-relaxed">{{ snippet }}</p>
    </div>
    <!-- Caret Icon -->
    <div class="self-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="text-gray-400" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';
import { useJournalStore } from '../stores/journalStore';

const journalStore = useJournalStore();

const props = defineProps({
  journal: {
    type: Object,
    required: true,
  },
});

// Create a snippet from the full content
const snippet = computed(() => {
  if (!props.journal.content) {
    return 'No content yet...';
  }
  // Truncate the content to 120 characters
  if (props.journal.content.length > 120) {
    return props.journal.content.substring(0, 120) + '...';
  }
  return props.journal.content;
});
</script>


# /end of file/


# api.js
import axios from 'axios';
import { useAuthStore } from '../stores/authStore';

// Create an Axios instance with a base URL from environment variables
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8099/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token in headers
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.token;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;

# /end of file/


# src/stores/aiStore.js
import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { useJournalStore } from './journalStore';

export const useAiStore = defineStore('ai', {
  state: () => ({
    feedback: [],
    isLoading: false,
    error: null,
  }),
  actions: {
    async getFeedback(date, text) {
      this.isLoading = true;
      this.error = null;
      this.feedback = []; // Clear previous feedback before fetching new results
      try {
        // According to the API docs, the endpoint is /api/ai/feedback/{journal_date}
        const response = await apiClient.post(`/ai/feedback/${date}`, { text });
        
        // The response body is expected to be an object like { "feedback": [...] }
        this.feedback = response.data.feedback || [];
      } catch (err) {
        this.error = 'An error occurred while getting AI feedback. Please try again.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    // --- New Action: Chat with the AI ---
    async chatWithAI(date, message) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.post(`/ai/chat/${date}`, { message });
        const { updated_journal_content } = response.data;
        
        // After getting the response, update the journal's content in the journalStore
        const journalStore = useJournalStore();
        journalStore.setJournalContent(date, updated_journal_content);

      } catch (err) {
        this.error = 'An error occurred during the chat. Please try again.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});

# /end of file/


# src/stores/authStore.js
import { defineStore } from 'pinia';
import apiClient from '../services/api';
import router from '../router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    error: null,
    isLoading: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
  },
  actions: {
    async login(credentials) {
      this.isLoading = true;
      this.error = null;
      try {
        // API expects form data for the token endpoint
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const response = await apiClient.post('/auth/token', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        const token = response.data.access_token;
        this.token = token;
        localStorage.setItem('token', token);

        // After getting token, fetch user profile
        await this.fetchUser();
        
        // Redirect to dashboard
        router.push('/');
      } catch (err) {
        this.error = 'Login failed. Please check your credentials.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchUser() {
        if (!this.token) return;
        try {
            const response = await apiClient.get('/auth/me');
            this.user = response.data;
        } catch (err) {
            console.error('Failed to fetch user:', err);
            // If fetching user fails (e.g., expired token), log them out
            this.logout();
        }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
      router.push('/login');
    },
  },
});

# /end of file/


# src/stores/journalStore.js
import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { format, parseISO } from 'date-fns';
import { useRouter } from 'vue-router';

export const useJournalStore = defineStore('journal', {
  state: () => ({
    journals: [],
    isLoading: false,
    error: null,
  }),
  getters: {
    getJournalByDate: (state) => (date) => {
      return state.journals.find(j => j.journal_date === date);
    }
  },
  actions: {
    // --- Existing actions ---
    async fetchJournals() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/journals/');
        // The API returns journal_date as a string like "2025-09-10"
        // We'll format it for display later, but store as is.
        this.journals = response.data;
      } catch (err) {
        this.error = 'Failed to load journal entries.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    async fetchJournalByDate(date) {
        // Check if we already have it
        const existing = this.getJournalByDate(date);
        if (existing) {
            return existing;
        }

        // If not, fetch it from the API
        this.isLoading = true;
        this.error = null;
        try {
            const response = await apiClient.get(`/journals/${date}`);
            // Add the newly fetched journal to our list
            this.journals.push(response.data);
            return response.data;
        } catch (err) {
            this.error = 'Failed to load journal entry.';
            console.error(err);
            return null; // Return null on failure
        } finally {
            this.isLoading = false;
        }
    },

    // --- New Action: Create a journal entry ---
    async createJournal(content) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.post('/journals/', { content });
        // Add the new journal to the front of our local list
        this.journals.unshift(response.data);
        return response.data; // Return the created journal
      } catch (err) {
        this.error = 'Failed to create journal entry.';
        console.error(err);
        return null;
      } finally {
        this.isLoading = false;
      }
    },

    // --- New Action: Update a journal entry ---
    async updateJournal(date, content) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.put(`/journals/${date}`, { content });
        // Find and update the journal in our local list
        const index = this.journals.findIndex(j => j.journal_date === date);
        if (index !== -1) {
          this.journals[index] = response.data;
        }
        return response.data;
      } catch (err) {
        this.error = 'Failed to update journal entry.';
        console.error(err);
        return null;
      } finally {
        this.isLoading = false;
      }
    },

    // --- New Action: Directly set a journal's content ---
    // This allows other stores (like the AI store) to update content reactively
    setJournalContent(date, newContent) {
      const index = this.journals.findIndex(j => j.journal_date === date);
      if (index !== -1) {
        this.journals[index].content = newContent;
      }
    },

    formatDisplayDate(dateString) {
      if (!dateString) return '';
      // parseISO handles the 'YYYY-MM-DD' format
      const date = parseISO(dateString);
      return format(date, 'MMMM d, yyyy');
    }
  },
});


# /end of file/


# src/views/DashboardView.vue
<template>
  <main id="dashboard-view" class="fade-in">
    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 class="text-xl font-bold">Welcome Back, {{ authStore.user?.username }}!</h2>
          <p class="text-gray-500">Ready to practice your English today?</p>
        </div>
        <div class="flex items-center gap-3 bg-orange-100 text-orange-700 p-3 rounded-lg">
          <!-- Fire Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 256 256">
            <path d="M221.5,145.45C221.5,184.12,190,224,150,224s-72-39.88-72-78.55c0-20.93,12.35-46,29.9-71.55,14.28-20.81,28.2-38,33.43-45.11a8,8,0,0,1,13.34,0c5.23,7.07,19.15,24.3,33.43,45.11C209.15,99.44,221.5,124.52,221.5,145.45ZM152,80a16,16,0,1,0-16,16A16,16,0,0,0,152,80Z"></path>
          </svg>
          <div>
            <div class="font-bold text-lg">12 Day Streak</div>
            <p class="text-sm">Keep it up!</p>
          </div>
        </div>
      </div>
    </div>

    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold">Your Journal Entries</h3>
      <router-link
        to="/writer"
        class="bg-indigo-600 text-white font-semibold px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
      >
        <!-- Plus Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path></svg>
        New Entry
      </router-link>
    </div>

    <!-- Loading and Error States -->
    <div v-if="journalStore.isLoading" class="text-center py-10">
      <p class="text-gray-500">Loading your journals...</p>
    </div>
    <div v-else-if="journalStore.error" class="bg-red-50 text-red-700 p-4 rounded-lg">
      <p>{{ journalStore.error }}</p>
    </div>

    <!-- Journal List -->
    <div v-else-if="journalStore.journals.length > 0" id="journal-list" class="space-y-4">
       <JournalCard
         v-for="journal in journalStore.journals"
         :key="journal.id"
         :journal="journal"
       />
    </div>
    <div v-else class="text-center py-10 bg-white rounded-xl border border-gray-200">
        <h4 class="font-semibold text-lg">No entries yet!</h4>
        <p class="text-gray-500">Click "New Entry" to start your first journal.</p>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useJournalStore } from '../stores/journalStore';
import JournalCard from '../components/JournalCard.vue';

const authStore = useAuthStore();
const journalStore = useJournalStore();

// Fetch journals when the component is first mounted
onMounted(() => {
  journalStore.fetchJournals();
});
</script>


# /end of file/


# src/views/LoginView.vue
<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50">
    <main class="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-md border border-gray-200">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-indigo-600">LingoJourn</h1>
        <p class="text-gray-500">Log in to continue your journey</p>
      </div>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="text-sm font-medium text-gray-700">Username or Email</label>
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
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="w-full py-2 px-4 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300 transition-colors"
        >
          {{ authStore.isLoading ? 'Logging in...' : 'Log In' }}
        </button>
      </form>
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

# /end of file/


# src/views/WriterView.vue
<template>
  <main id="writer-view" class="fade-in">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <router-link to="/" class="text-gray-500 hover:text-gray-800 font-medium flex items-center gap-2">
         <!-- ArrowLeft Icon -->
         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        Back to Dashboard
      </router-link>
      <div class="flex items-center gap-2 text-sm text-gray-500">
        <span>Status:</span>
        <span class="font-semibold text-gray-700">{{ statusText }}</span>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="p-6 border-b border-gray-200">
        <h2 id="journal-title" class="text-2xl font-bold">{{ currentJournal?.title || 'New Journal Entry' }}</h2>
        <p id="journal-date" class="text-gray-500">{{ displayDate }}</p>
      </div>

      <!-- Mode Toggle -->
      <div class="p-4 bg-gray-50 flex justify-center gap-2 rounded-t-lg border-b border-gray-200">
        <button @click="setMode('editor')" :class="modeButtonClass('editor')">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M227.31,73.37,182.63,28.68a16,16,0,0,0-22.63,0L36.69,152A15.86,15.86,0,0,0,32,163.31V208a16,16,0,0,0,16,16H92.69A15.86,15.86,0,0,0,104,219.31L227.31,96a16,16,0,0,0,0-22.63ZM92.69,208H48V163.31l88-88L180.69,120ZM192,108.68,147.31,64l24-24L216,84.68Z"></path></svg>
          Editor Mode
        </button>
        <button @click="setMode('chat')" :class="modeButtonClass('chat')">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,212.3a16,16,0,0,0,20.55,18.85l37.81-12.6A104,104,0,1,0,128,24Zm0,192a88.1,88.1,0,0,1-45.43-13.25a8,8,0,0,0-9-1.33L40,211.52l9.9-32.68a8,8,0,0,0-1.12-8.52A88,88,0,1,1,128,216Zm72-96a16,16,0,1,1-16-16A16,16,0,0,1,200,120Zm-56,0a16,16,0,1,1-16-16A16,16,0,0,1,144,120Zm-56,0a16,16,0,1,1-16-16A16,16,0,0,1,88,120Z"></path></svg>
          Chat Mode
        </button>
      </div>
      
      <!-- Editor & Chat Content -->
      <div>
          <!-- Editor Mode UI -->
          <div v-show="activeMode === 'editor'" id="editor-content" class="p-6">
            <textarea v-model="content" class="w-full h-96 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"></textarea>
          </div>

          <!-- Chat Mode UI -->
          <div v-show="activeMode === 'chat'" id="chat-content" class="p-6">
             <div class="w-full h-96 border border-gray-300 rounded-lg flex flex-col bg-gray-50">
                <div ref="chatContainer" class="flex-grow p-4 overflow-y-auto space-y-4">
                   <div v-for="(message, index) in chatHistory" :key="index" class="flex" :class="message.sender === 'User' ? 'justify-end' : 'justify-start'">
                      <div class="p-3 rounded-lg max-w-xs break-words" :class="message.sender === 'User' ? 'bg-indigo-500 text-white' : 'bg-gray-200'">
                         <p class="text-sm">{{ message.text }}</p>
                      </div>
                   </div>
                   <div v-if="aiStore.isLoading" class="flex justify-start">
                        <div class="bg-gray-200 p-3 rounded-lg animate-pulse">
                            <p class="text-sm text-gray-400">...</p>
                        </div>
                   </div>
                </div>
                <div class="p-4 border-t border-gray-200 bg-white">
                  <input v-model="newMessage" @keyup.enter="sendMessage" :disabled="aiStore.isLoading || !currentJournal" type="text" placeholder="Type your message..." class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none disabled:bg-gray-100">
                </div>
              </div>
          </div>
      </div>

      <!-- Action Buttons (only for Editor mode) -->
      <div v-if="activeMode === 'editor'" id="editor-actions" class="p-6 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center gap-4">
        <button class="w-full md:w-auto bg-gray-100 text-gray-700 font-semibold px-4 py-2 rounded-lg hover:bg-gray-200">
          Upload Image
        </button>
        <div class="flex flex-col md:flex-row items-center gap-4 w-full md:w-auto">
            <button @click="saveJournal" :disabled="journalStore.isLoading" class="w-full md:w-auto bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300 transition-colors">
                {{ journalStore.isLoading ? 'Saving...' : 'Save Changes' }}
            </button>
            <button v-if="currentJournal" @click="getAIFeedback" :disabled="aiStore.isLoading" class="w-full md:w-auto bg-teal-500 text-white font-semibold px-6 py-2 rounded-lg hover:bg-teal-600 disabled:bg-teal-300">
                {{ aiStore.isLoading ? 'Analyzing...' : 'Get AI Feedback' }}
            </button>
        </div>
      </div>
    </div>
    <!-- AI Feedback Section -->
    <div v-if="showAIFeedback" id="ai-feedback-section" class="mt-6 bg-white p-6 rounded-xl shadow-sm border border-gray-200 fade-in">
        <h3 class="text-lg font-semibold mb-4 text-teal-700">AI Feedback & Learning Points</h3>
        <div v-if="aiStore.isLoading" class="text-center py-4">
            <p class="text-gray-500 animate-pulse">Analyzing your text...</p>
        </div>
        <div v-else-if="aiStore.error" class="bg-red-50 text-red-700 p-4 rounded-lg">
            <p>{{ aiStore.error }}</p>
        </div>
        <div v-else-if="aiStore.feedback.length > 0" class="space-y-4">
            <AIFeedbackCard 
                v-for="(item, index) in aiStore.feedback"
                :key="index"
                :feedback-item="item"
            />
        </div>
        <div v-else class="text-center py-4">
            <p class="text-gray-600 font-semibold">Great job!</p>
            <p class="text-gray-500">The AI didn't find any specific errors to correct in your text.</p>
        </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useJournalStore } from '../stores/journalStore';
import { useAiStore } from '../stores/aiStore';
import { format } from 'date-fns';
import AIFeedbackCard from '../components/AIFeedbackCard.vue';

const route = useRoute();
const router = useRouter();
const journalStore = useJournalStore();
const aiStore = useAiStore();

const currentJournal = ref(null);
const content = ref('');
const statusText = ref('Saved');
const activeMode = ref('editor');
const showAIFeedback = ref(false);
const newMessage = ref('');
const chatContainer = ref(null);

const displayDate = computed(() => {
  if (currentJournal.value) {
    return journalStore.formatDisplayDate(currentJournal.value.journal_date);
  }
  return format(new Date(), 'MMMM d, yyyy');
});

const loadJournalData = async () => {
  const date = route.params.date;
  if (date) {
    let journal = journalStore.getJournalByDate(date);
    if (!journal) {
      await journalStore.fetchJournalByDate(date);
      journal = journalStore.getJournalByDate(date);
    }
    currentJournal.value = journal;
  } else {
    currentJournal.value = null;
  }
  content.value = currentJournal.value?.content || '';
};

onMounted(loadJournalData);
watch(() => route.params.date, loadJournalData);

// This 'watcher' is the critical fix. It ensures that if the journal's
// content is updated in the central store (e.g., by the AI chat action),
// our local 'content' variable is also updated, which makes the UI refresh.
watch(
  () => currentJournal.value?.content,
  (newContentFromStore) => {
    if (newContentFromStore !== undefined && newContentFromStore !== content.value) {
      content.value = newContentFromStore;
    }
  }
);

const saveJournal = async () => {
  statusText.value = 'Saving...';
  let savedJournal;
  if (currentJournal.value) {
    savedJournal = await journalStore.updateJournal(currentJournal.value.journal_date, content.value);
  } else {
    savedJournal = await journalStore.createJournal(content.value);
  }
  if (savedJournal) {
    statusText.value = 'All changes saved!';
    if (!route.params.date) {
      router.push(`/writer/${savedJournal.journal_date}`);
    }
  } else {
    statusText.value = 'Error saving.';
  }
};

const getAIFeedback = async () => {
  if (!currentJournal.value) return;
  showAIFeedback.value = true; 
  await aiStore.getFeedback(currentJournal.value.journal_date, content.value);
};

const setMode = (mode) => { activeMode.value = mode; };

const modeButtonClass = (mode) => {
  const base = 'px-4 py-2 rounded-md text-sm font-semibold flex items-center gap-2';
  if (activeMode.value === mode) {
    return `${base} bg-indigo-100 text-indigo-700`;
  }
  return `${base} text-gray-600 hover:bg-gray-200`;
};

const chatHistory = computed(() => {
  if (!content.value) return [];
  const messages = [];
  const lines = content.value.split('\n\n');
  for (const line of lines) {
    if (line.startsWith('User: ')) {
      messages.push({ sender: 'User', text: line.substring(6) });
    } else if (line.startsWith('Lingo: ')) {
      messages.push({ sender: 'Lingo', text: line.substring(7) });
    }
  }
  return messages;
});

const sendMessage = async () => {
  if (!newMessage.value.trim() || !currentJournal.value || aiStore.isLoading) return;
  const messageToSend = newMessage.value;
  newMessage.value = '';
  await aiStore.chatWithAI(currentJournal.value.journal_date, messageToSend);
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

watch(chatHistory, scrollToBottom, { deep: true });
</script>


# /end of file/


# src/App.vue
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


# /end of file/


# src/main.js
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './style.css';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.mount('#app');
# /end of file/


# src/style.css
@tailwind base;
@tailwind components;
@tailwind utilities;

# /end of file/


# index.html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LingoJourn - AI Journal</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
# /end of file/