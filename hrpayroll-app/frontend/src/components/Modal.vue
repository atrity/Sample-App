<template>
  <Teleport to="body">
    <Transition
      enter-active-class="ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click="closeOnBackdrop && $emit('update:modelValue', false)"
      >
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

        <!-- Modal Panel -->
        <div class="flex min-h-screen items-center justify-center p-4 text-center sm:p-0">
          <Transition
            enter-active-class="ease-out duration-300"
            enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="opacity-100 translate-y-0 sm:scale-100"
            leave-active-class="ease-in duration-200"
            leave-from-class="opacity-100 translate-y-0 sm:scale-100"
            leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div
              v-if="modelValue"
              class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 w-full"
              :class="[
                size === 'small' ? 'sm:max-w-sm' : null,
                size === 'medium' ? 'sm:max-w-lg' : null,
                size === 'large' ? 'sm:max-w-xl' : null,
                size === 'xl' ? 'sm:max-w-2xl' : null,
                size === 'full' ? 'sm:max-w-full sm:mx-4' : null
              ]"
              @click.stop
            >
              <!-- Header -->
              <div v-if="$slots.header || title" class="bg-white px-4 py-5 sm:px-6">
                <div class="flex items-center justify-between">
                  <slot name="header">
                    <h3 class="text-lg font-medium leading-6 text-gray-900">
                      {{ title }}
                    </h3>
                  </slot>
                  <button
                    v-if="showClose"
                    type="button"
                    class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none"
                    @click="$emit('update:modelValue', false)"
                  >
                    <span class="sr-only">Close</span>
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <p
                  v-if="description"
                  class="mt-1 text-sm text-gray-500"
                >
                  {{ description }}
                </p>
              </div>

              <!-- Content -->
              <div
                :class="[
                  'bg-white',
                  $slots.footer ? 'sm:p-6' : 'sm:p-6 pb-6'
                ]"
              >
                <slot></slot>
              </div>

              <!-- Footer -->
              <div
                v-if="$slots.footer"
                class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6"
              >
                <slot name="footer"></slot>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { Teleport, Transition } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'xl', 'full'].includes(value)
  },
  showClose: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  }
})

defineEmits(['update:modelValue'])

// Close modal on escape key
const handleEscape = (e) => {
  if (e.key === 'Escape' && props.modelValue) {
    emit('update:modelValue', false)
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
/* Prevent body scroll when modal is open */
:deep(body.modal-open) {
  overflow: hidden;
}
</style>
