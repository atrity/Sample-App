<template>
  <div>
    <!-- Page Header -->
    <header class="mb-8">
      <Container>
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-gray-900">Departments</h1>
          <Button
            variant="primary"
            icon="fas fa-plus"
            @click="showAddModal = true"
          >
            Add Department
          </Button>
        </div>
      </Container>
    </header>

    <!-- Department Cards -->
    <section class="mb-8">
      <Container>
        <Grid :cols="{ default: 1, md: 2, lg: 3 }" gap="4">
          <Card
            v-for="dept in departments"
            :key="dept.id"
            class="hover:shadow-lg transition-shadow duration-200"
          >
            <div class="flex items-start justify-between">
              <div>
                <h3 class="text-lg font-medium text-gray-900">
                  {{ dept.name }}
                </h3>
                <p class="text-sm text-gray-500">
                  {{ dept.description }}
                </p>
              </div>
              <Dropdown>
                <template #trigger>
                  <Button
                    variant="ghost"
                    icon="fas fa-ellipsis-v"
                    size="sm"
                  />
                </template>
                <template #content>
                  <div class="py-1">
                    <a
                      href="#"
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      @click.prevent="handleEdit(dept)"
                    >
                      Edit
                    </a>
                    <a
                      href="#"
                      class="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                      @click.prevent="handleDelete(dept)"
                    >
                      Delete
                    </a>
                  </div>
                </template>
              </Dropdown>
            </div>

            <Divider class="my-4" />

            <!-- Department Stats -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">Employees</p>
                <p class="text-lg font-medium">{{ dept.employeeCount }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Budget</p>
                <p class="text-lg font-medium">
                  {{ formatCurrency(dept.budget) }}
                </p>
              </div>
            </div>

            <Divider class="my-4" />

            <!-- Department Manager -->
            <div class="flex items-center">
              <Avatar
                :src="dept.manager?.avatar"
                :name="dept.manager?.name"
                size="sm"
              />
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900">
                  {{ dept.manager?.name }}
                </p>
                <p class="text-xs text-gray-500">Department Manager</p>
              </div>
            </div>
          </Card>
        </Grid>
      </Container>
    </section>

    <!-- Add/Edit Modal -->
    <Modal
      v-model="showModal"
      :title="isEditing ? 'Edit Department' : 'Add Department'"
    >
      <Form
        ref="form"
        :validation-schema="schema"
        @submit="handleSubmit"
      >
        <div class="space-y-4">
          <FormInput
            v-model="formData.name"
            label="Department Name"
            name="name"
            required
          />

          <TextArea
            v-model="formData.description"
            label="Description"
            name="description"
            rows="3"
          />

          <Select
            v-model="formData.managerId"
            label="Department Manager"
            name="managerId"
            :options="employees"
            option-label="name"
            option-value="id"
            required
          />

          <FormInput
            v-model="formData.budget"
            type="number"
            label="Budget"
            name="budget"
            required
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
              {{ isEditing ? 'Update' : 'Create' }}
            </Button>
          </div>
        </template>
      </Form>
    </Modal>

    <!-- Delete Confirmation Dialog -->
    <Dialog
      v-model="showDeleteDialog"
      title="Delete Department"
      :loading="submitting"
      @confirm="confirmDelete"
    >
      <p>Are you sure you want to delete this department? This action cannot be undone.</p>
      <p class="mt-2 text-sm text-red-600">
        Note: This will affect all employees in this department.
      </p>
    </Dialog>

    <!-- Toast for notifications -->
    <Toast ref="toast" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as yup from 'yup'
import Container from '@/components/Container.vue'
import Grid from '@/components/Grid.vue'
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'
import Dropdown from '@/components/Dropdown.vue'
import Divider from '@/components/Divider.vue'
import Avatar from '@/components/Avatar.vue'
import Modal from '@/components/Modal.vue'
import Form from '@/components/Form.vue'
import FormInput from '@/components/FormInput.vue'
import TextArea from '@/components/TextArea.vue'
import Select from '@/components/Select.vue'
import Dialog from '@/components/Dialog.vue'
import Toast from '@/components/Toast.vue'

// State
const loading = ref(false)
const submitting = ref(false)
const showModal = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const selectedDepartment = ref(null)
const toast = ref(null)
const form = ref(null)

const departments = ref([])
const employees = ref([])

// Form data
const formData = ref({
  name: '',
  description: '',
  managerId: null,
  budget: 0
})

// Validation schema
const schema = yup.object({
  name: yup.string().required(),
  description: yup.string(),
  managerId: yup.number().required(),
  budget: yup.number().required().min(0)
})

// Methods
const fetchDepartments = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/departments')
    departments.value = response.data
  } catch (error) {
    console.error('Failed to fetch departments:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to fetch departments'
    })
  } finally {
    loading.value = false
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

const handleEdit = (department) => {
  isEditing.value = true
  selectedDepartment.value = department
  formData.value = { ...department }
  showModal.value = true
}

const handleDelete = (department) => {
  selectedDepartment.value = department
  showDeleteDialog.value = true
}

const handleSubmit = async (values) => {
  try {
    submitting.value = true
    
    if (isEditing.value) {
      await axios.put(`/api/departments/${selectedDepartment.value.id}`, values)
      toast.value.show({
        type: 'success',
        message: 'Department updated successfully'
      })
    } else {
      await axios.post('/api/departments', values)
      toast.value.show({
        type: 'success',
        message: 'Department created successfully'
      })
    }

    showModal.value = false
    fetchDepartments()
  } catch (error) {
    console.error('Failed to save department:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to save department'
    })
  } finally {
    submitting.value = false
  }
}

const confirmDelete = async () => {
  try {
    submitting.value = true
    await axios.delete(`/api/departments/${selectedDepartment.value.id}`)
    
    showDeleteDialog.value = false
    fetchDepartments()
    
    toast.value.show({
      type: 'success',
      message: 'Department deleted successfully'
    })
  } catch (error) {
    console.error('Failed to delete department:', error)
    toast.value.show({
      type: 'error',
      message: 'Failed to delete department'
    })
  } finally {
    submitting.value = false
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value)
}

// Lifecycle
onMounted(() => {
  fetchDepartments()
  fetchEmployees()
})
</script>
