<template>
  <div
    :class="[
      'flex items-center',
      vertical ? 'flex-col h-full' : 'w-full',
      className
    ]"
  >
    <!-- Left Content -->
    <div
      v-if="$slots.left && !vertical"
      class="flex-shrink-0 pr-4"
    >
      <slot name="left"></slot>
    </div>

    <!-- Top Content -->
    <div
      v-if="$slots.top && vertical"
      class="flex-shrink-0 pb-4"
    >
      <slot name="top"></slot>
    </div>

    <!-- Line -->
    <div
      :class="[
        vertical ? 'w-px h-full' : 'w-full h-px',
        {
          'border-t': !vertical && type === 'solid',
          'border-l': vertical && type === 'solid',
          'border-dashed': type === 'dashed',
          'border-dotted': type === 'dotted'
        },
        colorClasses,
        { 'flex-1': hasContent }
      ]"
    >
      <!-- Center Content -->
      <div
        v-if="$slots.default"
        :class="[
          'flex',
          vertical ? 'flex-col items-center' : 'items-center justify-center',
          { '-mt-3': !vertical, '-ml-3': vertical }
        ]"
      >
        <div
          :class="[
            'px-3',
            vertical ? 'rotate-90' : '',
            textColorClasses,
            backgroundClass
          ]"
        >
          <slot></slot>
        </div>
      </div>
    </div>

    <!-- Right Content -->
    <div
      v-if="$slots.right && !vertical"
      class="flex-shrink-0 pl-4"
    >
      <slot name="right"></slot>
    </div>

    <!-- Bottom Content -->
    <div
      v-if="$slots.bottom && vertical"
      class="flex-shrink-0 pt-4"
    >
      <slot name="bottom"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  vertical: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'solid',
    validator: (value) => ['solid', 'dashed', 'dotted'].includes(value)
  },
  color: {
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
  textColor: {
    type: String,
    default: 'gray'
  },
  className: {
    type: String,
    default: ''
  }
})

// Computed
const hasContent = computed(() => {
  return Boolean(
    props.vertical
      ? props.$slots.top || props.$slots.bottom
      : props.$slots.left || props.$slots.right
  )
})

const colorClasses = computed(() => {
  const colors = {
    gray: 'border-gray-200',
    primary: 'border-primary-200',
    success: 'border-green-200',
    danger: 'border-red-200',
    warning: 'border-yellow-200',
    info: 'border-blue-200'
  }
  return colors[props.color]
})

const textColorClasses = computed(() => {
  const colors = {
    gray: 'text-gray-500',
    primary: 'text-primary-500',
    success: 'text-green-500',
    danger: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500'
  }
  return colors[props.textColor]
})

const backgroundClass = computed(() => {
  return props.vertical ? 'bg-transparent' : 'bg-white'
})
</script>

<style scoped>
/* Optional: Add transition for hover effects */
.divider-hover {
  @apply transition-colors duration-200;
}

.divider-hover:hover {
  @apply border-opacity-75;
}

/* Optional: Add gradient effect */
.divider-gradient {
  background: linear-gradient(
    90deg,
    transparent,
    var(--divider-color),
    transparent
  );
}

.divider-gradient-vertical {
  background: linear-gradient(
    180deg,
    transparent,
    var(--divider-color),
    transparent
  );
}

/* Optional: Add shadow effect */
.divider-shadow {
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Optional: Add spacing utilities */
.divider-space-sm {
  @apply my-2;
}

.divider-space-md {
  @apply my-4;
}

.divider-space-lg {
  @apply my-6;
}

.divider-space-vertical-sm {
  @apply mx-2;
}

.divider-space-vertical-md {
  @apply mx-4;
}

.divider-space-vertical-lg {
  @apply mx-6;
}
</style>
