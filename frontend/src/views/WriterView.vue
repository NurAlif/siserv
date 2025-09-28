<template
  ><main
    id="writer-view"
    class="fade-in flex flex-col h-full w-full bg-white dark:bg-gray-800"
  >
    <!-- Hidden file input for image uploads -->
    <input
      ref="imageInput"
      type="file"
      @change="handleImageUpload"
      accept="image/*"
      class="hidden"
    />
    <!-- Fullscreen Image Carousel -->
    <ImageCarousel
      :show="isCarouselVisible"
      :images="carouselImages"
      :start-index="carouselStartIndex"
      @close="isCarouselVisible = false"
    />
    <!-- ================================== -->
    <!--  1. NEW COMPACT & ANIMATED HEADER  -->
    <!-- ================================== -->
    <div
      class="flex-shrink-0 p-2 flex justify-between items-center border-b border-gray-200 dark:border-gray-700"
    >
      <!-- Left Section: Navigation, Title, and Status -->
      <div class="flex items-center gap-2">
        <router-link
          to="/"
          title="Back to Dashboard"
          class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            fill="currentColor"
            viewBox="0 0 256 256"
          >
            <path
              d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"
            ></path>
          </svg>
        </router-link>
        <div>
          <h2
            class="text-sm font-bold text-gray-900 dark:text-gray-100 truncate"
          >
            {{ currentJournal?.title || 'New Journal Entry' }}
          </h2>
          <div
            class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2"
          >
            <span>{{ displayDate }}</span>
            <span class="mx-1">·</span>
            <span class="hidden sm:inline"
              >Status: <strong>{{ statusText }}</strong></span
            >
          </div>
        </div>
      </div>

      <!-- Right Section: Compact Phase Indicator -->
      <div class="flex items-center">
        <template v-for="(phase, index) in phases" :key="phase.id">
          <div class="flex items-center">
            <!-- Connector Line (appears after the first item) -->
            <div
              v-if="index > 0"
              class="w-6 h-0.5 rounded transition-colors"
              :class="getPhaseLineClass(phase.id)"
            ></div>
            <!-- Phase Circle with Tooltip -->
            <div
              @click="togglePhaseDescription(phase.id)"
              class="group relative cursor-pointer"
              title="Click to toggle phase description"
            >
              <div
                class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300"
                :class="getPhaseClass(phase.id)"
              >
                <svg
                  v-if="phase.id === 4"
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  fill="currentColor"
                  viewBox="0 0 256 256"
                >
                  <path
                    d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"
                  ></path></svg><span v-else>{{ phase.id }}</span>
              </div>
              <span
                class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-max opacity-0 group-hover:opacity-100 transition-opacity bg-gray-800 text-white text-xs font-semibold rounded-md py-1 px-2 pointer-events-none z-10"
              >
                {{ phase.name }}
              </span>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- ======================= -->
    <!--   2. MAIN CONTENT AREA  -->
    <!-- ======================= -->
    <div class="flex-grow overflow-hidden relative">
      <!-- A. Unified Layout for Scaffolding & Writing -->
      <div
        v-if="currentPhase === 'scaffolding' || currentPhase === 'writing'"
        class="h-full flex flex-col p-4 sm:p-8 gap-6"
      >
        <!-- Phase Banners -->
        <transition name="banner-fade">
          <div
            v-if="currentPhase === 'scaffolding' && isDescriptionVisible"
            class="relative flex-shrink-0 bg-indigo-50 dark:bg-indigo-900/50 p-4 rounded-lg"
          >
            <h3 class="font-bold text-indigo-800 dark:text-indigo-200">
              Phase 1: Let's build an outline!
            </h3>
            <p
              class="text-sm text-indigo-700 dark:text-indigo-300 mt-1 pr-8"
            >
              Answer Lingo's questions, write key points, or upload an image to get started.
            </p>
            <button
              @click="togglePhaseDescription()"
              class="absolute bottom-2 right-2 p-1 rounded-full hover:bg-indigo-100 dark:hover:bg-indigo-800/50 transition-colors"
              title="Toggle description"
            >
              <svg
                v-if="isDescriptionVisible"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="text-indigo-600 dark:text-indigo-300"
                viewBox="0 0 256 256"
              >
                <path
                  d="M213.66,165.66a8,8,0,0,1-11.32,0L128,91.31,53.66,165.66a8,8,0,0,1-11.32-11.32l80-80a8,8,0,0,1,11.32,0l80,80A8,8,0,0,1,213.66,165.66Z"
                ></path></svg><svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="text-indigo-600 dark:text-indigo-300"
                viewBox="0 0 256 256"
              >
                <path
                  d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80a8,8,0,0,1,11.32-11.32L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"
                ></path>
              </svg>
            </button>
          </div>
        </transition>
        <transition name="banner-fade">
          <div
            v-if="currentPhase === 'writing' && isDescriptionVisible"
            class="relative flex-shrink-0 bg-green-50 dark:bg-green-900/50 p-4 rounded-lg"
          >
            <h3 class="font-bold text-green-800 dark:text-green-200">
              Phase 2: Write your draft
            </h3>
            <p class="text-sm text-green-700 dark:text-green-300 mt-1 pr-8">
              Use your outline to write your journal entry. Your writing
              partner, Lingo, is here to help if you get stuck.
            </p>
            <button
              @click="togglePhaseDescription()"
              class="absolute bottom-2 right-2 p-1 rounded-full hover:bg-green-100 dark:hover:bg-green-800/50 transition-colors"
              title="Toggle description"
            >
              <svg
                v-if="isDescriptionVisible"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="text-green-600 dark:text-green-300"
                viewBox="0 0 256 256"
              >
                <path
                  d="M213.66,165.66a8,8,0,0,1-11.32,0L128,91.31,53.66,165.66a8,8,0,0,1-11.32-11.32l80-80a8,8,0,0,1,11.32,0l80,80A8,8,0,0,1,213.66,165.66Z"
                ></path></svg><svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="text-green-600 dark:text-green-300"
                viewBox="0 0 256 256"
              >
                <path
                  d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80a8,8,0,0,1,11.32-11.32L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"
                ></path>
              </svg>
            </button>
          </div>
        </transition>

        <!-- Mobile View Switcher (Tabs) -->
        <div
          class="md:hidden flex-shrink-0 flex border border-gray-300 dark:border-gray-600 rounded-lg p-1 bg-gray-100 dark:bg-gray-900"
        >
          <button
            @click="mobileView = 'main'"
            :class="[
              mobileView === 'main'
                ? 'bg-indigo-600 text-white shadow'
                : 'text-gray-600 dark:text-gray-300',
              'flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out',
            ]"
          >
            <span v-if="currentPhase === 'scaffolding'">📝 Outline</span
            ><span v-else>📝 Writer</span>
          </button>
          <button
            @click="mobileView = 'chat'"
            :class="[
              mobileView === 'chat'
                ? 'bg-indigo-600 text-white shadow'
                : 'text-gray-600 dark:text-gray-300',
              'flex-1 p-2 rounded-md font-semibold text-sm transition-all duration-200 ease-in-out',
            ]"
          >
            🤖 Lingo Chat
          </button>
        </div>

        <!-- Main Grid for Desktop & Mobile content -->
        <div class="flex-grow overflow-hidden grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Left Column: Outline / Writer -->
          <div
            class="relative flex flex-col gap-4 min-h-0"
            :class="{ 'hidden md:flex': mobileView !== 'main' }"
          >
            <!-- NEW: Image Stack Display -->
            <ImageStack
              v-if="currentJournal?.images?.length > 0"
              :images="currentJournal.images"
              @stack-clicked="openCarousel(currentJournal.images[0].id)"
            />
            <!-- Scaffolding View -->
            <template v-if="currentPhase === 'scaffolding'">
              <div
                class="flex-shrink-0 space-y-2 text-sm text-gray-600 dark:text-gray-300"
              >
                <p><strong>Guiding questions:</strong></p>
                <ul
                  class="list-disc list-inside bg-gray-50 dark:bg-gray-700/50 p-3 rounded-md"
                >
                  <li>What was the most memorable part of your day?</li>
                  <li>Did you learn or try something new?</li>
                </ul>
              </div>
              <textarea
                v-model="outlineContent"
                placeholder="Write down your main ideas or key points here..."
                class="flex-grow w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
              >
              </textarea>
            </template>
            <!-- Writing View -->
            <template v-if="currentPhase === 'writing'">
              <div
                class="flex-shrink-0 bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border dark:border-gray-700"
              >
                <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Your Outline
                </h4>
                <div
                  class="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap max-h-24 overflow-y-auto custom-scrollbar"
                >
                  {{ outlineContent || 'No outline was created.' }}
                </div>
              </div>
              <textarea
                v-model="content"
                class="flex-grow w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none transition bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
              ></textarea>
            </template>
          </div>

          <!-- Right Column: UNIFIED CHAT PANEL -->
          <div
            class="flex flex-col min-h-0"
            :class="{ 'hidden md:flex': mobileView !== 'chat' }"
          >
            <div
              class="flex-grow w-full border border-gray-300 dark:border-gray-600 rounded-lg flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden"
            >
              <div
                class="p-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between flex-shrink-0"
              >
                <div class="flex items-center gap-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    class="text-indigo-500 dark:text-indigo-400"
                    fill="currentColor"
                    viewBox="0 0 256 256"
                  >
                    <path
                      d="M128,24A104,104,0,0,0,36.18,176.88L24.83,212.3a16,16,0,0,0,20.55,18.85l37.81-12.6A104,104,0,1,0,128,24Zm0,192a88.1,88.1,0,0,1-45.43-13.25a8,8,0,0,0-9-1.33L40,211.52l9.9-32.68a8,8,0,0,0-1.12-8.52A88,88,0,1,1,128,216Z"
                    ></path>
                  </svg>
                  <h4 class="font-semibold text-gray-800 dark:text-gray-200">
                    Lingo Chat
                  </h4>
                </div>
                <!-- Controls: Camera button and correction toggle -->
                <div class="flex items-center gap-3">
                  <button
                    @click="triggerImageUpload"
                    :disabled="journalStore.isUploading || currentPhase !== 'scaffolding'"
                    title="Add Image from Device"
                    class="p-1.5 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      fill="currentColor"
                      class="text-gray-600 dark:text-gray-300"
                      viewBox="0 0 256 256"
                    >
                      <path
                        d="M208,56H180.28L166.65,35.56A16,16,0,0,0,152.28,24H103.72a16,16,0,0,0-14.37,11.56L75.72,56H48A24,24,0,0,0,24,80V192a24,24,0,0,0,24,24H208a24,24,0,0,0,24-24V80A24,24,0,0,0,208,56Zm16,136a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V80a8,8,0,0,1,8-8h32a8,8,0,0,0,7.18-4.44l13.63-20.44a.18.18,0,0,1,0-.05H152.28a.18.18,0,0,1,0,.05l13.63,20.44A8,8,0,0,0,173.09,72H208a8,8,0,0,1,8,8ZM128,88a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,88Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,168Z"
                      ></path>
                    </svg>
                  </button>
                  <label
                    for="correction-toggle"
                    class="flex items-center cursor-pointer"
                  >
                    <span class="mr-2 text-xs text-gray-500 dark:text-gray-400"
                      >Correct</span
                    >
                    <div class="relative">
                      <input
                        type="checkbox"
                        id="correction-toggle"
                        class="sr-only"
                        v-model="isCorrectionModeEnabled"
                      />
                      <div
                        class="block bg-gray-200 dark:bg-gray-600 w-10 h-6 rounded-full"
                      ></div>
                      <div
                        class="dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform"
                      ></div>
                    </div>
                  </label>
                </div>
              </div>
              <div
                ref="chatContainer"
                class="flex-grow p-4 overflow-y-auto space-y-4 custom-scrollbar"
              >
                <!-- Existing messages -->
                <template
                  v-for="message in currentJournal?.chat_messages"
                  :key="message.id"
                >
                  <!-- Conversation Text Message -->
                  <div
                    v-if="message.message_type === 'conversation'"
                    class="flex"
                    :class="
                      message.sender === 'user'
                        ? 'justify-end'
                        : 'justify-start'
                    "
                  >
                    <div
                      class="p-3 rounded-lg max-w-xs break-words"
                      :class="{
                        'bg-indigo-500 text-white chat-bubble-user':
                          message.sender === 'user',
                        'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 chat-bubble-ai':
                          message.sender !== 'user',
                      }"
                    >
                      <p class="text-sm">{{ message.message_text }}</p>
                    </div>
                  </div>
                  <!-- Image Message -->
                  <div
                    v-else-if="
                      message.message_type === 'image' && message.image
                    "
                    class="flex"
                    :class="
                      message.sender === 'user'
                        ? 'justify-end'
                        : 'justify-start'
                    "
                  >
                    <ImageChatMessage
                      :image="message.image"
                      :description="message.message_text"
                      @image-clicked="openCarousel(message.image.id)"
                    />
                  </div>
                  <!-- Feedback Message -->
                  <div
                    v-else-if="message.message_type === 'feedback'"
                    class="flex justify-start"
                  >
                    <ChatFeedbackCard :message="message" />
                  </div>
                </template>
                <!-- Loading Indicators -->
                <div v-if="aiStore.isLoading" class="flex justify-start">
                  <div
                    class="bg-gray-200 dark:bg-gray-700 p-3 rounded-lg animate-pulse chat-bubble-ai"
                  >
                    <p class="text-sm text-gray-400">...</p>
                  </div>
                </div>
                <div v-if="journalStore.isUploading" class="flex justify-start">
                  <div
                    class="p-3 rounded-lg max-w-xs break-words bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 italic animate-pulse"
                  >
                    <p class="text-sm">Uploading image...</p>
                  </div>
                </div>
              </div>
              <!-- NEW: Captioning Prompt -->
              <div v-if="captioningImage" class="p-2 border-t border-gray-200 dark:border-gray-700 bg-indigo-50 dark:bg-indigo-900/50 flex items-center gap-3 transition-all flex-shrink-0">
                <img :src="getImageUrl(captioningImage.file_path)" alt="caption preview" class="w-12 h-12 object-cover rounded-md">
                <div class="flex-grow">
                  <p class="text-sm font-semibold text-indigo-800 dark:text-indigo-200">Image added!</p>
                  <p class="text-xs text-indigo-700 dark:text-indigo-300">Type your caption in the box below and press send.</p>
                </div>
                <button @click="captioningImage = null" title="Cancel caption" class="p-1.5 rounded-full hover:bg-indigo-100 dark:hover:bg-indigo-800">
                   <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="text-indigo-600 dark:text-indigo-300" viewBox="0 0 256 256"><path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"></path></svg>
                </button>
              </div>
              <div
                class="p-2 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 flex-shrink-0"
              >
                <div class="relative">
                  <input
                    v-model="newMessage"
                    @keyup.enter="sendMessage"
                    :disabled="isChatDisabled"
                    type="text"
                    :placeholder="chatPlaceholder"
                    class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:outline-none disabled:bg-gray-100 dark:disabled:bg-gray-700 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 pr-28"
                  />
                  <span
                    class="absolute right-12 top-1/2 -translate-y-1/2 text-xs text-gray-400 dark:text-gray-500 pointer-events-none"
                  >
                    {{ chatTurnCount }} / {{ MAX_CHAT_TURNS }}
                  </span>
                  <button
                    @click="sendMessage"
                    :disabled="!newMessage.trim()"
                    class="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded-full transition-colors bg-indigo-600 text-white hover:bg-indigo-700 disabled:bg-gray-300 dark:disabled:bg-gray-500 disabled:cursor-not-allowed"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="18"
                      height="18"
                      fill="currentColor"
                      viewBox="0 0 256 256"
                    >
                      <path
                        d="M231.72,122.53,46.3,27.11a8,8,0,0,0-10.83,10.83L60.89,128,35.47,218.06a8,8,0,0,0,5.46,10.2,7.92,7.92,0,0,0,5.37.17L231.72,133.47a8,8,0,0,0,0-10.94Z"
                      ></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- B. Standard scrolling container for other phases -->
      <div
        v-if="currentPhase !== 'scaffolding' && currentPhase !== 'writing'"
        class="absolute inset-0 h-full overflow-y-auto custom-scrollbar"
      >
        <!-- Phase 3: Evaluation -->
        <div v-if="currentPhase === 'evaluation'" class="p-8">
          <transition name="banner-fade">
            <div
              v-if="isDescriptionVisible"
              class="relative bg-rose-50 dark:bg-rose-900/50 p-4 rounded-lg mb-4"
            >
              <h3 class="font-bold text-rose-800 dark:text-rose-200">
                Phase 3: Review Your Evaluation
              </h3>
              <p class="text-sm text-rose-700 dark:text-rose-300 mt-1 pr-8">
                Review the AI's suggestions below to improve your grammar,
                vocabulary, and style. Your original text is highlighted with
                suggestions.
              </p>
              <button
                @click="togglePhaseDescription()"
                class="absolute bottom-2 right-2 p-1 rounded-full hover:bg-rose-100 dark:hover:bg-rose-800/50 transition-colors"
                title="Toggle description"
              >
                <svg
                  v-if="isDescriptionVisible"
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="text-rose-600 dark:text-rose-300"
                  viewBox="0 0 256 256"
                >
                  <path
                    d="M213.66,165.66a8,8,0,0,1-11.32,0L128,91.31,53.66,165.66a8,8,0,0,1-11.32-11.32l80-80a8,8,0,0,1,11.32,0l80,80A8,8,0,0,1,213.66,165.66Z"
                  ></path></svg><svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="text-rose-600 dark:text-rose-300"
                  viewBox="0 0 256 256"
                >
                  <path
                    d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80a8,8,0,0,1,11.32-11.32L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"
                  ></path>
                </svg>
              </button>
            </div>
          </transition>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-2">
              <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Your Corrected Text
              </h4>
              <div
                v-html="highlightedContent"
                class="w-full h-[30rem] p-4 border border-gray-300 dark:border-gray-600 rounded-lg overflow-y-auto bg-gray-50 dark:bg-gray-700/50 whitespace-pre-wrap custom-scrollbar"
              ></div>
            </div>
            <div class="md:col-span-1">
              <h4 class="font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Suggestions
              </h4>
              <div id="ai-feedback-section" class="space-y-3">
                <div v-if="aiStore.isLoading" class="text-center py-4">
                  <p class="text-gray-500 dark:text-gray-400 animate-pulse">
                    Analyzing your text...
                  </p>
                </div>
                <div
                  v-else-if="aiStore.error"
                  class="bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300 p-4 rounded-lg"
                >
                  <p>{{ aiStore.error }}</p>
                </div>
                <div v-else-if="aiStore.feedback.length > 0">
                  <AIFeedbackCard
                    v-for="(item, index) in aiStore.feedback"
                    :key="index"
                    :feedback-item="item"
                    :is-applied="
                      appliedSuggestions.includes(item.incorrect_phrase)
                    "
                    @apply-suggestion="applySuggestion"
                  />
                </div>
                <div
                  v-else
                  class="text-center py-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
                >
                  <p class="text-gray-600 dark:text-gray-300 font-semibold">
                    Great job!
                  </p>
                  <p class="text-gray-500 dark:text-gray-400">
                    The AI didn't find any specific errors to correct.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Phase 4: Completed -->
        <div v-if="currentPhase === 'completed'" class="p-8 text-center">
          <div class="max-w-md mx-auto">
            <div
              class="bg-green-100 text-green-700 w-16 h-16 rounded-full flex items-center justify-center mx-auto"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="40"
                height="40"
                fill="currentColor"
                viewBox="0 0 256 256"
              >
                <path
                  d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"
                ></path>
              </svg>
            </div>
            <h3
              class="text-2xl font-bold mt-4 text-gray-900 dark:text-gray-100"
            >
              Journal Completed!
            </h3>
            <p class="text-gray-600 dark:text-gray-400 mt-2">
              Excellent work! You've finished this entry. All your learning
              points have been saved to your progress hub.
            </p>
            <div class="mt-6">
              <div
                class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg border dark:border-gray-700 text-left"
              >
                <h4
                  class="font-semibold text-gray-700 dark:text-gray-300 mb-2"
                >
                  Your Final Entry
                </h4>
                <div
                  class="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap"
                >
                  {{ content }}
                </div>
              </div>
              <!-- Image Stack moved below the text box and made larger -->
              <div
                v-if="currentJournal?.images?.length > 0"
                class="mt-8"
              >
                <ImageStack
                  :images="currentJournal.images"
                  @stack-clicked="openCarousel(currentJournal.images[0].id)"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ======================= -->
    <!-- 3. ACTION FOOTER        -->
    <!-- ======================= -->
    <div
      class="flex-shrink-0 p-4 border-t border-gray-200 dark:border-gray-700"
    >
      <div
        v-if="currentPhase === 'scaffolding'"
        class="flex flex-col sm:flex-row justify-end items-center gap-2"
      >
        <span class="text-xs text-gray-500 dark:text-gray-400">
          {{ outlineStats.count }} / {{ outlineStats.min }} items complete
        </span>
        <div class="w-full sm:w-auto">
          <transition name="action-button">
            <button
              v-if="outlineStats.isComplete"
              @click="moveToPhase('writing')"
              class="w-full sm:w-auto bg-indigo-600 text-white font-semibold px-5 py-1.5 text-sm rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Start Writing
            </button>
          </transition>
        </div>
      </div>

      <div
        v-if="currentPhase === 'writing'"
        class="flex flex-col sm:flex-row justify-end items-center gap-2"
      >
        <span class="text-xs text-gray-500 dark:text-gray-400">
          Words: {{ writingStats.words }} / {{ writingStats.minWords }} |
          Sentences: {{ writingStats.sentences }} /
          {{ writingStats.minSentences }}
        </span>
        <div class="w-full sm:w-auto">
          <transition name="action-button">
            <button
              v-if="writingStats.isComplete"
              @click="moveToPhase('evaluation')"
              class="w-full sm:w-auto bg-teal-500 text-white font-semibold px-5 py-1.5 text-sm rounded-lg hover:bg-teal-600 transition-colors"
            >
              Evaluate Writing
            </button>
          </transition>
        </div>
      </div>

      <div
        v-if="currentPhase === 'evaluation'"
        class="flex flex-col sm:flex-row sm:justify-between items-center gap-2"
      >
        <div class="flex w-full sm:w-auto gap-2">
          <button
            @click="saveJournal()"
            :disabled="journalStore.isLoading"
            class="w-1/2 sm:w-auto bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold px-4 py-1.5 text-sm rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
          >
            {{ journalStore.isLoading ? 'Saving...' : 'Save Changes' }}
          </button>
          <button
            @click="moveToPhase('writing')"
            class="w-1/2 sm:w-auto bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold px-4 py-1.5 text-sm rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
          >
            Back to Writing
          </button>
        </div>
        <div class="w-full sm:w-auto">
          <transition name="action-button">
            <button
              v-if="allSuggestionsApplied"
              @click="moveToPhase('completed')"
              class="w-full sm:w-auto bg-green-600 text-white font-semibold px-5 py-1.5 text-sm rounded-lg hover:bg-green-700 transition-colors"
            >
              Mark as Complete
            </button>
          </transition>
        </div>
      </div>

      <div
        v-if="currentPhase === 'completed'"
        class="flex justify-center gap-4"
      >
        <router-link
          to="/"
          class="bg-indigo-600 text-white font-semibold px-5 py-1.5 text-sm rounded-lg hover:bg-indigo-700 transition-colors"
        >
          Back to Dashboard
        </router-link>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useJournalStore } from '../stores/journalStore';
