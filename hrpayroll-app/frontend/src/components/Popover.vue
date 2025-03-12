<template>
  <div class="relative inline-block">
    <!-- Trigger -->
    <div
      ref="triggerRef"
      @mouseenter="trigger === 'hover' && show()"
      @mouseleave="trigger === 'hover' && hide()"
      @click="trigger === 'click' && toggle()"
      @focus="trigger === 'focus' && show()"
      @blur="trigger === 'focus' && hide()"
    >
      <slot name="trigger"></slot>
    </div>

    <!-- Popover -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div
        v-if="isVisible"
        ref="popoverRef"
        :class="[
          'absolute z-50',
          positionClass,
          {
            'bg-white': !transparent,
            'shadow-lg': !transparent,
            'rounded-lg': !transparent,
            'border border-gray-200': !transparent
          },
          className
        ]"
        v-click-outside="handleClickOutside"
      >
        <!-- Arrow -->
        <div
          v-if="arrow && !transparent"
          :class="[
            'absolute w-3 h-3 bg-white border transform rotate-45',
            arrowPositionClass,
            arrowBorderClass
          ]"
        ></div>

        <!-- Content -->
        <div
          :class="[
            'relative',
            { 'p-4': !transparent && padding }
          ]"
        >
          <slot></slot>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { usePopper } from '@vueuse/core'

const props = defineProps({
  trigger: {
    type: String,
    default: 'click',
    validator: (value) => ['click', 'hover', 'focus'].includes(value)
  },
  placement: {
    type: String,
    default: 'bottom',
    validator: (value) => [
      'top',
      'top-start',
      'top-end',
      'bottom',
      'bottom-start',
      'bottom-end',
      'left',
      'left-start',
      'left-end',
      'right',
      'right-start',
      'right-end'
    ].includes(value)
  },
  offset: {
    type: Array,
    default: () => [0, 8]
  },
  arrow: {
    type: Boolean,
    default: true
  },
  padding: {
    type: Boolean,
    default: true
  },
  transparent: {
    type: Boolean,
    default: false
  },
  closeOnClickOutside: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['show', 'hide'])

// State
const isVisible = ref(false)
const triggerRef = ref(null)
const popoverRef = ref(null)

// Popper instance
const { x, y, strategy, update } = usePopper(
  triggerRef,
  popoverRef,
  {
    placement: props.placement,
    modifiers: [
      { name: 'offset', options: { offset: props.offset } },
      { name: 'arrow', options: { element: '.popover-arrow' } }
    ]
  }
)

// Computed
const positionClass = computed(() => {
  return `${strategy.value} top-${y.value}px left-${x.value}px`
})

const arrowPositionClass = computed(() => {
  const positions = {
    top: '-bottom-1.5 left-1/2 -translate-x-1/2 border-b border-r',
    'top-start': '-bottom-1.5 left-4 border-b border-r',
    'top-end': '-bottom-1.5 right-4 border-b border-r',
    bottom: '-top-1.5 left-1/2 -translate-x-1/2 border-t border-l',
    'bottom-start': '-top-1.5 left-4 border-t border-l',
    'bottom-end': '-top-1.5 right-4 border-t border-l',
    left: '-right-1.5 top-1/2 -translate-y-1/2 border-t border-r',
    'left-start': '-right-1.5 top-4 border-t border-r',
    'left-end': '-right-1.5 bottom-4 border-t border-r',
    right: '-left-1.5 top-1/2 -translate-y-1/2 border-b border-l',
    'right-start': '-left-1.5 top-4 border-b border-l',
    'right-end': '-left-1.5 bottom-4 border-b border-l'
  }
  return positions[props.placement]
})

const arrowBorderClass = computed(() => {
  return 'border-gray-200'
})

// Methods
const show = () => {
  isVisible.value = true
  emit('show')
  nextTick(() => update())
}

const hide = () => {
  isVisible.value = false
  emit('hide')
}

const toggle = () => {
  isVisible.value ? hide() : show()
}

const handleClickOutside = (event) => {
  if (props.closeOnClickOutside && !triggerRef.value?.contains(event.target)) {
    hide()
  }
}

// Lifecycle
onMounted(() => {
  if (props.trigger === 'hover') {
    document.addEventListener('mouseover', handleClickOutside)
  }
})

onBeforeUnmount(() => {
  if (props.trigger === 'hover') {
    document.removeEventListener('mouseover', handleClickOutside)
  }
})
</script>

<style scoped>
/* Optional: Add custom arrow styles */
.popover-arrow {
  @apply absolute w-2 h-2 bg-white transform rotate-45;
}

/* Optional: Add custom transition classes */
.popover-transition-enter-active,
.popover-transition-leave-active {
  @apply transition-all duration-200;
}

.popover-transition-enter-from,
.popover-transition-leave-to {
  @apply opacity-0 scale-95;
}

/* Optional: Add backdrop blur effect */
.popover-blur {
  @apply backdrop-blur-sm bg-white/90;
}

/* Optional: Add custom shadow */
.popover-shadow {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Optional: Add custom border radius */
.popover-rounded {
  @apply rounded-lg overflow-hidden;
}

/* Optional: Add max-width and max-height */
.popover-constrain {
  @apply max-w-sm max-h-[80vh] overflow-auto;
}
</style>
