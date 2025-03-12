<template>
  <div class="relative inline-block">
    <!-- Trigger Element -->
    <div
      ref="trigger"
      @mouseenter="show"
      @mouseleave="hide"
      @focus="show"
      @blur="hide"
    >
      <slot></slot>
    </div>

    <!-- Tooltip -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isVisible"
        ref="tooltip"
        :class="[
          'absolute z-50 px-2 py-1 text-sm font-medium text-white bg-gray-900 rounded shadow-sm',
          maxWidth ? `max-w-${maxWidth}` : 'max-w-xs',
          className
        ]"
        :style="positionStyles"
        role="tooltip"
      >
        <!-- Content -->
        <div class="relative z-20">
          <slot name="content">
            {{ content }}
          </slot>
        </div>

        <!-- Arrow -->
        <div
          :class="[
            'absolute w-2 h-2 bg-gray-900 transform rotate-45',
            getArrowPositionClass
          ]"
        ></div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  position: {
    type: String,
    default: 'top',
    validator: (value) => ['top', 'right', 'bottom', 'left'].includes(value)
  },
  offset: {
    type: Number,
    default: 8
  },
  delay: {
    type: Number,
    default: 0
  },
  maxWidth: {
    type: String,
    default: ''
  },
  className: {
    type: String,
    default: ''
  }
})

// Refs
const trigger = ref(null)
const tooltip = ref(null)
const isVisible = ref(false)
let showTimeout = null

// Computed
const positionStyles = computed(() => {
  if (!trigger.value || !tooltip.value) return {}

  const triggerRect = trigger.value.getBoundingClientRect()
  const tooltipRect = tooltip.value.getBoundingClientRect()

  const positions = {
    top: {
      top: -(tooltipRect.height + props.offset),
      left: (triggerRect.width - tooltipRect.width) / 2
    },
    right: {
      top: (triggerRect.height - tooltipRect.height) / 2,
      left: triggerRect.width + props.offset
    },
    bottom: {
      top: triggerRect.height + props.offset,
      left: (triggerRect.width - tooltipRect.width) / 2
    },
    left: {
      top: (triggerRect.height - tooltipRect.height) / 2,
      left: -(tooltipRect.width + props.offset)
    }
  }

  return {
    top: `${positions[props.position].top}px`,
    left: `${positions[props.position].left}px`
  }
})

const getArrowPositionClass = computed(() => {
  const positions = {
    top: '-bottom-1',
    right: '-left-1',
    bottom: '-top-1',
    left: '-right-1'
  }
  return positions[props.position]
})

// Methods
const show = () => {
  if (props.delay) {
    showTimeout = setTimeout(() => {
      isVisible.value = true
    }, props.delay)
  } else {
    isVisible.value = true
  }
}

const hide = () => {
  if (showTimeout) {
    clearTimeout(showTimeout)
  }
  isVisible.value = false
}

const handleScroll = () => {
  if (isVisible.value) {
    hide()
  }
}

// Lifecycle
onMounted(() => {
  window.addEventListener('scroll', handleScroll, true)
  window.addEventListener('resize', hide)
})

onUnmounted(() => {
  if (showTimeout) {
    clearTimeout(showTimeout)
  }
  window.removeEventListener('scroll', handleScroll, true)
  window.removeEventListener('resize', hide)
})
</script>

<style scoped>
.tooltip-enter-active,
.tooltip-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Arrow positions */
.tooltip-arrow {
  position: absolute;
  width: 8px;
  height: 8px;
  background: inherit;
  visibility: hidden;
}

.tooltip-arrow::before {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  background: inherit;
  visibility: visible;
  transform: rotate(45deg);
}

/* Dark theme */
.tooltip-dark {
  @apply bg-gray-900 text-white;
}

/* Light theme */
.tooltip-light {
  @apply bg-white text-gray-900 border border-gray-200;
}

/* Custom arrow colors */
.tooltip-dark .tooltip-arrow::before {
  @apply bg-gray-900;
}

.tooltip-light .tooltip-arrow::before {
  @apply bg-white border border-gray-200;
}
</style>
