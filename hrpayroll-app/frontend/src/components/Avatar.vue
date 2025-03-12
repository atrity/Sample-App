<template>
  <div
    :class="[
      'inline-flex items-center justify-center rounded-full',
      sizeClasses,
      { 'ring-2 ring-white': bordered },
      { 'cursor-pointer hover:opacity-80': clickable },
      className
    ]"
    @click="handleClick"
  >
    <!-- Image Avatar -->
    <img
      v-if="src && !error"
      :src="src"
      :alt="alt"
      class="h-full w-full rounded-full object-cover"
      @error="handleImageError"
    />

    <!-- Initials Avatar -->
    <template v-else>
      <div
        :class="[
          'flex items-center justify-center rounded-full',
          colorClasses,
          sizeClasses
        ]"
      >
        <span
          :class="[
            'font-medium',
            textSizeClasses
          ]"
        >
          {{ initials }}
        </span>
      </div>
    </template>

    <!-- Status Indicator -->
    <span
      v-if="status"
      :class="[
        'absolute bottom-0 right-0 block rounded-full ring-2 ring-white',
        statusSizeClasses,
        {
          'bg-green-400': status === 'online',
          'bg-red-400': status === 'offline',
          'bg-yellow-400': status === 'away',
          'bg-gray-400': status === 'busy'
        }
      ]"
    ></span>

    <!-- Badge -->
    <span
      v-if="badge"
      class="absolute -top-1 -right-1"
    >
      <Badge
        :variant="badgeVariant"
        :label="badge"
        size="sm"
      />
    </span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Badge from './Badge.vue'

const props = defineProps({
  src: {
    type: String,
    default: ''
  },
  alt: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl', '2xl'].includes(value)
  },
  name: {
    type: String,
    default: ''
  },
  color: {
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
  status: {
    type: String,
    default: '',
    validator: (value) => ['', 'online', 'offline', 'away', 'busy'].includes(value)
  },
  badge: {
    type: [String, Number],
    default: ''
  },
  badgeVariant: {
    type: String,
    default: 'primary'
  },
  bordered: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click', 'error'])

// State
const error = ref(false)

// Computed
const initials = computed(() => {
  if (!props.name) return '?'
  return props.name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'h-6 w-6',
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12',
    xl: 'h-14 w-14',
    '2xl': 'h-16 w-16'
  }
  return sizes[props.size]
})

const textSizeClasses = computed(() => {
  const sizes = {
    xs: 'text-xs',
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
    '2xl': 'text-2xl'
  }
  return sizes[props.size]
})

const statusSizeClasses = computed(() => {
  const sizes = {
    xs: 'h-1.5 w-1.5',
    sm: 'h-2 w-2',
    md: 'h-2.5 w-2.5',
    lg: 'h-3 w-3',
    xl: 'h-3.5 w-3.5',
    '2xl': 'h-4 w-4'
  }
  return sizes[props.size]
})

const colorClasses = computed(() => {
  const colors = {
    primary: 'bg-primary-100 text-primary-800',
    secondary: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    danger: 'bg-red-100 text-red-800',
    warning: 'bg-yellow-100 text-yellow-800',
    info: 'bg-blue-100 text-blue-800',
    light: 'bg-gray-100 text-gray-800',
    dark: 'bg-gray-800 text-white'
  }
  return colors[props.color]
})

// Methods
const handleImageError = (e) => {
  error.value = true
  emit('error', e)
}

const handleClick = (e) => {
  if (props.clickable) {
    emit('click', e)
  }
}
</script>

<style scoped>
.avatar-group {
  @apply flex -space-x-2;
}

.avatar-group > div {
  @apply ring-2 ring-white;
}

/* Hover effect for clickable avatars */
.avatar-hover:hover {
  @apply opacity-80 transition-opacity duration-200;
}
</style>
