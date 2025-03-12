<template>
  <TransitionGroup
    tag="div"
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="transform translate-y-2 opacity-0"
    enter-to-class="transform translate-y-0 opacity-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="transform translate-y-0 opacity-100"
    leave-to-class="transform translate-y-2 opacity-0"
    class="fixed bottom-0 right-0 p-4 z-50 space-y-4"
  >
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="[
        'max-w-sm w-full shadow-lg rounded-lg pointer-events-auto overflow-hidden',
        toast.type === 'success' ? 'bg-green-500' : 'bg-red-500'
      ]"
    >
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <i
              :class="[
                'text-white text-lg',
                toast.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'
              ]"
            ></i>
          </div>
          <div class="ml-3 w-0 flex-1">
            <p class="text-sm font-medium text-white">
              {{ toast.message }}
            </p>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <button
              @click="removeToast(toast.id)"
              class="inline-flex text-white hover:text-gray-200 focus:outline-none"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </TransitionGroup>
</template>

<script setup>
import { ref } from 'vue'
import { TransitionGroup } from 'vue'

const toasts = ref([])
const toastDuration = 5000 // 5 seconds

const addToast = (message, type = 'success') => {
  const id = Date.now()
  toasts.value.push({ id, message, type })

  // Auto remove toast after duration
  setTimeout(() => {
    removeToast(id)
  }, toastDuration)
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// Expose methods to parent components
defineExpose({
  addToast,
  removeToast
})
</script>

<script>
// Create a global toast instance
let toastInstance = null

export function useToast() {
  return {
    setInstance(instance) {
      toastInstance = instance
    },
    show(message, type = 'success') {
      if (toastInstance) {
        toastInstance.addToast(message, type)
      }
    },
    success(message) {
      this.show(message, 'success')
    },
    error(message) {
      this.show(message, 'error')
    }
  }
}
</script>
