<template>
  <div class="relative">
    <!-- Label -->
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- Select Container -->
    <div class="relative">
      <select
        :id="id"
        v-model="localValue"
        :class="[
          'block w-full rounded-md shadow-sm transition duration-150 ease-in-out sm:text-sm sm:leading-5',
          error
            ? 'border-red-300 text-red-900 focus:border-red-300 focus:ring-red-300'
            : 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
          disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white',
          className
        ]"
        :disabled="disabled"
        :required="required"
        v-bind="$attrs"
        @change="handleChange"
      >
        <!-- Placeholder Option -->
        <option
          v-if="placeholder"
          value=""
          disabled
          :selected="!modelValue"
          class="text-gray-400"
        >
          {{ placeholder }}
        </option>

        <!-- Option Groups -->
        <template v-if="hasGroups">
          <optgroup
            v-for="group in options"
            :key="group.label"
            :label="group.label"
          >
            <option
              v-for="option in group.options"
              :key="getOptionValue(option)"
              :value="getOptionValue(option)"
              :disabled="option.disabled"
            >
              {{ getOptionLabel(option) }}
            </option>
          </optgroup>
        </template>

        <!-- Regular Options -->
        <template v-else>
          <option
            v-for="option in options"
            :key="getOptionValue(option)"
            :value="getOptionValue(option)"
            :disabled="option.disabled"
          >
            {{ getOptionLabel(option) }}
          </option>
        </template>
      </select>

      <!-- Custom Arrow Icon -->
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2">
        <i class="fas fa-chevron-down text-gray-400"></i>
      </div>
    </div>

    <!-- Helper Text -->
    <p
      v-if="helperText && !error"
      class="mt-1 text-sm text-gray-500"
    >
      {{ helperText }}
    </p>

    <!-- Error Message -->
    <p
      v-if="error"
      class="mt-1 text-sm text-red-600"
    >
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean, Array, Object],
    default: ''
  },
  options: {
    type: Array,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select an option'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
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
  valueKey: {
    type: String,
    default: 'value'
  },
  labelKey: {
    type: String,
    default: 'label'
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// State
const localValue = ref(props.modelValue)
const id = computed(() => `select-${Math.random().toString(36).substr(2, 9)}`)

// Computed
const hasGroups = computed(() => {
  return props.options.length > 0 && 'options' in props.options[0]
})

// Methods
const getOptionValue = (option) => {
  if (typeof option === 'object') {
    return option[props.valueKey]
  }
  return option
}

const getOptionLabel = (option) => {
  if (typeof option === 'object') {
    return option[props.labelKey]
  }
  return option
}

const handleChange = (event) => {
  const value = event.target.value
  emit('update:modelValue', value)
  emit('change', value)
}

// Watchers
watch(() => props.modelValue, (newValue) => {
  localValue.value = newValue
})
</script>

<style scoped>
/* Custom select styles */
select {
  @apply appearance-none;
  background-image: none;
}

/* Focus styles */
select:focus {
  @apply outline-none ring-2 ring-offset-2;
}

/* Disabled styles */
select:disabled {
  @apply opacity-50 cursor-not-allowed;
}

/* Custom arrow styles */
.select-arrow {
  @apply pointer-events-none absolute inset-y-0 right-0 flex items-center px-2;
}

/* Animation */
.select-enter-active,
.select-leave-active {
  @apply transition-all duration-200;
}

.select-enter-from,
.select-leave-to {
  @apply opacity-0;
}

/* Size variants */
.select-sm {
  @apply py-1 text-sm;
}

.select-lg {
  @apply py-3 text-lg;
}

/* Custom scrollbar for dropdown */
select {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.gray.400') theme('colors.gray.100');
}

select::-webkit-scrollbar {
  width: 8px;
}

select::-webkit-scrollbar-track {
  @apply bg-gray-100;
}

select::-webkit-scrollbar-thumb {
  @apply bg-gray-400 rounded;
}

select::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-500;
}
</style>
