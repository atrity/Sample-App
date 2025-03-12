<template>
  <div class="flex flex-col">
    <!-- Table Header Actions -->
    <div class="flex justify-between items-center mb-4" v-if="$slots.actions || showSearch">
      <!-- Search Input -->
      <div v-if="showSearch" class="flex-1 max-w-sm">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            class="form-input pl-10 w-full"
            :placeholder="searchPlaceholder"
          />
          <i class="fas fa-search absolute left-3 top-3 text-gray-400"></i>
        </div>
      </div>

      <!-- Custom Actions -->
      <div class="flex space-x-2">
        <slot name="actions"></slot>
      </div>
    </div>

    <!-- Table Container -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <!-- Table Header -->
          <thead class="bg-gray-50">
            <tr>
              <!-- Selection Checkbox -->
              <th
                v-if="selectable"
                scope="col"
                class="px-6 py-3 w-12"
              >
                <input
                  type="checkbox"
                  class="form-checkbox h-4 w-4 text-primary-600"
                  :checked="allSelected"
                  @change="toggleSelectAll"
                />
              </th>

              <!-- Column Headers -->
              <th
                v-for="column in columns"
                :key="column.key"
                scope="col"
                :class="[
                  'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
                  column.sortable ? 'cursor-pointer select-none' : '',
                  column.align === 'right' ? 'text-right' : '',
                  column.align === 'center' ? 'text-center' : ''
                ]"
                @click="column.sortable && sort(column.key)"
              >
                <div class="flex items-center space-x-1">
                  <span>{{ column.label }}</span>
                  <span v-if="column.sortable" class="text-gray-400">
                    <i
                      :class="[
                        'fas',
                        sortKey === column.key
                          ? sortOrder === 'asc'
                            ? 'fa-sort-up'
                            : 'fa-sort-down'
                          : 'fa-sort'
                      ]"
                    ></i>
                  </span>
                </div>
              </th>

              <!-- Actions Column -->
              <th
                v-if="$slots.actions"
                scope="col"
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>

          <!-- Table Body -->
          <tbody class="bg-white divide-y divide-gray-200">
            <template v-if="filteredItems.length">
              <tr
                v-for="item in paginatedItems"
                :key="item[itemKey]"
                :class="{ 'bg-gray-50': isSelected(item) }"
              >
                <!-- Selection Checkbox -->
                <td v-if="selectable" class="px-6 py-4 whitespace-nowrap w-12">
                  <input
                    type="checkbox"
                    class="form-checkbox h-4 w-4 text-primary-600"
                    :checked="isSelected(item)"
                    @change="toggleSelect(item)"
                  />
                </td>

                <!-- Data Cells -->
                <td
                  v-for="column in columns"
                  :key="column.key"
                  :class="[
                    'px-6 py-4 whitespace-nowrap',
                    column.align === 'right' ? 'text-right' : '',
                    column.align === 'center' ? 'text-center' : ''
                  ]"
                >
                  <slot
                    :name="column.key"
                    :item="item"
                    :value="item[column.key]"
                  >
                    {{ formatValue(item[column.key], column.format) }}
                  </slot>
                </td>

                <!-- Actions -->
                <td
                  v-if="$slots.actions"
                  class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                >
                  <slot name="actions" :item="item"></slot>
                </td>
              </tr>
            </template>

            <!-- Empty State -->
            <tr v-else>
              <td
                :colspan="totalColumns"
                class="px-6 py-10 text-center text-gray-500"
              >
                <slot name="empty">
                  <div class="text-center">
                    <i class="fas fa-inbox text-4xl text-gray-400 mb-3"></i>
                    <p class="text-gray-500">No items found</p>
                  </div>
                </slot>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div
        v-if="showPagination && filteredItems.length"
        class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6"
      >
        <div class="flex items-center justify-between">
          <!-- Mobile Pagination -->
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              :disabled="currentPage === 1"
              @click="currentPage--"
              class="btn btn-secondary"
            >
              Previous
            </button>
            <button
              :disabled="currentPage === totalPages"
              @click="currentPage++"
              class="btn btn-secondary"
            >
              Next
            </button>
          </div>

          <!-- Desktop Pagination -->
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing
                <span class="font-medium">{{ paginationStart }}</span>
                to
                <span class="font-medium">{{ paginationEnd }}</span>
                of
                <span class="font-medium">{{ filteredItems.length }}</span>
                results
              </p>
            </div>

            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  :disabled="currentPage === 1"
                  @click="currentPage = 1"
                  class="btn btn-secondary rounded-l-md"
                >
                  <i class="fas fa-angle-double-left"></i>
                </button>
                <button
                  :disabled="currentPage === 1"
                  @click="currentPage--"
                  class="btn btn-secondary"
                >
                  <i class="fas fa-angle-left"></i>
                </button>

                <button
                  v-for="page in displayedPages"
                  :key="page"
                  @click="currentPage = page"
                  :class="[
                    'btn',
                    currentPage === page ? 'btn-primary' : 'btn-secondary'
                  ]"
                >
                  {{ page }}
                </button>

                <button
                  :disabled="currentPage === totalPages"
                  @click="currentPage++"
                  class="btn btn-secondary"
                >
                  <i class="fas fa-angle-right"></i>
                </button>
                <button
                  :disabled="currentPage === totalPages"
                  @click="currentPage = totalPages"
                  class="btn btn-secondary rounded-r-md"
                >
                  <i class="fas fa-angle-double-right"></i>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  itemKey: {
    type: String,
    default: 'id'
  },
  selectable: {
    type: Boolean,
    default: false
  },
  showSearch: {
    type: Boolean,
    default: true
  },
  searchPlaceholder: {
    type: String,
    default: 'Search...'
  },
  showPagination: {
    type: Boolean,
    default: true
  },
  itemsPerPage: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits(['update:selected', 'sort'])

