<template>
  <form
    :class="[
      'space-y-6',
      className
    ]"
    @submit.prevent="handleSubmit"
  >
    <!-- Form Header -->
    <div v-if="title || description" class="mb-6">
      <h3
        v-if="title"
        class="text-lg font-medium text-gray-900"
      >
        {{ title }}
      </h3>
      <p
        v-if="description"
        class="mt-1 text-sm text-gray-500"
      >
        {{ description }}
      </p>
    </div>

    <!-- Form Fields -->
    <div :class="{ 'space-y-6': !inline }">
      <slot
        :values="values"
        :errors="errors"
        :touched="touched"
        :handleChange="handleChange"
        :handleBlur="handleBlur"
        :isSubmitting="isSubmitting"
        :resetForm="resetForm"
      ></slot>
    </div>

    <!-- Form Actions -->
    <div
      v-if="$slots.actions || showDefaultActions"
      :class="[
        'flex items-center',
        actionsAlign === 'right' ? 'justify-end' : '',
        actionsAlign === 'center' ? 'justify-center' : '',
        actionsAlign === 'between' ? 'justify-between' : '',
        actionsClass
      ]"
    >
      <slot name="actions">
        <!-- Default Actions -->
        <template v-if="showDefaultActions">
          <Button
            v-if="showReset"
            type="button"
            variant="secondary"
            :disabled="isSubmitting"
            @click="resetForm"
          >
            {{ resetLabel }}
          </Button>
          <Button
            type="submit"
            :variant="submitVariant"
            :loading="isSubmitting"
            :disabled="isSubmitting || (disableIfInvalid && !isValid)"
          >
            {{ submitLabel }}
          </Button>
        </template>
      </slot>
    </div>

    <!-- Form Error -->
    <p
      v-if="error"
      class="mt-2 text-sm text-red-600"
    >
      {{ error }}
    </p>
  </form>
</template>

<script setup>
import { ref, computed } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  initialValues: {
    type: Object,
    default: () => ({})
  },
  validationSchema: {
    type: Object,
    default: null
  },
  onSubmit: {
    type: Function,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  inline: {
    type: Boolean,
    default: false
  },
  showDefaultActions: {
    type: Boolean,
    default: true
  },
  showReset: {
    type: Boolean,
    default: true
  },
  submitLabel: {
    type: String,
    default: 'Submit'
  },
  resetLabel: {
    type: String,
    default: 'Reset'
  },
  submitVariant: {
    type: String,
    default: 'primary'
  },
  actionsAlign: {
    type: String,
    default: 'right',
    validator: (value) => ['left', 'center', 'right', 'between'].includes(value)
  },
  disableIfInvalid: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  },
  actionsClass: {
    type: String,
    default: 'space-x-3'
  }
})

const emit = defineEmits(['submit', 'reset', 'change'])

// State
const values = ref({ ...props.initialValues })
const errors = ref({})
const touched = ref({})
const isSubmitting = ref(false)
const error = ref('')

// Computed
const isValid = computed(() => {
  if (!props.validationSchema) return true
  try {
    props.validationSchema.validateSync(values.value, { abortEarly: false })
    return true
  } catch {
    return false
  }
})

// Methods
const validate = async () => {
  if (!props.validationSchema) return true

  try {
    await props.validationSchema.validate(values.value, { abortEarly: false })
    errors.value = {}
    return true
  } catch (validationError) {
    const newErrors = {}
    validationError.inner.forEach((error) => {
      newErrors[error.path] = error.message
    })
    errors.value = newErrors
    return false
  }
}

const handleChange = (field, value) => {
  values.value[field] = value
  emit('change', values.value)
  validate()
}

const handleBlur = (field) => {
  touched.value[field] = true
  validate()
}

const handleSubmit = async () => {
  error.value = ''
  
  if (await validate()) {
    try {
      isSubmitting.value = true
      await props.onSubmit(values.value)
      emit('submit', values.value)
    } catch (err) {
      error.value = err.message || 'An error occurred'
    } finally {
      isSubmitting.value = false
    }
  }
}

const resetForm = () => {
  values.value = { ...props.initialValues }
  errors.value = {}
  touched.value = {}
  error.value = ''
  emit('reset')
}
</script>

<style scoped>
/* Optional: Add form field animations */
.form-field-enter-active,
.form-field-leave-active {
  @apply transition-all duration-300;
}

.form-field-enter-from,
.form-field-leave-to {
  @apply opacity-0 transform -translate-y-2;
}

/* Optional: Add error message animations */
.error-message-enter-active,
.error-message-leave-active {
  @apply transition-all duration-200;
}

.error-message-enter-from,
.error-message-leave-to {
  @apply opacity-0 transform scale-95;
}

/* Optional: Add inline form styles */
.form-inline {
  @apply flex items-start space-x-4;
}

.form-inline .form-field {
  @apply flex-1;
}

/* Optional: Add form grid layout */
.form-grid {
  @apply grid gap-6;
}

/* Optional: Add responsive form layout */
@screen sm {
  .form-responsive {
    @apply grid grid-cols-2 gap-6;
  }
}

@screen lg {
  .form-responsive {
    @apply grid-cols-3;
  }
}
</style>
