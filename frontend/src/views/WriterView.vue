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

      <!-- Phase Indicator -->
      <div class="p-4 bg-gray-50 border-b border-gray-200">
        <div class="flex items-center justify-between max-w-md mx-auto">
          <div v-for="phase in phases" :key="phase.id" class="flex items-center" :class="{'flex-1': phase.id < 3}">
            <div class="flex flex-col items-center">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold" :class="getPhaseClass(phase.id)">
                {{ phase.id }}
              </div>
              <p class="text-xs mt-1 font-semibold" :class="{'text-indigo-600': isPhaseActive(phase.id), 'text-gray-500': !isPhaseActive(phase.id)}">{{ phase.name }}</p>
            </div>
            <div v-if="phase.id < 3" class="flex-1 h-1 mx-2 rounded" :class="getPhaseLineClass(phase.id)"></div>
          </div>
        </div>
      </div>
      
      <!-- Phase 1: Scaffolding -->
      <div v-if="currentPhase === 'scaffolding'" class="p-6">
        <div class="bg-indigo-50 p-4 rounded-lg mb-4">
            <h3 class="font-bold text-indigo-800">Phase 1: Let's build an outline!</h3>
            <p class="text-sm text-indigo-700 mt-1">Answer the questions, chat with the AI, or write your own key points below. The goal is to create a simple plan for your journal entry.</p>
        </div>
        <div class="mb-4 space-y-2 text-sm text-gray-600">
            <p><strong>Guiding questions:</strong></p>
            <ul class="list-disc list-inside bg-gray-50 p-3 rounded-md">
                <li>What was the most memorable part of your day?</li>
                <li>Did you learn or try something new?</li>
                <li>How are you feeling right now?</li>
            </ul>
        </div>
        <textarea 
            v-model="outlineContent" 
            placeholder="Write down your main ideas or key points here..." 
            class="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition">
        </textarea>
        <div class="mt-4 flex flex-col sm:flex-row gap-4">
            <button @click="toggleChatMode" class="w-full sm:w-auto flex-1 bg-gray-100 text-gray-800 font-semibold px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,212.3a16,16,0,0,0,20.55,18.85l37.81-12.6A104,104,0,1,0,128,24Zm0,192a88.1,88.1,0,0,1-45.43-13.25a8,8,0,0,0-9-1.33L40,211.52l9.9-32.68a8,8,0,0,0-1.12-8.52A88,88,0,1,1,128,216Z"></path></svg>
                Chat with Lingo to Find a Topic
            </button>
            <button @click="moveToPhase('writing')" class="w-full sm:w-auto flex-1 bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                Start Writing
            </button>
        </div>
      </div>

      <!-- Phase 2: Writing -->
      <div v-if="currentPhase === 'writing'" class="p-6">
        <div class="bg-green-50 p-4 rounded-lg mb-4">
            <h3 class="font-bold text-green-800">Phase 2: Write your draft</h3>
            <p class="text-sm text-green-700 mt-1">Now, expand on your outline. Don't worry about perfection, just focus on telling your story and getting your ideas down.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-2">
                <textarea v-model="content" class="w-full h-96 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"></textarea>
            </div>
            <div class="md:col-span-1 bg-gray-50 p-4 rounded-lg border">
                <h4 class="font-semibold text-gray-700 mb-2">Your Outline</h4>
                <div class="text-sm text-gray-600 whitespace-pre-wrap">{{ outlineContent || "No outline was created."}}</div>
            </div>
        </div>
        <div class="mt-4 flex flex-col sm:flex-row justify-between items-center gap-4">
             <button @click="toggleChatMode" class="w-full sm:w-auto bg-gray-100 text-gray-800 font-semibold px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,212.3a16,16,0,0,0,20.55,18.85l37.81-12.6A104,104,0,1,0,128,24Zm0,192a88.1,88.1,0,0,1-45.43-13.25a8,8,0,0,0-9-1.33L40,211.52l9.9-32.68a8,8,0,0,0-1.12-8.52A88,88,0,1,1,128,216Z"></path></svg>
                Ask Lingo for Help
            </button>
            <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
                 <button disabled class="w-full sm:w-auto bg-gray-200 text-gray-500 font-semibold px-4 py-2 rounded-lg cursor-not-allowed">
                    Get High-Level Feedback
                </button>
                <button @click="moveToPhase('finishing')" class="w-full sm:w-auto bg-teal-500 text-white font-semibold px-6 py-2 rounded-lg hover:bg-teal-600 transition-colors">
                    Finish & Get Final Feedback
                </button>
            </div>
        </div>
      </div>

      <!-- Phase 3: Finishing -->
      <div v-if="currentPhase === 'finishing'" class="p-6">
         <div class="bg-rose-50 p-4 rounded-lg mb-4">
            <h3 class="font-bold text-rose-800">Phase 3: Polish your writing</h3>
            <p class="text-sm text-rose-700 mt-1">Review the AI's suggestions below to improve your grammar, vocabulary, and style. Your original text is highlighted with suggestions.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-2">
                <h4 class="font-semibold text-gray-700 mb-2">Your Corrected Text</h4>
                <div v-html="highlightedContent" class="w-full h-96 p-4 border border-gray-300 rounded-lg overflow-y-auto bg-gray-50 whitespace-pre-wrap"></div>
            </div>
            <div class="md:col-span-1">
                 <h4 class="font-semibold text-gray-700 mb-2">Suggestions</h4>
                <div id="ai-feedback-section" class="space-y-3">
                    <div v-if="aiStore.isLoading" class="text-center py-4">
                        <p class="text-gray-500 animate-pulse">Analyzing your text...</p>
                    </div>
                    <div v-else-if="aiStore.error" class="bg-red-50 text-red-700 p-4 rounded-lg">
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
                    <div v-else class="text-center py-4 bg-gray-50 rounded-lg">
                        <p class="text-gray-600 font-semibold">Great job!</p>
                        <p class="text-gray-500">The AI didn't find any specific errors to correct.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-6 pt-4 border-t flex flex-col sm:flex-row justify-between items-center gap-4">
            <button @click="moveToPhase('writing')" class="w-full sm:w-auto bg-gray-200 text-gray-800 font-semibold px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors">
                Back to Writing
            </button>
            <button 
                @click="handleCompletion"
                :disabled="!allSuggestionsApplied" 
                class="w-full sm:w-auto bg-green-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed">
                Mark as Complete
            </button>
        </div>
      </div>

       <div v-show="isChatActive" class="p-6 border-t border-gray-200">
         <div class="w-full h-96 border border-gray-300 rounded-lg flex flex-col bg-gray-50">
            <div ref="chatContainer" class="flex-grow p-4 overflow-y-auto space-y-4">
               <div v-for="message in currentJournal?.chat_messages" :key="message.id" class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
                  <div v-if="message.message_type === 'conversation'" class="p-3 rounded-lg max-w-xs break-words" :class="message.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200'">
                     <p class="text-sm">{{ message.message_text }}</p>
                  </div>
                  <ChatFeedbackCard v-else-if="message.message_type === 'feedback'" :message="message" />
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

      <div class="p-6 border-t border-gray-200 flex justify-end">
        <button @click="saveJournal" :disabled="journalStore.isLoading" class="bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300 transition-colors">
            {{ journalStore.isLoading ? 'Saving...' : 'Save Changes' }}
        </button>
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