import { useAiStore } from '../stores/aiStore';
import { format } from 'date-fns';
import apiClient from '../services/api'; // Import apiClient
import AIFeedbackCard from '../components/AIFeedbackCard.vue';
import ChatFeedbackCard from '../components/ChatFeedbackCard.vue';
import ImageChatMessage from '../components/ImageChatMessage.vue';
import ImageCarousel from '../components/ImageCarousel.vue';
import ImageStack from '../components/ImageStack.vue';

// --- Constants for validation and limits ---
const MIN_SCAFFOLD_ITEMS = 5;
const MIN_WRITING_WORDS = 50;
const MIN_WRITING_SENTENCES = 3;
const MAX_CHAT_TURNS = 40;

const route = useRoute();
const router = useRouter();
const journalStore = useJournalStore();
const aiStore = useAiStore();

const currentJournal = computed(() =>
  journalStore.getJournalByDate(route.params.date)
);
const currentPhase = computed(
  () => currentJournal.value?.writing_phase || 'scaffolding'
);

// --- Image State ---
const imageInput = ref(null);
const isCarouselVisible = ref(false);
const carouselImages = ref([]);
const carouselStartIndex = ref(0);
const captioningImage = ref(null); // Will hold { id, file_path } for the image being captioned

const mobileView = ref('main');
const isCorrectionModeEnabled = ref(true);

