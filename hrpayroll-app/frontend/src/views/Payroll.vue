<template>
  <div>
    <!-- Page Header -->
    <header class="mb-8">
      <Container>
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-gray-900">Payroll Management</h1>
          <Button
            variant="primary"
            icon="fas fa-money-check"
            @click="handleProcessPayroll"
            :loading="processing"
          >
            Process Payroll
          </Button>
        </div>
      </Container>
    </header>

    <!-- Payroll Summary -->
    <section class="mb-8">
      <Container>
        <Grid :cols="{ default: 1, md: 2, lg: 4 }" gap="4">
          <Stats
            title="Total Payroll"
            :value="formatCurrency(summary.totalPayroll)"
            icon="fas fa-money-bill"
            color="primary"
            trend="up"
            :percentage="summary.payrollGrowth"
          />
          <Stats
            title="Total Employees"
            :value="summary.totalEmployees"
            icon="fas fa-users"
            color="success"
          />
          <Stats
            title="Average Salary"
            :value="formatCurrency(summary.averageSalary)"
            icon="fas fa-chart-line"
            color="info"
          />
          <Stats
            title="Next Payroll Date"
            :value="formatDate(summary.nextPayrollDate)"
            icon="fas fa-calendar"
            color="warning"
          />
        </Grid>
      </Container>
    </section>

    <!-- Payroll Filters -->
    <section class="mb-6">
      <Container>
        <Card>
          <Grid :cols="{ default: 1, md: 4 }" gap="4">
            <FormInput
              v-model="filters.search"
              placeholder="Search employees..."
              icon="fas fa-search"
              @input="handleSearch"
            />
            <Select
              v-model="filters.department"
              placeholder="Filter by department"
              :options="departments"
              option-label="name"
              option-value="id"
              @change="handleFilter"
            />
            <FormInput
              v-model="filters.fromDate"
              type="date"
              label="From Date"
              @input="handleFilter"
            />
            <FormInput
              v-model="filters.toDate"
              type="date"
              label="To Date"
              @input="handleFilter"
            />
          </Grid>
        </Card>
      </Container>
    </section>

    <!-- Payroll Table -->
    <section class="mb-8">
      <Container>
        <Card>
          <DataTable
            :columns="columns"
            :data="payrollData"
            :loading="loading"
            :total="total"
            :per-page="perPage"
            :current-page="currentPage"
            @page-change="handlePageChange"
          >
            <!-- Employee Column -->
            <template #column-employee="{ item }">
              <div class="flex items-center">
                <Avatar
                  :src="item.avatar"
                  :name="item.name"
                  size="sm"
                />
                <div class="ml-3">
                  <p class="font-medium text-gray-900">{{ item.name }}</p>
                  <p class="text-sm text-gray-500">{{ item.position }}</p>
                </div>
              </div>
            </template>

            <!-- Department Column -->
            <template #column-department="{ item }">
              <Badge :color="getDepartmentColor(item.department)">
                {{ item.department }}
              </Badge>
            </template>

            <!-- Salary Column -->
            <template #column-salary="{ item }">
              {{ formatCurrency(item.salary) }}
            </template>

            <!-- Deductions Column -->
            <template #column-deductions="{ item }">
              <Tooltip :content="getDeductionsBreakdown(item)">
                {{ formatCurrency(item.totalDeductions) }}
              </Tooltip>
            </template>

            <!-- Net Pay Column -->
            <template #column-netPay="{ item }">
              <span class="font-medium text-gray-900">
                {{ formatCurrency(item.netPay) }}
              </span>
            </template>

            <!-- Status Column -->
            <template #column-status="{ item }">
              <Badge
                :color="getStatusColor(item.status)"
              >
                {{ item.status }}
              </Badge>
            </template>

            <!-- Actions Column -->
            <template #column-actions="{ item }">
              <Button
                variant="secondary"
                size="sm"
                icon="fas fa-file-pdf"
                @click="handleDownloadPayslip(item)"
              >
                Payslip
              </Button>
            </template>
          </DataTable>
        </Card>
      </Container>
    </section>

    <!-- Process Payroll Modal -->
    <Modal
      v-model="showProcessModal"
      title="Process Payroll"
      size="lg"
    >
      <div class="space-y-6">
        <!-- Period Selection -->
        <div class="grid grid-cols-2 gap-4">
          <FormInput
            v-model="processForm.fromDate"
            type="date"
            label="From Date"
            required
          />
          <FormInput
            v-model="processForm.toDate"
            type="date"
            label="To Date"
            required
          />
        </div>

        <!-- Summary -->
        <Card class="bg-gray-50">
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-600">Total Employees</span>
              <span class="font-medium">{{ processForm.totalEmployees }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Total Salary</span>
              <span class="font-medium">{{ formatCurrency(processForm.totalSalary) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Total Deductions</span>
              <span class="font-medium">{{ formatCurrency(processForm.totalDeductions) }}</span>
            </div>
            <Divider />
            <div class="flex justify-between text-lg">
              <span class="font-medium">Net Payable</span>
              <span class="font-bold text-primary-600">
                {{ formatCurrency(processForm.netPayable) }}
              </span>
            </div>
          </div>
        </Card>

        <!-- Confirmation -->
        <Alert type="warning">
          This will process payroll for all eligible employees. Please verify the details before proceeding.
        </Alert>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button
            variant="secondary"
            @click="showProcessModal = false"
          >
            Cancel
          </Button>
          <Button
            variant="primary"
            :loading="processing"
            @click="confirmProcessPayroll"
          >
            Confirm & Process
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Toast for notifications -->
    <Toast ref="toast" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Container from '@/components/Container.vue'
import Grid from '@/components/Grid.vue'
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'
import Stats from '@/components/Stats.vue'
import FormInput from '@/components/FormInput.vue'
import Select from '@/components/Select.vue'
import DataTable from '@/components/DataTable.vue'
import Avatar from '@/components/Avatar.vue'
import Badge from '@/components/Badge.vue'
import Tooltip from '@/components/Tooltip.vue'
import Modal from '@/components/Modal.vue'
import Divider from '@/components/Divider.vue'
import Alert from '@/components/Alert.vue'
import Toast from '@/components/Toast.vue'

// State
const loading = ref(false)
const processing = ref(false)
const showProcessModal = ref(false)
const toast = ref(null)

const payrollData = ref([])
const departments = ref([])
const total = ref(0)
const perPage = ref(10)
const currentPage = ref(1)

// Summary data
const summary = ref({
  totalPayroll: 0,
  totalEmployees: 0,
  averageSalary: 0,
  nextPayrollDate: null,
  payrollGrowth: 0
})

// Filters
const filters = ref({
  search: '',
  department: null,
  fromDate: '',
  toDate: ''
})

// Process form
const processForm = ref({
  fromDate: '',
  toDate: '',
  totalEmployees: 0,
  totalSalary: 0,
  totalDeductions: 0,
  netPayable: 0
})

// Table columns
const columns = [
  {
    key: 'employee',
    label: 'Employee',
    sortable: true
  },
  {
    key: 'department',
    label: 'Department',
    sortable: true
  },
  {
    key: 'salary',
    label: 'Base Salary',
    sortable: true
  },
  {
    key: 'deductions',
    label: 'Deductions',
    sortable: true
  },
  {
    key: 'netPay',
    label: 'Net Pay',
    sortable: true
  },
  {
    key: 'status',
    label: 'Status'
  },
  {
    key: 'actions',
    label: ''
  }
]

// Methods
const fetchPayrollData = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/payroll', {
      params: {
        page: currentPage.value,
        perPage: perPage.value,
        ...filters.value
      }
    })
    payrollData.value = response.data.data
    total.value = response.data.total
  } catch (error) {
    console.error('Failed to fetch payroll data:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to fetch payroll data'
    })
  } finally {
    loading.value = false
  }
}

