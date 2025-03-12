<template>
  <div
    :class="[
      'inline-flex items-center',
      disabled ? 'opacity-50 cursor-not-allowed' : '',
      className
    ]"
  >
    <!-- Stars -->
    <div class="flex">
      <template v-for="index in maxValue" :key="index">
        <button
          type="button"
          :class="[
            'focus:outline-none transition-colors duration-150',
            disabled ? 'cursor-not-allowed' : 'cursor-pointer',
            getStarClass(index)
          ]"
          :style="{ fontSize: size + 'px' }"
          @click="!disabled && updateValue(index)"
          @mouseover="!disabled && hover(index)"
          @mouseleave="!disabled && hover(0)"
        >
          <i
            :class="[
              getStarIconClass(index),
              'transform transition-transform duration-150 hover:scale-110'
            ]"
          ></i>
        </button>
      </template>
    </div>

    <!-- Label -->
    <span
      v-if="showValue"
      class="ml-2 text-sm text-gray-600"
    >
      {{ hoverValue || modelValue || 0 }} / {{ maxValue }}
    </span>

    <!-- Description -->
    <span
      v-if="descriptions?.length"
      class="ml-2 text-sm text-gray-600"
    >
      {{ getCurrentDescription }}
    </span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0
  },
  maxValue: {
    type: Number,
    default: 5
  },
  size: {
    type: Number,
    default: 24
  },
  disabled: {
    type: Boolean,
    default: false
  },
  showValue: {
    type: Boolean,
    default: false
  },
  descriptions: {
    type: Array,
    default: () => []
  },
  color: {
    type: String,
    default: 'warning',
    validator: (value) => [
      'primary',
      'secondary',
      'success',
      'danger',
      'warning',
      'info'
    ].includes(value)
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// State
const hoverValue = ref(0)

// Computed
const colorClass = computed(() => {
  const colors = {
    primary: 'text-primary-400',
    secondary: 'text-gray-400',
    success: 'text-green-400',
    danger: 'text-red-400',
    warning: 'text-yellow-400',
    info: 'text-blue-400'
  }
  return colors[props.color]
})

const activeColorClass = computed(() => {
  const colors = {
    primary: 'text-primary-500',
    secondary: 'text-gray-500',
    success: 'text-green-500',
    danger: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500'
  }
  return colors[props.color]
})

const getCurrentDescription = computed(() => {
  const value = hoverValue.value || props.modelValue || 0
  return props.descriptions[value - 1] || ''
})

// Methods
const getStarClass = (index) => {
  const isActive = index <= (hoverValue.value || props.modelValue)
  return isActive ? activeColorClass.value : colorClass.value
}

const getStarIconClass = (index) => {
  const value = hoverValue.value || props.modelValue
  
  if (index <= value) {
    return 'fas fa-star'
  }
  
  if (index - value < 1 && index - value > 0) {
    return 'fas fa-star-half-alt'
  }
  
  return 'far fa-star'
}

const updateValue = (value) => {
  if (value === props.modelValue) {
    value = 0
  }
  emit('update:modelValue', value)
  emit('change', value)
}

const hover = (value) => {
  if (!props.disabled) {
    hoverValue.value = value
  }
}
</script>

<style scoped>
/* Optional: Add hover animations */
.star-hover {
  @apply transition-all duration-200;
}

.star-hover:hover {
  @apply transform scale-110;
}

/* Optional: Add click animation */
.star-click {
  @apply transition-transform duration-100;
}

.star-click:active {
  @apply transform scale-90;
}

/* Optional: Add glow effect */
.star-glow {
  filter: drop-shadow(0 0 2px currentColor);
}

/* Optional: Add rating descriptions fade */
.rating-description-enter-active,
.rating-description-leave-active {
  @apply transition-opacity duration-200;
}

.rating-description-enter-from,
.rating-description-leave-to {
  @apply opacity-0;
}

/* Optional: Add responsive sizes */
@screen sm {
  .rating-responsive {
    font-size: 1.25rem;
  }
}

@screen lg {
  .rating-responsive {
    font-size: 1.5rem;
  }
}
</style>
