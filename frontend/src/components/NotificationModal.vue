<template>
  <div v-if="notification" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex justify-center items-center p-4 transition-opacity duration-300" @click.self="handleOverlayClick">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg w-full max-w-lg max-h-[90vh] flex flex-col transform transition-transform duration-300 scale-95" :class="{ 'scale-100': notification }">
      <!-- Modal Header -->
      <header class="p-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">{{ notification.title }}</h2>
      </header>
      
      <!-- Modal Content -->
      <main class="flex-grow overflow-y-auto p-6 custom-scrollbar">
        <!-- Announcement Content -->
        <div v-if="notification.notification_type === 'announcement'">
          <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{{ notification.content }}</p>
        </div>
        
        <!-- Survey Content -->
        <div v-if="notification.notification_type === 'survey'" class="space-y-6">
          <p class="text-gray-700 dark:text-gray-300">{{ notification.content }}</p>
          
          <!-- Questions -->
          <div v-for="(question, q_index) in notification.questions" :key="question.id" class="border-t border-gray-200 dark:border-gray-700 pt-4">
            <p class="font-semibold text-gray-800 dark:text-gray-200">{{ q_index + 1 }}. {{ question.question_text }}</p>
            
            <!-- Multiple Choice (Single) -->
            <div v-if="question.question_type === 'multiple_choice_single'" class="mt-2 space-y-2">
              <label v-for="option in question.options" :key="option.id" class="flex items-center p-2 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                <input type="radio" :name="'question_' + question.id" :value="option.id" v-model="responses[question.id]" class="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500">
                <span class="ml-3 text-sm text-gray-700 dark:text-gray-300">{{ option.option_text }}</span>
              </label>
            </div>
            
            <!-- Multiple Choice (Multiple) -->
            <div v-if="question.question_type === 'multiple_choice_multiple'" class="mt-2 space-y-2">
              <label v-for="option in question.options" :key="option.id" class="flex items-center p-2 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                <input type="checkbox" :value="option.id" v-model="responses[question.id]" class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500">
                <span class="ml-3 text-sm text-gray-700 dark:text-gray-300">{{ option.option_text }}</span>
              </label>
            </div>
            
            <!-- Text Input -->
            <div v-if="question.question_type === 'text'" class="mt-2">
              <textarea v-model="responses[question.id]" rows="3" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"></textarea>
            </div>
          </div>
        </div>
      </main>

      <!-- Modal Footer -->
      <footer class="p-4 border-t border-gray-200 dark:border-gray-700 flex-shrink-0 flex justify-end gap-3">
        <button v-if="isSurvey && !isSurveyComplete" class="text-sm font-medium text-gray-500 dark:text-gray-400 px-4 py-2 rounded-lg" disabled>
          Please complete the survey
        </button>
        <button v-if="isSurvey" @click="submitSurvey" :disabled="!isSurveyComplete || isLoading" class="px-4 py-2 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-400 dark:disabled:bg-indigo-800 transition-colors">
          {{ isLoading ? 'Submitting...' : 'Submit Survey' }}
        </button>
        <button v-if="!isSurvey" @click="close" class="px-4 py-2 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors">
          Got it
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  notification: {
    type: Object,
    default: null,
  },
  isLoading: Boolean,
});

const emit = defineEmits(['close', 'submit']);

const responses = ref({});

const isSurvey = computed(() => props.notification?.notification_type === 'survey');

// Logic to check if all survey questions have been answered
const isSurveyComplete = computed(() => {
  if (!isSurvey.value) return false;
  const questions = props.notification.questions;
  return questions.every(q => {
    const response = responses.value[q.id];
    if (response === null || response === undefined) return false;
    if (Array.isArray(response) && response.length === 0) return false;
    if (typeof response === 'string' && response.trim() === '') return false;
    return true;
  });
});

// Initialize responses state when a new notification is shown
watch(() => props.notification, (newVal) => {
  if (newVal && newVal.notification_type === 'survey') {
    const initialResponses = {};
    newVal.questions.forEach(q => {
      initialResponses[q.id] = q.question_type === 'multiple_choice_multiple' ? [] : null;
    });
    responses.value = initialResponses;
  } else {
    responses.value = {};
  }
}, { immediate: true });

const close = () => {
  emit('close');
};

const submitSurvey = () => {
  if (!isSurveyComplete.value) return;
  const payload = {
    notification_id: props.notification.id,
    responses: Object.entries(responses.value).map(([question_id, answer]) => {
      const question = props.notification.questions.find(q => q.id === parseInt(question_id));
      if (question.question_type === 'text') {
        return { question_id: parseInt(question_id), text_response: answer };
      } else {
        const ids = Array.isArray(answer) ? answer : [answer];
        return { question_id: parseInt(question_id), selected_option_ids: ids.filter(id => id !== null) };
      }
    }),
  };
  emit('submit', payload);
};

const handleOverlayClick = () => {
    // Only allow closing via overlay for announcements
    if (!isSurvey.value) {
        close();
    }
}
</script>