// Data
const searchQuery = ref('')
const currentPage = ref(1)
const sortKey = ref('')
const sortOrder = ref('asc')
const selectedItems = ref([])

// Computed
const totalColumns = computed(() => {
  let count = props.columns.length
  if (props.selectable) count++
  if (props.$slots.actions) count++
  return count
})

const filteredItems = computed(() => {
  let items = [...props.items]

  // Search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(item =>
      props.columns.some(column => {
        const value = item[column.key]
        return value && String(value).toLowerCase().includes(query)
      })
    )
  }

  // Sort
  if (sortKey.value) {
    items.sort((a, b) => {
      const aVal = a[sortKey.value]
      const bVal = b[sortKey.value]
      
      if (aVal === bVal) return 0
      const comparison = aVal > bVal ? 1 : -1
      return sortOrder.value === 'asc' ? comparison : -comparison
    })
  }

  return items
})

const paginatedItems = computed(() => {
  if (!props.showPagination) return filteredItems.value
  
  const start = (currentPage.value - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return filteredItems.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredItems.value.length / props.itemsPerPage)
})

const displayedPages = computed(() => {
  const pages = []
  const maxPages = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxPages / 2))
  let end = Math.min(totalPages.value, start + maxPages - 1)

  if (end - start + 1 < maxPages) {
    start = Math.max(1, end - maxPages + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const paginationStart = computed(() => {
  return ((currentPage.value - 1) * props.itemsPerPage) + 1
})

const paginationEnd = computed(() => {
  return Math.min(currentPage.value * props.itemsPerPage, filteredItems.value.length)
})

const allSelected = computed(() => {
  return paginatedItems.value.length > 0 &&
    paginatedItems.value.every(item => isSelected(item))
})

// Methods
const sort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  emit('sort', { key: sortKey.value, order: sortOrder.value })
}

const formatValue = (value, format) => {
  if (!value) return ''
  if (!format) return value
  
  switch (format) {
    case 'date':
      return new Date(value).toLocaleDateString()
    case 'datetime':
      return new Date(value).toLocaleString()
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(value)
    case 'number':
      return new Intl.NumberFormat().format(value)
    case 'percentage':
      return `${value}%`
    default:
      return value
  }
}

const isSelected = (item) => {
  return selectedItems.value.some(selected => selected[props.itemKey] === item[props.itemKey])
}

const toggleSelect = (item) => {
  const index = selectedItems.value.findIndex(
    selected => selected[props.itemKey] === item[props.itemKey]
  )
  
  if (index === -1) {
    selectedItems.value.push(item)
  } else {
    selectedItems.value.splice(index, 1)
  }
  
  emit('update:selected', selectedItems.value)
}

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedItems.value = []
  } else {
    selectedItems.value = [...paginatedItems.value]
  }
  emit('update:selected', selectedItems.value)
}

// Watchers
watch(filteredItems, () => {
  currentPage.value = 1
})
</script>
