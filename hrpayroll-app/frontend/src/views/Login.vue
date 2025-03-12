<template>
  <div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <!-- Logo -->
      <div class="flex justify-center">
        <img
          class="h-12 w-auto"
          src="@/assets/logo.png"
          alt="HR Payroll"
        >
      </div>

      <!-- Title -->
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Sign in to your account
      </h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <!-- Login Form -->
        <Form
          class="space-y-6"
          :validation-schema="schema"
          @submit="handleSubmit"
        >
          <!-- Email Field -->
          <div>
            <FormInput
              v-model="form.email"
              type="email"
              label="Email address"
              name="email"
              autocomplete="email"
              required
            />
          </div>

          <!-- Password Field -->
          <div>
            <FormInput
              v-model="form.password"
              type="password"
              label="Password"
              name="password"
              autocomplete="current-password"
              required
            />
          </div>

          <!-- Remember Me & Forgot Password -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <Checkbox
                v-model="form.remember"
                label="Remember me"
                name="remember"
              />
            </div>

            <div class="text-sm">
              <Link
                href="#"
                @click.prevent="handleForgotPassword"
              >
                Forgot your password?
              </Link>
            </div>
          </div>

          <!-- Submit Button -->
          <div>
            <Button
              type="submit"
              variant="primary"
              class="w-full"
              :loading="loading"
            >
              Sign in
            </Button>
          </div>
        </Form>

        <!-- Error Alert -->
        <Alert
          v-if="error"
          class="mt-4"
          type="error"
          :message="error"
          dismissible
          @dismiss="error = null"
        />
      </div>
    </div>

    <!-- Forgot Password Modal -->
    <Modal
      v-model="showForgotPasswordModal"
      title="Reset Password"
      :loading="loading"
    >
      <Form
        class="space-y-6"
        :validation-schema="forgotPasswordSchema"
        @submit="handleForgotPasswordSubmit"
      >
        <FormInput
          v-model="forgotPasswordEmail"
          type="email"
          label="Email address"
          name="email"
          required
        />

        <div class="flex justify-end space-x-3">
          <Button
            variant="secondary"
            @click="showForgotPasswordModal = false"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            :loading="loading"
          >
            Send Reset Link
          </Button>
        </div>
      </Form>
    </Modal>

    <!-- Toast for notifications -->
    <Toast ref="toast" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import * as yup from 'yup'
import Form from '@/components/Form.vue'
import FormInput from '@/components/FormInput.vue'
import Button from '@/components/Button.vue'
import Checkbox from '@/components/Checkbox.vue'
import Link from '@/components/Link.vue'
import Alert from '@/components/Alert.vue'
import Modal from '@/components/Modal.vue'
import Toast from '@/components/Toast.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const toast = ref(null)

// Form state
const form = ref({
  email: '',
  password: '',
  remember: false
})

const loading = ref(false)
const error = ref(null)

// Validation schema
const schema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().required().min(8)
})

// Handle form submission
const handleSubmit = async (values) => {
  try {
    loading.value = true
    error.value = null

    await authStore.login({
      email: values.email,
      password: values.password,
      remember: values.remember
    })

    // Redirect to intended route or dashboard
    const redirectPath = route.query.redirect || '/dashboard'
    router.push(redirectPath)

    toast.value.show({
      type: 'success',
      message: 'Welcome back!'
    })
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed'
  } finally {
    loading.value = false
  }
}

// Forgot password
const showForgotPasswordModal = ref(false)
const forgotPasswordEmail = ref('')

const forgotPasswordSchema = yup.object({
  email: yup.string().email().required()
})

const handleForgotPassword = () => {
  showForgotPasswordModal.value = true
}

const handleForgotPasswordSubmit = async (values) => {
  try {
    loading.value = true
    error.value = null

    await authStore.forgotPassword(values.email)
    
    showForgotPasswordModal.value = false
    forgotPasswordEmail.value = ''

    toast.value.show({
      type: 'success',
      message: 'Password reset instructions have been sent to your email.'
    })
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to send reset email'
  } finally {
    loading.value = false
  }
}
</script>
