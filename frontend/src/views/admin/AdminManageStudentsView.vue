<template>
  <main id="admin-manage-students-view" class="fade-in">
    <!-- Header -->
    <div class="mb-6">
      <router-link to="/admin" class="text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-100 font-medium flex items-center gap-2 mb-4">
         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path></svg>
        Back to Admin Dashboard
      </router-link>
       <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Manage Student Whitelist</h2>
          <p class="text-gray-500 dark:text-gray-400">Add or remove students who are allowed to register for an account.</p>
        </div>
    </div>

    <!-- Add Student Form -->
    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-6">
      <h3 class="font-semibold text-lg text-gray-800 dark:text-gray-200 mb-4">Add New Student</h3>
      <form @submit.prevent="handleAddStudent" class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        <div>
          <label for="student_id" class="text-sm font-medium text-gray-700 dark:text-gray-300">Student ID</label>
          <input
            v-model="newStudent.student_id"
            type="text"
            id="student_id"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="e.g., 411223344"
          />
        </div>
        <div>
          <label for="email" class="text-sm font-medium text-gray-700 dark:text-gray-300">Email Address</label>
          <input
            v-model="newStudent.email"
            type="email"
            id="email"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="student@example.com"
          />
        </div>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full md:w-auto py-2 px-4 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-400 dark:disabled:bg-indigo-800 transition-colors"
        >
          {{ isSubmitting ? 'Adding...' : 'Add Student' }}
        </button>
      </form>
       <div v-if="adminStore.error" class="mt-4 text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/50 p-3 rounded-lg">
          {{ adminStore.error }}
        </div>
        <div v-if="successMessage" class="mt-4 text-sm text-green-700 dark:text-green-300 bg-green-50 dark:bg-green-900/50 p-3 rounded-lg">
          {{ successMessage }}
        </div>
    </div>

    <!-- Whitelist Table -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-4">
        <h4 class="font-semibold text-gray-800 dark:text-gray-200">Whitelisted Students ({{ adminStore.whitelist.length }})</h4>
      </div>
      <div v-if="adminStore.isLoadingWhitelist" class="text-center p-8 text-gray-500 dark:text-gray-400">
        Loading whitelist...
      </div>
      <table v-else class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700/50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Student ID</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Email</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Date Added</th>
            <th scope="col" class="relative px-6 py-3"><span class="sr-only">Actions</span></th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-if="adminStore.whitelist.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
              No students have been added to the whitelist yet.
            </td>
          </tr>
          <tr v-for="student in adminStore.whitelist" :key="student.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap font-mono text-sm text-gray-800 dark:text-gray-200">{{ student.student_id }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ student.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ formatDate(student.created_at) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="handleRemoveStudent(student.student_id)" class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300">
                Remove
              </button>
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

const newStudent = reactive({
  student_id: '',
  email: '',
});

const isSubmitting = ref(false);
const successMessage = ref('');

onMounted(() => {
  adminStore.fetchWhitelist();
});

const handleAddStudent = async () => {
  isSubmitting.value = true;
  successMessage.value = '';
  const result = await adminStore.addStudentToWhitelist({ ...newStudent });
  if (result.success) {
    successMessage.value = 'Student added to whitelist successfully!';
    newStudent.student_id = '';
    newStudent.email = '';
  }
  isSubmitting.value = false;
};

const handleRemoveStudent = async (studentId) => {
    // In a production app, it's better to use a modal component for confirmation.
    // For this implementation, we proceed directly to keep it simple.
    await adminStore.removeStudentFromWhitelist(studentId);
};


const formatDate = (dateString) => {
  if (!dateString) return '';
  return format(new Date(dateString), 'MMM d, yyyy');
};
</script>
