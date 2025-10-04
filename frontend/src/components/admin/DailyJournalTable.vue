<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
    <div class="p-4">
      <h4 class="font-semibold text-gray-800 dark:text-gray-200">Daily Submissions</h4>
    </div>
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700/50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Student</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Group</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
            <th scope="col" class="relative px-6 py-3"><span class="sr-only">View</span></th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-if="journals.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
              No students to display.
            </td>
          </tr>
          <tr v-for="journal in journals" :key="journal.user_id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ journal.realname }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ journal.student_id }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ journal.group }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getPhaseClass(journal.writing_phase)">
                {{ journal.writing_phase || 'Not Started' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <router-link v-if="journal.journal_id" :to="`/admin/student/${journal.user_id}/journal/${journal.journal_date}`" class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300">View</router-link>
              <span v-else class="text-gray-400 dark:text-gray-500">N/A</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  journals: {
    type: Array,
    required: true,
  },
});

const getPhaseClass = (phase) => {
  switch (phase) {
    case 'scaffolding':
      return 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300';
    case 'writing':
      return 'bg-teal-100 text-teal-800 dark:bg-teal-900/50 dark:text-teal-300';
    case 'evaluation':
      return 'bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-300';
    case 'completed':
      return 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'; // Class for "Not Started"
  }
};
</script>

