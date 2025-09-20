<template>
  <main id="writer-view" class="fade-in flex flex-col h-full w-full bg-white dark:bg-gray-800">

    <!-- ================================== -->
    <!--  1. NEW COMPACT & ANIMATED HEADER  -->
    <!-- ================================== -->
    <div class="flex-shrink-0 p-3 flex justify-between items-center border-b border-gray-200 dark:border-gray-700">
      <!-- Left Section: Navigation, Title, and Status -->
      <div class="flex items-center gap-3">
        <router-link to="/" title="Back to Dashboard" class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        </router-link>
        <div>
          <h2 class="text-md font-bold text-gray-900 dark:text-gray-100 truncate">{{ currentJournal?.title || 'New Journal Entry' }}</h2>
          <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center">
            <span>{{ displayDate }}</span>
            <span class="mx-2">·</span>
            <span>Status: <strong>{{ statusText }}</strong></span>
          </div>
        </div>
      </div>

      <!-- Right Section: Compact Phase Indicator -->
      <div class="flex items-center">
        <template v-for="(phase, index) in phases" :key="phase.id">
          <div class="flex items-center">
            <!-- Connector Line (appears after the first item) -->
            <div v-if="index > 0" class="w-8 h-1 rounded transition-colors" :class="getPhaseLineClass(phase.id)"></div>
            <!-- Phase Circle with Tooltip -->
            <div class="group relative">
              <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300" :class="getPhaseClass(phase.id)">
                 <svg v-if="phase.id === 4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"></path></svg>
                 <span v-else>{{ phase.id }}</span>
              </div>
              <span class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-max opacity-0 group-hover:opacity-100 transition-opacity bg-gray-800 text-white text-xs font-semibold rounded-md py-1 px-2 pointer-events-none z-10">
                {{ phase.name }}
              </span>
            </div>
          </div>
        </template>
      </div>
    </div>


    <!-- ======================= -->
    <!--   2. MAIN CONTENT AREA  -->
    <!-- ======================= -->
    <div class="flex-grow overflow-hidden relative">

      <!-- A. Standard scrolling container for most phases -->
      <div v-if="currentPhase !== 'writing'" class="absolute inset-0 h-full overflow-y-auto">
        <!-- Phase 1: Scaffolding -->
        <div v-if="currentPhase === 'scaffolding'" class="p-6">
          <div class="bg-indigo-50 dark:bg-indigo-900/50 p-4 rounded-lg mb-4">
              <h3 class="font-bold text-indigo-800 dark:text-indigo-200">Phase 1: Let's build an outline!</h3>
              <p class="text-sm text-indigo-700 dark:text-indigo-300 mt-1">Answer the questions, chat with the AI, or write your own key points below. The goal is to create a simple plan for your journal entry.</p>
          </div>
          <div class="mb-4 space-y-2 text-sm text-gray-600 dark:text-gray-300">
              <p><strong>Guiding questions:</strong></p>
              <ul class="list-disc list-inside bg-gray-50 dark:bg-gray-700/50 p-3 rounded-md">
                  <li>What was the most memorable part of your day?</li>
                  <li>Did you learn or try something new?</li>
                  <li>How are you feeling right now?</li>
              </ul>
          </div>
          <textarea 
            v-model="outlineContent" 
            placeholder="Write down your main ideas or key points here..." 
            class="w-full h-48 p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
          </textarea>
        </div>
        
        <!-- Scaffolding Chat -->
        <div v-show="isChatActive && currentPhase === 'scaffolding'" class="p-6 border-t border-gray-200 dark:border-gray-700">
            <div class="w-full h-96 border border-gray-300 dark:border-gray-600 rounded-lg flex flex-col bg-gray-50 dark:bg-gray-900">
            <div ref="scaffoldingChatContainer" class="flex-grow p-4 overflow-y-auto space-y-4">
                <div v-for="message in currentJournal?.chat_messages" :key="message.id" class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
                <div v-if="message.message_type === 'conversation'" class="p-3 rounded-lg max-w-xs break-words" :class="message.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'">
                    <p class="text-sm">{{ message.message_text }}</p>
                </div>
                </div>
                <div v-if="aiStore.isLoading" class="flex justify-start">
                    <div class="bg-gray-200 dark:bg-gray-700 p-3 rounded-lg animate-pulse">
                        <p class="text-sm text-gray-400">...</p>
                    </div>
                </div>
            </div>
            <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <input v-model="newMessage" @keyup.enter="sendMessage" :disabled="aiStore.isLoading || !currentJournal" type="text" :placeholder="chatPlaceholder" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none disabled:bg-gray-100 dark:disabled:bg-gray-700 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
            </div>
            </div>
        </div>

        <!-- Phase 3: Finishing -->
        <div v-if="currentPhase === 'finishing'" class="p-6">
          <div class="bg-rose-50 dark:bg-rose-900/50 p-4 rounded-lg mb-4">
              <h3 class="font-bold text-rose-800 dark:text-rose-200">Phase 3: Polish your writing</h3>
              <p class="text-sm text-rose-700 dark:text-rose-300 mt-1">Review the AI's suggestions below to improve your grammar, vocabulary, and style. Your original text is highlighted with suggestions.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2">
                  <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Corrected Text</h4>
                  <div v-html="highlightedContent" class="w-full h-96 p-4 border border-gray-300 dark:border-gray-600 rounded-lg overflow-y-auto bg-gray-50 dark:bg-gray-700/50 whitespace-pre-wrap"></div>
              </div>
              <div class="md:col-span-1">
                  <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Suggestions</h4>
                  <div id="ai-feedback-section" class="space-y-3">
                      <div v-if="aiStore.isLoading" class="text-center py-4">
                          <p class="text-gray-500 dark:text-gray-400 animate-pulse">Analyzing your text...</p>
                      </div>
                      <div v-else-if="aiStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
                          <p>{{ aiStore.error }}</p>
                      </div>
                      <div v-else-if="aiStore.feedback.length > 0">
                          <AIFeedbackCard 
                              v-for="(item, index) in aiStore.feedback"
                              :key="index"
                              :feedback-item="item"
                              :is-applied="appliedSuggestions.includes(item.incorrect_phrase)"
                              @apply-suggestion="applySuggestion"
                          />
                      </div>
                      <div v-else class="text-center py-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                          <p class="text-gray-600 dark:text-gray-300 font-semibold">Great job!</p>
                          <p class="text-gray-500 dark:text-gray-400">The AI didn't find any specific errors to correct.</p>
                      </div>
                  </div>
              </div>
          </div>
        </div>
        
        <!-- Phase 4: Completed -->
        <div v-if="currentPhase === 'completed'" class="p-6 text-center">
          <div class="max-w-md mx-auto">
            <div class="bg-green-100 text-green-700 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
              <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 256 256"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"></path></svg>
            </div>
            <h3 class="text-2xl font-bold mt-4 text-gray-900 dark:text-gray-100">Journal Completed!</h3>
            <p class="text-gray-600 dark:text-gray-400 mt-2">Excellent work! You've finished this entry. All your learning points have been saved to your progress hub.</p>
            <div class="mt-6">
              <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg border dark:border-gray-700 text-left">
                  <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Final Entry</h4>
                  <div class="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">{{ content }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- B. Special non-scrolling layout for Writing Phase -->
      <div v-if="currentPhase === 'writing'" class="h-full flex flex-col p-6 gap-4">
        <!-- Banner -->
        <div class="flex-shrink-0 bg-green-50 dark:bg-green-900/50 p-4 rounded-lg">
            <h3 class="font-bold text-green-800 dark:text-green-200">Phase 2: Write your draft</h3>
            <p class="text-sm text-green-700 dark:text-green-300 mt-1">Use your outline to write your journal entry. Your writing partner, Lingo, is here to help if you get stuck.</p>
        </div>
        
        <!-- Mobile View Switcher -->
        <div class="md:hidden flex-shrink-0 flex border border-gray-300 dark:border-gray-600 rounded-lg p-1 bg-gray-100 dark:bg-gray-900">
            <button @click="mobileView = 'writer'" :class="[mobileView === 'writer' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 dark:text-gray-300', 'flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out']">📝 Writer</button>
            <button @click="mobileView = 'partner'" :class="[mobileView === 'partner' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 dark:text-gray-300', 'flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out']">🤖 Partner</button>
        </div>
        
        <!-- Main Grid for Desktop -->
        <div class="flex-grow overflow-hidden grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Left Column: Outline + Writer -->
          <div class="flex flex-col gap-4 min-h-0" :class="{'hidden md:flex': mobileView !== 'writer'}">
            <!-- Outline Section -->
            <div class="flex-shrink-0 bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border dark:border-gray-700">
                <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Outline</h4>
                <div class="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap max-h-24 overflow-y-auto">{{ outlineContent || "No outline was created."}}</div>
            </div>
            <!-- Writing Area -->
            <textarea v-model="content" class="flex-grow w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"></textarea>
          </div>
          
          <!-- Right Column: Partner Sidebar -->
          <div class="flex flex-col min-h-0" :class="{'hidden md:flex': mobileView !== 'partner'}">
            <!-- Chat Section (takes full height of this column) -->
            <div class="flex-grow w-full border border-gray-300 dark:border-gray-600 rounded-lg flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden">
                <div class="p-3 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2 flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" class="text-indigo-500 dark:text-indigo-400" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,212.3a16,16,0,0,0,20.55,18.85l37.81-12.6A104,104,0,1,0,128,24Zm0,192a88.1,88.1,0,0,1-45.43-13.25a8,8,0,0,0-9-1.33L40,211.52l9.9-32.68a8,8,0,0,0-1.12-8.52A88,88,0,1,1,128,216Z"></path></svg>
                    <h4 class="font-semibold text-gray-800 dark:text-gray-200">Writing Partner</h4>
                </div>
                <div ref="chatContainer" class="flex-grow p-4 overflow-y-auto space-y-4">
                    <!-- Chat Messages -->
                      <div v-for="message in currentJournal?.chat_messages" :key="message.id" class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
                        <div v-if="message.message_type === 'conversation'" class="p-3 rounded-lg max-w-xs break-words" :class="message.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'">
                            <p class="text-sm">{{ message.message_text }}</p>
                        </div>
                      </div>
                      <div v-if="aiStore.isLoading" class="flex justify-start">
                          <div class="bg-gray-200 dark:bg-gray-700 p-3 rounded-lg animate-pulse">
                              <p class="text-sm text-gray-400">...</p>
                          </div>
                      </div>
                </div>
                <div class="p-2 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 flex-shrink-0">
                    <input v-model="newMessage" @keyup.enter="sendMessage" :disabled="aiStore.isLoading || !currentJournal" type="text" :placeholder="chatPlaceholder" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none disabled:bg-gray-100 dark:disabled:bg-gray-700 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ======================= -->
    <!-- 3. NON-SCROLLABLE BOTTOM -->
    <!-- ======================= -->
    <div class="flex-shrink-0 p-4 border-t border-gray-200 dark:border-gray-700">
      <!-- Hoisted Buttons -->
      <div v-if="currentPhase === 'scaffolding'" class="flex flex-col sm:flex-row gap-4">
        <button @click="toggleChatMode" class="w-full sm:w-auto flex-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 font-semibold px-4 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,212.3a16,16,0,0,0,20.55,18.85l37.81-12.6A104,104,0,1,0,128,24Zm0,192a88.1,88.1,0,0,1-45.43-13.25a8,8,0,0,0-9-1.33L40,211.52l9.9-32.68a8,8,0,0,0-1.12-8.52A88,88,0,1,1,128,216Z"></path></svg>
            Chat with Lingo
        </button>
        <button @click="moveToPhase('writing')" class="w-full sm:w-auto flex-1 bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
            Start Writing
        </button>
      </div>

      <div v-if="currentPhase === 'writing'" class="flex justify-end">
        <button @click="moveToPhase('finishing')" class="w-full sm:w-auto bg-teal-500 text-white font-semibold px-6 py-2 rounded-lg hover:bg-teal-600 transition-colors">
            Finish & Get Final Feedback
        </button>
      </div>
      
      <div v-if="currentPhase === 'finishing'" class="flex flex-col sm:flex-row justify-between items-center gap-4">
         <button @click="saveJournal()" :disabled="journalStore.isLoading" class="w-full sm:w-auto bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">
            {{ journalStore.isLoading ? 'Saving...' : 'Save Changes' }}
        </button>
        <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <button @click="moveToPhase('writing')" class="w-full sm:w-auto bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">
                Back to Writing
            </button>
            <button 
                @click="moveToPhase('completed')"
                :disabled="!allSuggestionsApplied" 
                class="w-full sm:w-auto bg-green-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400 dark:disabled:bg-gray-600 disabled:cursor-not-allowed">
                Mark as Complete
            </button>
        </div>
      </div>
      
      <div v-if="currentPhase === 'completed'" class="flex justify-center gap-4">
          <router-link to="/" class="bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
            Back to Dashboard
        </router-link>
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

const currentJournal = computed(() => journalStore.getJournalByDate(route.params.date));
const currentPhase = computed(() => currentJournal.value?.writing_phase || 'scaffolding');

// New state for mobile tab view
const mobileView = ref('writer'); // 'writer' or 'partner'

const content = ref('');
const outlineContent = ref('');
const statusText = ref('Saved');
const newMessage = ref('');
const chatContainer = ref(null); // For writing phase chat
const scaffoldingChatContainer = ref(null); // For scaffolding phase chat
const isChatActive = ref(false); // Only for scaffolding now
const appliedSuggestions = ref([]);
const phases = ref([
    { id: 1, name: 'Scaffolding' },
    { id: 2, name: 'Writing' },
    { id: 3, name: 'Finishing' },
    { id: 4, name: 'Completed' },
]);

const displayDate = computed(() => {
  if (currentJournal.value) {
    return journalStore.formatDisplayDate(currentJournal.value.journal_date);
  }
  return format(new Date(), 'MMMM d, yyyy');
});

const chatPlaceholder = computed(() => {
    if (currentPhase.value === 'scaffolding') {
        return 'Not sure what to write about? Chat here!';
    }
    if (currentPhase.value === 'writing') {
        return "Ask for help, e.g., 'What should I write next?'";
    }
    return 'Type your message...';
});

const loadJournalData = async () => {
  const date = route.params.date;
  if (date) {
    await journalStore.fetchJournalByDate(date);
  } else {
    const today = format(new Date(), 'yyyy-MM-dd');
    const existing = journalStore.getJournalByDate(today);
    if (!existing) {
        const newJournal = await journalStore.createJournal('');
        if (newJournal) {
            router.replace(`/writer/${newJournal.journal_date}`);
        }
    } else {
       router.replace(`/writer/${today}`);
    }
  }
};

onMounted(loadJournalData);

const scrollToBottom = () => {
  nextTick(() => {
    const container = currentPhase.value === 'writing' ? chatContainer.value : scaffoldingChatContainer.value;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
};

watch(
  currentJournal,
  (newJournal) => {
    if (newJournal) {
      content.value = newJournal.content || '';
      outlineContent.value = newJournal.outline_content || '';
      appliedSuggestions.value = []; // Reset when journal changes
      
      if(newJournal.writing_phase === 'finishing' && (!aiStore.feedback.length || aiStore.error)) {
        aiStore.getFeedback(newJournal.journal_date, newJournal.content);
      }
    }
  },
  { deep: true, immediate: true }
);

watch(() => currentJournal.value?.chat_messages, () => {
    scrollToBottom();
}, { deep: true });

// Auto-save content changes during the writing phase
watch(content, (newValue, oldValue) => {
    if (currentPhase.value === 'writing' && newValue !== oldValue) {
        saveJournal();
    }
});

const saveJournal = async (showStatus = true) => {
  if (!currentJournal.value) return;
  if (showStatus) statusText.value = 'Saving...';
  const payload = {
    content: content.value,
    outline_content: outlineContent.value,
  };
  const savedJournal = await journalStore.updateJournal(currentJournal.value.journal_date, payload);
  
  if (showStatus) statusText.value = savedJournal ? 'All changes saved!' : 'Error saving.';
};

const moveToPhase = async (phase) => {
    if (!currentJournal.value) return;
    isChatActive.value = false; // Close chat when moving phase
    await saveJournal();
    await journalStore.updateJournalPhase(currentJournal.value.journal_date, phase);
};

const toggleChatMode = () => {
    isChatActive.value = !isChatActive.value;
    if(isChatActive.value) {
        scrollToBottom();
    }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !currentJournal.value || aiStore.isLoading) return;
  // Save journal before sending to give AI the latest context
  if (currentPhase.value === 'scaffolding' || currentPhase.value === 'writing') {
    await saveJournal(false);
  }

  const messageToSend = newMessage.value;
  newMessage.value = '';
  await aiStore.chatWithAI(currentJournal.value.journal_date, messageToSend);
};

// --- Phase 3 Logic ---
const highlightedContent = computed(() => {
    if (currentPhase.value !== 'finishing' || !aiStore.feedback.length) {
        return content.value;
    }
    
    let tempContent = content.value;
    
    const sortedFeedback = [...aiStore.feedback].sort((a, b) => b.incorrect_phrase.length - a.incorrect_phrase.length);

    sortedFeedback.forEach(item => {
        if (!appliedSuggestions.value.includes(item.incorrect_phrase)) {
            const regex = new RegExp(escapeRegExp(item.incorrect_phrase), 'g');
            tempContent = tempContent.replace(regex, `<span class="bg-yellow-200 dark:bg-yellow-400/30 rounded px-1">${item.incorrect_phrase}</span>`);
        }
    });
    return tempContent;
});

const applySuggestion = (feedbackItem) => {
    content.value = content.value.replace(feedbackItem.incorrect_phrase, feedbackItem.suggestion);
    appliedSuggestions.value.push(feedbackItem.incorrect_phrase);
};

const allSuggestionsApplied = computed(() => {
    if (!aiStore.feedback || aiStore.feedback.length === 0) return true;
    return appliedSuggestions.value.length >= aiStore.feedback.length;
});

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const phaseMap = { scaffolding: 1, writing: 2, finishing: 3, completed: 4 };

const isPhaseActive = (phaseId) => phaseMap[currentPhase.value] >= phaseId;

const getPhaseClass = (phaseId) => {
    const phaseValue = phaseMap[currentPhase.value];
    if (phaseValue > phaseId) return 'bg-green-500 text-white scale-100'; // Completed
    if (phaseValue === phaseId) return 'bg-indigo-600 text-white scale-110 shadow-lg'; // Active
    return 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 scale-100'; // Inactive
};

const getPhaseLineClass = (phaseId) => {
    if (phaseMap[currentPhase.value] >= phaseId) return 'bg-green-500'; // Completed line
    return 'bg-gray-200 dark:bg-gray-700'; // Inactive line
};

</script>
