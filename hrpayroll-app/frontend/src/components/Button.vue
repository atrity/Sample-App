<template>
  <component
    :is="tag"
    :class="[
      'inline-flex items-center justify-center rounded-md font-medium focus:outline-none transition-colors duration-200',
      sizeClasses,
      variantClasses,
      {
        'opacity-50 cursor-not-allowed': disabled || loading,
        'cursor-pointer': !disabled && !loading
      },
      className
    ]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <!-- Loading Spinner -->
    <span
      v-if="loading"
      class="mr-2"
    >
      <svg
        class="animate-spin h-4 w-4"
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
    </span>

    <!-- Left Icon -->
    <i
      v-if="icon && iconPosition === 'left'"
      :class="[icon, 'mr-2']"
    ></i>

    <!-- Content -->
    <span>
      <slot>{{ label }}</slot>
    </span>

    <!-- Right Icon -->
    <i
      v-if="icon && iconPosition === 'right'"
      :class="[icon, 'ml-2']"
    ></i>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tag: {
    type: String,
    default: 'button'
  },
  type: {
    type: String,
    default: 'button'
  },
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
      'dark',
      'link',
      'outline-primary',
      'outline-secondary',
      'outline-success',
      'outline-danger',
      'outline-warning',
      'outline-info',
      'outline-light',
      'outline-dark'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
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
  label: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  block: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  }
})

// Size classes
const sizeClasses = computed(() => {
  const sizes = {
    xs: 'px-2.5 py-1.5 text-xs',
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-4 py-2 text-base',
    xl: 'px-6 py-3 text-base'
  }
  return sizes[props.size]
})

// Variant classes
const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-2 focus:ring-offset-2 focus:ring-gray-500',
    success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-2 focus:ring-offset-2 focus:ring-green-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-2 focus:ring-offset-2 focus:ring-red-500',
    warning: 'bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500',
    info: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-offset-2 focus:ring-blue-500',
    light: 'bg-gray-100 text-gray-800 hover:bg-gray-200 focus:ring-2 focus:ring-offset-2 focus:ring-gray-500',
    dark: 'bg-gray-800 text-white hover:bg-gray-900 focus:ring-2 focus:ring-offset-2 focus:ring-gray-500',
    link: 'bg-transparent text-primary-600 hover:text-primary-700 hover:underline',
    'outline-primary': 'border border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
    'outline-secondary': 'border border-gray-600 text-gray-600 hover:bg-gray-50 focus:ring-2 focus:ring-offset-2 focus:ring-gray-500',
    'outline-success': 'border border-green-600 text-green-600 hover:bg-green-50 focus:ring-2 focus:ring-offset-2 focus:ring-green-500',
    'outline-danger': 'border border-red-600 text-red-600 hover:bg-red-50 focus:ring-2 focus:ring-offset-2 focus:ring-red-500',
    'outline-warning': 'border border-yellow-600 text-yellow-600 hover:bg-yellow-50 focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500',
    'outline-info': 'border border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-2 focus:ring-offset-2 focus:ring-blue-500',
    'outline-light': 'border border-gray-200 text-gray-700 hover:bg-gray-50 focus:ring-2 focus:ring-offset-2 focus:ring-gray-500',
    'outline-dark': 'border border-gray-800 text-gray-800 hover:bg-gray-50 focus:ring-2 focus:ring-offset-2 focus:ring-gray-500'
  }
  return `${variants[props.variant]} ${props.block ? 'w-full' : ''}`
})
</script>
