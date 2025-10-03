<template>
  <div class="bg-white dark:bg-gray-800 p-4 sm:p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
    <!-- Calendar Header (Days of the week) -->
    <div class="grid grid-cols-7 gap-2 text-center text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2">
      <div>Sun</div>
      <div>Mon</div>
      <div>Tue</div>
      <div>Wed</div>
      <div>Thu</div>
      <div>Fri</div>
      <div>Sat</div>
    </div>
    <!-- Calendar Grid -->
    <div class="grid grid-cols-7 gap-1 sm:gap-2">
      <div
        v-for="(day, index) in calendarDays"
        :key="index"
        :class="getCellClasses(day)"
        class="h-20 sm:h-32 rounded-lg flex flex-col p-1 sm:p-2 relative transition-all duration-200 group"
        @click="handleDateClick(day)"
      >
        <!-- A. Locked Future Date Cell -->
        <template v-if="isFutureDate(day.date)">
          <div class="w-full h-full flex items-center justify-center">
            <span class="font-semibold text-xs sm:text-sm">{{ day.date.getDate() }}</span>
          </div>
        </template>
        
        <!-- B. Active Past/Present Date Cell -->
        <template v-else-if="!day.placeholder">
          <!-- Header: Day Number & Late Indicator -->
          <div class="flex justify-between items-center">
            <div class="font-semibold text-xs sm:text-sm" :class="getDayNumberClasses(day.date)">
              {{ day.date.getDate() }}
            </div>
            <div v-if="getJournalIsLate(day.date)">
              <div class="sm:hidden w-2.5 h-2.5 bg-red-500 rounded-full" title="Submitted late"></div>
              <span class="hidden sm:inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300">LATE</span>
            </div>
          </div>

          <!-- Body: Content based on if a journal exists -->
          <div class="flex-grow flex items-center justify-center relative">
            <!-- Image Stack (Background) -->
            <ImageStack
              v-if="getJournalImages(day.date).length > 0"
              :images="getJournalImages(day.date)"
              class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-0 scale-75 sm:scale-100 opacity-80 group-hover:opacity-100 transition-all"
              @click.stop="handleDateClick(day)"
            />
            
            <div class="relative z-10">
                <!-- B1. Journal Exists: Show Status Icon -->
                <div v-if="journalsByDate[formatDateKey(day.date)]">
                  <!-- Completed Mark -->
                  <div v-if="getJournalPhase(day.date) === 'completed'" class="w-6 h-6 sm:w-8 sm:h-8 bg-green-500 rounded-full flex items-center justify-center shadow-lg" title="Completed">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="text-white w-5 h-5 sm:w-6 sm:h-6" viewBox="0 0 256 256"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"></path></svg>
                  </div>
                  <!-- In-progress Step Number -->
                  <div v-else class="w-6 h-6 sm:w-9 sm:h-9 bg-indigo-500 rounded-full flex items-center justify-center shadow-lg text-white text-sm sm:text-base" :title="`Phase: ${getJournalPhase(day.date)}`">
                     {{ getPhaseNumber(getJournalPhase(day.date)) }}
                  </div>
                </div>

                <!-- B2. No Journal: Show 'Add' Button -->
                <div v-else>
                   <div class="w-7 h-7 sm:w-10 sm:h-10 rounded-full flex items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-600 group-hover:bg-gray-100 dark:group-hover:bg-gray-700/50 transition-colors">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="text-gray-400 dark:text-gray-500 w-4 h-4 sm:w-5 sm:h-5" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path></svg>
                   </div>
                </div>
            </div>
          </div>
          
          <!-- Footer: Phase name (if journal exists) -->
          <div v-if="journalsByDate[formatDateKey(day.date)]" class="h-5 text-center hidden sm:flex items-center justify-center">
              <span class="px-1.5 py-0.5 text-[10px] font-bold rounded-full truncate" :class="getPhaseClass(getJournalPhase(day.date))">
                 {{ getJournalPhase(day.date) }}
               </span>
          </div>
        </template>
      </div>
    </div>
    <!-- Completion Progress Bar -->
    <div class="mt-4 sm:mt-6">
      <div class="flex justify-between items-center mb-1">
        <div>
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">Completion Progress</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 ml-2">{{ completedJournalsCount }} / {{ totalJournalSlots }} days</span>
        </div>
        <span class="text-sm font-bold text-gray-800 dark:text-gray-200">{{ completionPercentage }}%</span>
      </div>
      <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
        <div class="bg-green-500 h-2.5 rounded-full transition-all duration-500" :style="{ width: completionPercentage + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { format, isToday as checkIsToday, isFuture } from 'date-fns';
