<template>
  <div>
    <!-- Tab Navigation -->
    <div class="border-b border-gray-200">
      <nav
        class="-mb-px flex space-x-8"
        :class="[
          vertical ? 'flex-col space-x-0 space-y-2' : '',
          className
        ]"
        aria-label="Tabs"
      >
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          :class="[
            tab.id === modelValue
              ? 'border-primary-500 text-primary-600'
              : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
            'group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm',
            tab.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
            vertical ? 'border-b-0 border-l-2' : '',
            tabClass
          ]"
          :aria-current="tab.id === modelValue ? 'page' : undefined"
          @click="!tab.disabled && $emit('update:modelValue', tab.id)"
        >
          <!-- Icon -->
          <i
            v-if="tab.icon"
            :class="[
              tab.icon,
              tab.id === modelValue
                ? 'text-primary-500'
                : 'text-gray-400 group-hover:text-gray-500',
              'mr-2 h-5 w-5'
            ]"
          ></i>

          <!-- Label -->
          <span>{{ tab.label }}</span>

          <!-- Badge -->
          <Badge
            v-if="tab.badge"
            :variant="tab.id === modelValue ? 'primary' : 'secondary'"
            :label="tab.badge"
            class="ml-2"
          />
        </button>
      </nav>
    </div>

    <!-- Tab Panels -->
    <div
      class="mt-4"
      :class="contentClass"
    >
      <TransitionGroup
        :name="transition"
        mode="out-in"
      >
        <div
          v-for="tab in tabs"
          :key="tab.id"
          v-show="tab.id === modelValue"
          role="tabpanel"
          :aria-labelledby="`tab-${tab.id}`"
        >
          <slot
            :name="tab.id"
            :tab="tab"
          >
            {{ tab.content }}
          </slot>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup>
import Badge from './Badge.vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    required: true
  },
  tabs: {
    type: Array,
    required: true,
    validator: (tabs) => {
      return tabs.every(tab => 
        typeof tab === 'object' &&
        'id' in tab &&
        'label' in tab
      )
    }
  },
  vertical: {
    type: Boolean,
    default: false
  },
  transition: {
    type: String,
    default: 'fade',
    validator: (value) => ['fade', 'slide', 'none'].includes(value)
  },
  className: {
    type: String,
    default: ''
  },
  tabClass: {
    type: String,
    default: ''
  },
  contentClass: {
    type: String,
    default: ''
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* Vertical layout styles */
.vertical-tabs {
  @apply flex;
}

.vertical-tabs nav {
  @apply flex-shrink-0 border-r border-gray-200 pr-4;
}

.vertical-tabs nav button {
  @apply border-r-2 border-b-0;
}

.vertical-tabs .tab-content {
  @apply flex-grow pl-4;
}

/* Responsive styles */
@media (max-width: 640px) {
  .vertical-tabs {
    @apply flex-col;
  }

  .vertical-tabs nav {
    @apply border-r-0 border-b border-gray-200 pr-0 pb-4;
  }

  .vertical-tabs .tab-content {
    @apply pl-0 pt-4;
  }
}

/* Active tab indicator animation */
.tab-indicator {
  @apply absolute bottom-0 left-0 h-0.5 bg-primary-500 transition-all duration-200;
}

/* Hover effect */
.tab-hover {
  @apply transition-colors duration-200;
}

.tab-hover:hover {
  @apply text-primary-600;
}

/* Disabled state */
.tab-disabled {
  @apply opacity-50 cursor-not-allowed;
}

/* Badge positioning */
.tab-badge {
  @apply ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium;
}
</style>
