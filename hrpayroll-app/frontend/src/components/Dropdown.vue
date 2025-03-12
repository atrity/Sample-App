<template>
  <div class="relative" @keydown.esc="isOpen = false">
    <!-- Trigger Button -->
    <div
      ref="trigger"
      @click="toggle"
      :class="[
        'inline-flex items-center justify-between',
        { 'cursor-pointer': !disabled },
        { 'opacity-50 cursor-not-allowed': disabled },
        triggerClass
      ]"
    >
      <slot name="trigger">
        <Button
          :variant="buttonVariant"
          :size="buttonSize"
          :disabled="disabled"
          :class="buttonClass"
        >
          {{ label }}
          <i
            :class="[
              'fas fa-chevron-down ml-2 transition-transform duration-200',
              { 'transform rotate-180': isOpen }
            ]"
          ></i>
        </Button>
      </slot>
    </div>

    <!-- Dropdown Menu -->
    <Transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        ref="dropdown"
        :class="[
          'absolute z-50 mt-2 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5',
          positionClasses,
          menuClass
        ]"
      >
        <div
          class="py-1"
          role="menu"
          aria-orientation="vertical"
          :aria-labelledby="id"
        >
          <!-- Header -->
          <div
            v-if="$slots.header"
            class="px-4 py-2 text-sm text-gray-700 border-b border-gray-100"
          >
            <slot name="header"></slot>
          </div>

          <!-- Search Input -->
          <div v-if="searchable" class="px-3 py-2">
            <input
              v-model="searchQuery"
              type="text"
              class="w-full form-input text-sm"
              :placeholder="searchPlaceholder"
              @click.stop
            />
          </div>

          <!-- Items -->
          <div :class="{ 'max-h-60 overflow-auto': scrollable }">
            <slot>
              <template v-if="filteredItems.length">
                <button
                  v-for="item in filteredItems"
                  :key="item.value"
                  type="button"
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900"
                  role="menuitem"
                  @click="selectItem(item)"
                >
                  <div class="flex items-center">
                    <!-- Checkbox for multiple select -->
                    <input
                      v-if="multiple"
                      type="checkbox"
                      :checked="isSelected(item)"
                      class="form-checkbox h-4 w-4 text-primary-600 mr-2"
                      @click.stop
                    />
                    
                    <!-- Item content -->
                    <div class="flex-1">
                      <slot name="item" :item="item">
                        {{ item.label }}
                      </slot>
                    </div>

                    <!-- Selected indicator -->
                    <i
                      v-if="!multiple && isSelected(item)"
                      class="fas fa-check text-primary-600 ml-2"
                    ></i>
                  </div>
                </button>
              </template>
              <div
                v-else
                class="px-4 py-2 text-sm text-gray-500 text-center"
              >
                {{ noResultsText }}
              </div>
            </slot>
          </div>

          <!-- Footer -->
          <div
            v-if="$slots.footer"
            class="px-4 py-2 text-sm text-gray-700 border-t border-gray-100"
          >
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, Array],
    default: ''
  },
  items: {
    type: Array,
    default: () => []
  },
  label: {
    type: String,
    default: 'Select option'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  multiple: {
    type: Boolean,
    default: false
  },
  searchable: {
    type: Boolean,
    default: false
  },
  searchPlaceholder: {
    type: String,
    default: 'Search...'
  },
  noResultsText: {
    type: String,
    default: 'No results found'
  },
  scrollable: {
    type: Boolean,
    default: true
  },
  position: {
    type: String,
    default: 'bottom-left',
    validator: (value) => [
      'top-left',
      'top-right',
      'bottom-left',
      'bottom-right'
    ].includes(value)
  },
  buttonVariant: {
    type: String,
    default: 'primary'
  },
  buttonSize: {
    type: String,
    default: 'md'
  },
  buttonClass: {
    type: String,
    default: ''
  },
  triggerClass: {
    type: String,
    default: ''
  },
  menuClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// State
const isOpen = ref(false)
const searchQuery = ref('')
const trigger = ref(null)
const dropdown = ref(null)

// Computed
const filteredItems = computed(() => {
  if (!searchQuery.value) return props.items
  
  const query = searchQuery.value.toLowerCase()
  return props.items.filter(item =>
    item.label.toLowerCase().includes(query)
  )
})

const positionClasses = computed(() => {
  const positions = {
    'top-left': 'bottom-full right-0 mb-2',
    'top-right': 'bottom-full left-0 mb-2',
    'bottom-left': 'top-full right-0',
    'bottom-right': 'top-full left-0'
  }
  return positions[props.position]
})

// Methods
const toggle = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value
  }
}

const close = (e) => {
  if (!trigger.value?.contains(e.target) && !dropdown.value?.contains(e.target)) {
    isOpen.value = false
  }
}

const selectItem = (item) => {
  if (props.multiple) {
    const value = Array.isArray(props.modelValue) ? [...props.modelValue] : []
    const index = value.indexOf(item.value)
    
    if (index === -1) {
      value.push(item.value)
    } else {
      value.splice(index, 1)
    }
    
    emit('update:modelValue', value)
  } else {
    emit('update:modelValue', item.value)
    isOpen.value = false
  }
  
  emit('change', item)
}

const isSelected = (item) => {
  if (props.multiple) {
    return Array.isArray(props.modelValue) && props.modelValue.includes(item.value)
  }
  return props.modelValue === item.value
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', close)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      isOpen.value = false
    }
  })
})

onUnmounted(() => {
  document.removeEventListener('click', close)
})

// Watchers
watch(isOpen, (value) => {
  if (value) {
    searchQuery.value = ''
    nextTick(() => {
      const input = dropdown.value?.querySelector('input')
      if (input) {
        input.focus()
      }
    })
  }
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  @apply transition-all duration-200 ease-in-out;
}

.dropdown-enter-from,
.dropdown-leave-to {
  @apply opacity-0 scale-95;
}
</style>
