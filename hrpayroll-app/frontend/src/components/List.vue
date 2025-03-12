<template>
  <div :class="className">
    <!-- List Header -->
    <div
      v-if="$slots.header || title"
      class="mb-4"
    >
      <slot name="header">
        <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
        <p v-if="description" class="mt-1 text-sm text-gray-500">
          {{ description }}
        </p>
      </slot>
    </div>

    <!-- List Container -->
    <component
      :is="ordered ? 'ol' : 'ul'"
      :class="[
        'divide-y divide-gray-200',
        bordered && 'border border-gray-200 rounded-lg overflow-hidden',
        hoverable && 'hover:divide-gray-300'
      ]"
    >
      <!-- List Items -->
      <template v-for="(item, index) in items" :key="getItemKey(item, index)">
        <component
          :is="as"
          :class="[
            'relative',
            hoverable && !disabled && 'hover:bg-gray-50',
            getItemClass(item, index),
            { 'opacity-50 cursor-not-allowed': disabled }
          ]"
          @click="!disabled && handleClick(item, index)"
        >
          <div :class="[compact ? 'px-4 py-3' : 'px-4 py-4']">
            <!-- Custom Item Template -->
            <slot
              :item="item"
              :index="index"
            >
              <!-- Default Item Template -->
              <div class="flex items-center">
                <!-- Leading -->
                <div v-if="$slots.leading" class="flex-shrink-0 mr-4">
                  <slot name="leading" :item="item" :index="index"></slot>
                </div>

                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <slot name="title" :item="item" :index="index">
                    <p class="text-sm font-medium text-gray-900 truncate">
                      {{ getItemTitle(item) }}
                    </p>
                  </slot>
                  <slot name="description" :item="item" :index="index">
                    <p
                      v-if="getItemDescription(item)"
                      class="mt-1 text-sm text-gray-500"
                    >
                      {{ getItemDescription(item) }}
                    </p>
                  </slot>
                </div>

                <!-- Trailing -->
                <div v-if="$slots.trailing" class="flex-shrink-0 ml-4">
                  <slot name="trailing" :item="item" :index="index"></slot>
                </div>
              </div>
            </slot>
          </div>
        </component>
      </template>

      <!-- Empty State -->
      <li
        v-if="!items.length"
        class="px-4 py-6 text-center"
      >
        <slot name="empty">
          <div class="text-center">
            <i class="fas fa-inbox text-4xl text-gray-400 mb-3"></i>
            <p class="text-gray-500">{{ emptyText }}</p>
          </div>
        </slot>
      </li>
    </component>

    <!-- List Footer -->
    <div v-if="$slots.footer" class="mt-4">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  ordered: {
    type: Boolean,
    default: false
  },
  bordered: {
    type: Boolean,
    default: false
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  compact: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  as: {
    type: String,
    default: 'li',
    validator: (value) => ['li', 'div'].includes(value)
  },
  itemKey: {
    type: [String, Function],
    default: 'id'
  },
  titleKey: {
    type: String,
    default: 'title'
  },
  descriptionKey: {
    type: String,
    default: 'description'
  },
  emptyText: {
    type: String,
    default: 'No items to display'
  },
  className: {
    type: String,
    default: ''
  },
  itemClass: {
    type: [String, Function],
    default: ''
  }
})

const emit = defineEmits(['click'])

// Methods
const getItemKey = (item, index) => {
  if (typeof props.itemKey === 'function') {
    return props.itemKey(item)
  }
  return item[props.itemKey] || index
}

const getItemTitle = (item) => {
  return typeof item === 'string' ? item : item[props.titleKey]
}

const getItemDescription = (item) => {
  return typeof item === 'object' ? item[props.descriptionKey] : null
}

const getItemClass = (item, index) => {
  if (typeof props.itemClass === 'function') {
    return props.itemClass(item, index)
  }
  return props.itemClass
}

const handleClick = (item, index) => {
  emit('click', { item, index })
}
</script>

<style scoped>
/* Animation classes */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* Hover effect */
.list-item-hover {
  @apply transition-colors duration-200;
}

/* Optional: Add selection styles */
.list-item-selected {
  @apply bg-primary-50;
}

/* Optional: Add drag and drop styles */
.list-item-dragging {
  @apply opacity-50 bg-gray-50;
}

.list-item-drag-over {
  @apply border-primary-500;
}

/* Optional: Add nested list styles */
.list-nested {
  @apply pl-4 mt-2;
}

/* Optional: Add grid layout support */
.list-grid {
  @apply grid gap-4;
}
</style>
