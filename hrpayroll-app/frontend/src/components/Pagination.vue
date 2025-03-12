<template>
  <div
    class="flex items-center justify-between px-4 py-3 sm:px-6"
    :class="className"
  >
    <!-- Mobile View -->
    <div class="flex flex-1 justify-between sm:hidden">
      <Button
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
        variant="secondary"
        size="sm"
      >
        Previous
      </Button>
      <Button
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
        variant="secondary"
        size="sm"
      >
        Next
      </Button>
    </div>

    <!-- Desktop View -->
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <!-- Items per page and showing info -->
      <div>
        <div class="flex items-center gap-4">
          <!-- Items per page selector -->
          <div v-if="showPerPage" class="flex items-center gap-2">
            <span class="text-sm text-gray-700">Show</span>
            <select
              v-model="localPerPage"
              class="form-select rounded-md border-gray-300 py-1 pl-2 pr-8 text-sm focus:border-primary-500 focus:ring-primary-500"
            >
              <option
                v-for="option in perPageOptions"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Showing info -->
          <p class="text-sm text-gray-700">
            Showing
            <span class="font-medium">{{ startIndex }}</span>
            to
            <span class="font-medium">{{ endIndex }}</span>
            of
            <span class="font-medium">{{ totalItems }}</span>
            results
          </p>
        </div>
      </div>

      <!-- Page navigation -->
      <div>
        <nav
          class="isolate inline-flex -space-x-px rounded-md shadow-sm"
          aria-label="Pagination"
        >
          <!-- First page -->
          <Button
            v-if="showFirstLast"
            :disabled="currentPage === 1"
            @click="goToPage(1)"
            variant="secondary"
            class="rounded-l-md"
          >
            <i class="fas fa-angle-double-left"></i>
          </Button>

          <!-- Previous page -->
          <Button
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
            variant="secondary"
            :class="{ 'rounded-l-md': !showFirstLast }"
          >
            <i class="fas fa-angle-left"></i>
          </Button>

          <!-- Page numbers -->
          <template v-for="page in displayedPages" :key="page">
            <!-- Ellipsis -->
            <span
              v-if="page === '...'"
              class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300"
            >
              ...
            </span>
            <!-- Page number -->
            <Button
              v-else
              :variant="page === currentPage ? 'primary' : 'secondary'"
              @click="goToPage(page)"
            >
              {{ page }}
            </Button>
          </template>

          <!-- Next page -->
          <Button
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
            variant="secondary"
            :class="{ 'rounded-r-md': !showFirstLast }"
          >
            <i class="fas fa-angle-right"></i>
          </Button>

          <!-- Last page -->
          <Button
            v-if="showFirstLast"
            :disabled="currentPage === totalPages"
            @click="goToPage(totalPages)"
            variant="secondary"
            class="rounded-r-md"
          >
            <i class="fas fa-angle-double-right"></i>
          </Button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalItems: {
    type: Number,
    required: true
  },
  perPage: {
    type: Number,
    default: 10
  },
  maxVisiblePages: {
    type: Number,
    default: 5
  },
  showFirstLast: {
    type: Boolean,
    default: true
  },
  showPerPage: {
    type: Boolean,
    default: true
  },
  perPageOptions: {
    type: Array,
    default: () => [10, 25, 50, 100]
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:currentPage', 'update:perPage'])

// Local state
const localPerPage = ref(props.perPage)

// Computed
const totalPages = computed(() => Math.ceil(props.totalItems / localPerPage.value))

const startIndex = computed(() => {
  if (props.totalItems === 0) return 0
  return ((props.currentPage - 1) * localPerPage.value) + 1
})

const endIndex = computed(() => {
  return Math.min(startIndex.value + localPerPage.value - 1, props.totalItems)
})

const displayedPages = computed(() => {
  const pages = []
  const maxPages = props.maxVisiblePages
  const halfMaxPages = Math.floor(maxPages / 2)
  
  let startPage = Math.max(1, props.currentPage - halfMaxPages)
  let endPage = Math.min(totalPages.value, startPage + maxPages - 1)
  
  if (endPage - startPage + 1 < maxPages) {
    startPage = Math.max(1, endPage - maxPages + 1)
  }
  
  // Add first page and ellipsis
  if (startPage > 1) {
    pages.push(1)
    if (startPage > 2) pages.push('...')
  }
  
  // Add page numbers
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }
  
  // Add last page and ellipsis
  if (endPage < totalPages.value) {
    if (endPage < totalPages.value - 1) pages.push('...')
    pages.push(totalPages.value)
  }
  
  return pages
})

// Methods
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    emit('update:currentPage', page)
  }
}

// Watchers
watch(localPerPage, (newValue) => {
  emit('update:perPage', newValue)
  // Reset to first page when changing items per page
  emit('update:currentPage', 1)
})

watch(() => props.currentPage, (newPage) => {
  // Ensure current page is within valid range
  if (newPage < 1) {
    emit('update:currentPage', 1)
  } else if (newPage > totalPages.value) {
    emit('update:currentPage', totalPages.value)
  }
})
</script>

<style scoped>
.pagination-button {
  @apply relative inline-flex items-center px-4 py-2 text-sm font-semibold focus:z-20;
}

.pagination-button:disabled {
  @apply cursor-not-allowed opacity-50;
}

.pagination-button-active {
  @apply z-10 bg-primary-600 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600;
}

.pagination-button-inactive {
  @apply text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50;
}
</style>
