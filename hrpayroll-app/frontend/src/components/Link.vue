<template>
  <component
    :is="isExternal ? 'a' : 'router-link'"
    :to="isExternal ? undefined : to"
    :href="isExternal ? href : undefined"
    :target="target"
    :rel="isExternal ? 'noopener noreferrer' : undefined"
    :class="[
      'inline-flex items-center',
      underline ? 'underline' : '',
      disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer',
      variantClasses,
      sizeClasses,
      className
    ]"
    @click="handleClick"
  >
    <!-- Left Icon -->
    <i
      v-if="icon && iconPosition === 'left'"
      :class="[icon, iconClasses.left]"
    ></i>

    <!-- Content -->
    <span>
      <slot>{{ label }}</slot>
    </span>

    <!-- Right Icon -->
    <i
      v-if="icon && iconPosition === 'right'"
      :class="[icon, iconClasses.right]"
    ></i>

    <!-- External Link Icon -->
    <i
      v-if="isExternal && showExternalIcon"
      class="fas fa-external-link-alt ml-1 text-xs"
    ></i>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  to: {
    type: [String, Object],
    default: undefined
  },
  href: {
    type: String,
    default: undefined
  },
  label: {
    type: String,
    default: ''
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
      'dark'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
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
  underline: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  target: {
    type: String,
    default: '_self'
  },
  showExternalIcon: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click'])

// Computed
const isExternal = computed(() => {
  return !props.to && props.href !== undefined
})

const variantClasses = computed(() => {
  const variants = {
    primary: 'text-primary-600 hover:text-primary-700',
    secondary: 'text-gray-600 hover:text-gray-700',
    success: 'text-green-600 hover:text-green-700',
    danger: 'text-red-600 hover:text-red-700',
    warning: 'text-yellow-600 hover:text-yellow-700',
    info: 'text-blue-600 hover:text-blue-700',
    light: 'text-gray-400 hover:text-gray-500',
    dark: 'text-gray-800 hover:text-gray-900'
  }
  return variants[props.variant]
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  }
  return sizes[props.size]
})

const iconClasses = computed(() => ({
  left: props.iconPosition === 'left' ? 'mr-1' : '',
  right: props.iconPosition === 'right' ? 'ml-1' : ''
}))

// Methods
const handleClick = (event) => {
  if (props.disabled) {
    event.preventDefault()
    return
  }
  emit('click', event)
}
</script>

<style scoped>
/* Hover effect */
.link-hover {
  @apply transition-colors duration-200;
}

/* Focus styles */
.link-focus:focus {
  @apply outline-none ring-2 ring-offset-2;
}

.link-focus.primary:focus {
  @apply ring-primary-500;
}

.link-focus.secondary:focus {
  @apply ring-gray-500;
}

.link-focus.success:focus {
  @apply ring-green-500;
}

.link-focus.danger:focus {
  @apply ring-red-500;
}

.link-focus.warning:focus {
  @apply ring-yellow-500;
}

.link-focus.info:focus {
  @apply ring-blue-500;
}

/* Underline animation */
.link-underline-animate {
  @apply relative;
}

.link-underline-animate::after {
  content: '';
  @apply absolute bottom-0 left-0 w-0 h-0.5 transition-all duration-300;
}

.link-underline-animate:hover::after {
  @apply w-full;
}

/* Disabled state */
.link-disabled {
  @apply pointer-events-none opacity-50;
}

/* Active state */
.link-active {
  @apply font-medium;
}
</style>
