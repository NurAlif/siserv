<template>
  <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
    <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-4">{{ title }}</h4>
    
    <div class="relative h-72">
      <Line v-if="chartData.datasets.length > 0 && chartData.datasets[0].data.length > 0" :data="chartData" :options="chartOptions" />
      <div v-else class="text-center py-10 text-gray-500 dark:text-gray-400">
        <p>No data available to display the chart.</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale, Filler } from 'chart.js';
import { useUiStore } from '../../stores/uiStore';

// Register all necessary components for Chart.js
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale, Filler);

const props = defineProps({
  title: {
    type: String,
    required: true,
    default: 'Writing Activity (Last 30 Days)'
  },
  chartRawData: {
    type: Array,
    required: true,
    default: () => []
  }
});

const uiStore = useUiStore();

const chartData = computed(() => {
    // FIX: The property from the API is `activity_date`, not `date`.
    const labels = props.chartRawData.map(d => new Date(d.activity_date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }));
    const data = props.chartRawData.map(d => d.error_count);
    
    return {
        labels: labels,
        datasets: [
            {
                label: 'Errors per Day',
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                borderColor: '#4f46e5', // Indigo-600
                data: data,
                fill: true,
                tension: 0.3,
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
        color: uiStore.isDarkMode ? '#d1d5db' : '#4b5563', // Text color for dark/light mode
      },
      grid: {
        display: false, // Hide vertical grid lines
      },
    },
    y: {
      beginAtZero: true,
      ticks: {
        color: uiStore.isDarkMode ? '#d1d5db' : '#4b5563', // Text color for dark/light mode
        stepSize: 1, // Ensure y-axis labels are whole numbers
      },
      grid: {
        color: uiStore.isDarkMode ? '#374151' : '#e5e7eb', // Grid line color for dark/light mode
      },
    },
  },
}));
</script>
