<template>
  <div>
    <!-- Page Header -->
    <header class="mb-8">
      <Container>
        <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
      </Container>
    </header>

    <!-- Stats Overview -->
    <section class="mb-8">
      <Container>
        <Grid :cols="{ default: 1, sm: 2, lg: 4 }" gap="4">
          <!-- Total Employees -->
          <Stats
            title="Total Employees"
            :value="stats.totalEmployees"
            icon="fas fa-users"
            color="primary"
            trend="up"
            :percentage="stats.employeeGrowth"
          />

          <!-- Total Departments -->
          <Stats
            title="Departments"
            :value="stats.totalDepartments"
            icon="fas fa-building"
            color="success"
          />

          <!-- Monthly Payroll -->
          <Stats
            title="Monthly Payroll"
            :value="formatCurrency(stats.monthlyPayroll)"
            icon="fas fa-money-bill"
            color="warning"
            trend="up"
            :percentage="stats.payrollGrowth"
          />

          <!-- Attendance Rate -->
          <Stats
            title="Attendance Rate"
            :value="formatPercentage(stats.attendanceRate)"
            icon="fas fa-calendar-check"
            color="info"
          />
        </Grid>
      </Container>
    </section>

    <!-- Charts Section -->
    <section class="mb-8">
      <Container>
        <Grid :cols="{ default: 1, lg: 2 }" gap="4">
          <!-- Employee Distribution -->
          <Card>
            <template #header>
              <h3 class="text-lg font-medium">Employee Distribution</h3>
            </template>
            <Chart
              type="pie"
              :data="charts.employeeDistribution"
              :loading="loading"
            />
          </Card>

          <!-- Payroll Trends -->
          <Card>
            <template #header>
              <h3 class="text-lg font-medium">Payroll Trends</h3>
            </template>
            <Chart
              type="line"
              :data="charts.payrollTrends"
              :loading="loading"
            />
          </Card>
        </Grid>
      </Container>
    </section>

    <!-- Recent Activity -->
    <section class="mb-8">
      <Container>
        <Card>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium">Recent Activity</h3>
              <Link to="/activities">View all</Link>
            </div>
          </template>

          <Timeline
            :items="recentActivities"
            :loading="loading"
          >
            <template #item="{ item }">
              <div class="flex items-center space-x-3">
                <Avatar
                  :src="item.user.avatar"
                  :name="item.user.name"
                  size="sm"
                />
                <div>
                  <p class="text-sm">
                    <span class="font-medium">{{ item.user.name }}</span>
                    {{ item.action }}
                  </p>
                  <time class="text-xs text-gray-500">
                    {{ formatDate(item.timestamp) }}
                  </time>
                </div>
              </div>
            </template>
          </Timeline>
        </Card>
      </Container>
    </section>

    <!-- Quick Actions -->
    <section>
      <Container>
        <Grid :cols="{ default: 1, sm: 2, lg: 4 }" gap="4">
          <Card
            v-for="action in quickActions"
            :key="action.title"
            class="text-center hover:shadow-lg transition-shadow duration-200 cursor-pointer"
            @click="handleQuickAction(action)"
          >
            <i
              :class="[action.icon, 'text-3xl mb-3', `text-${action.color}-500`]"
            ></i>
            <h4 class="font-medium">{{ action.title }}</h4>
            <p class="text-sm text-gray-500">{{ action.description }}</p>
          </Card>
        </Grid>
      </Container>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Container from '@/components/Container.vue'
import Grid from '@/components/Grid.vue'
import Card from '@/components/Card.vue'
import Stats from '@/components/Stats.vue'
import Chart from '@/components/Chart.vue'
import Timeline from '@/components/Timeline.vue'
import Avatar from '@/components/Avatar.vue'
import Link from '@/components/Link.vue'

const router = useRouter()
const loading = ref(true)

// Stats data
const stats = ref({
  totalEmployees: 0,
  totalDepartments: 0,
  monthlyPayroll: 0,
  attendanceRate: 0,
  employeeGrowth: 0,
  payrollGrowth: 0
})

// Charts data
const charts = ref({
  employeeDistribution: {
    labels: [],
    datasets: []
  },
  payrollTrends: {
    labels: [],
    datasets: []
  }
})

// Recent activities
const recentActivities = ref([])

// Quick actions
const quickActions = [
  {
    title: 'Add Employee',
    description: 'Create a new employee record',
    icon: 'fas fa-user-plus',
    color: 'primary',
    route: '/employees/new'
  },
  {
    title: 'Process Payroll',
    description: 'Run monthly payroll',
    icon: 'fas fa-money-check',
    color: 'success',
    route: '/payroll/process'
  },
  {
    title: 'Attendance Report',
    description: 'View attendance summary',
    icon: 'fas fa-clipboard-list',
    color: 'warning',
    route: '/attendance/report'
  },
  {
    title: 'Department Overview',
    description: 'Manage departments',
    icon: 'fas fa-sitemap',
    color: 'info',
    route: '/departments'
  }
]

// Methods
const fetchDashboardData = async () => {
  try {
    loading.value = true
    
    // Fetch stats
    const statsResponse = await axios.get('/api/dashboard/stats')
    stats.value = statsResponse.data

    // Fetch charts data
    const chartsResponse = await axios.get('/api/dashboard/charts')
    charts.value = chartsResponse.data

    // Fetch recent activities
    const activitiesResponse = await axios.get('/api/dashboard/activities')
    recentActivities.value = activitiesResponse.data
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  } finally {
    loading.value = false
  }
}

const handleQuickAction = (action) => {
  router.push(action.route)
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value)
}

const formatPercentage = (value) => {
  return `${value}%`
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  })
}

// Lifecycle
onMounted(() => {
  fetchDashboardData()
})
</script>
