<template>
  <main id="writer-view" class="fade-in flex flex-col h-full w-full bg-white dark:bg-gray-800">

    <!-- ================================== -->
    <!--  1. NEW COMPACT & ANIMATED HEADER  -->
    <!-- ================================== -->
    <div class="flex-shrink-0 p-2 flex justify-between items-center border-b border-gray-200 dark:border-gray-700">
      <!-- Left Section: Navigation, Title, and Status -->
      <div class="flex items-center gap-2">
        <router-link to="/" title="Back to Dashboard" class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        </router-link>
        <div>
          <h2 class="text-sm font-bold text-gray-900 dark:text-gray-100 truncate">{{ currentJournal?.title || 'New Journal Entry' }}</h2>
          <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2">
            <span>{{ displayDate }}</span>
            <span class="mx-1">·</span>
            <span class="hidden sm:inline">Status: <strong>{{ statusText }}</strong></span>
          </div>
        </div>
      </div>

      <!-- Right Section: Compact Phase Indicator -->
      <div class="flex items-center">
        <template v-for="(phase, index) in phases" :key="phase.id">
          <div class="flex items-center">
            <!-- Connector Line (appears after the first item) -->
            <div v-if="index > 0" class="w-6 h-0.5 rounded transition-colors" :class="getPhaseLineClass(phase.id)"></div>
            <!-- Phase Circle with Tooltip -->
            <div class="group relative">
              <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300" :class="getPhaseClass(phase.id)">
                 <svg v-if="phase.id === 4" xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 256 256"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"></path></svg>
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

      <!-- A. Unified Layout for Scaffolding & Writing -->
      <div v-if="currentPhase === 'scaffolding' || currentPhase === 'writing'" class="h-full flex flex-col p-4 sm:p-6 gap-4">
        
        <!-- Phase Banners -->
        <div v-if="currentPhase === 'scaffolding'" class="flex-shrink-0 bg-indigo-50 dark:bg-indigo-900/50 p-4 rounded-lg">
          <h3 class="font-bold text-indigo-800 dark:text-indigo-200">Phase 1: Let's build an outline!</h3>
          <p class="text-sm text-indigo-700 dark:text-indigo-300 mt-1">Answer Lingo's questions or write your own key points below to create a plan for your journal entry.</p>
        </div>
        <div v-if="currentPhase === 'writing'" class="flex-shrink-0 bg-green-50 dark:bg-green-900/50 p-4 rounded-lg">
          <h3 class="font-bold text-green-800 dark:text-green-200">Phase 2: Write your draft</h3>
          <p class="text-sm text-green-700 dark:text-green-300 mt-1">Use your outline to write your journal entry. Your writing partner, Lingo, is here to help if you get stuck.</p>
        </div>
        
        <!-- Mobile View Switcher (Tabs) -->
        <div class="md:hidden flex-shrink-0 flex border border-gray-300 dark:border-gray-600 rounded-lg p-1 bg-gray-100 dark:bg-gray-900">
          <button @click="mobileView = 'main'" :class="[mobileView === 'main' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 dark:text-gray-300', 'flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out']">
            <span v-if="currentPhase === 'scaffolding'">📝 Outline</span>
            <span v-else>📝 Writer</span>
          </button>
          <button @click="mobileView = 'chat'" :class="[mobileView === 'chat' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 dark:text-gray-300', 'flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out']">
            🤖 Lingo Chat
          </button>
        </div>
        
        <!-- Main Grid for Desktop & Mobile content -->
        <div class="flex-grow overflow-hidden grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- Left Column: Outline / Writer -->
          <div class="flex flex-col gap-4 min-h-0" :class="{'hidden md:flex': mobileView !== 'main'}">
            <!-- Scaffolding View -->
            <template v-if="currentPhase === 'scaffolding'">
              <div class="flex-shrink-0 space-y-2 text-sm text-gray-600 dark:text-gray-300">
                <p><strong>Guiding questions:</strong></p>
                <ul class="list-disc list-inside bg-gray-50 dark:bg-gray-700/50 p-3 rounded-md">
                  <li>What was the most memorable part of your day?</li>
                  <li>Did you learn or try something new?</li>
                </ul>
              </div>
              <textarea 
                v-model="outlineContent" 
                placeholder="Write down your main ideas or key points here..." 
                class="flex-grow w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none">
              </textarea>
            </template>
            <!-- Writing View -->
            <template v-if="currentPhase === 'writing'">
              <div class="flex-shrink-0 bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border dark:border-gray-700">
                <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Outline</h4>
                <div class="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap max-h-24 overflow-y-auto custom-scrollbar">{{ outlineContent || "No outline was created."}}</div>
              </div>
              <textarea v-model="content" class="flex-grow w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"></textarea>
            </template>
          </div>
          
          <!-- Right Column: UNIFIED CHAT PANEL -->
          <div class="flex flex-col min-h-0" :class="{'hidden md:flex': mobileView !== 'chat'}">
            <div class="flex-grow w-full border border-gray-300 dark:border-gray-600 rounded-lg flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden">
              <div class="p-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between flex-shrink-0">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" class="text-indigo-500 dark:text-indigo-400" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,212.3a16,16,0,0,0,20.55,18.85l37.81-12.6A104,104,0,1,0,128,24Zm0,192a88.1,88.1,0,0,1-45.43-13.25a8,8,0,0,0-9-1.33L40,211.52l9.9-32.68a8,8,0,0,0-1.12-8.52A88,88,0,1,1,128,216Z"></path></svg>
                  <h4 class="font-semibold text-gray-800 dark:text-gray-200">Lingo Chat</h4>
                </div>
                <label for="correction-toggle" class="flex items-center cursor-pointer">
                  <span class="mr-2 text-xs text-gray-500 dark:text-gray-400">Correct</span>
                  <div class="relative">
                    <input type="checkbox" id="correction-toggle" class="sr-only" v-model="isCorrectionModeEnabled">
                    <div class="block bg-gray-200 dark:bg-gray-600 w-10 h-6 rounded-full"></div>
                    <div class="dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform"></div>
                  </div>
                </label>
              </div>
              <div ref="chatContainer" class="flex-grow p-4 overflow-y-auto space-y-4 custom-scrollbar">
                <template v-for="message in currentJournal?.chat_messages" :key="message.id">
                  <div v-if="message.message_type === 'conversation'" class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
                    <div class="p-3 rounded-lg max-w-xs break-words" :class="message.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'">
                      <p class="text-sm">{{ message.message_text }}</p>
                    </div>
                  </div>
                  <div v-else-if="message.message_type === 'feedback'" class="flex justify-start">
                    <ChatFeedbackCard :message="message" />
                  </div>
                </template>
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

      <!-- B. Standard scrolling container for other phases -->
      <div v-if="currentPhase !== 'scaffolding' && currentPhase !== 'writing'" class="absolute inset-0 h-full overflow-y-auto custom-scrollbar">
        <!-- Phase 3: Evaluation -->
        <div v-if="currentPhase === 'evaluation'" class="p-6">
          <div class="bg-rose-50 dark:bg-rose-900/50 p-4 rounded-lg mb-4">
              <h3 class="font-bold text-rose-800 dark:text-rose-200">Phase 3: Review Your Evaluation</h3>
              <p class="text-sm text-rose-700 dark:text-rose-300 mt-1">Review the AI's suggestions below to improve your grammar, vocabulary, and style. Your original text is highlighted with suggestions.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2">
                  <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Corrected Text</h4>
                  <div v-html="highlightedContent" class="w-full h-96 p-4 border border-gray-300 dark:border-gray-600 rounded-lg overflow-y-auto bg-gray-50 dark:bg-gray-700/50 whitespace-pre-wrap custom-scrollbar"></div>
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
    </div>

    <!-- ======================= -->
    <!-- 3. ACTION FOOTER        -->
    <!-- ======================= -->
    <div class="flex-shrink-0 p-4 border-t border-gray-200 dark:border-gray-700">
      <div v-if="currentPhase === 'scaffolding'" class="flex justify-end">
        <button @click="moveToPhase('writing')" class="w-full sm:w-auto bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
            Start Writing
        </button>
      </div>

      <div v-if="currentPhase === 'writing'" class="flex justify-end">
        <button @click="moveToPhase('evaluation')" class="w-full sm:w-auto bg-teal-500 text-white font-semibold px-6 py-2 rounded-lg hover:bg-teal-600 transition-colors">
            Evaluate Writing
        </button>
      </div>
      
      <div v-if="currentPhase === 'evaluation'" class="flex flex-col sm:flex-row justify-between items-center gap-4">
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
import ChatFeedbackCard from '../components/ChatFeedbackCard.vue';

