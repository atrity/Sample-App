<template>
  <Transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-100"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="show"
      :class="[
        'rounded-md p-4',
        variantClasses,
        { 'cursor-pointer': dismissible },
        className
      ]"
      role="alert"
      @click="dismissible && dismiss()"
    >
      <div class="flex">
        <!-- Icon -->
        <div class="flex-shrink-0">
          <i
            :class="[
              'text-lg',
              iconClasses,
              icon || defaultIcon
            ]"
          ></i>
        </div>

        <!-- Content -->
        <div class="ml-3 flex-1">
          <!-- Title -->
          <h3
            v-if="title"
            :class="[
              'text-sm font-medium',
              titleColorClasses
            ]"
          >
            {{ title }}
          </h3>

          <!-- Message -->
          <div
            :class="[
              'text-sm',
              messageColorClasses,
              title ? 'mt-2' : ''
            ]"
          >
            <slot>{{ message }}</slot>
          </div>

          <!-- Actions -->
          <div
            v-if="$slots.actions"
            class="mt-4"
          >
            <div class="-mx-2 -my-1.5 flex">
              <slot name="actions"></slot>
            </div>
          </div>
        </div>

        <!-- Dismiss Button -->
        <div
          v-if="dismissible"
          class="ml-auto pl-3"
        >
          <div class="-mx-1.5 -my-1.5">
            <button
              type="button"
              :class="[
                'inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2',
                dismissButtonClasses
              ]"
              @click.stop="dismiss"
            >
              <span class="sr-only">Dismiss</span>
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'info',
    validator: (value) => [
      'info',
      'success',
      'warning',
      'error'
    ].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  dismissible: {
    type: Boolean,
    default: true
  },
  duration: {
    type: Number,
    default: 0 // 0 means no auto-dismiss
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['dismiss'])

// State
const show = ref(true)

// Computed
const variantClasses = computed(() => {
  const variants = {
    info: 'bg-blue-50',
    success: 'bg-green-50',
    warning: 'bg-yellow-50',
    error: 'bg-red-50'
  }
  return variants[props.variant]
})

const iconClasses = computed(() => {
  const variants = {
    info: 'text-blue-400',
    success: 'text-green-400',
    warning: 'text-yellow-400',
    error: 'text-red-400'
  }
  return variants[props.variant]
})

const defaultIcon = computed(() => {
  const icons = {
    info: 'fas fa-info-circle',
    success: 'fas fa-check-circle',
    warning: 'fas fa-exclamation-triangle',
    error: 'fas fa-times-circle'
  }
  return icons[props.variant]
})

const titleColorClasses = computed(() => {
  const colors = {
    info: 'text-blue-800',
    success: 'text-green-800',
    warning: 'text-yellow-800',
    error: 'text-red-800'
  }
  return colors[props.variant]
})

const messageColorClasses = computed(() => {
  const colors = {
    info: 'text-blue-700',
    success: 'text-green-700',
    warning: 'text-yellow-700',
    error: 'text-red-700'
  }
  return colors[props.variant]
})

const dismissButtonClasses = computed(() => {
  const classes = {
    info: 'bg-blue-50 text-blue-500 hover:bg-blue-100 focus:ring-blue-600 focus:ring-offset-blue-50',
    success: 'bg-green-50 text-green-500 hover:bg-green-100 focus:ring-green-600 focus:ring-offset-green-50',
    warning: 'bg-yellow-50 text-yellow-500 hover:bg-yellow-100 focus:ring-yellow-600 focus:ring-offset-yellow-50',
    error: 'bg-red-50 text-red-500 hover:bg-red-100 focus:ring-red-600 focus:ring-offset-red-50'
  }
  return classes[props.variant]
})

// Methods
const dismiss = () => {
  show.value = false
  emit('dismiss')
}

// Auto-dismiss timer
if (props.duration > 0) {
  setTimeout(() => {
    dismiss()
  }, props.duration)
}
</script>

<style scoped>
.alert-enter-active,
.alert-leave-active {
  @apply transition-all duration-300 ease-in-out;
}

.alert-enter-from,
.alert-leave-to {
  @apply opacity-0 transform translate-y-2;
}

/* Slide variants */
.alert-slide-right-enter-active,
.alert-slide-right-leave-active {
  @apply transition-all duration-300 ease-in-out;
}

.alert-slide-right-enter-from,
.alert-slide-right-leave-to {
  @apply opacity-0 transform translate-x-full;
}

.alert-slide-left-enter-active,
.alert-slide-left-leave-active {
  @apply transition-all duration-300 ease-in-out;
}

.alert-slide-left-enter-from,
.alert-slide-left-leave-to {
  @apply opacity-0 transform -translate-x-full;
}
</style>
