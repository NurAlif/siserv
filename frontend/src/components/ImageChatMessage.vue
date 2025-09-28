<template>
  <div class="p-2 rounded-lg max-w-xs break-words bg-gray-200 dark:bg-gray-700">
    <img
      :src="imageUrl"
      alt="User upload"
      class="rounded-md cursor-pointer w-full object-cover"
      @click="$emit('image-clicked')"
      loading="lazy"
    />
    <p v-if="description" class="text-sm text-gray-800 dark:text-gray-200 mt-2 p-1 italic">
      "{{ description }}"
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import apiClient from '../services/api';

const props = defineProps({
  image: {
    type: Object,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
});

defineEmits(['image-clicked']);

const imageUrl = computed(() => {
  const path = props.image?.file_path;
  if (!path) return '';
  
  // FIX: Handle both local blob URLs for optimistic previews and server URLs.
  if (path.startsWith('blob:')) {
    return path;
  }
  
  // Construct the full URL to the static image file on the backend
  const baseUrl = (apiClient.defaults.baseURL || '').replace('/api', '');
  return `${baseUrl}${path}`;
});
</script>
