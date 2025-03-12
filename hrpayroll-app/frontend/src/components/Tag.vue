<template>
  <span
    :class="[
      'inline-flex items-center',
      sizeClasses,
      variantClasses,
      rounded ? 'rounded-full' : 'rounded-md',
      clickable ? 'cursor-pointer hover:opacity-80' : '',
      disabled ? 'opacity-50 cursor-not-allowed' : '',
      className
    ]"
    @click="handleClick"
  >
    <!-- Icon -->
    <i
      v-if="icon"
      :class="[icon, iconClasses]"
    ></i>

    <!-- Avatar -->
    <Avatar
      v-if="avatar"
      :src="avatar"
      :name="avatarName"
      :size="avatarSize"
      class="mr-1.5 -ml-1"
    />

    <!-- Content -->
    <span :class="{ 'font-medium': !light }">
      <slot>{{ label }}</slot>
    </span>

    <!-- Close Button -->
    <button
      v-if="closable"
      type="button"
      :class="[
        'ml-1 -mr-1 hover:opacity-80 focus:outline-none',
        disabled ? 'cursor-not-allowed' : 'cursor-pointer'
      ]"
      @click.stop="handleClose"
      :disabled="disabled"
    >
      <i class="fas fa-times"></i>
      <span class="sr-only">Remove</span>
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import Avatar from './Avatar.vue'

const props = defineProps({
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
      'info'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  light: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: Boolean,
    default: false
  },
  closable: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  icon: {
    type: String,
    default: ''
  },
  avatar: {
    type: String,
    default: ''
  },
  avatarName: {
    type: String,
    default: ''
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click', 'close'])

// Computed
const sizeClasses = computed(() => {
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-sm',
    lg: 'px-3 py-1 text-base'
  }
  return sizes[props.size]
})

const variantClasses = computed(() => {
  const baseClasses = props.light
    ? {
        primary: 'bg-primary-50 text-primary-700',
        secondary: 'bg-gray-50 text-gray-700',
        success: 'bg-green-50 text-green-700',
        danger: 'bg-red-50 text-red-700',
        warning: 'bg-yellow-50 text-yellow-700',
        info: 'bg-blue-50 text-blue-700'
      }
    : {
        primary: 'bg-primary-500 text-white',
        secondary: 'bg-gray-500 text-white',
        success: 'bg-green-500 text-white',
        danger: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-white',
        info: 'bg-blue-500 text-white'
      }
  return baseClasses[props.variant]
})

const iconClasses = computed(() => {
  const sizes = {
    sm: 'mr-1 text-xs',
    md: 'mr-1.5 text-sm',
    lg: 'mr-2 text-base'
  }
  return sizes[props.size]
})

const avatarSize = computed(() => {
  const sizes = {
    sm: 'xs',
    md: 'sm',
    lg: 'md'
  }
  return sizes[props.size]
})

// Methods
const handleClick = (event) => {
  if (!props.disabled && props.clickable) {
    emit('click', event)
  }
}

const handleClose = (event) => {
  if (!props.disabled) {
    emit('close', event)
  }
}
</script>

<style scoped>
/* Animation classes */
.tag-enter-active,
.tag-leave-active {
  transition: all 0.2s ease;
}

.tag-enter-from,
.tag-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Hover effect */
.tag-hover {
  @apply transition-all duration-200;
}

.tag-hover:hover {
  @apply shadow-sm;
}

/* Optional: Add gradient effect */
.tag-gradient {
  background-image: linear-gradient(
    to right,
    var(--tw-gradient-from),
    var(--tw-gradient-to)
  );
}

/* Optional: Add outline variant */
.tag-outline {
  @apply bg-transparent border;
}

.tag-outline.primary {
  @apply border-primary-500 text-primary-500;
}

.tag-outline.secondary {
  @apply border-gray-500 text-gray-500;
}

.tag-outline.success {
  @apply border-green-500 text-green-500;
}

.tag-outline.danger {
  @apply border-red-500 text-red-500;
}

.tag-outline.warning {
  @apply border-yellow-500 text-yellow-500;
}

.tag-outline.info {
  @apply border-blue-500 text-blue-500;
}
</style>
