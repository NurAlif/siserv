<template>
  <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Writing Analysis</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
      <!-- Radar Chart -->
      <div class="relative h-64 md:h-80">
        <Radar v-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
        <div v-else class="text-center py-10 text-gray-500 dark:text-gray-400">
          <p>Analysis data is not available.</p>
        </div>
      </div>
      <!-- Feedback List -->
      <div class="space-y-3">
        <div v-for="metric in metrics" :key="metric.name" class="bg-gray-50 dark:bg-gray-700/50 p-3 rounded-lg">
          <p class="font-semibold text-sm text-gray-800 dark:text-gray-200">{{ metric.name }} - {{ metric.score }}/{{ metric.max_score }}</p>
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">{{ metric.feedback }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Radar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, PointElement, LineElement, RadialLinearScale, Filler } from 'chart.js';
import { useUiStore } from '../stores/uiStore';

ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, RadialLinearScale, Filler);

const props = defineProps({
  metrics: {
    type: Array,
    required: true,
    default: () => []
  }
});

const uiStore = useUiStore();

const chartData = computed(() => {
  const labels = props.metrics.map(m => m.name);
  const data = props.metrics.map(m => m.score);
  return {
    labels: labels,
    datasets: [
      {
        label: 'Writing Score',
        backgroundColor: 'rgba(79, 70, 229, 0.2)', // Indigo-600 with opacity
        borderColor: '#4f46e5', // Indigo-600
        pointBackgroundColor: '#4f46e5',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#4f46e5',
        data: data,
      },
    ],
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    r: {
      angleLines: {
        color: uiStore.isDarkMode ? '#4b5563' : '#e5e7eb', // Grid lines color
      },
      grid: {
        color: uiStore.isDarkMode ? '#4b5563' : '#e5e7eb',
      },
      pointLabels: {
        color: uiStore.isDarkMode ? '#d1d5db' : '#374151', // Label text color
        font: {
            weight: 'bold'
        }
      },
      ticks: {
        color: uiStore.isDarkMode ? '#9ca3af' : '#6b7280',
        backdropColor: uiStore.isDarkMode ? 'rgba(23, 23, 23, 0.75)' : 'rgba(255, 255, 255, 0.75)',
        stepSize: 2,
      },
       min: 0,
       max: 10,
    },
  },
}));
</script>
