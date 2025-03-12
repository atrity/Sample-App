<template>
  <div :class="className">
    <!-- Label -->
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- Textarea Container -->
    <div class="relative">
      <!-- Textarea -->
      <textarea
        :id="id"
        ref="textareaRef"
        v-model="localValue"
        :class="[
          'block w-full rounded-md shadow-sm transition duration-150 ease-in-out sm:text-sm sm:leading-5',
          error
            ? 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-300 focus:ring-red-300'
            : 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
          disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white',
          resize === 'none' ? 'resize-none' : `resize-${resize}`
        ]"
        :placeholder="placeholder"
        :rows="rows"
        :maxlength="maxLength"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :autofocus="autofocus"
        v-bind="$attrs"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      ></textarea>

      <!-- Character Count -->
      <div
        v-if="showCount && maxLength"
        class="absolute bottom-2 right-2 text-xs text-gray-500"
      >
        {{ localValue.length }} / {{ maxLength }}
      </div>
    </div>

    <!-- Helper Text -->
    <p
      v-if="helperText && !error"
      class="mt-2 text-sm text-gray-500"
    >
      {{ helperText }}
    </p>

    <!-- Error Message -->
    <p
      v-if="error"
      class="mt-2 text-sm text-red-600"
    >
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  rows: {
    type: Number,
    default: 3
  },
  maxLength: {
    type: Number,
    default: null
  },
  showCount: {
    type: Boolean,
    default: false
  },
  resize: {
    type: String,
    default: 'vertical',
    validator: (value) => ['none', 'vertical', 'horizontal', 'both'].includes(value)
  },
  autoResize: {
    type: Boolean,
    default: false
  },
  minHeight: {
    type: Number,
    default: null
  },
  maxHeight: {
    type: Number,
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  autofocus: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  helperText: {
    type: String,
    default: ''
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'input', 'blur', 'focus'])

// Refs
const textareaRef = ref(null)
const localValue = ref(props.modelValue)
const id = computed(() => `textarea-${Math.random().toString(36).substr(2, 9)}`)

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  localValue.value = newValue
  if (props.autoResize) {
    nextTick(adjustHeight)
  }
})

// Methods
const handleInput = (event) => {
  const value = event.target.value
  localValue.value = value
  emit('update:modelValue', value)
  emit('input', event)

  if (props.autoResize) {
    adjustHeight()
  }
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const adjustHeight = () => {
  const textarea = textareaRef.value
  if (!textarea) return

  // Reset height to auto to get the correct scrollHeight
  textarea.style.height = 'auto'

  // Calculate new height
  let newHeight = textarea.scrollHeight

  // Apply min/max constraints
  if (props.minHeight) {
    newHeight = Math.max(newHeight, props.minHeight)
  }
  if (props.maxHeight) {
    newHeight = Math.min(newHeight, props.maxHeight)
  }

  // Set the new height
  textarea.style.height = `${newHeight}px`
}

// Initialize
if (props.autoResize) {
  nextTick(adjustHeight)
}
</script>

<style scoped>
/* Optional: Add focus styles */
textarea:focus {
  @apply outline-none ring-2 ring-offset-2;
}

/* Optional: Add transition for resize */
.textarea-resize {
  @apply transition-all duration-200;
}

/* Optional: Add custom scrollbar */
textarea {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.gray.400') theme('colors.gray.100');
}

textarea::-webkit-scrollbar {
  width: 6px;
}

textarea::-webkit-scrollbar-track {
  @apply bg-gray-100 rounded;
}

textarea::-webkit-scrollbar-thumb {
  @apply bg-gray-400 rounded hover:bg-gray-500;
}

/* Optional: Add placeholder styles */
textarea::placeholder {
  @apply text-gray-400;
}

/* Optional: Add disabled styles */
textarea:disabled::placeholder {
  @apply text-gray-300;
}

/* Optional: Add error state styles */
.textarea-error {
  @apply border-red-300 focus:border-red-300 focus:ring-red-300;
}

.textarea-error::placeholder {
  @apply text-red-300;
}
</style>
