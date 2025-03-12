<template>
  <span
    :class="[
      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
      sizeClasses,
      variantClasses,
      { 'cursor-pointer hover:opacity-80': clickable },
      className
    ]"
    :title="title"
    @click="handleClick"
  >
    <!-- Dot -->
    <span
      v-if="dot"
      :class="[
        'mr-1.5 h-2 w-2 rounded-full',
        dotColorClasses
      ]"
    ></span>

    <!-- Left Icon -->
    <i
      v-if="icon && iconPosition === 'left'"
      :class="[icon, 'mr-1']"
    ></i>

    <!-- Content -->
    <slot>{{ label }}</slot>

    <!-- Right Icon -->
    <i
      v-if="icon && iconPosition === 'right'"
      :class="[icon, 'ml-1']"
    ></i>

    <!-- Remove Button -->
    <button
      v-if="removable"
      type="button"
      class="ml-1 -mr-1 inline-flex rounded-full p-0.5 hover:bg-black hover:bg-opacity-10 focus:outline-none"
      @click.stop="handleRemove"
    >
      <span class="sr-only">Remove</span>
      <i class="fas fa-times text-xs"></i>
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => [
      'primary',
      'secondary',
      'success',
      'danger',
      'warning',
      'info',
      'light',
      'dark'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  iconPosition: {
    type: String,
    default: 'left',
    validator: (value) => ['left', 'right'].includes(value)
  },
  dot: {
    type: Boolean,
    default: false
  },
  removable: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click', 'remove'])

// Size classes
const sizeClasses = computed(() => {
  const sizes = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-2.5 py-0.5',
    lg: 'text-base px-3 py-1'
  }
  return sizes[props.size]
})

// Variant classes
const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-primary-100 text-primary-800',
    secondary: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    danger: 'bg-red-100 text-red-800',
    warning: 'bg-yellow-100 text-yellow-800',
    info: 'bg-blue-100 text-blue-800',
    light: 'bg-gray-100 text-gray-800',
    dark: 'bg-gray-800 text-white'
  }
  return variants[props.variant]
})

// Dot color classes
const dotColorClasses = computed(() => {
  const colors = {
    primary: 'bg-primary-400',
    secondary: 'bg-gray-400',
    success: 'bg-green-400',
    danger: 'bg-red-400',
    warning: 'bg-yellow-400',
    info: 'bg-blue-400',
    light: 'bg-gray-400',
    dark: 'bg-gray-600'
  }
  return colors[props.variant]
})

// Methods
const handleClick = (event) => {
  if (props.clickable) {
    emit('click', event)
  }
}

const handleRemove = (event) => {
  emit('remove', event)
}
</script>

<style scoped>
/* Animation classes */
.badge-enter-active,
.badge-leave-active {
  @apply transition-all duration-200 ease-in-out;
}

.badge-enter-from,
.badge-leave-to {
  @apply opacity-0 scale-95;
}

/* Pulse animation for dot */
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
