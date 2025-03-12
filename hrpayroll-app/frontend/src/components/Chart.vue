<template>
  <div class="relative" :style="{ height: height }">
    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75"
    >
      <Loading size="lg" />
    </div>

    <!-- No Data Message -->
    <div
      v-else-if="!hasData"
      class="absolute inset-0 flex items-center justify-center"
    >
      <div class="text-center text-gray-500">
        <i class="fas fa-chart-bar text-4xl mb-2"></i>
        <p>{{ noDataMessage }}</p>
      </div>
    </div>

    <!-- Chart Canvas -->
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import Loading from './Loading.vue'

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  type: {
    type: String,
    required: true,
    validator: (value) => ['line', 'bar', 'pie', 'doughnut', 'radar'].includes(value)
  },
  data: {
    type: Object,
    required: true
  },
  options: {
    type: Object,
    default: () => ({})
  },
  height: {
    type: String,
    default: '300px'
  },
  loading: {
    type: Boolean,
    default: false
  },
  noDataMessage: {
    type: String,
    default: 'No data available'
  }
})

// Refs
const chartRef = ref(null)
let chart = null

// Computed
const hasData = computed(() => {
  return props.data.datasets?.some(dataset => dataset.data?.length > 0)
})

// Default chart options by type
const getDefaultOptions = (type) => {
  const common = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleFont: {
          size: 13
        },
        bodyFont: {
          size: 12
        },
        padding: 12,
        cornerRadius: 6
      }
    }
  }

  const typeSpecific = {
    line: {
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            drawBorder: false
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      },
      elements: {
        line: {
          tension: 0.4
        },
        point: {
          radius: 4,
          hitRadius: 10,
          hoverRadius: 6
        }
      }
    },
    bar: {
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            drawBorder: false
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    },
    pie: {
      cutout: '0%'
    },
    doughnut: {
      cutout: '60%'
    },
    radar: {
      elements: {
        line: {
          tension: 0.4
        }
      }
    }
  }

  return {
    ...common,
    ...typeSpecific[type]
  }
}

// Methods
const createChart = () => {
  if (!chartRef.value) return

  const ctx = chartRef.value.getContext('2d')
  const mergedOptions = {
    ...getDefaultOptions(props.type),
    ...props.options
  }

  chart = new ChartJS(ctx, {
    type: props.type,
    data: props.data,
    options: mergedOptions
  })
}

const destroyChart = () => {
  if (chart) {
    chart.destroy()
    chart = null
  }
}

const updateChart = () => {
  if (!chart) return
  chart.data = props.data
  chart.options = {
    ...getDefaultOptions(props.type),
    ...props.options
  }
  chart.update()
}

// Lifecycle hooks
onMounted(() => {
  createChart()
})

onUnmounted(() => {
  destroyChart()
})

// Watchers
watch(
  () => props.data,
  () => {
    if (chart) {
      updateChart()
    }
  },
  { deep: true }
)

watch(
  () => props.options,
  () => {
    if (chart) {
      updateChart()
    }
  },
  { deep: true }
)

watch(
  () => props.type,
  () => {
    destroyChart()
    createChart()
  }
)
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
}

/* Animation classes */
.chart-fade-enter-active,
.chart-fade-leave-active {
  transition: opacity 0.3s ease;
}

.chart-fade-enter-from,
.chart-fade-leave-to {
  opacity: 0;
}

/* Loading overlay animation */
.loading-overlay-enter-active,
.loading-overlay-leave-active {
  transition: opacity 0.2s ease;
}

.loading-overlay-enter-from,
.loading-overlay-leave-to {
  opacity: 0;
}
</style>
