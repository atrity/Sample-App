<template>
  <div
    class="flex h-screen flex-col"
    :class="{ 'w-64': !collapsed, 'w-16': collapsed }"
  >
    <!-- Logo Section -->
    <div class="flex h-16 items-center justify-between px-4 bg-primary-700">
      <router-link
        to="/"
        class="flex items-center"
        :class="{ 'justify-center': collapsed }"
      >
        <img
          src="/logo.svg"
          alt="Logo"
          class="h-8 w-8"
        />
        <span
          v-if="!collapsed"
          class="ml-2 text-xl font-semibold text-white"
        >
          HR & Payroll
        </span>
      </router-link>
      <button
        v-if="collapsible"
        @click="toggleCollapse"
        class="text-white hover:text-gray-200"
      >
        <i
          :class="[
            'fas',
            collapsed ? 'fa-chevron-right' : 'fa-chevron-left'
          ]"
        ></i>
      </button>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 overflow-y-auto bg-primary-800 px-2 py-4">
      <ul class="space-y-1">
        <li v-for="item in filteredMenuItems" :key="item.path">
          <!-- Menu Item -->
          <router-link
            v-if="!item.children"
            :to="item.path"
            :class="[
              isActive(item.path)
                ? 'bg-primary-900 text-white'
                : 'text-primary-100 hover:bg-primary-700',
              'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
            ]"
          >
            <i
              v-if="item.icon"
              :class="[
                item.icon,
                'mr-3 flex-shrink-0 h-6 w-6',
                isActive(item.path) ? 'text-white' : 'text-primary-300'
              ]"
            ></i>
            <span v-if="!collapsed">{{ item.label }}</span>
            <Badge
              v-if="!collapsed && item.badge"
              :variant="isActive(item.path) ? 'light' : 'primary'"
              :label="item.badge"
              class="ml-auto"
            />
          </router-link>

          <!-- Submenu -->
          <div v-else class="space-y-1">
            <button
              @click="toggleSubmenu(item)"
              :class="[
                isSubmenuActive(item)
                  ? 'bg-primary-900 text-white'
                  : 'text-primary-100 hover:bg-primary-700',
                'group flex w-full items-center px-2 py-2 text-sm font-medium rounded-md'
              ]"
            >
              <i
                v-if="item.icon"
                :class="[
                  item.icon,
                  'mr-3 flex-shrink-0 h-6 w-6',
                  isSubmenuActive(item) ? 'text-white' : 'text-primary-300'
                ]"
              ></i>
              <span v-if="!collapsed">{{ item.label }}</span>
              <i
                v-if="!collapsed"
                :class="[
                  'fas ml-auto h-5 w-5 transform transition-transform',
                  { 'rotate-90': openSubmenus.includes(item.path) }
                ]"
                :class="[
                  isSubmenuActive(item) ? 'text-white' : 'text-primary-300',
                  'fa-chevron-right'
                ]"
              ></i>
            </button>

            <Transition
              enter-active-class="transition duration-100 ease-out"
              enter-from-class="transform scale-95 opacity-0"
              enter-to-class="transform scale-100 opacity-100"
              leave-active-class="transition duration-75 ease-in"
              leave-from-class="transform scale-100 opacity-100"
              leave-to-class="transform scale-95 opacity-0"
            >
              <ul
                v-if="!collapsed && openSubmenus.includes(item.path)"
                class="mt-1 space-y-1"
              >
                <li v-for="child in item.children" :key="child.path">
                  <router-link
                    :to="child.path"
                    :class="[
                      isActive(child.path)
                        ? 'bg-primary-900 text-white'
                        : 'text-primary-100 hover:bg-primary-700',
                      'group flex items-center pl-10 pr-2 py-2 text-sm font-medium rounded-md'
                    ]"
                  >
                    {{ child.label }}
                  </router-link>
                </li>
              </ul>
            </Transition>
          </div>
        </li>
      </ul>
    </nav>

    <!-- User Profile Section -->
    <div
      class="border-t border-primary-700 bg-primary-800 p-4"
      :class="{ 'text-center': collapsed }"
    >
      <div class="flex items-center" :class="{ 'justify-center': collapsed }">
        <Avatar
          :src="user?.avatar"
          :name="user?.name"
          size="md"
          :status="user?.status"
        />
        <div v-if="!collapsed" class="ml-3">
          <p class="text-sm font-medium text-white">
            {{ user?.name }}
          </p>
          <p class="text-xs text-primary-200">
            {{ user?.role }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Avatar from './Avatar.vue'
import Badge from './Badge.vue'

const props = defineProps({
  menuItems: {
    type: Array,
    required: true
  },
  collapsed: {
    type: Boolean,
    default: false
  },
  collapsible: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:collapsed'])

const route = useRoute()
const authStore = useAuthStore()
const openSubmenus = ref([])

// Computed
const user = computed(() => authStore.user)

const filteredMenuItems = computed(() => {
  return props.menuItems.filter(item => {
    if (!item.roles) return true
    return item.roles.some(role => authStore.hasRole(role))
  })
})

// Methods
const toggleCollapse = () => {
  emit('update:collapsed', !props.collapsed)
}

const toggleSubmenu = (item) => {
  const index = openSubmenus.value.indexOf(item.path)
  if (index === -1) {
    openSubmenus.value.push(item.path)
  } else {
    openSubmenus.value.splice(index, 1)
  }
}

const isActive = (path) => {
  return route.path === path || route.path.startsWith(`${path}/`)
}

const isSubmenuActive = (item) => {
  return item.children?.some(child => isActive(child.path))
}
</script>

<style scoped>
.sidebar-enter-active,
.sidebar-leave-active {
  @apply transition-all duration-300 ease-in-out;
}

.sidebar-enter-from,
.sidebar-leave-to {
  @apply transform -translate-x-full;
}

.submenu-enter-active,
.submenu-leave-active {
  @apply transition-all duration-200 ease-in-out;
}

.submenu-enter-from,
.submenu-leave-to {
  @apply transform -translate-y-2 opacity-0;
}
</style>
