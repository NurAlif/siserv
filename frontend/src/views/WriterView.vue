<template>
  <main id="writer-view" class="fade-in">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <router-link to="/" class="text-gray-500 hover:text-gray-800 font-medium flex items-center gap-2">
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

      <!-- Loading State -->
       <div v-if="journalStore.isLoading && !content" class="p-6 text-center text-gray-500">
        Loading journal...
      </div>
      
      <!-- Editor & Chat Content -->
      <div v-else>
        <!-- Editor mode UI -->
           <div v-show="activeMode === 'editor'" class="p-6">
            <textarea
              v-model="content"
              class="w-full h-96 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"
              placeholder="Start writing your journal here..."
            ></textarea>
          </div>

          <!-- Chat Mode UI -->
          <div v-show="activeMode === 'chat'" id="chat-content" class="p-6">
             <div class="w-full h-96 border border-gray-300 rounded-lg flex flex-col bg-gray-50">
                <div ref="chatContainer" class="flex-grow p-4 overflow-y-auto space-y-4">
                  <!-- Chat Messages will be rendered here -->
                   <div v-for="(message, index) in chatHistory" :key="index" class="flex" :class="message.sender === 'User' ? 'justify-end' : 'justify-start'">
                      <div class="p-3 rounded-lg max-w-xs" :class="message.sender === 'User' ? 'bg-indigo-500 text-white' : 'bg-gray-200'">
                         <p class="text-sm">{{ message.text }}</p>
                      </div>
                   </div>
                   <div v-if="aiStore.isLoading" class="flex justify-start">
                        <div class="bg-gray-200 p-3 rounded-lg animate-pulse">
                            <p class="text-sm text-transparent">...</p>
                        </div>
                   </div>
                </div>
                <div class="p-4 border-t border-gray-200 bg-white">
                  <input 
                    v-model="newMessage"
                    @keyup.enter="sendMessage"
                    :disabled="aiStore.isLoading"
                    type="text" 
                    placeholder="Type your message..." 
                    class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none disabled:bg-gray-100"
                  >
                </div>
              </div>
          </div>
      </div>

      <!-- Action Buttons -->
      <div class="p-6 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center gap-4">
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
        
        <!-- Loading State for AI Feedback -->
        <div v-if="aiStore.isLoading" class="text-center py-4">
            <p class="text-gray-500 animate-pulse">Analyzing your text...</p>
        </div>
        
        <!-- Error State for AI Feedback -->
        <div v-else-if="aiStore.error" class="bg-red-50 text-red-700 p-4 rounded-lg">
            <p>{{ aiStore.error }}</p>
        </div>

        <!-- Feedback Results -->
        <div v-else-if="aiStore.feedback.length > 0" class="space-y-4">
            <AIFeedbackCard 
                v-for="(item, index) in aiStore.feedback"
                :key="index"
                :feedback-item="item"
            />
        </div>

        <!-- No feedback/errors found -->
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
import { useAiStore } from '../stores/aiStore'; // Import the new AI store
import { format } from 'date-fns';
import AIFeedbackCard from '../components/AIFeedbackCard.vue'; // Import the new component

const route = useRoute();
const router = useRouter();
const journalStore = useJournalStore();
const aiStore = useAiStore(); // Initialize the AI store

const currentJournal = ref(null);
const content = ref('');
const statusText = ref('Saved');
const activeMode = ref('editor');
const showAIFeedback = ref(false);
const newMessage = ref('');
const chatContainer = ref(null);

const displayDate = computed(() => {
    if (currentJournal.value?.journal_date) {
        return journalStore.formatDisplayDate(currentJournal.value.journal_date);
    }
    return format(new Date(), 'MMMM d, yyyy');
});

const loadJournalData = async () => {
    const dateParam = route.params.date;
    if (dateParam) {
        const journal = await journalStore.fetchJournalByDate(dateParam);
        currentJournal.value = journal;
        content.value = journal?.content || '';
    } else {
        // This is a new entry
        currentJournal.value = null;
        content.value = '';
    }
};

onMounted(loadJournalData);
watch(() => route.params.date, loadJournalData);

const saveJournal = async () => {
  statusText.value = 'Saving...';
  let savedJournal;

  if (currentJournal.value) {
    // It's an existing journal, so update it
    savedJournal = await journalStore.updateJournal(currentJournal.value.journal_date, content.value);
  } else {
    // It's a new journal, so create it
    savedJournal = await journalStore.createJournal(content.value);
  }

  if (savedJournal) {
    statusText.value = 'All changes saved!';
    // If it was a new journal, we need to navigate to its new, permanent URL
    if (!currentJournal.value) {
      router.push(`/writer/${savedJournal.journal_date}`);
    }
  } else {
    statusText.value = 'Error saving.';
  }
};

// --- New Function to Get AI Feedback ---
const getAIFeedback = async () => {
  if (!currentJournal.value) return;
  
  // Show the feedback section so the user can see the loading state
  showAIFeedback.value = true; 
  
  // Call the action from the AI store
  await aiStore.getFeedback(currentJournal.value.journal_date, content.value);
};

const setMode = (mode) => {
  activeMode.value = mode;
};

const modeButtonClass = (mode) => {
  const base = 'px-4 py-2 rounded-md text-sm font-semibold flex items-center gap-2';
  if (activeMode.value === mode) {
    return `${base} bg-indigo-100 text-indigo-700`;
  }
  return `${base} text-gray-600 hover:bg-gray-200`;
};

// New Computed Property to parse the journal content into a chat history
const chatHistory = computed(() => {
  if (!content.value) return [];
  
  const messages = [];
  const lines = content.value.split('\n\n'); // Split by double newline
  
  for (const line of lines) {
    if (line.startsWith('User: ')) {
      messages.push({ sender: 'User', text: line.substring(6) });
    } else if (line.startsWith('Lingo: ')) {
      messages.push({ sender: 'Lingo', text: line.substring(7) });
    }
  }
  return messages;
});


// New Function to send a chat message
const sendMessage = async () => {
  if (!newMessage.value.trim() || !currentJournal.value || aiStore.isLoading) return;

  const messageToSend = newMessage.value;
  newMessage.value = ''; // Clear input immediately
  
  await aiStore.chatWithAI(currentJournal.value.journal_date, messageToSend);
};


// New Function to scroll chat to the bottom
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

// Watch for changes in chat history and content to auto-scroll
watch(chatHistory, () => {
  nextTick(scrollToBottom);
});

watch(content, () => {
    // This ensures that when switching to chat mode, the content is scrolled
    if(activeMode.value === 'chat'){
        nextTick(scrollToBottom);
    }
});

</script>

