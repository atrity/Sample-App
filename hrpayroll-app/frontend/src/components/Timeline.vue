<template>
  <div
    :class="[
      'relative',
      { 'space-y-8': !compact },
      { 'space-y-4': compact },
      className
    ]"
  >
    <!-- Line -->
    <div
      v-if="line"
      class="absolute top-0 left-4 h-full"
      :class="[
        position === 'left' ? 'left-4' : '',
        position === 'right' ? 'right-4' : '',
        position === 'center' ? 'left-1/2' : ''
      ]"
    >
      <div
        class="w-0.5 h-full"
        :class="lineColorClass"
      ></div>
    </div>

    <!-- Items -->
    <div
      v-for="(item, index) in items"
      :key="getItemKey(item, index)"
      :class="[
        'relative flex',
        position === 'left' ? 'flex-row' : '',
        position === 'right' ? 'flex-row-reverse' : '',
        position === 'center' ? index % 2 === 0 ? 'flex-row' : 'flex-row-reverse' : '',
        item.className
      ]"
    >
      <!-- Dot -->
      <div
        :class="[
          'relative flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
          getDotColorClass(item),
          position === 'center' ? 'mx-auto' : ''
        ]"
      >
        <i
          v-if="item.icon"
          :class="[item.icon, 'text-white text-sm']"
        ></i>
        <div
          v-else
          class="w-3 h-3 rounded-full bg-white"
        ></div>
      </div>

      <!-- Content -->
      <div
        :class="[
          'flex-grow',
          position === 'left' ? 'ml-6' : '',
          position === 'right' ? 'mr-6' : '',
          position === 'center' ? index % 2 === 0 ? 'ml-6' : 'mr-6' : ''
        ]"
      >
        <!-- Custom Content -->
        <slot
          :name="'item-' + index"
          :item="item"
          :index="index"
        >
          <!-- Default Content -->
          <div
            :class="[
              'bg-white rounded-lg shadow-sm',
              bordered && 'border',
              padding && 'p-4'
            ]"
          >
            <!-- Header -->
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-sm font-medium text-gray-900">
                {{ item.title }}
              </h4>
              <time
                v-if="item.date"
                class="text-xs text-gray-500"
              >
                {{ formatDate(item.date) }}
              </time>
            </div>

            <!-- Description -->
            <p
              v-if="item.description"
              class="text-sm text-gray-500"
            >
              {{ item.description }}
            </p>

            <!-- Tags -->
            <div
              v-if="item.tags?.length"
              class="mt-2 flex flex-wrap gap-2"
            >
              <Tag
                v-for="tag in item.tags"
                :key="tag"
                :label="tag"
                size="sm"
                variant="secondary"
              />
            </div>

            <!-- Actions -->
            <div
              v-if="item.actions?.length"
              class="mt-3 flex items-center space-x-4"
            >
              <button
                v-for="action in item.actions"
                :key="action.label"
                class="text-sm font-medium text-primary-600 hover:text-primary-500"
                @click="$emit('action', { item, action })"
              >
                {{ action.label }}
              </button>
            </div>
          </div>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Tag from './Tag.vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  },
  position: {
    type: String,
    default: 'left',
    validator: (value) => ['left', 'right', 'center'].includes(value)
  },
  line: {
    type: Boolean,
    default: true
  },
  lineColor: {
    type: String,
    default: 'gray',
    validator: (value) => [
      'gray',
      'primary',
      'success',
      'danger',
      'warning',
      'info'
    ].includes(value)
  },
  compact: {
    type: Boolean,
    default: false
  },
  bordered: {
    type: Boolean,
    default: true
  },
  padding: {
    type: Boolean,
    default: true
  },
  dateFormat: {
    type: [String, Function],
    default: 'default'
  },
  className: {
    type: String,
    default: ''
  }
})

// Methods
const getItemKey = (item, index) => {
  return item.id || index
}

const getDotColorClass = (item) => {
  const colors = {
    primary: 'bg-primary-500',
    success: 'bg-green-500',
    danger: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500',
    gray: 'bg-gray-500'
  }
  return colors[item.variant || 'primary']
}

const lineColorClass = computed(() => {
  const colors = {
    gray: 'bg-gray-200',
    primary: 'bg-primary-200',
    success: 'bg-green-200',
    danger: 'bg-red-200',
    warning: 'bg-yellow-200',
    info: 'bg-blue-200'
  }
  return colors[props.lineColor]
})

const formatDate = (date) => {
  if (!date) return ''
  
  if (typeof props.dateFormat === 'function') {
    return props.dateFormat(date)
  }

  const d = new Date(date)
  
  switch (props.dateFormat) {
    case 'relative':
      return getRelativeTime(d)
    case 'short':
      return d.toLocaleDateString()
    case 'long':
      return d.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    default:
      return d.toLocaleDateString()
  }
}

const getRelativeTime = (date) => {
  const now = new Date()
  const diff = now - date
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 7) {
    return date.toLocaleDateString()
  } else if (days > 0) {
    return `${days}d ago`
  } else if (hours > 0) {
    return `${hours}h ago`
  } else if (minutes > 0) {
    return `${minutes}m ago`
  } else {
    return 'just now'
  }
}
</script>

<style scoped>
/* Optional: Add item hover effect */
.timeline-item-hover {
  @apply transition-transform duration-200;
}

.timeline-item-hover:hover {
  @apply transform scale-[1.02];
}

/* Optional: Add dot pulse animation */
.timeline-dot-pulse::before {
  content: '';
  @apply absolute inset-0 rounded-full;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    @apply opacity-0 scale-100;
  }
  50% {
    @apply opacity-50 scale-150;
  }
}

/* Optional: Add line animation */
.timeline-line-animate {
  animation: grow 1s ease-out forwards;
  transform-origin: top;
}

@keyframes grow {
  from {
    transform: scaleY(0);
  }
  to {
    transform: scaleY(1);
  }
}

/* Optional: Add item slide animation */
.timeline-item-slide-left {
  animation: slideLeft 0.5s ease-out forwards;
}

.timeline-item-slide-right {
  animation: slideRight 0.5s ease-out forwards;
}

@keyframes slideLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
