<template>
  <div class="grid gap-4" :class="gridCols">
    <Card
      v-for="stat in stats"
      :key="stat.id"
      class="overflow-hidden"
      :class="{ 'hover:shadow-lg transition-shadow duration-200': stat.clickable }"
      @click="stat.clickable && $emit('click', stat)"
    >
      <div class="p-5">
        <div class="flex items-center justify-between">
          <!-- Stat Info -->
          <div class="truncate">
            <p class="text-sm font-medium text-gray-500 truncate" :title="stat.label">
              {{ stat.label }}
            </p>
            <p class="mt-1 text-xl font-semibold text-gray-900">
              {{ formatValue(stat.value, stat.format) }}
            </p>
          </div>

          <!-- Icon -->
          <div
            v-if="stat.icon"
            :class="[
              'flex-shrink-0 rounded-full p-3',
              `bg-${stat.variant || 'primary'}-100`
            ]"
          >
            <i
              :class="[
                stat.icon,
                'h-6 w-6',
                `text-${stat.variant || 'primary'}-600`
              ]"
            ></i>
          </div>
        </div>

        <!-- Change Indicator -->
        <div v-if="stat.change !== undefined" class="mt-4 flex items-center space-x-2">
          <div
            :class="[
              'flex items-center text-sm',
              stat.change >= 0 ? 'text-green-600' : 'text-red-600'
            ]"
          >
            <i
              :class="[
                'fas',
                stat.change >= 0 ? 'fa-arrow-up' : 'fa-arrow-down',
                'mr-1'
              ]"
            ></i>
            <span class="font-medium">{{ Math.abs(stat.change) }}%</span>
          </div>
          <span class="text-sm text-gray-500">
            {{ stat.changePeriod || 'vs last period' }}
          </span>
        </div>

        <!-- Progress Bar -->
        <div v-if="stat.progress !== undefined" class="mt-4">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">Progress</span>
            <span class="font-medium text-gray-900">{{ stat.progress }}%</span>
          </div>
          <div class="mt-1 h-2 rounded-full bg-gray-200">
            <div
              class="h-2 rounded-full transition-all duration-500"
              :class="`bg-${stat.variant || 'primary'}-600`"
              :style="{ width: `${stat.progress}%` }"
            ></div>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Card from './Card.vue'

const props = defineProps({
  stats: {
    type: Array,
    required: true,
    validator: (stats) => {
      return stats.every(stat => 
        typeof stat === 'object' &&
        'id' in stat &&
        'label' in stat &&
        'value' in stat
      )
    }
  },
  columns: {
    type: Object,
    default: () => ({
      sm: 1,
      md: 2,
      lg: 4
    })
  }
})

const gridCols = computed(() => ({
  [`grid-cols-${props.columns.sm}`]: true,
  [`sm:grid-cols-${props.columns.md}`]: true,
  [`lg:grid-cols-${props.columns.lg}`]: true
}))

const formatValue = (value, format) => {
  if (!format) return value

  switch (format) {
    case 'number':
      return new Intl.NumberFormat().format(value)
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(value)
    case 'percentage':
      return `${value}%`
    case 'decimal':
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value)
    default:
      return value
  }
}
</script>