const content = ref('');
const outlineContent = ref('');
const statusText = ref('Saved');
const newMessage = ref('');
const chatContainer = ref(null);
const appliedSuggestions = ref([]);
const saveTimeout = ref(null);
const isDescriptionVisible = ref(true);
const descriptionTimeout = ref(null);

const phases = ref([
  { id: 1, name: 'Scaffolding' },
  { id: 2, name: 'Writing' },
  { id: 3, name: 'Evaluation' },
  { id: 4, name: 'Completed' },
]);

const displayDate = computed(() => {
  if (currentJournal.value) {
    return journalStore.formatDisplayDate(currentJournal.value.journal_date);
  }
  return format(new Date(), 'MMMM d, yyyy');
});

// --- Validation and Limit Computeds ---
const wordCount = (str) => {
  if (!str) return 0;
  return str.trim().split(/\s+/).filter(Boolean).length;
};

const sentenceCount = (str) => {
  if (!str) return 0;
  const matches = str.match(/[.!?…]+(\s|$)/g);
  return matches ? matches.length : 0;
};

const outlineStats = computed(() => {
  const count = outlineContent.value
    .split('\n')
    .filter((line) => line.trim() !== '').length;
  return {
    count,
    min: MIN_SCAFFOLD_ITEMS,
    isComplete: count >= MIN_SCAFFOLD_ITEMS,
  };
});

