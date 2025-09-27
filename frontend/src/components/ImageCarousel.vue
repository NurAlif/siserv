<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black bg-opacity-80 z-50 flex items-center justify-center p-4 transition-opacity duration-300"
    @click.self="close"
  >
    <!-- Close Button -->
    <button
      @click="close"
      title="Close"
      class="absolute top-4 right-4 p-2 rounded-full bg-black/50 text-white hover:bg-black/80 transition-colors z-10"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256">
        <path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"></path>
      </svg>
    </button>

    <!-- Main Content -->
    <div class="relative w-full flex flex-col items-center justify-center">
      <!-- Image Container -->
      <div class="relative flex-grow flex items-center justify-center w-full max-w-4xl max-h-[80vh]">
        <img :src="currentImageUrl" :alt="currentImage.ai_description" class="max-w-full max-h-full object-contain rounded-lg" />
      </div>
      <!-- Description -->
      <div v-if="currentImage.ai_description" class="flex-shrink-0 mt-4 p-2 bg-black/60 rounded-lg text-center max-w-4xl">
        <p class="text-white text-sm">{{ currentImage.ai_description }}</p>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <button
      v-if="images.length > 1"
      @click.stop="prevImage"
      title="Previous"
      class="absolute left-4 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black/50 text-white hover:bg-black/80 transition-colors"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256">
        <path d="M165.66,202.34a8,8,0,0,1-11.32,0L80,128,154.34,53.66a8,8,0,0,1,11.32,11.32L97.31,128l68.35,68.34A8,8,0,0,1,165.66,202.34Z"></path>
      </svg>
    </button>
    <button
      v-if="images.length > 1"
      @click.stop="nextImage"
      title="Next"
      class="absolute right-4 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black/50 text-white hover:bg-black/80 transition-colors"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256">
        <path d="M90.34,53.66a8,8,0,0,0-11.32,0l-80,80a8,8,0,0,0,0,11.32l80,80a8,8,0,0,0,11.32-11.32L17.31,128,90.34,53.66Z" transform="rotate(180, 128, 128)"></path>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import apiClient from '../services/api';

const props = defineProps({
  show: Boolean,
  images: {
    type: Array,
    required: true,
  },
  startIndex: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(['close']);

const currentIndex = ref(props.startIndex);

watch(() => props.startIndex, (newIndex) => {
  currentIndex.value = newIndex;
});

const currentImage = computed(() => props.images[currentIndex.value] || {});

const currentImageUrl = computed(() => {
  if (!currentImage.value || !currentImage.value.file_path) return '';
  const baseUrl = (apiClient.defaults.baseURL || '').replace('/api', '');
  return `${baseUrl}${currentImage.value.file_path}`;
});

const close = () => {
  emit('close');
};

const nextImage = () => {
  currentIndex.value = (currentIndex.value + 1) % props.images.length;
};

const prevImage = () => {
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length;
};
</script>