const fetchSummary = async () => {
  try {
    const response = await axios.get('/api/payroll/summary')
    summary.value = response.data
  } catch (error) {
    console.error('Failed to fetch summary:', error)
  }
}

const fetchDepartments = async () => {
  try {
    const response = await axios.get('/api/departments')
    departments.value = response.data
  } catch (error) {
    console.error('Failed to fetch departments:', error)
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchPayrollData()
}

const handleSearch = () => {
  currentPage.value = 1
  fetchPayrollData()
}

const handleFilter = () => {
  currentPage.value = 1
  fetchPayrollData()
}

const handleProcessPayroll = async () => {
  try {
    const response = await axios.get('/api/payroll/preview')
    processForm.value = response.data
    showProcessModal.value = true
  } catch (error) {
    console.error('Failed to get payroll preview:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to get payroll preview'
    })
  }
}

const confirmProcessPayroll = async () => {
  try {
    processing.value = true
    await axios.post('/api/payroll/process', processForm.value)
    
    showProcessModal.value = false
    fetchPayrollData()
    fetchSummary()
    
    toast.value.show({
      type: 'success',
      message: 'Payroll processed successfully'
    })
  } catch (error) {
    console.error('Failed to process payroll:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to process payroll'
    })
  } finally {
    processing.value = false
  }
}

const handleDownloadPayslip = async (item) => {
  try {
    const response = await axios.get(`/api/payroll/${item.id}/payslip`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `payslip-${item.id}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Failed to download payslip:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to download payslip'
    })
  }
}

const getDepartmentColor = (department) => {
  const colors = {
    'Engineering': 'primary',
    'Marketing': 'success',
    'Sales': 'warning',
    'HR': 'info',
    'Finance': 'danger'
  }
  return colors[department] || 'secondary'
}

const getStatusColor = (status) => {
  const colors = {
    'Processed': 'success',
    'Pending': 'warning',
    'Failed': 'danger'
  }
  return colors[status] || 'secondary'
}

const getDeductionsBreakdown = (item) => {
  return `
    Tax: ${formatCurrency(item.deductions.tax)}
    Insurance: ${formatCurrency(item.deductions.insurance)}
    Other: ${formatCurrency(item.deductions.other)}
  `
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Lifecycle
onMounted(() => {
  fetchPayrollData()
  fetchSummary()
  fetchDepartments()
})
</script>