const writingStats = computed(() => {
  const words = wordCount(content.value);
  const sentences = sentenceCount(content.value);
  return {
    words,
    sentences,
    minWords: MIN_WRITING_WORDS,
    minSentences: MIN_WRITING_SENTENCES,
    isComplete:
      words >= MIN_WRITING_WORDS && sentences >= MIN_WRITING_SENTENCES,
  };
});

const chatTurnCount = computed(() => {
  if (!currentJournal.value || !currentJournal.value.chat_messages) return 0;
  return currentJournal.value.chat_messages.filter(
    (m) => m.message_type === 'conversation'
  ).length;
});

const isChatDisabled = computed(() => {
  return (
    aiStore.isLoading ||
    !currentJournal.value ||
    chatTurnCount.value >= MAX_CHAT_TURNS
  );
});

const chatPlaceholder = computed(() => {
  if (captioningImage.value) {
    return 'Add a caption for your new image...';
  }
  if (chatTurnCount.value >= MAX_CHAT_TURNS) {
    return 'Chat turn limit reached.';
  }
  if (currentPhase.value === 'scaffolding') {
    return 'Not sure what to write about? Chat here!';
  }
  if (currentPhase.value === 'writing') {
    return "Ask for help, e.g., 'What should I write next?'";
  }
  return 'Type your message...';
});

