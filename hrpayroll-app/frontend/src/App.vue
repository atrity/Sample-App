<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Auth Layout -->
    <template v-if="isAuthRoute">
      <router-view></router-view>
    </template>

    <!-- Main Layout -->
    <template v-else>
      <div class="flex h-screen overflow-hidden">
        <!-- Sidebar -->
        <Sidebar
          v-model:collapsed="sidebarCollapsed"
          :items="navigationItems"
        />

        <!-- Main Content -->
        <div class="flex-1 flex flex-col overflow-hidden">
          <!-- Top Navigation -->
          <header class="bg-white shadow-sm">
            <div class="flex items-center justify-between px-4 py-3">
              <!-- Toggle Sidebar -->
              <button
                class="text-gray-500 hover:text-gray-600"
                @click="sidebarCollapsed = !sidebarCollapsed"
              >
                <i class="fas fa-bars"></i>
              </button>

              <!-- User Menu -->
              <Dropdown>
                <template #trigger>
                  <button class="flex items-center space-x-2">
                    <Avatar
                      :src="user?.avatar"
                      :name="user?.name"
                      size="sm"
                    />
                    <span class="text-sm font-medium text-gray-700">
                      {{ user?.name }}
                    </span>
                  </button>
                </template>

                <template #content>
                  <div class="py-1">
                    <a
                      href="#"
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      @click="handleProfile"
                    >
                      Profile
                    </a>
                    <a
                      href="#"
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      @click="handleLogout"
                    >
                      Logout
                    </a>
                  </div>
                </template>
              </Dropdown>
            </div>
          </header>

          <!-- Page Content -->
          <main class="flex-1 overflow-y-auto p-4">
            <router-view v-slot="{ Component }">
              <transition
                name="fade"
                mode="out-in"
              >
                <component :is="Component" />
              </transition>
            </router-view>
          </main>
        </div>
      </div>
    </template>

    <!-- Global Components -->
    <Toast ref="toast" />
    <Loading ref="loading" />
    <Notification ref="notification" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/Sidebar.vue'
import Dropdown from '@/components/Dropdown.vue'
import Avatar from '@/components/Avatar.vue'
import Toast from '@/components/Toast.vue'
import Loading from '@/components/Loading.vue'
import Notification from '@/components/Notification.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// State
const sidebarCollapsed = ref(false)
const toast = ref(null)
const loading = ref(null)
const notification = ref(null)

// Computed
const user = computed(() => authStore.user)
const isAuthRoute = computed(() => route.meta.layout === 'auth')

// Navigation Items
const navigationItems = [
  {
    label: 'Dashboard',
    icon: 'fas fa-home',
    to: '/dashboard'
  },
  {
    label: 'Employees',
    icon: 'fas fa-users',
    to: '/employees'
  },
  {
    label: 'Departments',
    icon: 'fas fa-building',
    to: '/departments'
  },
  {
    label: 'Payroll',
    icon: 'fas fa-money-bill',
    to: '/payroll'
  },
  {
    label: 'Attendance',
    icon: 'fas fa-calendar-check',
    to: '/attendance'
  }
]

// Methods
const handleProfile = () => {
  router.push('/profile')
}

const handleLogout = async () => {
  try {
    loading.value.show()
    await authStore.logout()
    router.push('/login')
    toast.value.show({
      type: 'success',
      message: 'Logged out successfully'
    })
  } catch (error) {
    toast.value.show({
      type: 'error',
      message: 'Failed to logout'
    })
  } finally {
    loading.value.hide()
  }
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
