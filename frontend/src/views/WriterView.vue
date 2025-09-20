<template>
  <main id="writer-view" class="fade-in flex flex-col h-full w-full bg-white dark:bg-gray-800">
    
    <WriterHeader 
      :current-journal="currentJournal"
      :current-phase="currentPhase"
      :status-text="statusText"
    />

    <div class="flex-grow overflow-hidden relative">
      <component 
        :is="phaseComponent"
        :key="currentPhase"
        v-model:outlineContent="outlineContent"
        v-model:content="content"
        :current-journal="currentJournal"
        :is-chat-active="isChatActive"
        :ai-store="aiStore"
        :applied-suggestions="appliedSuggestions"
        :highlighted-content="highlightedContent"
        @apply-suggestion="applySuggestion"
      >
        <template #chat>
            <ChatPanel 
              :messages="currentJournal?.chat_messages"
              :is-loading="aiStore.isLoading"
              :placeholder="chatPlaceholder"
              @send-message="sendMessage"
            />
        </template>
      </component>
    </div>

    <WriterActions 
      :current-phase="currentPhase"
      :is-loading="journalStore.isLoading"
      :all-suggestions-applied="allSuggestionsApplied"
      @change-phase="moveToPhase"
      @toggle-chat="toggleChatMode"
      @save-journal="saveJournal"
    />
  </main>
</template>

<script setup>
// This refactored component still holds all the state management and business logic.
// Its responsibility is to fetch and manage data, then pass it down to the
// appropriate child components for rendering.

// ============== IMPORTS ==============
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useJournalStore } from '../stores/journalStore';
import { useAiStore } from '../stores/aiStore';
import { format } from 'date-fns';

// Child Component Imports
import WriterHeader from '../components/writer/WriterHeader.vue'; // Assumes components are in a 'writer' subfolder
import WriterActions from '../components/writer/WriterActions.vue';
import ChatPanel from '../components/writer/ChatPanel.vue';
import PhaseScaffolding from '../components/writer/phases/PhaseScaffolding.vue';
import PhaseWriting from '../components/writer/phases/PhaseWriting.vue';
import PhaseFinishing from '../components/writer/phases/PhaseFinishing.vue';
import PhaseCompleted from '../components/writer/phases/PhaseCompleted.vue';

// ============== STORE & ROUTER SETUP ==============
const route = useRoute();
const router = useRouter();
const journalStore = useJournalStore();
const aiStore = useAiStore();

// ============== STATE MANAGEMENT ==============
const content = ref('');
const outlineContent = ref('');
const statusText = ref('Saved');
const newMessage = ref('');
const isChatActive = ref(false);
const appliedSuggestions = ref([]);
let debounceTimer = null;

// ============== COMPUTED PROPERTIES ==============
const currentJournal = computed(() => journalStore.getJournalByDate(route.params.date));
const currentPhase = computed(() => currentJournal.value?.writing_phase || 'scaffolding');

const chatPlaceholder = computed(() => {
    if (currentPhase.value === 'scaffolding') {
        return 'Not sure what to write about? Chat here!';
    }
    if (currentPhase.value === 'writing') {
        return "Ask for help, e.g., 'What should I write next?'";
    }
    return 'Type your message...';
});

const allSuggestionsApplied = computed(() => {
    if (!aiStore.feedback || aiStore.feedback.length === 0) return true;
    return appliedSuggestions.value.length >= aiStore.feedback.length;
});

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

const phaseComponentMap = {
  scaffolding: PhaseScaffolding,
  writing: PhaseWriting,
  finishing: PhaseFinishing,
  completed: PhaseCompleted,
};

const phaseComponent = computed(() => phaseComponentMap[currentPhase.value] || PhaseScaffolding);

// ============== LIFECYCLE & WATCHERS ==============
onMounted(async () => {
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
});

watch(
  currentJournal,
  (newJournal) => {
    if (newJournal && newJournal.content !== content.value) {
      content.value = newJournal.content || '';
    }
    if (newJournal && newJournal.outline_content !== outlineContent.value) {
      outlineContent.value = newJournal.outline_content || '';
    }
    if (newJournal) {
      appliedSuggestions.value = [];
      if(newJournal.writing_phase === 'finishing' && (!aiStore.feedback.length || aiStore.error)) {
        aiStore.getFeedback(newJournal.journal_date, newJournal.content);
      }
    }
  },
  { deep: true, immediate: true }
);

watch(content, (newValue) => {
    if (!currentJournal.value || currentJournal.value.content === newValue) return;
    statusText.value = 'Typing...';
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        if (currentPhase.value === 'writing') {
            saveJournal();
        }
    }, 3000);
});

// ============== METHODS ==============
const saveJournal = async (showStatus = true) => {
  if (!currentJournal.value) return;
  if (showStatus) statusText.value = 'Saving...';
  
  const payload = {
    content: content.value,
    outline_content: outlineContent.value,
  };

  if (debounceTimer) clearTimeout(debounceTimer);

  const savedJournal = await journalStore.updateJournal(currentJournal.value.journal_date, payload);
  
  if (showStatus) {
      setTimeout(() => {
        statusText.value = savedJournal ? 'All changes saved' : 'Error saving.';
      }, 500);
  }
};

const moveToPhase = async (phase) => {
    if (!currentJournal.value) return;
    isChatActive.value = false;
    await saveJournal();
    await journalStore.updateJournalPhase(currentJournal.value.journal_date, phase);
};

const sendMessage = async (messageText) => {
  if (!messageText.trim() || !currentJournal.value || aiStore.isLoading) return;
  
  if (currentPhase.value === 'scaffolding' || currentPhase.value === 'writing') {
    await saveJournal(false);
  }
  
  await aiStore.chatWithAI(currentJournal.value.journal_date, messageText);
};

const toggleChatMode = () => {
    isChatActive.value = !isChatActive.value;
};

const applySuggestion = (feedbackItem) => {
    content.value = content.value.replace(feedbackItem.incorrect_phrase, feedbackItem.suggestion);
    appliedSuggestions.value.push(feedbackItem.incorrect_phrase);
};

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
</script>