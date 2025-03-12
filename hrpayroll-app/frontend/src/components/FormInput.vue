<template>
  <div>
    <!-- Label -->
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- Input Group -->
    <div class="relative">
      <!-- Prefix Icon or Text -->
      <div
        v-if="prefix || $slots.prefix"
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
      >
        <slot name="prefix">
          <i v-if="prefix" :class="['text-gray-400', prefix]"></i>
          <span v-else class="text-gray-500">{{ prefix }}</span>
        </slot>
      </div>

      <!-- Input Element -->
      <template v-if="type === 'textarea'">
        <textarea
          :id="id"
          v-model="inputValue"
          :class="[
            'form-input',
            { 'pl-10': prefix || $slots.prefix },
            { 'pr-10': suffix || $slots.suffix },
            errorMessage ? 'border-red-300' : 'border-gray-300',
            disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'
          ]"
          v-bind="$attrs"
          :placeholder="placeholder"
          :disabled="disabled"
          :required="required"
          @input="onInput"
          @blur="onBlur"
        ></textarea>
      </template>
      <template v-else>
        <input
          :id="id"
          :type="showPassword ? 'text' : type"
          v-model="inputValue"
          :class="[
            'form-input',
            { 'pl-10': prefix || $slots.prefix },
            { 'pr-10': suffix || $slots.suffix || type === 'password' },
            errorMessage ? 'border-red-300' : 'border-gray-300',
            disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'
          ]"
          v-bind="$attrs"
          :placeholder="placeholder"
          :disabled="disabled"
          :required="required"
          @input="onInput"
          @blur="onBlur"
        />
      </template>

      <!-- Suffix Icon or Text -->
      <div
        v-if="suffix || $slots.suffix || type === 'password'"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
      >
        <slot name="suffix">
          <template v-if="type === 'password'">
            <button
              type="button"
              class="text-gray-400 hover:text-gray-500 focus:outline-none"
              @click="togglePassword"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </template>
          <template v-else>
            <i v-if="suffix" :class="['text-gray-400', suffix]"></i>
            <span v-else class="text-gray-500">{{ suffix }}</span>
          </template>
        </slot>
      </div>
    </div>

    <!-- Helper Text -->
    <p
      v-if="helperText && !errorMessage"
      class="mt-1 text-sm text-gray-500"
    >
      {{ helperText }}
    </p>

    <!-- Error Message -->
    <p
      v-if="errorMessage"
      class="mt-1 text-sm text-red-600"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  },
  placeholder: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  prefix: {
    type: String,
    default: ''
  },
  suffix: {
    type: String,
    default: ''
  },
  helperText: {
    type: String,
    default: ''
  },
  errorMessage: {
    type: String,
    default: ''
  },
  validateOnBlur: {
    type: Boolean,
    default: false
  },
  rules: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'input'])

// Data
const showPassword = ref(false)
const inputValue = ref(props.modelValue)
const localErrorMessage = ref('')

// Computed
const computedErrorMessage = computed(() => {
  return props.errorMessage || localErrorMessage.value
})

// Methods
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const validate = () => {
  if (!props.rules.length) return true

  for (const rule of props.rules) {
    const result = rule(inputValue.value)
    if (result !== true) {
      localErrorMessage.value = result
      return false
    }
  }

  localErrorMessage.value = ''
  return true
}

const onInput = (event) => {
  const value = event.target.value
  inputValue.value = value
  emit('update:modelValue', value)
  emit('input', event)

  if (!props.validateOnBlur) {
    validate()
  }
}

const onBlur = (event) => {
  emit('blur', event)
  if (props.validateOnBlur) {
    validate()
  }
}

// Watchers
watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue
})
</script>

<style scoped>
.form-input {
  @apply block w-full rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm;
}

.form-input:disabled {
  @apply opacity-75 cursor-not-allowed;
}
</style>
