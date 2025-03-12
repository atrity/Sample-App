<template>
  <div
    :class="[
      'flex items-center justify-center',
      fullScreen ? 'fixed inset-0 bg-gray-900 bg-opacity-50 z-50' : 'p-4'
    ]"
  >
    <div class="text-center">
      <!-- Spinner -->
      <div class="spinner mb-4" :class="size"></div>
      
      <!-- Message -->
      <p v-if="message" class="text-gray-100 font-medium">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  fullScreen: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  message: {
    type: String,
    default: ''
  }
})

const spinnerSize = computed(() => {
  const sizes = {
    small: 'w-6 h-6 border-2',
    medium: 'w-10 h-10 border-3',
    large: 'w-16 h-16 border-4'
  }
  return sizes[props.size]
})
</script>

<style scoped>
.spinner {
  @apply animate-spin rounded-full;
  border-top-color: theme('colors.primary.500');
  border-right-color: theme('colors.primary.500');
  border-bottom-color: theme('colors.primary.500');
  border-left-color: transparent;
}

.spinner.small {
  @apply w-6 h-6 border-2;
}

.spinner.medium {
  @apply w-10 h-10 border-3;
}

.spinner.large {
  @apply w-16 h-16 border-4;
}
</style>
