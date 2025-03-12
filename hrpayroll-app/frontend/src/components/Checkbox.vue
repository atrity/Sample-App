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
        type="checkbox"
        :checked="modelValue"
        :disabled="disabled"
        :indeterminate="indeterminate"
        class="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
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
    type: [Boolean, Array],
    default: false
  },
  value: {
    type: [String, Number, Boolean, Object],
    default: null
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
  indeterminate: {
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
  return `checkbox-${Math.random().toString(36).substr(2, 9)}`
})

// Methods
const handleChange = (event) => {
  const checked = event.target.checked

  if (Array.isArray(props.modelValue)) {
    const newValue = [...props.modelValue]
    if (checked) {
      newValue.push(props.value)
    } else {
      const index = newValue.indexOf(props.value)
      if (index > -1) {
        newValue.splice(index, 1)
      }
    }
    emit('update:modelValue', newValue)
  } else {
    emit('update:modelValue', checked)
  }

  emit('change', checked)
}
</script>

<style scoped>
/* Custom checkbox styles */
input[type='checkbox'] {
  @apply transition-colors duration-200;
}

input[type='checkbox']:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z'/%3e%3c/svg%3e");
}

input[type='checkbox']:indeterminate {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M3 8a1 1 0 011-1h8a1 1 0 110 2H4a1 1 0 01-1-1z'/%3e%3c/svg%3e");
}

/* Hover effect */
input[type='checkbox']:not(:disabled):hover {
  @apply border-primary-500;
}

/* Focus ring */
input[type='checkbox']:focus {
  @apply ring-2 ring-offset-2 ring-primary-500;
}

/* Disabled state */
input[type='checkbox']:disabled {
  @apply bg-gray-100 border-gray-200;
}

/* Error state */
.checkbox-error input[type='checkbox'] {
  @apply border-red-300 focus:ring-red-500;
}

/* Animation */
.checkbox-enter-active,
.checkbox-leave-active {
  @apply transition-all duration-200;
}

.checkbox-enter-from,
.checkbox-leave-to {
  @apply opacity-0 scale-95;
}

/* Group styles */
.checkbox-group {
  @apply space-y-2;
}

.checkbox-group.inline {
  @apply space-y-0 space-x-4;
}
</style>
