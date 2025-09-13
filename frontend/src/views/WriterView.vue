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
                   <!-- Iterate over the new chat_messages array -->
                   <div v-for="message in currentJournal?.chat_messages" :key="message.id" class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
                      <!-- Standard Conversation Bubble -->
                      <div v-if="message.message_type === 'conversation'" class="p-3 rounded-lg max-w-xs break-words" :class="message.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200'">
                         <p class="text-sm">{{ message.message_text }}</p>
                      </div>
                      <!-- Feedback Card -->
                      <ChatFeedbackCard v-else-if="message.message_type === 'feedback'" :message="message" />
                   </div>
                   <!-- Loading Indicator -->
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
import ChatFeedbackCard from '../components/ChatFeedbackCard.vue';

const route = useRoute();
const router = useRouter();
const journalStore = useJournalStore();
const aiStore = useAiStore();

// CHANGED: currentJournal is now a computed property for full reactivity.
const currentJournal = computed(() => journalStore.getJournalByDate(route.params.date));

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

// REWORKED: This function now only ensures the data is present in the store.
const loadJournalData = async () => {
  const date = route.params.date;
  if (date && !currentJournal.value) { // Check the computed property
    await journalStore.fetchJournalByDate(date);
  }
};

onMounted(loadJournalData);
watch(() => route.params.date, loadJournalData);

// ADDED: This watcher syncs local state and handles side effects like scrolling.
const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

watch(
  currentJournal,
  (newJournal, oldJournal) => {
    // Sync the textarea content when the journal changes.
    content.value = newJournal?.content || '';

    // Scroll chat to the bottom if the number of messages has changed.
    if (newJournal?.chat_messages?.length !== oldJournal?.chat_messages?.length) {
        scrollToBottom();
    }
  },
  { deep: true, immediate: true }
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

const sendMessage = async () => {
  if (!newMessage.value.trim() || !currentJournal.value || aiStore.isLoading) return;
  const messageToSend = newMessage.value;
  newMessage.value = '';

  // --- FIX: Ensure auto-scrolling on optimistic update ---
  // The chatWithAI action performs an optimistic update synchronously at the beginning.
  // By not awaiting the promise immediately, we allow the optimistic UI update to render.
  const chatPromise = aiStore.chatWithAI(currentJournal.value.journal_date, messageToSend);

  // We then manually trigger scrollToBottom. It uses nextTick, which waits for the DOM 
  // to be updated with the new optimistic message before scrolling.
  scrollToBottom();

  // Finally, we await the promise to ensure the full round trip (including the AI's response)
  // completes. The watcher will handle the scroll after the AI response is fetched.
  await chatPromise;
};
</script>