const route = useRoute();
const router = useRouter();
const journalStore = useJournalStore();
const aiStore = useAiStore();

const currentJournal = computed(() => journalStore.getJournalByDate(route.params.date));
const currentPhase = computed(() => currentJournal.value?.writing_phase || 'scaffolding');

const mobileView = ref('main'); // Can be 'main' or 'chat'
const isCorrectionModeEnabled = ref(true);

const content = ref('');
const outlineContent = ref('');
const statusText = ref('Saved');
const newMessage = ref('');
const chatContainer = ref(null);
const appliedSuggestions = ref([]);

const phases = ref([
    { id: 1, name: 'Scaffolding' },
    { id: 2, name: 'Writing' },
    { id: 3, name: 'Evaluation' },
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
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

watch(
  currentJournal,
  (newJournal) => {
    if (newJournal) {
      content.value = newJournal.content || '';
      outlineContent.value = newJournal.outline_content || '';
      appliedSuggestions.value = []; 
      
      if(newJournal.writing_phase === 'evaluation' && (!aiStore.feedback.length || aiStore.error)) {
        aiStore.getFeedback(newJournal.journal_date, newJournal.content);
      }
      scrollToBottom();
    }
  },
  { deep: true, immediate: true }
);

watch(() => currentJournal.value?.chat_messages, () => {
    scrollToBottom();
}, { deep: true });

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
    await saveJournal();
    await journalStore.updateJournalPhase(currentJournal.value.journal_date, phase);
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !currentJournal.value || aiStore.isLoading) return;
  
  await saveJournal(false);

  const messageToSend = newMessage.value;
  newMessage.value = '';

  aiStore.chatWithAI(
    currentJournal.value.journal_date,
    messageToSend,
    isCorrectionModeEnabled.value
  );
};

const highlightedContent = computed(() => {
    if (currentPhase.value !== 'evaluation' || !aiStore.feedback.length) {
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

const phaseMap = { scaffolding: 1, writing: 2, evaluation: 3, completed: 4 };

const getPhaseClass = (phaseId) => {
    const phaseValue = phaseMap[currentPhase.value];
    if (phaseValue > phaseId) return 'bg-green-500 text-white scale-100';
    if (phaseValue === phaseId) return 'bg-indigo-600 text-white scale-110 shadow-lg';
    return 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 scale-100';
};

const getPhaseLineClass = (phaseId) => {
    if (phaseMap[currentPhase.value] >= phaseId) return 'bg-green-500';
    return 'bg-gray-200 dark:bg-gray-700';
};

</script>

<style>
/* Styles for the correction toggle switch */
#correction-toggle:checked ~ .dot {
  transform: translateX(100%);
  background-color: #4f46e5; /* indigo-600 */
}
#correction-toggle:checked ~ .block {
    background-color: #c7d2fe; /* indigo-200 */
}
.dark #correction-toggle:checked ~ .block {
    background-color: #3730a3; /* indigo-800 */
}
</style>
