<template>
  <div
    :class="[
      'animate-pulse rounded',
      { 'flex items-center space-x-4': variant === 'list-item' },
      className
    ]"
  >
    <!-- Text Lines -->
    <template v-if="variant === 'text'">
      <div
        v-for="i in lines"
        :key="i"
        class="h-4 bg-gray-200 rounded"
        :class="[
          i === lines && !fullWidth ? `w-${width}` : 'w-full',
          i !== lines ? 'mb-2' : ''
        ]"
      ></div>
    </template>

    <!-- Card -->
    <template v-else-if="variant === 'card'">
      <div class="space-y-4">
        <!-- Image -->
        <div
          v-if="hasImage"
          class="h-48 bg-gray-200 rounded"
        ></div>
        <!-- Content -->
        <div class="space-y-3">
          <div class="h-4 bg-gray-200 rounded w-3/4"></div>
          <div class="h-4 bg-gray-200 rounded"></div>
          <div class="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    </template>

    <!-- List Item -->
    <template v-else-if="variant === 'list-item'">
      <!-- Avatar -->
      <div
        v-if="hasAvatar"
        class="rounded-full bg-gray-200 h-10 w-10"
      ></div>
      <!-- Content -->
      <div class="flex-1 space-y-2">
        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
        <div class="h-4 bg-gray-200 rounded w-1/2"></div>
      </div>
    </template>

    <!-- Table -->
    <template v-else-if="variant === 'table'">
      <div class="space-y-4">
        <!-- Header -->
        <div class="flex space-x-4">
          <div
            v-for="i in columns"
            :key="i"
            class="h-4 bg-gray-200 rounded flex-1"
          ></div>
        </div>
        <!-- Rows -->
        <div
          v-for="i in rows"
          :key="i"
          class="flex space-x-4"
        >
          <div
            v-for="j in columns"
            :key="j"
            class="h-4 bg-gray-200 rounded flex-1"
          ></div>
        </div>
      </div>
    </template>

    <!-- Circle -->
    <template v-else-if="variant === 'circle'">
      <div
        class="rounded-full bg-gray-200"
        :style="{
          width: `${size}px`,
          height: `${size}px`
        }"
      ></div>
    </template>

    <!-- Rectangle -->
    <template v-else-if="variant === 'rectangle'">
      <div
        class="bg-gray-200"
        :style="{
          width: `${width}px`,
          height: `${height}px`
        }"
      ></div>
    </template>

    <!-- Custom -->
    <template v-else>
      <slot></slot>
    </template>
  </div>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'text',
    validator: (value) => [
      'text',
      'card',
      'list-item',
      'table',
      'circle',
      'rectangle',
      'custom'
    ].includes(value)
  },
  lines: {
    type: Number,
    default: 3
  },
  width: {
    type: [String, Number],
    default: '3/4'
  },
  height: {
    type: Number,
    default: 20
  },
  fullWidth: {
    type: Boolean,
    default: false
  },
  hasImage: {
    type: Boolean,
    default: false
  },
  hasAvatar: {
    type: Boolean,
    default: true
  },
  columns: {
    type: Number,
    default: 4
  },
  rows: {
    type: Number,
    default: 3
  },
  size: {
    type: Number,
    default: 40
  },
  className: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Optional: Add shimmer effect */
.shimmer {
  position: relative;
  overflow: hidden;
}

.shimmer::after {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  transform: translateX(-100%);
  background-image: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0,
    rgba(255, 255, 255, 0.2) 20%,
    rgba(255, 255, 255, 0.5) 60%,
    rgba(255, 255, 255, 0)
  );
  animation: shimmer 2s infinite;
  content: '';
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style>