import apiClient from '../services/api';
import ImageStack from './ImageStack.vue';

const props = defineProps({
  journals: {
    type: Array,
    required: true,
  },
});

const router = useRouter();

const today = new Date();
// Set hours to 0 to compare dates only
today.setHours(0, 0, 0, 0);

const getCalendarDays = () => {
  const days = [];
  const start = new Date('2025-09-29T00:00:00');
  const end = new Date('2025-11-14T00:00:00');
  let current = new Date(start);

  const startDayOfWeek = start.getDay();
  for (let i = 0; i < startDayOfWeek; i++) {
    days.push({ placeholder: true });
  }

  while (current <= end) {
    days.push({ date: new Date(current), placeholder: false });
    current.setDate(current.getDate() + 1);
  }

  return days;
};

const calendarDays = ref(getCalendarDays());

// --- Progress Calculation ---
const totalJournalSlots = computed(() => {
  return calendarDays.value.filter(day => !day.placeholder).length;
});

const completedJournalsCount = computed(() => {
  return props.journals.filter(j => j.writing_phase === 'completed').length;
});

const completionPercentage = computed(() => {
    const totalPossible = totalJournalSlots.value;
    if (totalPossible === 0) return 0;
    return Math.round((completedJournalsCount.value / totalPossible) * 100);
});


const formatDateKey = (date) => format(date, 'yyyy-MM-dd');

const journalsByDate = computed(() => {
  return props.journals.reduce((acc, journal) => {
    acc[journal.journal_date] = journal;
    return acc;
  }, {});
});

const isFutureDate = (date) => date > today;
const isToday = (date) => checkIsToday(date);

const getJournalForDate = (date) => journalsByDate.value[formatDateKey(date)];

const getJournalPhase = (date) => getJournalForDate(date)?.writing_phase || 'not_started';
const getJournalIsLate = (date) => getJournalForDate(date)?.is_late || false;
const getJournalImages = (date) => {
    const journal = getJournalForDate(date);
    return journal?.images || [];
};

const getPhaseNumber = (phase) => {
    const phaseMap = {
        scaffolding: '1/3',
        writing: '2/3',
        evaluation: '3/3',
    };
    return phaseMap[phase] || '';
};

const handleDateClick = (day) => {
  if (day.placeholder || isFutureDate(day.date)) {
    return; // Do nothing for placeholders or future dates
  }
  const dateKey = formatDateKey(day.date);
  router.push(`/writer/${dateKey}`);
};

// --- Styling Helpers ---
const getCellClasses = (day) => {
  if (day.placeholder) return 'bg-gray-50 dark:bg-gray-800/50';
  
  const journal = getJournalForDate(day.date);
  const baseClasses = [];

  if (isToday(day.date)) {
    baseClasses.push('border-2 border-indigo-500');
  } else if (journal && journal.writing_phase === 'completed') {
    baseClasses.push('border-2 border-green-500');
  } else {
    baseClasses.push('border border-gray-200 dark:border-gray-700');
  }

  if (isFutureDate(day.date)) {
    baseClasses.push('bg-gray-100 dark:bg-gray-700/50 text-gray-400 dark:text-gray-500 cursor-not-allowed');
    return baseClasses.join(' ');
  }

  if (journal) {
     baseClasses.push('bg-white dark:bg-gray-800 cursor-pointer hover:border-indigo-400 dark:hover:border-indigo-500');
  } else {
     baseClasses.push('bg-gray-50 dark:bg-gray-800/50 cursor-pointer hover:border-gray-300 dark:hover:border-gray-600');
  }
  return baseClasses.join(' ');
};

const getDayNumberClasses = (date) => {
  if (isToday(date)) return 'bg-indigo-600 text-white rounded-full w-5 h-5 flex items-center justify-center';
  return 'text-gray-700 dark:text-gray-300';
};

const getPhaseClass = (phase) => {
  switch (phase) {
    case 'scaffolding':
      return 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300';
    case 'writing':
      return 'bg-teal-100 text-teal-800 dark:bg-teal-900/50 dark:text-teal-300';
    case 'evaluation':
      return 'bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-300';
    case 'completed':
      return 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300';
    default:
      return '';
  }
};
</script>

