<template>
  <div>
    <!-- Page Header -->
    <header class="mb-8">
      <Container>
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-gray-900">Attendance Management</h1>
          <div class="flex space-x-3">
            <Button
              variant="secondary"
              icon="fas fa-download"
              @click="handleExport"
            >
              Export
            </Button>
            <Button
              variant="primary"
              icon="fas fa-plus"
              @click="showAddModal = true"
            >
              Record Attendance
            </Button>
          </div>
        </div>
      </Container>
    </header>

    <!-- Attendance Summary -->
    <section class="mb-8">
      <Container>
        <Grid :cols="{ default: 1, md: 2, lg: 4 }" gap="4">
          <Stats
            title="Present Today"
            :value="summary.presentToday"
            icon="fas fa-user-check"
            color="success"
            :percentage="summary.presentPercentage"
          />
          <Stats
            title="Absent Today"
            :value="summary.absentToday"
            icon="fas fa-user-times"
            color="danger"
            :percentage="summary.absentPercentage"
          />
          <Stats
            title="On Leave"
            :value="summary.onLeave"
            icon="fas fa-user-clock"
            color="warning"
          />
          <Stats
            title="Average Attendance"
            :value="formatPercentage(summary.averageAttendance)"
            icon="fas fa-chart-line"
            color="info"
            trend="up"
          />
        </Grid>
      </Container>
    </section>

    <!-- Calendar View -->
    <section class="mb-8">
      <Container>
        <Card>
          <Calendar
            v-model="selectedDate"
            :events="attendanceEvents"
            view="month"
            @date-click="handleDateClick"
            @event-click="handleEventClick"
          >
            <template #event="{ event }">
              <div
                class="flex items-center space-x-2 p-1 rounded"
                :class="getEventClass(event)"
              >
                <i :class="getEventIcon(event)"></i>
                <span class="text-sm truncate">{{ event.title }}</span>
              </div>
            </template>
          </Calendar>
        </Card>
      </Container>
    </section>

    <!-- Attendance List -->
    <section>
      <Container>
        <Card>
          <!-- Filters -->
          <div class="mb-6">
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
              <Select
                v-model="filters.status"
                placeholder="Filter by status"
                :options="[
                  { label: 'Present', value: 'present' },
                  { label: 'Absent', value: 'absent' },
                  { label: 'Late', value: 'late' },
                  { label: 'Leave', value: 'leave' }
                ]"
                @change="handleFilter"
              />
              <FormInput
                v-model="filters.date"
                type="date"
                @input="handleFilter"
              />
            </Grid>
          </div>

          <!-- Table -->
          <DataTable
            :columns="columns"
            :data="attendanceData"
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
                  <p class="text-sm text-gray-500">{{ item.department }}</p>
                </div>
              </div>
            </template>

            <!-- Time Column -->
            <template #column-time="{ item }">
              <div>
                <p>In: {{ formatTime(item.checkIn) }}</p>
                <p>Out: {{ formatTime(item.checkOut) }}</p>
              </div>
            </template>

            <!-- Status Column -->
            <template #column-status="{ item }">
              <Badge :color="getStatusColor(item.status)">
                {{ item.status }}
              </Badge>
            </template>

            <!-- Actions Column -->
            <template #column-actions="{ item }">
              <Button
                variant="secondary"
                size="sm"
                icon="fas fa-edit"
                @click="handleEdit(item)"
              />
            </template>
          </DataTable>
        </Card>
      </Container>
    </section>

    <!-- Add/Edit Modal -->
    <Modal
      v-model="showModal"
      :title="isEditing ? 'Edit Attendance' : 'Record Attendance'"
    >
      <Form
        ref="form"
        :validation-schema="schema"
        @submit="handleSubmit"
      >
        <div class="space-y-4">
          <Select
            v-if="!isEditing"
            v-model="formData.employeeId"
            label="Employee"
            name="employeeId"
            :options="employees"
            option-label="name"
            option-value="id"
            required
          />

          <FormInput
            v-model="formData.date"
            type="date"
            label="Date"
            name="date"
            required
          />

          <Grid :cols="2" gap="4">
            <FormInput
              v-model="formData.checkIn"
              type="time"
              label="Check In"
              name="checkIn"
              required
            />
            <FormInput
              v-model="formData.checkOut"
              type="time"
              label="Check Out"
              name="checkOut"
            />
          </Grid>

          <Select
            v-model="formData.status"
            label="Status"
            name="status"
            :options="[
              { label: 'Present', value: 'present' },
              { label: 'Absent', value: 'absent' },
              { label: 'Late', value: 'late' },
              { label: 'Leave', value: 'leave' }
            ]"
            required
          />

          <TextArea
            v-model="formData.notes"
            label="Notes"
            name="notes"
            rows="3"
          />
        </div>

        <!-- Footer -->
        <template #footer>
          <div class="flex justify-end space-x-3">
            <Button
              variant="secondary"
              @click="showModal = false"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              :loading="submitting"
            >
              {{ isEditing ? 'Update' : 'Record' }}
            </Button>
          </div>
        </template>
      </Form>
    </Modal>

    <!-- Toast for notifications -->
    <Toast ref="toast" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import * as yup from 'yup'
