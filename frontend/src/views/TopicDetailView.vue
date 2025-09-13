<template>
  <main id="topic-detail-view" class="fade-in">
    <!-- Header -->
    <div class="mb-6">
      <router-link to="/learning-hub" class="text-gray-500 hover:text-gray-800 font-medium flex items-center gap-2 mb-4">
         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        Back to Learning Hub
      </router-link>
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h2 class="text-2xl font-bold">{{ progressStore.currentTopicDetails?.topic_name || 'Loading Topic...' }}</h2>
        <p v-if="progressStore.currentTopicDetails" class="text-gray-500 mt-1">
          A review of your {{ progressStore.currentTopicDetails.error_count }} unique error{{ progressStore.currentTopicDetails.error_count > 1 ? 's' : '' }} in this area.
        </p>
      </div>
    </div>

    <!-- Loading and Error States -->
    <div v-if="progressStore.isLoading" class="text-center py-10">
      <p class="text-gray-500">Loading your error history...</p>
    </div>
    <div v-else-if="progressStore.error" class="bg-red-50 text-red-700 p-4 rounded-lg">
      <p>{{ progressStore.error }}</p>
    </div>

    <!-- Error Details List -->
    <div v-else-if="progressStore.currentTopicDetails?.errors.length > 0" class="space-y-4">
      <ErrorDetailCard 
        v-for="(error, index) in progressStore.currentTopicDetails.errors"
        :key="index"
        :error="error"
      />
    </div>
    <div v-else class="text-center py-10 bg-white rounded-xl border border-gray-200">
        <h4 class="font-semibold text-lg">No errors found!</h4>
        <p class="text-gray-500">There's no specific error history to show for this topic.</p>
    </div>
  </main>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useProgressStore } from '../stores/progressStore';
import ErrorDetailCard from '../components/ErrorDetailCard.vue';

const route = useRoute();
const progressStore = useProgressStore();
const topicId = route.params.topic_id;

const loadDetails = () => {
  if (topicId) {
    progressStore.fetchTopicDetails(topicId);
  }
};

onMounted(loadDetails);

// Watch for route changes if the user navigates between topics
watch(() => route.params.topic_id, (newId) => {
  if (newId) {
    loadDetails();
  }
});
</script>