// --- Image Handling Methods ---
const triggerImageUpload = () => {
  imageInput.value?.click();
};

const handleImageUpload = async (event) => {
  if (!event.target.files || !currentJournal.value) return;
  const file = event.target.files[0];
  if (!file) return;

  const updatedJournal = await journalStore.uploadImage(currentJournal.value.journal_date, file);
  event.target.value = ''; // Reset file input to allow re-uploading the same file

  if (updatedJournal && updatedJournal.images.length > 0) {
    const newImage = updatedJournal.images[updatedJournal.images.length - 1];
    captioningImage.value = { id: newImage.id, file_path: newImage.file_path };
  }
};

const getImageUrl = (filePath) => {
    if (!filePath) return '';
    if (filePath.startsWith('blob:')) return filePath;
    const baseUrl = (apiClient.defaults.baseURL || '').replace('/api', '');
    return `${baseUrl}${filePath}`;
};

const openCarousel = (imageId) => {
  if (!currentJournal.value?.images) return;
  carouselImages.value = currentJournal.value.images;
  const index = carouselImages.value.findIndex((img) => img.id === imageId);
  carouselStartIndex.value = index >= 0 ? index : 0;
  isCarouselVisible.value = true;
};

const loadJournalData = async () => {
  const date = route.params.date;
  if (date) {
    await journalStore.fetchJournalByDate(date);
  } else {
    const today = format(new Date(), 'yyyy-MM-dd');
    const existing = journalStore.getJournalByDate(today);
    if (!existing) {
      const newJournal = await journalStore.createJournal('');
      if (newJournal) {
        router.replace(`/writer/${newJournal.journal_date}`);
      }
    } else {
      router.replace(`/writer/${today}`);
    }
  }
};

