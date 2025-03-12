<template>
  <Portal>
    <Transition name="fade">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click="closeOnBackdropClick && close()"
      >
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>

        <!-- Dialog Container -->
        <div class="flex min-h-screen items-center justify-center p-4">
          <!-- Dialog Panel -->
          <Transition name="scale">
            <div
              v-if="modelValue"
              class="relative w-full max-w-lg transform rounded-lg bg-white shadow-xl transition-all"
              :class="[maxWidth, className]"
              @click.stop
            >
              <!-- Close Button -->
              <button
                v-if="showClose"
                class="absolute right-4 top-4 text-gray-400 hover:text-gray-500"
                @click="close"
              >
                <i class="fas fa-times"></i>
                <span class="sr-only">Close</span>
              </button>

              <!-- Icon -->
              <div v-if="icon || type" class="mx-auto flex h-12 w-12 items-center justify-center rounded-full mt-6" :class="iconBackgroundClass">
                <i :class="[iconClass, 'text-2xl']"></i>
              </div>

              <!-- Content -->
              <div class="p-6">
                <!-- Title -->
                <h3
                  v-if="title"
                  class="text-center text-lg font-medium text-gray-900 mb-4"
                >
                  {{ title }}
                </h3>

                <!-- Message -->
                <div
                  v-if="message"
                  class="text-center text-sm text-gray-500"
                  v-html="message"
                ></div>

                <!-- Custom Content -->
                <slot></slot>
              </div>

              <!-- Actions -->
              <div
                v-if="$slots.actions || showActions"
                class="bg-gray-50 px-6 py-4 rounded-b-lg flex items-center"
                :class="actionsAlign === 'right' ? 'justify-end' : 'justify-center'"
              >
                <slot name="actions">
                  <!-- Cancel Button -->
                  <Button
                    v-if="showCancel"
                    variant="secondary"
                    :label="cancelLabel"
                    @click="handleCancel"
                    class="mr-3"
                  />

                  <!-- Confirm Button -->
                  <Button
                    :variant="confirmVariant"
                    :label="confirmLabel"
                    :loading="loading"
                    @click="handleConfirm"
                  />
                </slot>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </Transition>
  </Portal>
</template>

<script setup>
import { computed } from 'vue'
import Portal from './Portal.vue'
import Button from './Button.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: '',
    validator: (value) => ['', 'info', 'success', 'warning', 'danger'].includes(value)
  },
  icon: {
    type: String,
    default: ''
  },
  maxWidth: {
    type: String,
    default: 'max-w-lg',
    validator: (value) => [
      'max-w-sm',
      'max-w-md',
      'max-w-lg',
      'max-w-xl',
      'max-w-2xl',
      'max-w-3xl',
      'max-w-4xl',
      'max-w-5xl',
      'max-w-6xl',
      'max-w-7xl'
    ].includes(value)
  },
  showClose: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showCancel: {
    type: Boolean,
    default: true
  },
  confirmLabel: {
    type: String,
    default: 'Confirm'
  },
  cancelLabel: {
    type: String,
    default: 'Cancel'
  },
  confirmVariant: {
    type: String,
    default: 'primary'
  },
  actionsAlign: {
    type: String,
    default: 'right',
    validator: (value) => ['left', 'center', 'right'].includes(value)
  },
  closeOnBackdropClick: {
    type: Boolean,
    default: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

// Computed
const iconClass = computed(() => {
  if (props.icon) return props.icon

  const icons = {
    info: 'fas fa-info-circle text-blue-400',
    success: 'fas fa-check-circle text-green-400',
    warning: 'fas fa-exclamation-triangle text-yellow-400',
    danger: 'fas fa-exclamation-circle text-red-400'
  }

  return icons[props.type] || ''
})

const iconBackgroundClass = computed(() => {
  const backgrounds = {
    info: 'bg-blue-100',
    success: 'bg-green-100',
    warning: 'bg-yellow-100',
    danger: 'bg-red-100'
  }

  return backgrounds[props.type] || 'bg-gray-100'
})

// Methods
const close = () => {
  emit('update:modelValue', false)
}

const handleConfirm = () => {
  emit('confirm')
  if (!props.loading) close()
}

const handleCancel = () => {
  emit('cancel')
  close()
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

/* Scale transition */
.scale-enter-active,
.scale-leave-active {
  @apply transition-all duration-300;
}

.scale-enter-from,
.scale-leave-to {
  @apply opacity-0 scale-95;
}

/* Optional: Add slide transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  @apply transition-all duration-300;
}

.slide-up-enter-from,
.slide-up-leave-to {
  @apply opacity-0 translate-y-4;
}

/* Optional: Add focus trap styles */
.dialog-focus-trap {
  @apply focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500;
}

/* Optional: Add custom scrollbar */
.dialog-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.gray.400') theme('colors.gray.100');
}

.dialog-scrollbar::-webkit-scrollbar {
  @apply w-2;
}

.dialog-scrollbar::-webkit-scrollbar-track {
  @apply bg-gray-100 rounded;
}

.dialog-scrollbar::-webkit-scrollbar-thumb {
  @apply bg-gray-400 rounded hover:bg-gray-500;
}
</style>
