<template>
  <div
    :class="[
      'divide-y divide-gray-200',
      bordered && 'border rounded-lg',
      className
    ]"
  >
    <!-- Sections -->
    <template v-for="(section, index) in sections" :key="getKey(section, index)">
      <Collapse
        v-model="activeItems[index]"
        :title="getTitle(section)"
        :icon="getIcon(section)"
        :arrow="arrow"
        :bordered="false"
        :padding="padding"
        :alternate="alternate"
        :clickable="!section.disabled"
        :class="[
          section.className,
          { 'opacity-50 cursor-not-allowed': section.disabled }
        ]"
        @change="handleChange(index)"
      >
        <!-- Custom Header -->
        <template v-if="$slots.header" #header="slotProps">
          <slot
            name="header"
            v-bind="{ ...slotProps, section, index, active: activeItems[index] }"
          ></slot>
        </template>

        <!-- Content -->
        <template v-if="$slots.default" #default="slotProps">
          <slot
            v-bind="{ ...slotProps, section, index, active: activeItems[index] }"
          ></slot>
        </template>
        <template v-else>
          {{ section.content }}
        </template>
      </Collapse>
    </template>

    <!-- Empty State -->
    <div
      v-if="!sections.length"
      class="p-4 text-center text-gray-500"
    >
      <slot name="empty">
        No sections available
      </slot>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Collapse from './Collapse.vue'

const props = defineProps({
  sections: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: [Number, Array],
    default: null
  },
  multiple: {
    type: Boolean,
    default: false
  },
  arrow: {
    type: Boolean,
    default: true
  },
  bordered: {
    type: Boolean,
    default: false
  },
  padding: {
    type: Boolean,
    default: true
  },
  alternate: {
    type: Boolean,
    default: false
  },
  keyField: {
    type: String,
    default: 'id'
  },
  titleField: {
    type: String,
    default: 'title'
  },
  iconField: {
    type: String,
    default: 'icon'
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// State
const activeItems = ref(initializeActiveItems())

// Methods
function initializeActiveItems() {
  if (props.multiple) {
    return props.sections.map((_, index) => 
      Array.isArray(props.modelValue) && props.modelValue.includes(index)
    )
  } else {
    return props.sections.map((_, index) => 
      props.modelValue === index
    )
  }
}

function getKey(section, index) {
  return section[props.keyField] || index
}

function getTitle(section) {
  return section[props.titleField] || section.title || ''
}

function getIcon(section) {
  return section[props.iconField] || section.icon || ''
}

function handleChange(index) {
  if (props.multiple) {
    const newActive = activeItems.value.map((state, i) => 
      i === index ? !state : state
    )
    activeItems.value = newActive
    emit('update:modelValue', newActive.reduce((acc, state, i) => 
      state ? [...acc, i] : acc, []
    ))
  } else {
    const newActive = activeItems.value.map((_, i) => 
      i === index ? !activeItems.value[i] : false
    )
    activeItems.value = newActive
    emit('update:modelValue', newActive.findIndex(state => state))
  }

  emit('change', {
    index,
    active: activeItems.value[index],
    section: props.sections[index]
  })
}

// Watch for external changes
watch(() => props.modelValue, () => {
  activeItems.value = initializeActiveItems()
}, { deep: true })

// Watch for sections changes
watch(() => props.sections.length, () => {
  activeItems.value = initializeActiveItems()
})
</script>

<style scoped>
/* Optional: Add section hover effect */
.accordion-section-hover:hover {
  @apply bg-gray-50;
}

/* Optional: Add active section styles */
.accordion-section-active {
  @apply bg-primary-50;
}

/* Optional: Add transition for section background */
.accordion-section-transition {
  @apply transition-colors duration-200;
}

/* Optional: Add nested accordion styles */
.accordion-nested {
  @apply pl-4;
}

/* Optional: Add custom border styles */
.accordion-bordered {
  @apply border-l-4;
}

.accordion-bordered.active {
  @apply border-primary-500;
}

/* Optional: Add shadow for active section */
.accordion-shadow {
  @apply transition-shadow duration-200;
}

.accordion-shadow.active {
  @apply shadow-md;
}

/* Optional: Add icon styles */
.accordion-icon {
  @apply transition-colors duration-200;
}

.accordion-icon.active {
  @apply text-primary-500;
}

/* Optional: Add group hover effects */
.group:hover .group-hover\:bg-gray-50 {
  @apply bg-gray-50;
}
</style>
