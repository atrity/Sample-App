<template>
  <div>
    <!-- Page Header -->
    <header class="mb-8">
      <Container>
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-gray-900">Employees</h1>
          <Button
            variant="primary"
            icon="fas fa-plus"
            @click="showAddModal = true"
          >
            Add Employee
          </Button>
        </div>
      </Container>
    </header>

    <!-- Filters -->
    <section class="mb-6">
      <Container>
        <Card>
          <Grid :cols="{ default: 1, md: 3 }" gap="4">
            <!-- Search -->
            <FormInput
              v-model="filters.search"
              placeholder="Search employees..."
              icon="fas fa-search"
              @input="handleSearch"
            />

            <!-- Department Filter -->
            <Select
              v-model="filters.department"
              placeholder="Filter by department"
              :options="departments"
              option-label="name"
              option-value="id"
              @change="handleFilter"
            />

            <!-- Status Filter -->
            <Select
              v-model="filters.status"
              placeholder="Filter by status"
              :options="[
                { label: 'Active', value: 'active' },
                { label: 'Inactive', value: 'inactive' }
              ]"
              @change="handleFilter"
            />
          </Grid>
        </Card>
      </Container>
    </section>

    <!-- Employees Table -->
    <section>
      <Container>
        <Card>
          <DataTable
            :columns="columns"
            :data="employees"
            :loading="loading"
            :total="total"
            :per-page="perPage"
            :current-page="currentPage"
            @page-change="handlePageChange"
          >
            <!-- Avatar Column -->
            <template #column-avatar="{ item }">
              <Avatar
                :src="item.avatar"
                :name="item.name"
                size="sm"
              />
            </template>

            <!-- Name Column -->
            <template #column-name="{ item }">
              <div>
                <p class="font-medium text-gray-900">{{ item.name }}</p>
                <p class="text-sm text-gray-500">{{ item.email }}</p>
              </div>
            </template>

            <!-- Department Column -->
            <template #column-department="{ item }">
              <Badge :color="getDepartmentColor(item.department)">
                {{ item.department }}
              </Badge>
            </template>

            <!-- Status Column -->
            <template #column-status="{ item }">
              <Badge
                :color="item.status === 'active' ? 'success' : 'danger'"
              >
                {{ item.status }}
              </Badge>
            </template>

            <!-- Actions Column -->
            <template #column-actions="{ item }">
              <div class="flex items-center space-x-2">
                <Button
                  variant="secondary"
                  size="sm"
                  icon="fas fa-edit"
                  @click="handleEdit(item)"
                />
                <Button
                  variant="danger"
                  size="sm"
                  icon="fas fa-trash"
                  @click="handleDelete(item)"
                />
              </div>
            </template>
          </DataTable>
        </Card>
      </Container>
    </section>

    <!-- Add/Edit Modal -->
    <Modal
      v-model="showModal"
      :title="isEditing ? 'Edit Employee' : 'Add Employee'"
      size="lg"
    >
      <Form
        ref="form"
        :validation-schema="schema"
        @submit="handleSubmit"
      >
        <Grid :cols="{ default: 1, md: 2 }" gap="4">
          <!-- Personal Information -->
          <div class="space-y-4">
            <h3 class="font-medium text-gray-900">Personal Information</h3>
            
            <FormInput
              v-model="formData.name"
              label="Full Name"
              name="name"
              required
            />

            <FormInput
              v-model="formData.email"
              type="email"
              label="Email"
              name="email"
              required
            />

            <FormInput
              v-model="formData.phone"
              label="Phone"
              name="phone"
            />

            <FormInput
              v-model="formData.dateOfBirth"
              type="date"
              label="Date of Birth"
              name="dateOfBirth"
            />
          </div>

          <!-- Employment Information -->
          <div class="space-y-4">
            <h3 class="font-medium text-gray-900">Employment Information</h3>

            <Select
              v-model="formData.departmentId"
              label="Department"
              name="departmentId"
              :options="departments"
              option-label="name"
              option-value="id"
              required
            />

            <FormInput
              v-model="formData.position"
              label="Position"
              name="position"
              required
            />

            <FormInput
              v-model="formData.salary"
              type="number"
              label="Salary"
              name="salary"
              required
            />

            <FormInput
              v-model="formData.joinDate"
              type="date"
              label="Join Date"
              name="joinDate"
              required
            />
          </div>
        </Grid>

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
              {{ isEditing ? 'Update' : 'Create' }}
            </Button>
          </div>
        </template>
      </Form>
    </Modal>

    <!-- Delete Confirmation Dialog -->
    <Dialog
      v-model="showDeleteDialog"
      title="Delete Employee"
      :loading="submitting"
      @confirm="confirmDelete"
    >
      <p>Are you sure you want to delete this employee? This action cannot be undone.</p>
    </Dialog>

    <!-- Toast for notifications -->
    <Toast ref="toast" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import * as yup from 'yup'
