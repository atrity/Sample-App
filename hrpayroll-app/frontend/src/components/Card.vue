<template>
  <div
    :class="[
      'bg-white rounded-lg shadow',
      { 'overflow-hidden': !noPadding },
      className
    ]"
  >
    <!-- Card Header -->
    <div
      v-if="$slots.header || title"
      class="px-4 py-5 sm:px-6 border-b border-gray-200"
    >
      <slot name="header">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-medium text-gray-900">
              {{ title }}
            </h3>
            <p
              v-if="subtitle"
              class="mt-1 text-sm text-gray-500"
            >
              {{ subtitle }}
            </p>
          </div>
          <div v-if="$slots.headerActions">
            <slot name="headerActions"></slot>
          </div>
        </div>
      </slot>
    </div>

    <!-- Card Body -->
    <div
      :class="[
        { 'px-4 py-5 sm:p-6': !noPadding },
        bodyClass
      ]"
    >
      <slot></slot>
    </div>

    <!-- Card Footer -->
    <div
      v-if="$slots.footer"
      class="px-4 py-4 sm:px-6 bg-gray-50 border-t border-gray-200"
    >
      <slot name="footer"></slot>
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center"
    >
      <div class="text-center">
        <svg
          class="mx-auto h-12 w-12 text-primary-600 animate-spin"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        <p class="mt-2 text-sm text-gray-500">
          {{ loadingText }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: 'Loading...'
  },
  noPadding: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  },
  bodyClass: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.card-hover {
  @apply transition-shadow duration-300 ease-in-out;
}

.card-hover:hover {
  @apply shadow-lg;
}

/* Card variations */
.card-bordered {
  @apply border border-gray-200;
}

.card-compact {
  @apply p-2;
}

.card-flat {
  @apply shadow-none border border-gray-200;
}

/* Animation classes */
.card-enter-active,
.card-leave-active {
  @apply transition-all duration-300 ease-in-out;
}

.card-enter-from,
.card-leave-to {
  @apply opacity-0 transform scale-95;
}

.card-enter-to,
.card-leave-from {
  @apply opacity-100 transform scale-100;
}
</style>
