<template>
  <div
    :class="[
      vertical ? 'flex flex-col' : 'flex flex-row',
      alignClasses,
      justifyClasses,
      spaceClasses,
      divideClasses,
      {
        'inline-flex': inline,
        'flex-wrap': wrap,
        'flex-1': grow,
        'flex-shrink-0': !shrink
      },
      className
    ]"
  >
    <slot></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  vertical: {
    type: Boolean,
    default: true
  },
  inline: {
    type: Boolean,
    default: false
  },
  wrap: {
    type: Boolean,
    default: false
  },
  grow: {
    type: Boolean,
    default: false
  },
  shrink: {
    type: Boolean,
    default: true
  },
  space: {
    type: [Number, String],
    default: 4
  },
  align: {
    type: String,
    default: '',
    validator: (value) => [
      '',
      'start',
      'end',
      'center',
      'baseline',
      'stretch'
    ].includes(value)
  },
  justify: {
    type: String,
    default: '',
    validator: (value) => [
      '',
      'start',
      'end',
      'center',
      'between',
      'around',
      'evenly'
    ].includes(value)
  },
  divide: {
    type: Boolean,
    default: false
  },
  divideColor: {
    type: String,
    default: 'gray-200'
  },
  className: {
    type: String,
    default: ''
  }
})

// Computed
const alignClasses = computed(() => {
  if (!props.align) return ''
  return props.vertical ? `items-${props.align}` : `items-${props.align}`
})

const justifyClasses = computed(() => {
  if (!props.justify) return ''
  return `justify-${props.justify}`
})

const spaceClasses = computed(() => {
  if (!props.space) return ''
  return props.vertical
    ? `space-y-${props.space}`
    : `space-x-${props.space}`
})

const divideClasses = computed(() => {
  if (!props.divide) return ''
  return props.vertical
    ? `divide-y divide-${props.divideColor}`
    : `divide-x divide-${props.divideColor}`
})
</script>

<style scoped>
/* Animation classes */
.stack-enter-active,
.stack-leave-active {
  @apply transition-all duration-300;
}

.stack-enter-from,
.stack-leave-to {
  @apply opacity-0;
}

/* Optional: Add responsive spacing */
@screen sm {
  .stack-space-responsive {
    @apply space-y-2 sm:space-y-4 lg:space-y-6;
  }
}

/* Optional: Add hover effects for divided items */
.stack-hover-divide > :not([hidden]) ~ :not([hidden]) {
  @apply transition-colors duration-200;
}

.stack-hover-divide:hover > :not([hidden]) ~ :not([hidden]) {
  @apply divide-gray-300;
}

/* Optional: Add reverse order utility */
.stack-reverse {
  @apply flex-col-reverse;
}

.stack-reverse-horizontal {
  @apply flex-row-reverse;
}

/* Optional: Add nested stack styles */
.stack-nested {
  @apply pl-4 border-l border-gray-200;
}

/* Optional: Add collapsible stack styles */
.stack-collapsible {
  @apply transition-all duration-300;
}

.stack-collapsed {
  @apply h-0 overflow-hidden;
}
</style>