onMounted(loadJournalData);

onUnmounted(() => {
  if (saveTimeout.value) {
    clearTimeout(saveTimeout.value);
  }
  if (descriptionTimeout.value) {
    clearTimeout(descriptionTimeout.value);
  }
});

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

const startDescriptionTimer = () => {
  if (descriptionTimeout.value) clearTimeout(descriptionTimeout.value);
  isDescriptionVisible.value = true;
  descriptionTimeout.value = setTimeout(() => {
    isDescriptionVisible.value = false;
  }, 30000); // 30 seconds
};

watch(
  currentJournal,
  (newJournal, oldJournal) => {
    if (newJournal) {
      content.value = newJournal.content || '';
      outlineContent.value = newJournal.outline_content || '';
      appliedSuggestions.value = [];

      if (
        newJournal.writing_phase === 'evaluation' &&
        (!aiStore.feedback.length || aiStore.error)
      ) {
        aiStore.getFeedback(newJournal.journal_date, newJournal.content);
      }
      scrollToBottom();

      if (
        !oldJournal ||
        newJournal.writing_phase !== oldJournal.writing_phase
      ) {
        startDescriptionTimer();
      }
    }
  },
  { deep: true, immediate: true }
);

watch(
  () => currentJournal.value?.chat_messages.length,
  () => {
    scrollToBottom();
  }
);

