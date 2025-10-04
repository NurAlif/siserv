<template>
  <main id="admin-manage-notifications-view" class="fade-in">
    <!-- Header -->
    <div class="mb-6">
      <router-link to="/admin" class="text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-100 font-medium flex items-center gap-2 mb-4">
         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        Back to Admin Dashboard
      </router-link>
       <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Manage Notifications</h2>
          <p class="text-gray-500 dark:text-gray-400">Create announcements and surveys for your students.</p>
        </div>
    </div>

    <!-- Create Notification Form -->
    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-8">
      <h3 class="font-semibold text-lg text-gray-800 dark:text-gray-200 mb-4">{{ editingNotificationId ? 'Edit Notification' : 'Create New Notification' }}</h3>
      <form @submit.prevent="handleSaveNotification" class="space-y-4">
        <!-- Title -->
        <div>
          <label for="title" class="text-sm font-medium text-gray-700 dark:text-gray-300">Title</label>
          <input v-model="form.title" type="text" id="title" required class="w-full input-field" placeholder="e.g., Mid-term Survey">
        </div>
        <!-- Content -->
        <div>
          <label for="content" class="text-sm font-medium text-gray-700 dark:text-gray-300">Content / Description</label>
          <textarea v-model="form.content" id="content" required rows="3" class="w-full input-field" placeholder="A short description of the announcement or survey."></textarea>
        </div>
        <!-- Notification Type -->
        <div>
            <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Type</label>
            <div class="flex items-center gap-4 mt-1">
                <label class="flex items-center">
                    <input type="radio" v-model="form.notification_type" value="announcement" class="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500">
                    <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Announcement</span>
                </label>
                <label class="flex items-center">
                    <input type="radio" v-model="form.notification_type" value="survey" class="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500">
                    <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Survey</span>
                </label>
            </div>
        </div>
        
        <!-- Survey Questions (Conditional) -->
        <div v-if="form.notification_type === 'survey'" class="space-y-4 border-t border-gray-200 dark:border-gray-700 pt-4">
          <div v-for="(question, q_index) in form.questions" :key="q_index" class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
            <div class="flex justify-between items-center mb-2">
                <p class="font-semibold text-sm text-gray-800 dark:text-gray-200">Question {{ q_index + 1 }}</p>
                <button @click="removeQuestion(q_index)" type="button" class="text-red-500 hover:text-red-700 text-xs font-bold">REMOVE</button>
            </div>
            <input v-model="question.question_text" type="text" required class="w-full input-field mb-2" placeholder="Enter the survey question">
            <select v-model="question.question_type" class="w-full input-field mb-2">
                <option value="multiple_choice_single">Multiple Choice (Single Answer)</option>
                <option value="multiple_choice_multiple">Multiple Choice (Multiple Answers)</option>
                <option value="text">Text Answer</option>
            </select>
            <!-- Options for Multiple Choice -->
            <div v-if="question.question_type.startsWith('multiple_choice')" class="space-y-2 mt-2">
                <div v-for="(option, o_index) in question.options" :key="o_index" class="flex items-center gap-2">
                    <input v-model="option.option_text" type="text" required class="w-full input-field text-sm" placeholder="Option text">
                    <button @click="removeOption(q_index, o_index)" type="button" class="p-1 rounded-full text-gray-400 hover:bg-red-100 hover:text-red-600">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256"><path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"></path></svg>
                    </button>
                </div>
                <button @click="addOption(q_index)" type="button" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">+ Add Option</button>
            </div>
          </div>
          <button @click="addQuestion" type="button" class="w-full border-2 border-dashed border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 font-semibold py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">+ Add Question</button>
        </div>

        <div class="flex justify-end gap-3">
          <button v-if="editingNotificationId" @click="cancelEdit" type="button" class="w-full sm:w-auto py-2 px-6 font-semibold text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-600 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-500 transition-colors">
            Cancel
          </button>
          <button type="submit" :disabled="isSubmitting" class="w-full sm:w-auto py-2 px-6 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-400 dark:disabled:bg-indigo-800 transition-colors">
            {{ isSubmitting ? 'Saving...' : 'Save as Draft' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Existing Notifications List -->
     <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-4 border-b border-gray-200 dark:border-gray-700">
        <h4 class="font-semibold text-gray-800 dark:text-gray-200">Existing Notifications ({{ adminStore.notifications.length }})</h4>
      </div>
      <div v-if="adminStore.isLoadingNotifications" class="text-center p-8 text-gray-500 dark:text-gray-400">
        Loading notifications...
      </div>
      <table v-else class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700/50">
          <tr>
            <th class="th-cell">Title</th>
            <th class="th-cell">Type</th>
            <th class="th-cell">Status</th>
            <th class="th-cell">Created On</th>
            <th class="relative px-6 py-3"><span class="sr-only">Actions</span></th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-if="adminStore.notifications.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
              No notifications have been created yet.
            </td>
          </tr>
          <tr v-for="notif in adminStore.notifications" :key="notif.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
            <td class="td-cell font-medium text-gray-900 dark:text-gray-100">{{ notif.title }}</td>
            <td class="td-cell capitalize">{{ notif.notification_type }}</td>
            <td class="td-cell">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="notif.is_published ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300' : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300'">
                    {{ notif.is_published ? 'Published' : 'Draft' }}
                </span>
            </td>
            <td class="td-cell">{{ formatDate(notif.created_at) }}</td>
            <td class="td-cell text-right space-x-2">
                <button v-if="!notif.is_published" @click="handlePublish(notif.id)" class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300 font-semibold">Publish</button>
                <router-link
                  v-if="notif.notification_type === 'survey' && notif.is_published"
                  :to="`/admin/notification/${notif.id}/results`"
                  class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300 font-semibold"
                >
                  View Results
                </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useAdminStore } from '../../stores/adminStore';
import { format } from 'date-fns';

const adminStore = useAdminStore();
const isSubmitting = ref(false);
const editingNotificationId = ref(null); // To track if we are in edit mode

const createInitialForm = () => ({
  title: '',
  content: '',
  notification_type: 'announcement',
  questions: [],
});

const form = reactive(createInitialForm());

const addQuestion = () => {
  form.questions.push({
    question_text: '',
    question_type: 'multiple_choice_single',
    options: [{ option_text: '' }],
  });
};

const removeQuestion = (index) => {
  form.questions.splice(index, 1);
};

const addOption = (q_index) => {
  form.questions[q_index].options.push({ option_text: '' });
};

const removeOption = (q_index, o_index) => {
  form.questions[q_index].options.splice(o_index, 1);
};

const resetForm = () => {
    Object.assign(form, createInitialForm());
    editingNotificationId.value = null;
};

const handleSaveNotification = async () => {
  isSubmitting.value = true;
  if (editingNotificationId.value) {
    // Call update action
    // await adminStore.updateNotification(editingNotificationId.value, form);
  } else {
    // Call create action
    await adminStore.createNotification(form);
  }
  resetForm();
  isSubmitting.value = false;
};

const handlePublish = async (notificationId) => {
    await adminStore.publishNotification(notificationId);
};

const cancelEdit = () => {
    resetForm();
};

onMounted(() => {
  adminStore.fetchAllNotifications();
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  return format(new Date(dateString), 'MMM d, yyyy');
};
</script>

<style scoped>
.input-field {
  @apply px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100;
}
.th-cell {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider;
}
.td-cell {
  @apply px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400;
}
</style>
