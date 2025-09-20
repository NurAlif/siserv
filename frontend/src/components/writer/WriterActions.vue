<template>
  <div class="flex-shrink-0 p-4 border-t border-gray-200 dark:border-gray-700">
    <div v-if="currentPhase === 'scaffolding'" class="flex flex-col sm:flex-row gap-4">
      <button @click="$emit('toggle-chat')" class="...">Chat with Lingo</button>
      <button @click="$emit('change-phase', 'writing')" class="...">Start Writing</button>
    </div>

    <div v-if="currentPhase === 'writing'" class="flex justify-end">
      <button @click="$emit('change-phase', 'finishing')" class="...">Finish & Get Final Feedback</button>
    </div>

    <div v-if="currentPhase === 'finishing'" class="flex justify-between items-center gap-4">
       <button @click="$emit('save-journal')" :disabled="isLoading" class="...">{{ isLoading ? 'Saving...' : 'Save Changes' }}</button>
       <div class="flex gap-4">
          <button @click="$emit('change-phase', 'writing')" class="...">Back to Writing</button>
          <button @click="$emit('change-phase', 'completed')" :disabled="!allSuggestionsApplied" class="...">Mark as Complete</button>
       </div>
    </div>

    <div v-if="currentPhase === 'completed'" class="flex justify-center">
        <router-link to="/" class="...">Back to Dashboard</router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  currentPhase: String,
  isLoading: Boolean,
  allSuggestionsApplied: Boolean,
});
defineEmits(['change-phase', 'toggle-chat', 'save-journal']);
</script>