watch(content, (newValue, oldValue) => {
  if (currentPhase.value === 'writing' && newValue !== oldValue) {
    statusText.value = 'Saving...';
    if (saveTimeout.value) clearTimeout(saveTimeout.value);
    saveTimeout.value = setTimeout(() => {
      saveJournal(true);
    }, 5000);
  }
});

const saveJournal = async (showStatus = true) => {
  if (!currentJournal.value) return;
  const payload = {
    content: content.value,
    outline_content: outlineContent.value,
  };
  const savedJournal = await journalStore.updateJournal(
    currentJournal.value.journal_date,
    payload
  );
  if (showStatus) {
    statusText.value = savedJournal ? 'All changes saved!' : 'Error saving.';
  }
};

const moveToPhase = async (phase) => {
  // Front-end validation as a safeguard, though buttons are disabled.
  if (
    currentPhase.value === 'scaffolding' &&
    phase === 'writing' &&
    !outlineStats.value.isComplete
  )
    return;
  if (
    currentPhase.value === 'writing' &&
    phase === 'evaluation' &&
    !writingStats.value.isComplete
  )
    return;

  if (!currentJournal.value) return;
  if (saveTimeout.value) clearTimeout(saveTimeout.value);
  await saveJournal(false);
  await journalStore.updateJournalPhase(
    currentJournal.value.journal_date,
    phase
  );
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;
  
  const imageIdForMessage = captioningImage.value ? captioningImage.value.id : null;
  
  if (imageIdForMessage) {
    captioningImage.value = null; // Clear captioning state immediately
  }

  await saveJournal(false);

  const messageToSend = newMessage.value;
  newMessage.value = '';

  aiStore.chatWithAI(
    currentJournal.value.journal_date,
    messageToSend,
    isCorrectionModeEnabled.value,
    imageIdForMessage
  );
};

