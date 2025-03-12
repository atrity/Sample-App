<template>
  <div
    :class="[
      'relative flex items-start',
      inline ? 'inline-flex mr-4' : 'flex',
      className
    ]"
  >
    <div class="flex items-center h-5">
      <input
        :id="id"
        type="radio"
        :name="name"
        :value="value"
        :checked="isChecked"
        :disabled="disabled"
        class="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        v-bind="$attrs"
        @change="handleChange"
      >
    </div>
    <div class="ml-3 text-sm">
      <label
        v-if="label"
        :for="id"
        :class="[
          'font-medium select-none',
          disabled ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 cursor-pointer'
        ]"
      >
        {{ label }}
      </label>
      <p
        v-if="description"
        :class="[
          'text-gray-500',
          disabled ? 'text-gray-400' : ''
        ]"
      >
        {{ description }}
      </p>
    </div>

    <!-- Error Message -->
    <p
      v-if="error"
      class="mt-1 text-sm text-red-600"
    >
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean, Object],
    default: null
  },
  value: {
    type: [String, Number, Boolean, Object],
    required: true
  },
  name: {
    type: String,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  inline: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// Computed
const id = computed(() => {
  return `radio-${Math.random().toString(36).substr(2, 9)}`
})

const isChecked = computed(() => {
  return props.modelValue === props.value
})

// Methods
const handleChange = (event) => {
  if (event.target.checked) {
    emit('update:modelValue', props.value)
    emit('change', props.value)
  }
}
</script>

<style scoped>
/* Custom radio styles */
input[type='radio'] {
  @apply transition-colors duration-200;
}

input[type='radio']:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3ccircle cx='8' cy='8' r='3'/%3e%3c/svg%3e");
}

/* Hover effect */
input[type='radio']:not(:disabled):hover {
  @apply border-primary-500;
}

/* Focus ring */
input[type='radio']:focus {
  @apply ring-2 ring-offset-2 ring-primary-500;
}

/* Disabled state */
input[type='radio']:disabled {
  @apply bg-gray-100 border-gray-200;
}

/* Error state */
.radio-error input[type='radio'] {
  @apply border-red-300 focus:ring-red-500;
}

/* Animation */
.radio-enter-active,
.radio-leave-active {
  @apply transition-all duration-200;
}

.radio-enter-from,
.radio-leave-to {
  @apply opacity-0 scale-95;
}

/* Group styles */
.radio-group {
  @apply space-y-2;
}

.radio-group.inline {
  @apply space-y-0 space-x-4;
}

/* Custom radio button size variants */
.radio-sm input[type='radio'] {
  @apply h-3 w-3;
}

.radio-lg input[type='radio'] {
  @apply h-5 w-5;
}

/* Custom radio button color variants */
.radio-primary input[type='radio']:checked {
  @apply bg-primary-600 border-primary-600;
}

.radio-success input[type='radio']:checked {
  @apply bg-green-600 border-green-600;
}

.radio-danger input[type='radio']:checked {
  @apply bg-red-600 border-red-600;
}

.radio-warning input[type='radio']:checked {
  @apply bg-yellow-600 border-yellow-600;
}

.radio-info input[type='radio']:checked {
  @apply bg-blue-600 border-blue-600;
}
</style>