import Container from '@/components/Container.vue'
import Card from '@/components/Card.vue'
import Grid from '@/components/Grid.vue'
import Button from '@/components/Button.vue'
import FormInput from '@/components/FormInput.vue'
import Select from '@/components/Select.vue'
import DataTable from '@/components/DataTable.vue'
import Avatar from '@/components/Avatar.vue'
import Badge from '@/components/Badge.vue'
import Modal from '@/components/Modal.vue'
import Form from '@/components/Form.vue'
import Dialog from '@/components/Dialog.vue'
import Toast from '@/components/Toast.vue'

// State
const loading = ref(false)
const submitting = ref(false)
const showModal = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const selectedEmployee = ref(null)
const toast = ref(null)
const form = ref(null)

const employees = ref([])
const departments = ref([])
const total = ref(0)
const perPage = ref(10)
const currentPage = ref(1)

// Filters
const filters = ref({
  search: '',
  department: null,
  status: null
})

// Form data
const formData = ref({
  name: '',
  email: '',
  phone: '',
  dateOfBirth: '',
  departmentId: null,
  position: '',
  salary: '',
  joinDate: '',
  status: 'active'
})

// Table columns
const columns = [
  {
    key: 'avatar',
    label: '',
    width: '50px'
  },
  {
    key: 'name',
    label: 'Employee',
    sortable: true
  },
  {
    key: 'department',
    label: 'Department',
    sortable: true
  },
  {
    key: 'position',
    label: 'Position',
    sortable: true
  },
  {
    key: 'status',
    label: 'Status',
    width: '100px'
  },
  {
    key: 'actions',
    label: '',
    width: '100px'
  }
]

// Validation schema
const schema = yup.object({
  name: yup.string().required(),
  email: yup.string().email().required(),
  phone: yup.string(),
  dateOfBirth: yup.date(),
  departmentId: yup.number().required(),
  position: yup.string().required(),
  salary: yup.number().required().min(0),
  joinDate: yup.date().required()
})

// Methods
const fetchEmployees = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/employees', {
      params: {
        page: currentPage.value,
        perPage: perPage.value,
        ...filters.value
      }
    })
    employees.value = response.data.data
    total.value = response.data.total
  } catch (error) {
    console.error('Failed to fetch employees:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to fetch employees'
    })
  } finally {
    loading.value = false
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
  fetchEmployees()
}

const handleSearch = () => {
  currentPage.value = 1
  fetchEmployees()
}

const handleFilter = () => {
  currentPage.value = 1
  fetchEmployees()
}

const handleEdit = (employee) => {
  isEditing.value = true
  selectedEmployee.value = employee
  formData.value = { ...employee }
  showModal.value = true
}

const handleDelete = (employee) => {
  selectedEmployee.value = employee
  showDeleteDialog.value = true
}

const handleSubmit = async (values) => {
  try {
    submitting.value = true
    
    if (isEditing.value) {
      await axios.put(`/api/employees/${selectedEmployee.value.id}`, values)
      toast.value.show({
        type: 'success',
        message: 'Employee updated successfully'
      })
    } else {
      await axios.post('/api/employees', values)
      toast.value.show({
        type: 'success',
        message: 'Employee created successfully'
      })
    }

    showModal.value = false
    fetchEmployees()
  } catch (error) {
    console.error('Failed to save employee:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to save employee'
    })
  } finally {
    submitting.value = false
  }
}

const confirmDelete = async () => {
  try {
    submitting.value = true
    await axios.delete(`/api/employees/${selectedEmployee.value.id}`)
    
    showDeleteDialog.value = false
    fetchEmployees()
    
    toast.value.show({
      type: 'success',
      message: 'Employee deleted successfully'
    })
  } catch (error) {
    console.error('Failed to delete employee:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to delete employee'
    })
  } finally {
    submitting.value = false
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

// Lifecycle
onMounted(() => {
  fetchEmployees()
  fetchDepartments()
})
</script>
