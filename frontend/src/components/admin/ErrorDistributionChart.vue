<template>
  <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
    <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-4">{{ title }}</h4>
    
    <div class="relative h-72">
      <Bar v-if="chartData.datasets.length > 0" :data="chartData" :options="chartOptions" />
      <div v-else class="text-center py-10 text-gray-500 dark:text-gray-400">
        <p>No data available to display the chart.</p>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { useUiStore } from '../../stores/uiStore';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  title: {
    type: String,
    required: true,
    default: 'Error Distribution'
  },
  chartRawData: {
    type: Array,
    required: true,
    default: () => []
  }
});

const uiStore = useUiStore();

const chartData = computed(() => {
    const labels = props.chartRawData.map(d => d.topic_name);
    const data = props.chartRawData.map(d => d.error_count);
    return {
        labels: labels,
        datasets: [
            {
                label: 'Error Count',
                backgroundColor: '#4f46e5', // Indigo-600
                borderColor: '#4f46e5',
                borderRadius: 4,
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
    x: {
      ticks: {
        color: uiStore.isDarkMode ? '#d1d5db' : '#4b5563', // Gray-300 for dark, Gray-600 for light
      },
      grid: {
        display: false,
      },
    },
    y: {
      ticks: {
        color: uiStore.isDarkMode ? '#d1d5db' : '#4b5563',
      },
      grid: {
        color: uiStore.isDarkMode ? '#374151' : '#e5e7eb', // Gray-700 for dark, Gray-200 for light
      },
    },
  },
}));
</script>
