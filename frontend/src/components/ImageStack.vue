<template>
  <div
    v-if="images && images.length > 0"
    @click="$emit('stack-clicked')"
    class="group absolute top-4 right-4 z-10 cursor-pointer flex items-center justify-center w-20 h-20"
    title="View attached images"
  >
    <!-- Stacked Images -->
    <img
      v-for="(image, index) in visibleImages"
      :key="image.id"
      :src="getImageUrl(image.file_path)"
      alt="Journal image thumbnail"
      class="absolute w-14 h-14 object-cover rounded-md border-2 border-white dark:border-gray-800 shadow-lg transition-transform duration-300 ease-in-out group-hover:shadow-xl"
      :style="{ transform: `rotate(${rotations[index]}deg) translate(${translations[index].x}px, ${translations[index].y}px)`, zIndex: 2 - index }"
    />
    <!-- Image Count Badge -->
    <div
      v-if="images.length > 1"
      class="absolute -top-1 -right-1 bg-indigo-600 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center border-2 border-white dark:border-gray-800"
      style="z-index: 3;"
    >
      {{ images.length }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import apiClient from '../services/api';

const props = defineProps({
  images: {
    type: Array,
    required: true,
  },
});

defineEmits(['stack-clicked']);

const getImageUrl = (filePath) => {
  if (!filePath) return '';
  // Construct the full URL to the static image file on the backend
  const baseUrl = (apiClient.defaults.baseURL || '').replace('/api', '');
  return `${baseUrl}${filePath}`;
};

// Show up to 3 images in the stack for visual effect
const visibleImages = computed(() => props.images.slice(0, 3).reverse());

// Pre-defined rotations and translations for a nice stacked effect
const rotations = [-10, 5, 15];
const translations = [
  { x: -5, y: 0 },
  { x: 5, y: 2 },
  { x: 0, y: -3 },
];

</script>
