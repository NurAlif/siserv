<template>
  <main id="learning-hub-view" class="fade-in">
    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Learning Hub</h2>
      <p class="text-gray-500 dark:text-gray-400 mt-1">Review your common mistakes and track your progress over time.</p>
    </div>

    <!-- Loading and Error States -->
    <div v-if="progressStore.isLoading" class="text-center py-10">
      <p class="text-gray-500 dark:text-gray-400">Loading your learning topics...</p>
    </div>
    <div v-else-if="progressStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
      <p>{{ progressStore.error }}</p>
    </div>

    <!-- Topics List -->
    <div v-else-if="progressStore.topics.length > 0" class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-200">Your Focus Areas</h3>
      <TopicCard
        v-for="topic in progressStore.topics"
        :key="topic.topic_id"
        :topic="topic"
      />
    </div>
    <div v-else class="text-center py-10 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
      <h4 class="font-semibold text-lg text-gray-800 dark:text-gray-200">No Learning Topics Yet!</h4>
      <p class="text-gray-500 dark:text-gray-400">Get AI feedback on your journal entries to start building your Learning Hub.</p>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue';
import { useProgressStore } from '../stores/progressStore';
import TopicCard from '../components/TopicCard.vue';

const progressStore = useProgressStore();

onMounted(() => {
  progressStore.fetchTopics();
});
</script>
