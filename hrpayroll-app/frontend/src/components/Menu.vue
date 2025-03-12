<template>
  <div class="relative">
    <!-- Menu Trigger -->
    <div @click="toggle" ref="trigger">
      <slot name="trigger">
        <Button
          :variant="buttonVariant"
          :size="buttonSize"
          :class="buttonClass"
        >
          {{ label }}
          <i
            v-if="showIcon"
            :class="[
              'fas fa-chevron-down ml-2 transition-transform duration-200',
              { 'transform rotate-180': isOpen }
            ]"
          ></i>
        </Button>
      </slot>
    </div>

    <!-- Menu Items -->
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
        ref="menu"
        :class="[
          'absolute z-50 mt-2 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5',
          positionClass,
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

          <!-- Search -->
          <div v-if="searchable" class="px-3 py-2">
            <input
              v-model="searchQuery"
              type="text"
              class="w-full form-input text-sm"
              :placeholder="searchPlaceholder"
              @click.stop
            />
          </div>

          <!-- Menu Items -->
          <template v-for="(item, index) in filteredItems" :key="index">
            <!-- Divider -->
            <div
              v-if="item.divider"
              class="my-1 border-t border-gray-100"
            ></div>

            <!-- Group -->
            <div v-else-if="item.group" class="px-3 py-2">
              <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                {{ item.label }}
              </div>
            </div>

            <!-- Item -->
            <template v-else>
              <component
                :is="item.to ? 'router-link' : 'button'"
                v-bind="item.to ? { to: item.to } : {}"
                :class="[
                  'block w-full text-left px-4 py-2 text-sm',
                  item.disabled
                    ? 'text-gray-400 cursor-not-allowed'
                    : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900',
                  { 'bg-gray-100 text-gray-900': isActive(item) }
                ]"
                :disabled="item.disabled"
                @click="selectItem(item)"
                role="menuitem"
              >
                <div class="flex items-center">
                  <!-- Icon -->
                  <i
                    v-if="item.icon"
                    :class="[item.icon, 'mr-3 text-gray-400']"
                  ></i>

                  <!-- Label -->
                  <span>{{ item.label }}</span>

                  <!-- Badge -->
                  <Badge
                    v-if="item.badge"
                    :variant="item.badgeVariant"
                    :label="item.badge"
                    class="ml-auto"
                  />

                  <!-- Active Indicator -->
                  <i
                    v-if="isActive(item)"
                    class="fas fa-check ml-auto text-primary-600"
                  ></i>
                </div>

                <!-- Description -->
                <p
                  v-if="item.description"
                  class="mt-1 text-xs text-gray-500"
                >
                  {{ item.description }}
                </p>
              </component>
            </template>
          </template>

          <!-- Empty State -->
          <div
            v-if="searchable && !filteredItems.length"
            class="px-4 py-2 text-sm text-gray-500 text-center"
          >
            No results found
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Button from './Button.vue'
import Badge from './Badge.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  label: {
    type: String,
    default: 'Menu'
  },
  showIcon: {
    type: Boolean,
    default: true
  },
  position: {
    type: String,
    default: 'bottom-right',
    validator: (value) => [
      'top-left',
      'top-right',
      'bottom-left',
      'bottom-right'
    ].includes(value)
  },
  searchable: {
    type: Boolean,
    default: false
  },
  searchPlaceholder: {
    type: String,
    default: 'Search...'
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
  menuClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['select'])

// State
const route = useRoute()
const isOpen = ref(false)
const searchQuery = ref('')
const trigger = ref(null)
const menu = ref(null)

// Computed
const positionClass = computed(() => {
  const positions = {
    'top-left': 'bottom-full right-0 mb-2',
    'top-right': 'bottom-full left-0 mb-2',
    'bottom-left': 'top-full right-0',
    'bottom-right': 'top-full left-0'
  }
  return positions[props.position]
})

const filteredItems = computed(() => {
  let items = props.items
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(item =>
      !item.divider &&
      !item.group &&
      item.label.toLowerCase().includes(query)
    )
  }
  return items
})

// Methods
const toggle = () => {
  isOpen.value = !isOpen.value
}

const close = (e) => {
  if (
    !trigger.value?.contains(e.target) &&
    !menu.value?.contains(e.target)
  ) {
    isOpen.value = false
  }
}

const selectItem = (item) => {
  if (!item.disabled) {
    emit('select', item)
    isOpen.value = false
  }
}

const isActive = (item) => {
  if (item.to) {
    return route.path === item.to
  }
  return item.active
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
</script>

<style scoped>
.menu-enter-active,
.menu-leave-active {
  @apply transition-all duration-200 ease-in-out;
}

.menu-enter-from,
.menu-leave-to {
  @apply opacity-0 scale-95;
}

/* Optional: Add custom scrollbar styles */
.menu-items {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.gray.400') theme('colors.gray.100');
}

.menu-items::-webkit-scrollbar {
  width: 6px;
}

.menu-items::-webkit-scrollbar-track {
  @apply bg-gray-100 rounded;
}

.menu-items::-webkit-scrollbar-thumb {
  @apply bg-gray-400 rounded;
}
</style>
