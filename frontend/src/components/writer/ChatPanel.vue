<template>
  <div class="w-full h-full border rounded-lg flex flex-col bg-gray-50 dark:bg-gray-900">
    <div ref="chatContainer" class="flex-grow p-4 overflow-y-auto space-y-4">
      <div v-for="message in messages" :key="message.id" class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
        <div v-if="message.message_type === 'conversation'" class="p-3 rounded-lg max-w-xs break-words" :class="message.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200 dark:bg-gray-700'">
            <p class="text-sm">{{ message.message_text }}</p>
        </div>
      </div>
      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-gray-200 dark:bg-gray-700 p-3 rounded-lg animate-pulse">
            <p class="text-sm text-gray-400">...</p>
        </div>
      </div>
    </div>
    <div class="p-4 border-t bg-white dark:bg-gray-800">
      <input v-model="newMessage" @keyup.enter="sendMessage" :disabled="isLoading" type="text" :placeholder="placeholder" class="w-full p-2 border rounded-lg ...">
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
const props = defineProps({
  messages: Array,
  isLoading: Boolean,
  placeholder: String,
});
const emit = defineEmits(['send-message']);

const newMessage = ref('');
const chatContainer = ref(null);

const sendMessage = () => {
  if (!newMessage.value.trim()) return;
  emit('send-message', newMessage.value);
  newMessage.value = '';
};

watch(() => props.messages, () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
}, { deep: true });
</script>