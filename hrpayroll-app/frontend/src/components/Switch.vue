<template>
  <button
    type="button"
    :class="[
      'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
      modelValue ? enabledClass : disabledClass,
      disabled ? 'opacity-50 cursor-not-allowed' : '',
      className
    ]"
    :disabled="disabled"
    @click="toggle"
    role="switch"
    :aria-checked="modelValue"
  >
    <span class="sr-only">{{ label }}</span>
    <span
      :class="[
        'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200',
        modelValue ? 'translate-x-5' : 'translate-x-0'
      ]"
    >
      <!-- Icons -->
      <span
        :class="[
          'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity',
          modelValue ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200'
        ]"
        aria-hidden="true"
      >
        <slot name="off-icon">
          <i v-if="icons" class="fas fa-times text-gray-400 text-xs"></i>
        </slot>
      </span>
      <span
        :class="[
          'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity',
          modelValue ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100'
        ]"
        aria-hidden="true"
      >
        <slot name="on-icon">
          <i v-if="icons" class="fas fa-check text-primary-600 text-xs"></i>
        </slot>
      </span>
    </span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  label: {
    type: String,
    default: 'Toggle'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  icons: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => [
      'primary',
      'success',
      'danger',
      'warning',
      'info'
    ].includes(value)
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// Computed
const enabledClass = computed(() => {
  const classes = {
    primary: 'bg-primary-600 focus:ring-primary-500',
    success: 'bg-green-600 focus:ring-green-500',
    danger: 'bg-red-600 focus:ring-red-500',
    warning: 'bg-yellow-600 focus:ring-yellow-500',
    info: 'bg-blue-600 focus:ring-blue-500'
  }
  return classes[props.variant]
})

const disabledClass = computed(() => {
  return 'bg-gray-200'
})

// Methods
const toggle = () => {
  if (!props.disabled) {
    emit('update:modelValue', !props.modelValue)
    emit('change', !props.modelValue)
  }
}
</script>

<style scoped>
/* Optional: Add custom transition for the switch */
.switch-enter-active,
.switch-leave-active {
  @apply transition-all duration-300;
}

.switch-enter-from,
.switch-leave-to {
  @apply opacity-0 transform scale-95;
}

/* Optional: Add focus ring styles */
.switch-focus {
  @apply ring-2 ring-offset-2;
}

/* Optional: Add hover effect */
.switch-hover:not(:disabled) {
  @apply hover:opacity-90;
}

/* Optional: Add pressed effect */
.switch-active:not(:disabled) {
  @apply transform scale-95;
}

/* Optional: Custom sizes */
.switch-sm {
  @apply h-5 w-9;
}

.switch-sm .switch-handle {
  @apply h-4 w-4;
}

.switch-lg {
  @apply h-7 w-14;
}

.switch-lg .switch-handle {
  @apply h-6 w-6;
}
</style>
