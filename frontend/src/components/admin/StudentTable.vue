<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
    <div class="p-4">
      <h4 class="font-semibold text-gray-800 dark:text-gray-200">Students</h4>
    </div>
    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
      <thead class="bg-gray-50 dark:bg-gray-700/50">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Student Info</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Journals</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Errors</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Last Active</th>
          <th scope="col" class="relative px-6 py-3"><span class="sr-only">View</span></th>
        </tr>
      </thead>
      <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
        <tr v-for="student in students" :key="student.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ student.realname }} ({{ student.username }}) [{{ student.group }}]</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">{{ student.student_id }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">{{ student.email }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ student.journal_count }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ student.total_errors }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ formatDate(student.last_active) }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <router-link :to="`/admin/student/${student.id}`" class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300">View</router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { formatDistanceToNow } from 'date-fns';

defineProps({
  students: {
    type: Array,
    required: true,
  },
});

const formatDate = (dateString) => {
  if (!dateString) return 'Never';
  return formatDistanceToNow(new Date(dateString), { addSuffix: true });
};
</script>