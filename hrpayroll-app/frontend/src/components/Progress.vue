<template>
  <div>
    <!-- Label -->
    <div
      v-if="label || showPercentage"
      class="flex justify-between items-center mb-1"
    >
      <span
        v-if="label"
        class="text-sm font-medium text-gray-700"
      >
        {{ label }}
      </span>
      <span
        v-if="showPercentage"
        class="text-sm font-medium text-gray-600"
      >
        {{ percentage }}%
      </span>
    </div>

    <!-- Progress Bar Container -->
    <div
      class="relative"
      :class="[
        rounded ? 'rounded-full' : 'rounded',
        sizeClasses.container
      ]"
    >
      <!-- Background -->
      <div
        class="overflow-hidden w-full bg-gray-200"
        :class="[
          rounded ? 'rounded-full' : 'rounded',
          sizeClasses.container
        ]"
      >
        <!-- Progress Bar -->
        <div
          class="transition-all duration-300 ease-in-out"
          :class="[
            rounded ? 'rounded-full' : 'rounded',
            variantClasses,
            sizeClasses.bar,
            animated ? 'animate-progress' : ''
          ]"
          :style="{
            width: `${percentage}%`,
            transitionDuration: `${animationDuration}ms`
          }"
        >
          <!-- Indeterminate Animation -->
          <div
            v-if="indeterminate"
            class="progress-indeterminate"
          ></div>

          <!-- Inner Label -->
          <span
            v-if="showLabel && !indeterminate"
            class="absolute inset-0 flex items-center justify-center text-white text-sm font-semibold"
          >
            {{ percentage }}%
          </span>
        </div>
      </div>

      <!-- Steps -->
      <div
        v-if="steps > 0"
        class="absolute top-0 left-0 w-full h-full flex"
        :class="{ 'px-2': steps > 1 }"
      >
        <div
          v-for="step in steps - 1"
          :key="step"
          class="flex-1 border-l-2 border-gray-100"
          :style="{ left: `${(step / steps) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Description -->
    <p
      v-if="description"
      class="mt-1 text-sm text-gray-500"
    >
      {{ description }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100
  },
  label: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  variant: {
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
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  rounded: {
    type: Boolean,
    default: false
  },
  showPercentage: {
    type: Boolean,
    default: true
  },
  showLabel: {
    type: Boolean,
    default: false
  },
  animated: {
    type: Boolean,
    default: true
  },
  indeterminate: {
    type: Boolean,
    default: false
  },
  steps: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0
  },
  animationDuration: {
    type: Number,
    default: 600
  }
})

// Computed
const percentage = computed(() => {
  return Math.min(Math.max(Math.round(props.value), 0), 100)
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: {
      container: 'h-1.5',
      bar: 'h-1.5'
    },
    md: {
      container: 'h-2.5',
      bar: 'h-2.5'
    },
    lg: {
      container: 'h-4',
      bar: 'h-4'
    }
  }
  return sizes[props.size]
})

const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-primary-600',
    secondary: 'bg-gray-600',
    success: 'bg-green-600',
    danger: 'bg-red-600',
    warning: 'bg-yellow-600',
    info: 'bg-blue-600'
  }
  return variants[props.variant]
})
</script>

<style scoped>
/* Indeterminate animation */
.progress-indeterminate {
  @apply absolute inset-0;
  background-image: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.15) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.15) 75%,
    transparent 75%,
    transparent
  );
  background-size: 1rem 1rem;
  animation: progress-stripes 1s linear infinite;
}

@keyframes progress-stripes {
  from {
    background-position: 1rem 0;
  }
  to {
    background-position: 0 0;
  }
}

/* Progress animation */
.animate-progress {
  transition-property: width;
  transition-timing-function: ease-in-out;
}

/* Pulse animation for indeterminate state */
.progress-pulse {
  animation: progress-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes progress-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Optional: Add gradient effect */
.progress-gradient {
  background-image: linear-gradient(
    to right,
    var(--tw-gradient-from),
    var(--tw-gradient-to)
  );
}
</style>
