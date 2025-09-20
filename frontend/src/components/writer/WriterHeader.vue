<template>
  <div class="flex-shrink-0 p-3 flex justify-between items-center border-b border-gray-200 dark:border-gray-700">
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

    <div class="flex items-center"> 
      <template v-for="(phase, index) in phases" :key="phase.id">
        <div class="flex items-center">
          <div v-if="index > 0" class="w-8 h-1 rounded transition-colors" :class="getPhaseLineClass(phase.id)"></div>
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
</template>

<script setup>
import { computed } from 'vue';
import { format } from 'date-fns';

const props = defineProps({
  currentJournal: Object,
  currentPhase: String,
  statusText: String,
});

const phases = [
    { id: 1, name: 'Scaffolding' },
    { id: 2, name: 'Writing' },
    { id: 3, name: 'Finishing' },
    { id: 4, name: 'Completed' },
];

const displayDate = computed(() => {
  if (props.currentJournal) {
    // Assuming you move formatDisplayDate to a utility file
    return format(new Date(props.currentJournal.journal_date.replace(/-/g, '/')), 'MMMM d, yyyy');
  }
  return format(new Date(), 'MMMM d, yyyy');
});

const phaseMap = { scaffolding: 1, writing: 2, finishing: 3, completed: 4 };

const getPhaseClass = (phaseId) => {
    const phaseValue = phaseMap[props.currentPhase];
    if (phaseValue > phaseId) return 'bg-green-500 text-white'; // Completed
    if (phaseValue === phaseId) return 'bg-indigo-600 text-white scale-110 shadow-lg'; // Active
    return 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'; // Inactive
};

const getPhaseLineClass = (phaseId) => {
    if (phaseMap[props.currentPhase] >= phaseId) return 'bg-green-500'; // Completed line
    return 'bg-gray-200 dark:bg-gray-700'; // Inactive line
};
</script>