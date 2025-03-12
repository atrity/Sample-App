<template>
  <div
    :class="[
      'text-center',
      padded ? 'py-12' : '',
      className
    ]"
  >
    <!-- Image -->
    <div v-if="image || $slots.image" class="mb-4">
      <slot name="image">
        <img
          :src="image"
          :alt="title"
          class="mx-auto h-24 w-24"
        />
      </slot>
    </div>

    <!-- Icon -->
    <div v-else-if="icon" class="mb-4">
      <i
        :class="[
          icon,
          'text-4xl',
          iconColorClasses
        ]"
      ></i>
    </div>

    <!-- Title -->
    <h3
      v-if="title || $slots.title"
      class="text-lg font-medium text-gray-900 mb-2"
    >
      <slot name="title">{{ title }}</slot>
    </h3>

    <!-- Description -->
    <p
      v-if="description || $slots.description"
      class="text-sm text-gray-500 max-w-sm mx-auto"
    >
      <slot name="description">{{ description }}</slot>
    </p>

    <!-- Action -->
    <div
      v-if="$slots.action || action"
      class="mt-6"
    >
      <slot name="action">
        <Button
          v-if="action"
          :variant="actionVariant"
          :label="action"
          @click="$emit('action-click')"
        >
          {{ action }}
        </Button>
      </slot>
    </div>

    <!-- Extra Content -->
    <div v-if="$slots.default" class="mt-6">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'No data available'
  },
  description: {
    type: String,
    default: ''
  },
  image: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: 'fas fa-inbox'
  },
  iconColor: {
    type: String,
    default: 'gray',
    validator: (value) => [
      'gray',
      'primary',
      'success',
      'danger',
      'warning',
      'info'
    ].includes(value)
  },
  action: {
    type: String,
    default: ''
  },
  actionVariant: {
    type: String,
    default: 'primary'
  },
  padded: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  }
})

// Computed
const iconColorClasses = computed(() => {
  const colors = {
    gray: 'text-gray-400',
    primary: 'text-primary-400',
    success: 'text-green-400',
    danger: 'text-red-400',
    warning: 'text-yellow-400',
    info: 'text-blue-400'
  }
  return colors[props.iconColor]
})
</script>

<style scoped>
/* Animation classes */
.empty-enter-active,
.empty-leave-active {
  @apply transition-all duration-300;
}

.empty-enter-from,
.empty-leave-to {
  @apply opacity-0 scale-95;
}

/* Optional: Add hover effect for interactive elements */
.empty-hover {
  @apply transition-transform duration-200;
}

.empty-hover:hover {
  @apply transform scale-105;
}

/* Optional: Add different sizes */
.empty-sm {
  @apply py-8;
}

.empty-sm img,
.empty-sm i {
  @apply h-16 w-16;
}

.empty-lg {
  @apply py-16;
}

.empty-lg img,
.empty-lg i {
  @apply h-32 w-32;
}

/* Optional: Add different layouts */
.empty-horizontal {
  @apply flex items-center justify-center space-x-6;
}

.empty-horizontal img,
.empty-horizontal i {
  @apply mb-0 mr-6;
}

/* Optional: Add background variations */
.empty-subtle {
  @apply bg-gray-50 rounded-lg;
}

.empty-bordered {
  @apply border-2 border-dashed border-gray-200 rounded-lg;
}
</style>
