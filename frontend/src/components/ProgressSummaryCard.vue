<template>
  <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
    <h3 class="text-lg font-semibold mb-4">Your Learning Snapshot</h3>
    <div v-if="isLoading" class="text-center text-gray-500">
      Loading progress...
    </div>
    <div v-else-if="error" class="bg-red-50 text-red-700 p-3 rounded-lg">
      {{ error }}
    </div>
    <div v-else-if="summary" class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Total Errors -->
      <div class="bg-blue-50 p-4 rounded-lg text-center">
        <p class="text-3xl font-bold text-blue-600">{{ summary.total_errors }}</p>
        <p class="text-sm font-medium text-blue-800">Total Errors Logged</p>
      </div>
      <!-- Topics Encountered -->
      <div class="bg-green-50 p-4 rounded-lg text-center">
        <p class="text-3xl font-bold text-green-600">{{ summary.topics_encountered }}</p>
        <p class="text-sm font-medium text-green-800">Topics Encountered</p>
      </div>
      <!-- Top Focus Topic -->
      <div class="bg-yellow-50 p-4 rounded-lg text-center flex flex-col justify-center">
        <p class="text-lg font-bold text-yellow-700 leading-tight truncate">
            {{ topTopicName }}
        </p>
        <p class="text-sm font-medium text-yellow-800 mt-1">Your Top Focus Area</p>
      </div>
    </div>
    <div v-else class="text-center text-gray-500">
      <p>No progress data yet. Start writing and get some feedback!</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  summary: {
    type: Object,
    default: null,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: null,
  },
});

const topTopicName = computed(() => {
    if (props.summary && props.summary.top_topics && props.summary.top_topics.length > 0) {
        return props.summary.top_topics[0].topic_name;
    }
    return 'N/A';
});
</script>
