<template>
  <Teleport :to="target">
    <div
      v-if="mounted"
      :class="[
        'portal-content',
        className
      ]"
      :style="style"
    >
      <slot></slot>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  target: {
    type: String,
    default: 'body'
  },
  append: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  },
  style: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['mount', 'unmount'])

// State
const mounted = ref(false)
let targetElement = null

// Methods
const createTargetElement = () => {
  if (!props.append) return

  const existingTarget = document.querySelector(props.target)
  if (existingTarget) return

  const el = document.createElement('div')
  el.id = props.target.replace(/[#.]/g, '')
  document.body.appendChild(el)
  targetElement = el
}

const removeTargetElement = () => {
  if (targetElement && props.append) {
    targetElement.remove()
    targetElement = null
  }
}

// Lifecycle
onMounted(() => {
  if (!props.disabled) {
    createTargetElement()
    mounted.value = true
    emit('mount')
  }
})

onBeforeUnmount(() => {
  mounted.value = false
  removeTargetElement()
  emit('unmount')
})

// Watch for disabled prop changes
watch(() => props.disabled, (newValue) => {
  if (newValue) {
    mounted.value = false
    removeTargetElement()
    emit('unmount')
  } else {
    createTargetElement()
    mounted.value = true
    emit('mount')
  }
})
</script>

<style scoped>
/* Animation classes */
.portal-enter-active,
.portal-leave-active {
  @apply transition-all duration-300;
}

.portal-enter-from,
.portal-leave-to {
  @apply opacity-0 transform scale-95;
}

/* Optional: Add z-index utilities */
.portal-z-10 {
  @apply z-10;
}

.portal-z-20 {
  @apply z-20;
}

.portal-z-30 {
  @apply z-30;
}

.portal-z-40 {
  @apply z-40;
}

.portal-z-50 {
  @apply z-50;
}

/* Optional: Add positioning utilities */
.portal-fixed {
  @apply fixed;
}

.portal-absolute {
  @apply absolute;
}

/* Optional: Add backdrop styles */
.portal-backdrop {
  @apply fixed inset-0 bg-black bg-opacity-50;
}

/* Optional: Add container styles */
.portal-container {
  @apply fixed inset-0 overflow-y-auto;
}

/* Optional: Add centering utilities */
.portal-center {
  @apply flex items-center justify-center min-h-screen;
}

/* Optional: Add focus trap styles */
.portal-focus-trap {
  @apply focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500;
}
</style>
