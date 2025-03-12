<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <!-- Table Header -->
      <thead class="bg-gray-50">
        <tr>
          <!-- Selection Column -->
          <th
            v-if="selectable"
            scope="col"
            class="px-6 py-3 w-12"
          >
            <Checkbox
              :model-value="allSelected"
              @update:model-value="toggleSelectAll"
              :indeterminate="someSelected"
            />
          </th>

          <!-- Columns -->
          <th
            v-for="column in columns"
            :key="column.key"
            scope="col"
            :class="[
              'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
              column.align === 'right' ? 'text-right' : '',
              column.align === 'center' ? 'text-center' : '',
              column.width ? `w-${column.width}` : ''
            ]"
          >
            {{ column.label }}
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
        <template v-if="data.length">
          <tr
            v-for="(item, index) in data"
            :key="getItemKey(item)"
            :class="[
              getRowClass(item, index),
              { 'bg-gray-50': isSelected(item) }
            ]"
          >
            <!-- Selection Column -->
            <td v-if="selectable" class="px-6 py-4 whitespace-nowrap w-12">
              <Checkbox
                :model-value="isSelected(item)"
                @update:model-value="toggleSelect(item)"
              />
            </td>

            <!-- Data Cells -->
            <td
              v-for="column in columns"
              :key="column.key"
              :class="[
                'px-6 py-4 whitespace-nowrap',
                column.align === 'right' ? 'text-right' : '',
                column.align === 'center' ? 'text-center' : '',
                getCellClass(column, item)
              ]"
            >
              <slot
                :name="`cell-${column.key}`"
                :item="item"
                :value="item[column.key]"
                :column="column"
              >
                {{ formatValue(item[column.key], column.format) }}
              </slot>
            </td>

            <!-- Actions Column -->
            <td
              v-if="$slots.actions"
              class="px-6 py-4 whitespace-nowrap text-right text-sm"
            >
              <slot name="actions" :item="item" :index="index"></slot>
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
                <p class="text-gray-500">{{ emptyText }}</p>
              </div>
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Checkbox from './Checkbox.vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true,
    validator: (columns) => {
      return columns.every(column =>
        typeof column === 'object' &&
        'key' in column &&
        'label' in column
      )
    }
  },
  selectable: {
    type: Boolean,
    default: false
  },
  selected: {
    type: Array,
    default: () => []
  },
  itemKey: {
    type: String,
    default: 'id'
  },
  emptyText: {
    type: String,
    default: 'No data available'
  },
  rowClass: {
    type: [String, Function],
    default: ''
  },
  cellClass: {
    type: [String, Function],
    default: ''
  }
})

const emit = defineEmits(['update:selected'])

// Computed
const totalColumns = computed(() => {
  let count = props.columns.length
  if (props.selectable) count++
  if (props.$slots.actions) count++
  return count
})

const allSelected = computed(() => {
  return props.data.length > 0 && props.data.every(item => isSelected(item))
})

const someSelected = computed(() => {
  return !allSelected.value && props.data.some(item => isSelected(item))
})

// Methods
const getItemKey = (item) => {
  return item[props.itemKey]
}

const isSelected = (item) => {
  return props.selected.some(selectedItem => 
    getItemKey(selectedItem) === getItemKey(item)
  )
}

const toggleSelect = (item) => {
  const newSelected = [...props.selected]
  const index = newSelected.findIndex(selectedItem => 
    getItemKey(selectedItem) === getItemKey(item)
  )

  if (index === -1) {
    newSelected.push(item)
  } else {
    newSelected.splice(index, 1)
  }

  emit('update:selected', newSelected)
}

const toggleSelectAll = () => {
  emit('update:selected', allSelected.value ? [] : [...props.data])
}

const formatValue = (value, format) => {
  if (!value || !format) return value

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

const getRowClass = (item, index) => {
  if (typeof props.rowClass === 'function') {
    return props.rowClass(item, index)
  }
  return props.rowClass
}

const getCellClass = (column, item) => {
  if (typeof props.cellClass === 'function') {
    return props.cellClass(column, item)
  }
  return props.cellClass
}
</script>

<style scoped>
.table-hover tr:hover {
  @apply bg-gray-50;
}

.table-striped tr:nth-child(even) {
  @apply bg-gray-50;
}

.table-bordered {
  @apply border border-gray-200;
}

.table-bordered th,
.table-bordered td {
  @apply border border-gray-200;
}

.table-compact th,
.table-compact td {
  @apply px-4 py-2;
}
</style>
