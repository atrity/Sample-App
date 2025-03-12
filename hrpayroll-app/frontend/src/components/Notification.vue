<template>
  <Portal>
    <div
      class="fixed inset-0 z-50 pointer-events-none flex items-start justify-center"
      :class="positionClasses"
    >
      <TransitionGroup
        name="notification"
        tag="div"
        class="space-y-2"
      >
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5"
          :class="[
            notification.className,
            { 'cursor-pointer': notification.clickable }
          ]"
          @click="notification.clickable && handleClick(notification)"
        >
          <div class="p-4">
            <div class="flex items-start">
              <!-- Icon -->
              <div
                v-if="notification.icon || notification.type"
                class="flex-shrink-0"
                :class="getIconColorClass(notification.type)"
              >
                <i :class="[getIconClass(notification), 'text-lg']"></i>
              </div>

              <!-- Content -->
              <div class="ml-3 w-0 flex-1">
                <!-- Title -->
                <p
                  v-if="notification.title"
                  class="text-sm font-medium text-gray-900"
                >
                  {{ notification.title }}
                </p>

                <!-- Message -->
                <p
                  class="mt-1 text-sm text-gray-500"
                  :class="{ 'mt-0': !notification.title }"
                >
                  {{ notification.message }}
                </p>

                <!-- Actions -->
                <div
                  v-if="notification.actions?.length"
                  class="mt-3 flex space-x-4"
                >
                  <button
                    v-for="action in notification.actions"
                    :key="action.label"
                    class="text-sm font-medium focus:outline-none"
                    :class="[
                      action.variant === 'primary'
                        ? 'text-primary-600 hover:text-primary-500'
                        : 'text-gray-700 hover:text-gray-500'
                    ]"
                    @click.stop="handleAction(notification, action)"
                  >
                    {{ action.label }}
                  </button>
                </div>
              </div>

              <!-- Close Button -->
              <div class="ml-4 flex flex-shrink-0">
                <button
                  class="inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
                  @click.stop="remove(notification.id)"
                >
                  <i class="fas fa-times"></i>
                  <span class="sr-only">Close</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Progress Bar -->
          <div
            v-if="notification.duration && notification.duration > 0"
            class="h-1 bg-gray-100"
          >
            <div
              class="h-full transition-all duration-300 bg-primary-500"
              :class="getProgressColorClass(notification.type)"
              :style="{
                width: `${getProgress(notification)}%`
              }"
            ></div>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Portal>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import Portal from './Portal.vue'

const props = defineProps({
  position: {
    type: String,
    default: 'top-right',
    validator: (value) => [
      'top',
      'top-right',
      'top-left',
      'bottom',
      'bottom-right',
      'bottom-left'
    ].includes(value)
  },
  maxNotifications: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['action', 'remove', 'click'])

// State
const notifications = ref([])
const timers = new Map()

// Computed
const positionClasses = computed(() => {
  const positions = {
    'top': 'items-start justify-center pt-4',
    'top-right': 'items-start justify-end p-4',
    'top-left': 'items-start justify-start p-4',
    'bottom': 'items-end justify-center pb-4',
    'bottom-right': 'items-end justify-end p-4',
    'bottom-left': 'items-end justify-start p-4'
  }
  return positions[props.position]
})

// Methods
const getIconClass = (notification) => {
  if (notification.icon) return notification.icon

  const icons = {
    success: 'fas fa-check-circle',
    info: 'fas fa-info-circle',
    warning: 'fas fa-exclamation-triangle',
    error: 'fas fa-exclamation-circle'
  }
  return icons[notification.type] || 'fas fa-bell'
}

const getIconColorClass = (type) => {
  const colors = {
    success: 'text-green-500',
    info: 'text-blue-500',
    warning: 'text-yellow-500',
    error: 'text-red-500'
  }
  return colors[type] || 'text-gray-400'
}

const getProgressColorClass = (type) => {
  const colors = {
    success: 'bg-green-500',
    info: 'bg-blue-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500'
  }
  return colors[type] || 'bg-primary-500'
}

const getProgress = (notification) => {
  const elapsed = Date.now() - notification.timestamp
  const progress = 100 - (elapsed / notification.duration) * 100
  return Math.max(0, Math.min(100, progress))
}

const add = (notification) => {
  const id = Date.now().toString()
  const newNotification = {
    id,
    timestamp: Date.now(),
    type: 'info',
    duration: 5000,
    ...notification
  }

  notifications.value = [
    newNotification,
    ...notifications.value.slice(0, props.maxNotifications - 1)
  ]

  if (newNotification.duration > 0) {
    const timer = setTimeout(() => {
      remove(id)
    }, newNotification.duration)
    timers.set(id, timer)
  }

  return id
}

const remove = (id) => {
  const timer = timers.get(id)
  if (timer) {
    clearTimeout(timer)
    timers.delete(id)
  }

  notifications.value = notifications.value.filter(n => n.id !== id)
  emit('remove', id)
}

const handleAction = (notification, action) => {
  emit('action', { notification, action })
  if (action.close !== false) {
    remove(notification.id)
  }
}

const handleClick = (notification) => {
  emit('click', notification)
  if (notification.closeOnClick !== false) {
    remove(notification.id)
  }
}

// Lifecycle
onBeforeUnmount(() => {
  timers.forEach(timer => clearTimeout(timer))
  timers.clear()
})

// Expose methods
defineExpose({
  add,
  remove
})
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  @apply transition-all duration-300;
}

.notification-enter-from {
  @apply opacity-0 translate-x-4;
}

.notification-leave-to {
  @apply opacity-0 scale-95;
}

.notification-move {
  @apply transition-transform duration-300;
}
</style>