const highlightedContent = computed(() => {
  if (currentPhase.value !== 'evaluation' || !aiStore.feedback.length) {
    return content.value;
  }
  let tempContent = content.value;
  const sortedFeedback = [...aiStore.feedback].sort(
    (a, b) => b.incorrect_phrase.length - a.incorrect_phrase.length
  );
  sortedFeedback.forEach((item) => {
    if (!appliedSuggestions.value.includes(item.incorrect_phrase)) {
      const regex = new RegExp(escapeRegExp(item.incorrect_phrase), 'g');
      tempContent = tempContent.replace(
        regex,
        `<span class="bg-yellow-200 dark:bg-yellow-400/30 rounded px-1">${item.incorrect_phrase}</span>`
      );
    }
  });
  return tempContent;
});

const applySuggestion = (feedbackItem) => {
  content.value = content.value.replace(
    feedbackItem.incorrect_phrase,
    feedbackItem.suggestion
  );
  appliedSuggestions.value.push(feedbackItem.incorrect_phrase);
};

const allSuggestionsApplied = computed(() => {
  if (!aiStore.feedback || aiStore.feedback.length === 0) return true;
  return appliedSuggestions.value.length >= aiStore.feedback.length;
});

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const phaseMap = { scaffolding: 1, writing: 2, evaluation: 3, completed: 4 };

const togglePhaseDescription = (phaseId) => {
  if (phaseId && phaseMap[currentPhase.value] !== phaseId) return;
  if (isDescriptionVisible.value) {
    isDescriptionVisible.value = false;
    if (descriptionTimeout.value) clearTimeout(descriptionTimeout.value);
  } else {
    startDescriptionTimer();
  }
};

const getPhaseClass = (phaseId) => {
  const phaseValue = phaseMap[currentPhase.value];
  if (phaseValue === 4) {
    return 'bg-green-500 text-white scale-100';
  }
  if (phaseValue > phaseId) return 'bg-green-500 text-white scale-100';
  if (phaseValue === phaseId)
    return 'bg-indigo-600 text-white scale-110 shadow-lg';
  return 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 scale-100';
};

const getPhaseLineClass = (phaseId) => {
  if (phaseMap[currentPhase.value] >= phaseId) return 'bg-green-500';
  return 'bg-gray-200 dark:bg-gray-700';
};
</script>

<style>
#correction-toggle:checked ~ .dot {
  transform: translateX(100%);
  background-color: #4f46e5;
}
#correction-toggle:checked ~ .block {
  background-color: #c7d2fe;
}
.dark #correction-toggle:checked ~ .block {
  background-color: #3730a3;
}
.banner-fade-enter-active,
.banner-fade-leave-active {
  transition: all 0.4s ease-in-out;
  max-height: 120px;
  overflow: hidden;
}
.banner-fade-enter-from,
.banner-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
  margin-top: 0;
  margin-bottom: 0;
}
.action-button-enter-active,
.action-button-leave-active {
  /* Be specific about what to transition to avoid conflicts */
  transition: opacity 0.3s ease-out, transform 0.3s ease-out;
  /* Hint to the browser to optimize animations */
  will-change: opacity, transform;
}
.action-button-enter-from,
.action-button-leave-to {
  opacity: 0;
  transform: translateY(10px); /* A slightly more subtle effect */
}
/* UPDATED: Chat bubble notch styles */
.chat-bubble-user {
    position: relative;
    margin-right: 10px;
    /* rounded-lg is on the element, this makes the notch corner sharper */
    border-top-right-radius: 0.25rem;
}
.chat-bubble-ai {
    position: relative;
    margin-left: 10px;
    /* rounded-lg is on the element, this makes the notch corner sharper */
    border-top-left-radius: 0.25rem;
}

/* User bubble notch (points right) */
.chat-bubble-user::after {
    content: '';
    position: absolute;
    top: 10px;
    right: -10px;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 5px 0 5px 10px; /* t r b l */
    border-color: transparent transparent transparent #4f46e5; /* Tailwind's indigo-500 */
}

/* AI bubble notch (points left) */
.chat-bubble-ai::after {
    content: '';
    position: absolute;
    top: 10px;
    left: -10px;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 5px 10px 5px 0; /* t r b l */
    border-color: transparent #e5e7eb transparent transparent; /* Tailwind's gray-200 */
}

/* Dark mode style for AI bubble notch */
.dark .chat-bubble-ai::after {
    border-color: transparent #374151 transparent transparent; /* Tailwind's gray-700 */
}
</style>
