<template>
  <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-full">
    <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-4">Daily Phase Distribution</h4>
    <div class="relative h-72">
      <Doughnut v-if="hasData" :data="chartData" :options="chartOptions" />
      <div v-else class="flex items-center justify-center h-full text-center text-gray-500 dark:text-gray-400">
        <p>No student data to display.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { useUiStore } from '../../stores/uiStore';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const props = defineProps({
  journals: {
    type: Array,
    required: true,
    default: () => []
  }
});

const uiStore = useUiStore();

const phaseCounts = computed(() => {
  const counts = {
    scaffolding: 0,
    writing: 0,
    evaluation: 0,
    completed: 0,
    not_started: 0, // New category
  };
  props.journals.forEach(journal => {
    if (journal.writing_phase && journal.writing_phase in counts) {
      counts[journal.writing_phase]++;
    } else {
      counts.not_started++;
    }
  });
  return counts;
});

const hasData = computed(() => props.journals.length > 0);

const chartData = computed(() => {
  const counts = phaseCounts.value;
  return {
    labels: ['Not Started', 'Scaffolding', 'Writing', 'Evaluation', 'Completed'],
    datasets: [
      {
        backgroundColor: ['#9CA3AF', '#6366F1', '#14B8A6', '#F43F5E', '#22C55E'], // Gray, Indigo, Teal, Rose, Green
        data: [counts.not_started, counts.scaffolding, counts.writing, counts.evaluation, counts.completed],
      },
    ],
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: uiStore.isDarkMode ? '#d1d5db' : '#4b5563',
      },
    },
  },
}));
</script>

