<template>
  <div
    :class="[
      'overflow-hidden',
      bordered && 'border rounded-lg',
      className
    ]"
  >
    <!-- Header -->
    <div
      :class="[
        'flex items-center justify-between',
        clickable && 'cursor-pointer select-none hover:bg-gray-50',
        bordered && 'border-b',
        padding && 'p-4'
      ]"
      @click="clickable && toggle()"
    >
      <slot name="header">
        <div class="flex items-center">
          <!-- Icon -->
          <i
            v-if="icon"
            :class="[icon, 'mr-3 text-gray-400']"
          ></i>

          <!-- Title -->
          <h3
            class="text-sm font-medium text-gray-900"
            :class="{ 'text-primary-600': isActive }"
          >
            {{ title }}
          </h3>
        </div>
      </slot>

      <!-- Arrow Icon -->
      <i
        v-if="arrow"
        :class="[
          'fas fa-chevron-down transition-transform duration-200',
          { 'transform rotate-180': isActive }
        ]"
      ></i>
    </div>

    <!-- Content -->
    <Transition
      name="collapse"
      @enter="startTransition"
      @leave="startTransition"
      @after-enter="endTransition"
      @after-leave="endTransition"
    >
      <div v-show="isActive">
        <div
          ref="content"
          :class="[
            padding && 'p-4',
            { 'bg-gray-50': alternate }
          ]"
        >
          <slot></slot>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  arrow: {
    type: Boolean,
    default: true
  },
  bordered: {
    type: Boolean,
    default: false
  },
  padding: {
    type: Boolean,
    default: true
  },
  alternate: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// Refs
const content = ref(null)

// Computed
const isActive = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Methods
const toggle = () => {
  isActive.value = !isActive.value
  emit('change', isActive.value)
}

const startTransition = (el) => {
  el.style.height = '0'
  el.style.overflow = 'hidden'
  el.style.transition = 'height 0.3s ease'
  
  // Force a reflow
  el.offsetHeight

  // Set the final height
  el.style.height = `${el.scrollHeight}px`
}

const endTransition = (el) => {
  el.style.height = ''
  el.style.overflow = ''
  el.style.transition = ''
}
</script>

<style scoped>
/* Base transition classes */
.collapse-enter-active,
.collapse-leave-active {
  @apply transition-all duration-300 ease-in-out;
  overflow: hidden;
}

.collapse-enter-from,
.collapse-leave-to {
  @apply opacity-0;
  height: 0;
}

/* Optional: Add fade transition */
.fade-enter-active,
.fade-leave-active {
  @apply transition-opacity duration-300;
}

.fade-enter-from,
.fade-leave-to {
  @apply opacity-0;
}

/* Optional: Add border animation */
.border-animate {
  @apply transition-all duration-300;
}

.border-animate:hover {
  @apply border-primary-500;
}

/* Optional: Add shadow on hover */
.shadow-hover {
  @apply transition-shadow duration-200;
}

.shadow-hover:hover {
  @apply shadow-md;
}

/* Optional: Add background transition */
.bg-transition {
  @apply transition-colors duration-200;
}

.bg-transition:hover {
  @apply bg-gray-50;
}

/* Optional: Add icon rotation */
.icon-rotate {
  @apply transition-transform duration-200;
}

.icon-rotate.active {
  @apply transform rotate-180;
}

/* Optional: Add nested collapse styles */
.nested {
  @apply pl-4 border-l border-gray-200;
}

/* Optional: Add group hover effects */
.group:hover .group-hover\:text-primary-600 {
  @apply text-primary-600;
}
</style>
