<template>
  <Portal>
    <!-- Backdrop -->
    <Transition name="fade">
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        :class="{ 'cursor-pointer': closeOnBackdropClick }"
        @click="closeOnBackdropClick && close()"
      ></div>
    </Transition>

    <!-- Drawer -->
    <Transition :name="transitionClass">
      <div
        v-if="modelValue"
        :class="[
          'fixed bg-white shadow-xl transition-transform',
          positionClasses,
          sizeClasses,
          className
        ]"
      >
        <!-- Header -->
        <div
          v-if="$slots.header || title || showClose"
          class="flex items-center justify-between px-4 py-3 border-b border-gray-200"
        >
          <slot name="header">
            <h3 class="text-lg font-medium text-gray-900">
              {{ title }}
            </h3>
          </slot>
          <button
            v-if="showClose"
            class="text-gray-400 hover:text-gray-500"
            @click="close"
          >
            <i class="fas fa-times"></i>
            <span class="sr-only">Close</span>
          </button>
        </div>

        <!-- Content -->
        <div
          :class="[
            'overflow-y-auto',
            contentClass,
            { 'p-4': padding }
          ]"
          :style="{ height: contentHeight }"
        >
          <slot></slot>
        </div>

        <!-- Footer -->
        <div
          v-if="$slots.footer"
          class="border-t border-gray-200 px-4 py-3 bg-gray-50"
        >
          <slot name="footer"></slot>
        </div>
      </div>
    </Transition>
  </Portal>
</template>

<script setup>
import { computed } from 'vue'
import Portal from './Portal.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  position: {
    type: String,
    default: 'right',
    validator: (value) => ['left', 'right', 'top', 'bottom'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  showClose: {
    type: Boolean,
    default: true
  },
  closeOnBackdropClick: {
    type: Boolean,
    default: true
  },
  padding: {
    type: Boolean,
    default: true
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

const emit = defineEmits(['update:modelValue', 'close'])

// Computed
const positionClasses = computed(() => {
  const positions = {
    left: 'inset-y-0 left-0',
    right: 'inset-y-0 right-0',
    top: 'inset-x-0 top-0',
    bottom: 'inset-x-0 bottom-0'
  }
  return positions[props.position]
})

const sizeClasses = computed(() => {
  const isVertical = ['left', 'right'].includes(props.position)
  const sizes = {
    sm: isVertical ? 'w-64' : 'h-64',
    md: isVertical ? 'w-80' : 'h-80',
    lg: isVertical ? 'w-96' : 'h-96',
    xl: isVertical ? 'w-[32rem]' : 'h-[32rem]',
    full: isVertical ? 'w-screen' : 'h-screen'
  }
  return sizes[props.size]
})

const transitionClass = computed(() => {
  const transitions = {
    left: 'slide-right',
    right: 'slide-left',
    top: 'slide-down',
    bottom: 'slide-up'
  }
  return transitions[props.position]
})

const contentHeight = computed(() => {
  if (['top', 'bottom'].includes(props.position)) {
    return 'auto'
  }
  return 'calc(100% - 4rem)'
})

// Methods
const close = () => {
  emit('update:modelValue', false)
  emit('close')
}
</script>

<style scoped>
/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  @apply transition-opacity duration-300;
}

.fade-enter-from,
.fade-leave-to {
  @apply opacity-0;
}

/* Slide transitions */
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active,
.slide-up-enter-active,
.slide-up-leave-active,
.slide-down-enter-active,
.slide-down-leave-active {
  @apply transition-transform duration-300 ease-in-out;
}

/* Right drawer */
.slide-left-enter-from,
.slide-left-leave-to {
  @apply translate-x-full;
}

/* Left drawer */
.slide-right-enter-from,
.slide-right-leave-to {
  @apply -translate-x-full;
}

/* Bottom drawer */
.slide-up-enter-from,
.slide-up-leave-to {
  @apply translate-y-full;
}

/* Top drawer */
.slide-down-enter-from,
.slide-down-leave-to {
  @apply -translate-y-full;
}

/* Optional: Add focus styles */
.drawer-focus {
  @apply focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2;
}

/* Optional: Add hover effects */
.drawer-hover {
  @apply transition-shadow duration-200;
}

.drawer-hover:hover {
  @apply shadow-2xl;
}

/* Optional: Add resize handle */
.drawer-resizable {
  @apply resize overflow-auto;
}

/* Optional: Add scroll shadows */
.drawer-scroll-shadow {
  background:
    linear-gradient(white 30%, rgba(255, 255, 255, 0)),
    linear-gradient(rgba(255, 255, 255, 0), white 70%) 0 100%,
    radial-gradient(farthest-side at 50% 0, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0)),
    radial-gradient(farthest-side at 50% 100%, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0)) 0 100%;
  background-repeat: no-repeat;
  background-size: 100% 40px, 100% 40px, 100% 14px, 100% 14px;
  background-attachment: local, local, scroll, scroll;
}
</style>
