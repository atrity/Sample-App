<template>
  <div class="stepper">
    <!-- Horizontal Layout -->
    <div v-if="!vertical" class="relative">
      <!-- Steps -->
      <div class="flex items-center justify-between">
        <template v-for="(step, index) in steps" :key="step.id">
          <!-- Step -->
          <div class="relative flex items-center">
            <!-- Step Circle -->
            <div
              :class="[
                'h-8 w-8 rounded-full flex items-center justify-center',
                getStepClass(index)
              ]"
            >
              <template v-if="step.completed">
                <i class="fas fa-check text-white"></i>
              </template>
              <template v-else>
                <span :class="currentStep > index ? 'text-white' : 'text-gray-500'">
                  {{ index + 1 }}
                </span>
              </template>
            </div>

            <!-- Step Label -->
            <div
              v-if="showLabels"
              class="absolute -bottom-8 w-32 text-center"
              :class="[
                index === 0 ? 'left-0' : '',
                index === steps.length - 1 ? 'right-0' : '',
                index !== 0 && index !== steps.length - 1 ? '-left-16' : ''
              ]"
            >
              <span
                class="text-sm font-medium"
                :class="getTextClass(index)"
              >
                {{ step.label }}
              </span>
            </div>
          </div>

          <!-- Connector Line -->
          <div
            v-if="index < steps.length - 1"
            class="flex-1 mx-4"
          >
            <div
              class="h-1 rounded"
              :class="currentStep > index ? 'bg-primary-600' : 'bg-gray-200'"
            ></div>
          </div>
        </template>
      </div>
    </div>

    <!-- Vertical Layout -->
    <div v-else class="space-y-4">
      <template v-for="(step, index) in steps" :key="step.id">
        <div class="relative flex items-start">
          <!-- Step Circle -->
          <div class="relative flex items-center">
            <div
              :class="[
                'h-8 w-8 rounded-full flex items-center justify-center',
                getStepClass(index)
              ]"
            >
              <template v-if="step.completed">
                <i class="fas fa-check text-white"></i>
              </template>
              <template v-else>
                <span :class="currentStep > index ? 'text-white' : 'text-gray-500'">
                  {{ index + 1 }}
                </span>
              </template>
            </div>
          </div>

          <!-- Step Content -->
          <div class="ml-4 min-w-0 flex-1">
            <div class="text-sm font-medium" :class="getTextClass(index)">
              {{ step.label }}
            </div>
            <div v-if="step.description" class="mt-1 text-sm text-gray-500">
              {{ step.description }}
            </div>
          </div>

          <!-- Step Status -->
          <div v-if="showStatus" class="ml-4">
            <template v-if="step.completed">
              <Badge variant="success" label="Completed" />
            </template>
            <template v-else-if="currentStep === index">
              <Badge variant="primary" label="Current" />
            </template>
          </div>
        </div>

        <!-- Connector Line -->
        <div
          v-if="index < steps.length - 1"
          class="ml-4 h-12 w-0.5"
          :class="currentStep > index ? 'bg-primary-600' : 'bg-gray-200'"
        ></div>
      </template>
    </div>

    <!-- Content -->
    <div v-if="$slots.default" class="mt-8">
      <slot></slot>
    </div>

    <!-- Navigation -->
    <div
      v-if="showNavigation"
      class="mt-8 flex justify-between"
      :class="{ 'flex-col space-y-4': vertical }"
    >
      <Button
        v-if="currentStep > 0"
        variant="secondary"
        @click="previousStep"
      >
        <i class="fas fa-chevron-left mr-2"></i>
        Previous
      </Button>
      <Button
        v-if="currentStep < steps.length - 1"
        variant="primary"
        @click="nextStep"
        :disabled="!canProceed"
      >
        Next
        <i class="fas fa-chevron-right ml-2"></i>
      </Button>
      <Button
        v-else
        variant="success"
        @click="complete"
        :disabled="!canComplete"
      >
        Complete
        <i class="fas fa-check ml-2"></i>
      </Button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from './Button.vue'
import Badge from './Badge.vue'

const props = defineProps({
  steps: {
    type: Array,
    required: true,
    validator: (steps) => {
      return steps.every(step =>
        typeof step === 'object' &&
        'id' in step &&
        'label' in step
      )
    }
  },
  currentStep: {
    type: Number,
    default: 0
  },
  vertical: {
    type: Boolean,
    default: false
  },
  showLabels: {
    type: Boolean,
    default: true
  },
  showStatus: {
    type: Boolean,
    default: false
  },
  showNavigation: {
    type: Boolean,
    default: true
  },
  canProceed: {
    type: Boolean,
    default: true
  },
  canComplete: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['previous', 'next', 'complete'])

// Methods
const getStepClass = (index) => {
  if (props.steps[index].completed) {
    return 'bg-primary-600'
  }
  if (props.currentStep === index) {
    return 'bg-primary-600'
  }
  if (props.currentStep > index) {
    return 'bg-primary-600'
  }
  return 'bg-gray-200'
}

const getTextClass = (index) => {
  if (props.currentStep === index) {
    return 'text-primary-600'
  }
  if (props.steps[index].completed) {
    return 'text-primary-600'
  }
  return 'text-gray-500'
}

const previousStep = () => {
  emit('previous')
}

const nextStep = () => {
  emit('next')
}

const complete = () => {
  emit('complete')
}
</script>

<style scoped>
.stepper {
  @apply relative;
}

/* Animations */
.step-enter-active,
.step-leave-active {
  @apply transition-all duration-300;
}

.step-enter-from,
.step-leave-to {
  @apply opacity-0 transform translate-x-4;
}

/* Vertical line connector animation */
.connector-line {
  @apply transition-all duration-500;
}

/* Step circle hover effect */
.step-circle {
  @apply transition-colors duration-200;
}

.step-circle:hover {
  @apply opacity-80;
}
</style>
