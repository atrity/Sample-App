<template>
  <div
    :class="[
      'grid',
      gridCols,
      gridGap,
      autoFlow && `grid-flow-${autoFlow}`,
      alignItems && `items-${alignItems}`,
      justifyItems && `justify-items-${justifyItems}`,
      alignContent && `content-${alignContent}`,
      justifyContent && `justify-${justifyContent}`,
      className
    ]"
  >
    <slot></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  cols: {
    type: [Number, Object],
    default: 1
  },
  gap: {
    type: [Number, String],
    default: 4
  },
  autoFlow: {
    type: String,
    default: '',
    validator: (value) => ['row', 'col', 'row-dense', 'col-dense', ''].includes(value)
  },
  alignItems: {
    type: String,
    default: '',
    validator: (value) => ['start', 'center', 'end', 'stretch', ''].includes(value)
  },
  justifyItems: {
    type: String,
    default: '',
    validator: (value) => ['start', 'center', 'end', 'stretch', ''].includes(value)
  },
  alignContent: {
    type: String,
    default: '',
    validator: (value) => ['start', 'center', 'end', 'between', 'around', 'evenly', ''].includes(value)
  },
  justifyContent: {
    type: String,
    default: '',
    validator: (value) => ['start', 'center', 'end', 'between', 'around', 'evenly', ''].includes(value)
  },
  className: {
    type: String,
    default: ''
  }
})

// Computed
const gridCols = computed(() => {
  if (typeof props.cols === 'number') {
    return `grid-cols-${props.cols}`
  }

  const breakpoints = {
    sm: 'sm:grid-cols-',
    md: 'md:grid-cols-',
    lg: 'lg:grid-cols-',
    xl: 'xl:grid-cols-',
    '2xl': '2xl:grid-cols-'
  }

  return Object.entries(props.cols)
    .map(([breakpoint, cols]) => {
      if (breakpoint === 'default') {
        return `grid-cols-${cols}`
      }
      return `${breakpoints[breakpoint]}${cols}`
    })
    .join(' ')
})

const gridGap = computed(() => {
  if (typeof props.gap === 'number') {
    return `gap-${props.gap}`
  }
  return props.gap
})
</script>

<style scoped>
/* Optional: Add animation for grid items */
.grid-item-enter-active,
.grid-item-leave-active {
  transition: all 0.3s ease;
}

.grid-item-enter-from,
.grid-item-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Optional: Add responsive gap adjustments */
@screen sm {
  .grid-gap-responsive {
    @apply gap-4;
  }
}

@screen md {
  .grid-gap-responsive {
    @apply gap-6;
  }
}

@screen lg {
  .grid-gap-responsive {
    @apply gap-8;
  }
}

/* Optional: Add masonry layout support */
.grid-masonry {
  grid-auto-flow: dense;
}

/* Optional: Add auto-fit and auto-fill support */
.grid-auto-fit {
  grid-template-columns: repeat(auto-fit, minmax(var(--min-width, 200px), 1fr));
}

.grid-auto-fill {
  grid-template-columns: repeat(auto-fill, minmax(var(--min-width, 200px), 1fr));
}

/* Optional: Add grid area support */
.grid-area {
  display: grid;
  grid-template-areas: var(--grid-template-areas);
}

/* Optional: Add grid line names support */
.grid-named-lines {
  grid-template-columns: [start] repeat(var(--cols, 12), minmax(0, 1fr)) [end];
}
</style>
