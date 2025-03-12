<template>
  <div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
      <!-- 404 Icon -->
      <div class="mx-auto h-24 w-24 text-primary-600">
        <i class="fas fa-exclamation-circle text-8xl"></i>
      </div>

      <!-- Error Message -->
      <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
        Page Not Found
      </h2>
      <p class="mt-2 text-sm text-gray-600">
        Sorry, we couldn't find the page you're looking for.
      </p>

      <!-- Actions -->
      <div class="mt-8 space-y-4">
        <Button
          variant="primary"
          class="w-full"
          @click="goBack"
        >
          <i class="fas fa-arrow-left mr-2"></i>
          Go Back
        </Button>

        <Button
          variant="secondary"
          class="w-full"
          @click="goHome"
        >
          <i class="fas fa-home mr-2"></i>
          Go to Dashboard
        </Button>
      </div>

      <!-- Help Text -->
      <p class="mt-8 text-sm text-gray-500">
        If you believe this is an error, please contact
        <a
          href="mailto:support@example.com"
          class="font-medium text-primary-600 hover:text-primary-500"
        >
          support
        </a>
      </p>
    </div>

    <!-- Suggested Links -->
    <div class="mt-12 sm:mx-auto sm:w-full sm:max-w-md">
      <h3 class="text-sm font-medium text-gray-500 text-center mb-4">
        You might be looking for:
      </h3>
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <nav class="space-y-3">
          <Link
            v-for="link in suggestedLinks"
            :key="link.to"
            :to="link.to"
            class="flex items-center p-3 rounded-lg hover:bg-gray-50 transition-colors duration-150"
          >
            <i
              :class="[link.icon, 'text-gray-400 mr-3']"
            ></i>
            <div>
              <p class="text-sm font-medium text-gray-900">
                {{ link.label }}
              </p>
              <p class="text-xs text-gray-500">
                {{ link.description }}
              </p>
            </div>
          </Link>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Button from '@/components/Button.vue'
import Link from '@/components/Link.vue'

const router = useRouter()

// Suggested links
const suggestedLinks = [
  {
    to: '/dashboard',
    icon: 'fas fa-home',
    label: 'Dashboard',
    description: 'Overview of key metrics and activities'
  },
  {
    to: '/employees',
    icon: 'fas fa-users',
    label: 'Employees',
    description: 'Manage employee information and records'
  },
  {
    to: '/departments',
    icon: 'fas fa-building',
    label: 'Departments',
    description: 'View and manage department structure'
  },
  {
    to: '/payroll',
    icon: 'fas fa-money-bill',
    label: 'Payroll',
    description: 'Process and manage employee payroll'
  }
]

// Methods
const goBack = () => {
  router.back()
}

const goHome = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
/* Optional: Add animation for the 404 icon */
.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(-5%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

/* Optional: Add hover effect for suggested links */
.suggested-link {
  @apply transition-all duration-200;
}

.suggested-link:hover {
  @apply transform translate-x-1;
}

/* Optional: Add focus styles */
.focus-visible {
  @apply outline-none ring-2 ring-offset-2 ring-primary-500;
}
</style>
