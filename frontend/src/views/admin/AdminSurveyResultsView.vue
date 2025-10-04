<template>
  <main id="admin-survey-results-view" class="fade-in">
    <!-- Loading and Error States -->
    <div v-if="adminStore.isLoadingSurveyResults" class="text-center py-20">
      <p class="text-gray-500 dark:text-gray-400">Loading survey results...</p>
    </div>
    <div v-else-if="adminStore.error" class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg">
      <p>{{ adminStore.error }}</p>
    </div>

    <div v-else-if="surveyData" class="space-y-6">
      <!-- Header -->
      <div class="mb-6">
        <router-link to="/admin/manage-notifications" class="text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-100 font-medium flex items-center gap-2 mb-4">
           <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
          Back to Notifications
        </router-link>
         <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Results: {{ surveyData.notification.title }}</h2>
            <p class="text-gray-500 dark:text-gray-400 mt-1">{{ surveyData.notification.content }}</p>
          </div>
      </div>
      
      <!-- Results for each question -->
      <div v-for="questionResult in surveyData.results" :key="questionResult.question_id" class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-800 dark:text-gray-200 mb-4">{{ questionResult.question_text }}</h3>

        <!-- Multiple Choice Results -->
        <div v-if="isMultipleChoice(questionResult.question_id)" class="space-y-2">
            <div v-for="option in getOptionsForQuestion(questionResult.question_id)" :key="option.id">
                <div class="flex justify-between items-center mb-1 text-sm">
                    <span class="font-medium text-gray-700 dark:text-gray-300">{{ option.option_text }}</span>
                    <span class="text-gray-500 dark:text-gray-400">{{ getResponseCountForOption(questionResult, option.id) }} votes</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div class="bg-indigo-600 h-2.5 rounded-full" :style="{ width: getPercentageForOption(questionResult, option.id) + '%' }"></div>
                </div>
            </div>
        </div>

        <!-- Text Answer Results -->
        <div v-else>
            <ul v-if="getTextResponses(questionResult).length > 0" class="space-y-3">
                <li v-for="response in getTextResponses(questionResult)" :key="response.id" class="bg-gray-50 dark:bg-gray-700/50 p-3 rounded-lg text-sm text-gray-800 dark:text-gray-200">
                    <p>"{{ response.text_response }}"</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400 text-right mt-1">- {{ response.user.realname }} ({{ response.user.student_id }})</p>
                </li>
            </ul>
            <p v-else class="text-sm text-gray-500 dark:text-gray-400">No text responses submitted for this question yet.</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAdminStore } from '../../stores/adminStore';

const route = useRoute();
const adminStore = useAdminStore();
const notificationId = route.params.id;

const surveyData = computed(() => adminStore.surveyResults);

onMounted(() => {
  if (notificationId) {
    adminStore.fetchSurveyResults(notificationId);
  }
});

const getQuestionById = (questionId) => {
    return surveyData.value?.notification.questions.find(q => q.id === questionId);
};

const isMultipleChoice = (questionId) => {
    const question = getQuestionById(questionId);
    return question && question.question_type.startsWith('multiple_choice');
};

const getOptionsForQuestion = (questionId) => {
    return getQuestionById(questionId)?.options || [];
};

const getResponseCountForOption = (questionResult, optionId) => {
    return questionResult.responses.filter(r => r.selected_option && r.selected_option.id === optionId).length;
};

const getTotalVotesForQuestion = (questionResult) => {
    // Only count responses that are for an option, not free text
    return questionResult.responses.filter(r => r.selected_option).length;
}

const getPercentageForOption = (questionResult, optionId) => {
    const totalVotes = getTotalVotesForQuestion(questionResult);
    if (totalVotes === 0) return 0;
    const optionVotes = getResponseCountForOption(questionResult, optionId);
    return (optionVotes / totalVotes) * 100;
};

const getTextResponses = (questionResult) => {
    return questionResult.responses.filter(r => r.text_response);
};
</script>
