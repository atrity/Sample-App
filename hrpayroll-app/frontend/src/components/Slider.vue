<template>
  <div
    :class="[
      'relative',
      disabled ? 'opacity-50 cursor-not-allowed' : '',
      className
    ]"
  >
    <!-- Label -->
    <div
      v-if="label"
      class="flex items-center justify-between mb-2"
    >
      <label class="block text-sm font-medium text-gray-700">
        {{ label }}
      </label>
      <span
        v-if="showValue"
        class="text-sm text-gray-500"
      >
        {{ formatValue(modelValue) }}
      </span>
    </div>

    <!-- Slider Container -->
    <div
      ref="container"
      class="relative h-2 bg-gray-200 rounded-full"
      :class="{ 'cursor-pointer': !disabled }"
      @click="handleContainerClick"
    >
      <!-- Track Fill -->
      <div
        class="absolute h-full rounded-full transition-all duration-150"
        :class="[
          trackColorClass,
          { 'opacity-75': disabled }
        ]"
        :style="{ width: `${percentage}%` }"
      ></div>

      <!-- Thumb -->
      <div
        ref="thumb"
        class="absolute w-4 h-4 -mt-1.5 -ml-2 rounded-full shadow transition-all duration-150 focus:outline-none"
        :class="[
          thumbColorClass,
          disabled ? 'cursor-not-allowed' : 'cursor-grab active:cursor-grabbing',
          { 'ring-2 ring-offset-2': focused }
        ]"
        :style="{ left: `${percentage}%` }"
        tabindex="0"
        role="slider"
        :aria-valuemin="min"
        :aria-valuemax="max"
        :aria-valuenow="modelValue"
        :aria-disabled="disabled"
        @mousedown="!disabled && startDrag"
        @touchstart="!disabled && startDrag"
        @focus="focused = true"
        @blur="focused = false"
        @keydown.left="!disabled && decrease"
        @keydown.right="!disabled && increase"
        @keydown.down="!disabled && decrease"
        @keydown.up="!disabled && increase"
      ></div>

      <!-- Marks -->
      <template v-if="marks">
        <div
          v-for="mark in markPositions"
          :key="mark.value"
          class="absolute w-1 h-1 -mt-0.5 rounded-full bg-gray-400"
          :style="{ left: `${mark.percentage}%` }"
          :class="{ 'bg-white': mark.percentage <= percentage }"
        ></div>
      </template>
    </div>

    <!-- Steps -->
    <div
      v-if="showSteps"
      class="flex justify-between mt-2"
    >
      <template v-for="step in steps" :key="step">
        <span class="text-xs text-gray-500">
          {{ formatValue(step) }}
        </span>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  min: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 100
  },
  step: {
    type: Number,
    default: 1
  },
  disabled: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: ''
  },
  showValue: {
    type: Boolean,
    default: true
  },
  marks: {
    type: Boolean,
    default: false
  },
  showSteps: {
    type: Boolean,
    default: false
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
      'info'
    ].includes(value)
  },
  format: {
    type: Function,
    default: value => value
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// Refs
const container = ref(null)
const thumb = ref(null)
const isDragging = ref(false)
const focused = ref(false)

// Computed
const percentage = computed(() => {
  return ((props.modelValue - props.min) / (props.max - props.min)) * 100
})

const steps = computed(() => {
  const count = (props.max - props.min) / props.step
  return Array.from({ length: count + 1 }, (_, i) => props.min + (i * props.step))
})

const markPositions = computed(() => {
  return steps.value.map(value => ({
    value,
    percentage: ((value - props.min) / (props.max - props.min)) * 100
  }))
})

const trackColorClass = computed(() => {
  const colors = {
    primary: 'bg-primary-500',
    secondary: 'bg-gray-500',
    success: 'bg-green-500',
    danger: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500'
  }
  return colors[props.color]
})

const thumbColorClass = computed(() => {
  const colors = {
    primary: 'bg-primary-600 hover:bg-primary-700',
    secondary: 'bg-gray-600 hover:bg-gray-700',
    success: 'bg-green-600 hover:bg-green-700',
    danger: 'bg-red-600 hover:bg-red-700',
    warning: 'bg-yellow-600 hover:bg-yellow-700',
    info: 'bg-blue-600 hover:bg-blue-700'
  }
  return colors[props.color]
})

// Methods
const formatValue = (value) => {
  return props.format(value)
}

const updateValue = (value) => {
  const newValue = Math.min(
    props.max,
    Math.max(props.min, Math.round(value / props.step) * props.step)
  )
  emit('update:modelValue', newValue)
  emit('change', newValue)
}

const getValueFromPosition = (position) => {
  const rect = container.value.getBoundingClientRect()
  const percentage = Math.min(1, Math.max(0, (position - rect.left) / rect.width))
  return props.min + percentage * (props.max - props.min)
}

const handleContainerClick = (event) => {
  if (!props.disabled) {
    updateValue(getValueFromPosition(event.clientX))
  }
}

const startDrag = (event) => {
  event.preventDefault()
  isDragging.value = true
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchmove', handleDrag)
  document.addEventListener('touchend', stopDrag)
}

const handleDrag = (event) => {
  if (isDragging.value) {
    const clientX = event.touches ? event.touches[0].clientX : event.clientX
    updateValue(getValueFromPosition(clientX))
  }
}

const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', handleDrag)
  document.removeEventListener('touchend', stopDrag)
}

const increase = () => {
  updateValue(props.modelValue + props.step)
}

const decrease = () => {
  updateValue(props.modelValue - props.step)
}

// Lifecycle
onBeforeUnmount(() => {
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', handleDrag)
  document.removeEventListener('touchend', stopDrag)
})
</script>

<style scoped>
/* Optional: Add thumb hover effect */
.slider-thumb-hover {
  @apply transition-transform duration-200;
}

.slider-thumb-hover:hover {
  @apply transform scale-110;
}

/* Optional: Add track hover effect */
.slider-track-hover {
  @apply transition-colors duration-200;
}

.slider-track-hover:hover {
  @apply bg-opacity-75;
}

/* Optional: Add focus styles */
.slider-focus {
  @apply ring-2 ring-offset-2 ring-primary-500;
}

/* Optional: Add disabled styles */
.slider-disabled {
  @apply opacity-50 cursor-not-allowed;
}

/* Optional: Add marks animation */
.slider-mark-enter-active,
.slider-mark-leave-active {
  @apply transition-all duration-200;
}

.slider-mark-enter-from,
.slider-mark-leave-to {
  @apply opacity-0 scale-0;
}
</style>
