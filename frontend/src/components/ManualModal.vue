<template>
  <!-- 
    This is a reusable modal component. 
    It appears as an overlay and can be closed by clicking the background or the 'X' button.
  -->
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex justify-center items-center p-4 transition-opacity duration-300" @click.self="close">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg w-full max-w-3xl max-h-[90vh] flex flex-col transform transition-transform duration-300 scale-95" :class="{ 'scale-100': show }">
      <!-- Modal Header -->
      <header class="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center flex-shrink-0">
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">{{ title }}</h2>
        <button @click="close" title="Close manual" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="text-gray-600 dark:text-gray-300" fill="currentColor" viewBox="0 0 256 256"><path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"></path></svg>
        </button>
      </header>
      <!-- Modal Content -->
      <main class="flex-grow overflow-y-auto p-6 prose dark:prose-invert max-w-none custom-scrollbar">
        <!-- The manual content will be injected here -->
        <div v-html="content"></div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { watch, onUnmounted } from 'vue';

// This component receives 'show', 'title', and 'content' as properties from its parent.
const props = defineProps({
  show: Boolean,
  title: String,
  content: String,
});

// Defines a custom event 'close' that the parent component can listen for.
const emit = defineEmits(['close']);

// Emits the 'close' event when the modal should be closed.
const close = () => {
  emit('close');
};

// This watcher adds/removes a class to the body to prevent background scrolling when the modal is open.
watch(() => props.show, (isShowing) => {
  if (isShowing) {
    document.body.classList.add('modal-open');
  } else {
    document.body.classList.remove('modal-open');
  }
});

// This ensures that if the component is ever removed from the DOM unexpectedly, the class is cleaned up.
onUnmounted(() => {
  document.body.classList.remove('modal-open');
});
</script>

<style>
/* These are basic styles to make the HTML from the manual content look good.
  They are scoped to the `.prose` class which is applied to the content area.
*/
.prose h1, .prose h2, .prose h3 { @apply font-bold mb-2; }
.prose h1 { @apply text-2xl; }
.prose h2 { @apply text-xl border-b border-gray-200 dark:border-gray-700 pb-2 mb-4; }
.prose h3 { @apply text-lg; }
.prose p { @apply mb-4 leading-relaxed; }
.prose ul, .prose ol { @apply list-inside mb-4 pl-2; }
.prose li { @apply mb-2; }
.prose code { @apply bg-gray-100 dark:bg-gray-700 rounded px-1 py-0.5 text-sm font-mono text-indigo-600 dark:text-indigo-400; }
.prose strong { @apply font-semibold; }
.prose a { @apply text-indigo-600 dark:text-indigo-400 hover:underline; }
.prose hr { @apply my-6 border-gray-200 dark:border-gray-700; }
/* This new style will make images in the manual responsive and visually appealing. */
.prose img { @apply rounded-lg shadow-md my-4 max-w-full h-auto; }
</style>

