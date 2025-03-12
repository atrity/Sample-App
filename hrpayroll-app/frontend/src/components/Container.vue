<template>
  <div
    :class="[
      'mx-auto',
      maxWidthClass,
      paddingClass,
      {
        'relative': relative,
        'overflow-hidden': overflow,
        'bg-white': background,
        'shadow-sm': shadow,
        'rounded-lg': rounded
      },
      className
    ]"
  >
    <!-- Container Header -->
    <div
      v-if="$slots.header || title"
      :class="[
        'mb-6',
        { 'border-b border-gray-200 pb-5': divider }
      ]"
    >
      <slot name="header">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">
              {{ title }}
            </h2>
            <p
              v-if="description"
              class="mt-1 text-sm text-gray-500"
            >
              {{ description }}
            </p>
          </div>
          <div v-if="$slots.headerActions" class="flex items-center space-x-3">
            <slot name="headerActions"></slot>
          </div>
        </div>
      </slot>
    </div>

    <!-- Container Content -->
    <div
      :class="[
        contentClass,
        { 'space-y-6': spacing }
      ]"
    >
      <slot></slot>
    </div>

    <!-- Container Footer -->
    <div
      v-if="$slots.footer"
      :class="[
        'mt-6',
        { 'border-t border-gray-200 pt-5': divider }
      ]"
    >
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  maxWidth: {
    type: String,
    default: '7xl',
    validator: (value) => [
      'sm',
      'md',
      'lg',
      'xl',
      '2xl',
      '3xl',
      '4xl',
      '5xl',
      '6xl',
      '7xl',
      'full',
      'min',
      'max',
      'prose'
    ].includes(value)
  },
  padding: {
    type: [Boolean, String],
    default: true
  },
  spacing: {
    type: Boolean,
    default: true
  },
  divider: {
    type: Boolean,
    default: false
  },
  relative: {
    type: Boolean,
    default: false
  },
  overflow: {
    type: Boolean,
    default: false
  },
  background: {
    type: Boolean,
    default: false
  },
  shadow: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  },
  contentClass: {
    type: String,
    default: ''
  }
})

// Computed
const maxWidthClass = computed(() => {
  if (props.maxWidth === 'full') return 'w-full'
  if (props.maxWidth === 'min') return 'min-w-0'
  if (props.maxWidth === 'max') return 'max-w-full'
  if (props.maxWidth === 'prose') return 'max-w-prose'
  return `max-w-${props.maxWidth}`
})

const paddingClass = computed(() => {
  if (!props.padding) return ''
  if (typeof props.padding === 'string') return props.padding
  return 'px-4 sm:px-6 lg:px-8'
})
</script>

<style scoped>
/* Animation classes */
.container-enter-active,
.container-leave-active {
  @apply transition-all duration-300;
}

.container-enter-from,
.container-leave-to {
  @apply opacity-0 transform scale-95;
}

/* Optional: Add responsive padding adjustments */
@screen sm {
  .container-responsive {
    @apply px-6;
  }
}

@screen lg {
  .container-responsive {
    @apply px-8;
  }
}

/* Optional: Add background variations */
.container-subtle {
  @apply bg-gray-50;
}

.container-bordered {
  @apply border border-gray-200;
}

/* Optional: Add shadow variations */
.container-shadow-md {
  @apply shadow-md;
}

.container-shadow-lg {
  @apply shadow-lg;
}

/* Optional: Add gradient background */
.container-gradient {
  background: linear-gradient(
    to bottom right,
    var(--tw-gradient-from),
    var(--tw-gradient-to)
  );
}

/* Optional: Add backdrop blur effect */
.container-glass {
  @apply bg-white bg-opacity-80 backdrop-blur-sm;
}
</style>