const content = ref('');
const outlineContent = ref('');
const statusText = ref('Saved');
const newMessage = ref('');
const chatContainer = ref(null);
const isChatActive = ref(false);
const appliedSuggestions = ref([]);

const phases = ref([
    { id: 1, name: 'Scaffolding' },
    { id: 2, name: 'Writing' },
    { id: 3, name: 'Finishing' },
]);

const displayDate = computed(() => {
  if (currentJournal.value) {
    return journalStore.formatDisplayDate(currentJournal.value.journal_date);
  }
  return format(new Date(), 'MMMM d, yyyy');
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
      appliedSuggestions.value = []; // Reset when journal changes
      
      if(newJournal.writing_phase === 'finishing' && (!aiStore.feedback.length || aiStore.error)) {
        aiStore.getFeedback(newJournal.journal_date, newJournal.content);
      }
    }
  },
  { deep: true, immediate: true }
);

watch(() => currentJournal.value?.chat_messages, () => {
    if(isChatActive.value) {
        scrollToBottom();
    }
}, { deep: true });

const saveJournal = async () => {
  if (!currentJournal.value) return;
  statusText.value = 'Saving...';

  const payload = {
    content: content.value,
    outline_content: outlineContent.value,
  };
  
  const savedJournal = await journalStore.updateJournal(currentJournal.value.journal_date, payload);
  
  statusText.value = savedJournal ? 'All changes saved!' : 'Error saving.';
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
            tempContent = tempContent.replace(regex, `<span class="bg-yellow-200 rounded px-1">${item.incorrect_phrase}</span>`);
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

const handleCompletion = async () => {
    await saveJournal();
    statusText.value = 'Journal Completed!';
    // Optionally, navigate away or show a success message
    // router.push('/');
};

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const phaseMap = { scaffolding: 1, writing: 2, finishing: 3 };
const isPhaseActive = (phaseId) => phaseMap[currentPhase.value] >= phaseId;
const getPhaseClass = (phaseId) => {
    if (phaseMap[currentPhase.value] > phaseId) return 'bg-green-500 text-white';
    if (phaseMap[currentPhase.value] === phaseId) return 'bg-indigo-600 text-white';
    return 'bg-gray-200 text-gray-500';
};
const getPhaseLineClass = (phaseId) => {
    if (phaseMap[currentPhase.value] > phaseId) return 'bg-green-500';
    return 'bg-gray-200';
};
</script>