import Container from '@/components/Container.vue'
import Grid from '@/components/Grid.vue'
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'
import Stats from '@/components/Stats.vue'
import Calendar from '@/components/Calendar.vue'
import FormInput from '@/components/FormInput.vue'
import Select from '@/components/Select.vue'
import DataTable from '@/components/DataTable.vue'
import Avatar from '@/components/Avatar.vue'
import Badge from '@/components/Badge.vue'
import Modal from '@/components/Modal.vue'
import Form from '@/components/Form.vue'
import TextArea from '@/components/TextArea.vue'
import Toast from '@/components/Toast.vue'

// State
const loading = ref(false)
const submitting = ref(false)
const showModal = ref(false)
const isEditing = ref(false)
const selectedDate = ref(new Date())
const toast = ref(null)
const form = ref(null)

const attendanceData = ref([])
const departments = ref([])
const employees = ref([])
const total = ref(0)
const perPage = ref(10)
const currentPage = ref(1)

// Summary data
const summary = ref({
  presentToday: 0,
  absentToday: 0,
  onLeave: 0,
  averageAttendance: 0,
  presentPercentage: 0,
  absentPercentage: 0
})

// Filters
const filters = ref({
  search: '',
  department: null,
  status: null,
  date: ''
})

// Form data
const formData = ref({
  employeeId: null,
  date: '',
  checkIn: '',
  checkOut: '',
  status: '',
  notes: ''
})

// Validation schema
const schema = yup.object({
  employeeId: yup.number().when('isEditing', {
    is: false,
    then: yup.number().required()
  }),
  date: yup.date().required(),
  checkIn: yup.string().required(),
  checkOut: yup.string(),
  status: yup.string().required(),
  notes: yup.string()
})

// Table columns
const columns = [
  {
    key: 'employee',
    label: 'Employee',
    sortable: true
  },
  {
    key: 'time',
    label: 'Time',
    sortable: true
  },
  {
    key: 'status',
    label: 'Status',
    sortable: true
  },
  {
    key: 'actions',
    label: '',
    width: '100px'
  }
]

// Computed
const attendanceEvents = computed(() => {
  return attendanceData.value.map(item => ({
    id: item.id,
    title: item.name,
    start: item.date,
    end: item.date,
    status: item.status
  }))
})

// Methods
const fetchAttendanceData = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/attendance', {
      params: {
        page: currentPage.value,
        perPage: perPage.value,
        ...filters.value
      }
    })
    attendanceData.value = response.data.data
    total.value = response.data.total
  } catch (error) {
    console.error('Failed to fetch attendance data:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to fetch attendance data'
    })
  } finally {
    loading.value = false
  }
}

const fetchSummary = async () => {
  try {
    const response = await axios.get('/api/attendance/summary')
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

const fetchEmployees = async () => {
  try {
    const response = await axios.get('/api/employees')
    employees.value = response.data
  } catch (error) {
    console.error('Failed to fetch employees:', error)
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchAttendanceData()
}

const handleSearch = () => {
  currentPage.value = 1
  fetchAttendanceData()
}

const handleFilter = () => {
  currentPage.value = 1
  fetchAttendanceData()
}

const handleDateClick = (date) => {
  filters.value.date = date
  handleFilter()
}

const handleEventClick = (event) => {
  // Handle event click
}

const handleEdit = (item) => {
  isEditing.value = true
  formData.value = { ...item }
  showModal.value = true
}

const handleSubmit = async (values) => {
  try {
    submitting.value = true
    
    if (isEditing.value) {
      await axios.put(`/api/attendance/${formData.value.id}`, values)
      toast.value.show({
        type: 'success',
        message: 'Attendance updated successfully'
      })
    } else {
      await axios.post('/api/attendance', values)
      toast.value.show({
        type: 'success',
        message: 'Attendance recorded successfully'
      })
    }

    showModal.value = false
    fetchAttendanceData()
    fetchSummary()
  } catch (error) {
    console.error('Failed to save attendance:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to save attendance'
    })
  } finally {
    submitting.value = false
  }
}

const handleExport = async () => {
  try {
    const response = await axios.get('/api/attendance/export', {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'attendance.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Failed to export attendance:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to export attendance'
    })
  }
}

const getStatusColor = (status) => {
  const colors = {
    'present': 'success',
    'absent': 'danger',
    'late': 'warning',
    'leave': 'info'
  }
  return colors[status] || 'secondary'
}

const getEventClass = (event) => {
  const classes = {
    'present': 'bg-green-100 text-green-800',
    'absent': 'bg-red-100 text-red-800',
    'late': 'bg-yellow-100 text-yellow-800',
    'leave': 'bg-blue-100 text-blue-800'
  }
  return classes[event.status] || 'bg-gray-100 text-gray-800'
}

const getEventIcon = (event) => {
  const icons = {
    'present': 'fas fa-check',
    'absent': 'fas fa-times',
    'late': 'fas fa-clock',
    'leave': 'fas fa-calendar'
  }
  return icons[event.status] || 'fas fa-circle'
}

const formatTime = (time) => {
  return time ? new Date(`1970-01-01T${time}`).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  }) : '-'
}

const formatPercentage = (value) => {
  return `${value}%`
}

// Lifecycle
onMounted(() => {
  fetchAttendanceData()
  fetchSummary()
  fetchDepartments()
  fetchEmployees()
})
</script>
