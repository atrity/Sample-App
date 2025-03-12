<template>
  <div class="calendar">
    <!-- Calendar Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-4">
        <h2 class="text-lg font-semibold text-gray-900">
          {{ currentMonthYear }}
        </h2>
        <div class="flex items-center space-x-2">
          <Button
            variant="secondary"
            size="sm"
            @click="previousMonth"
          >
            <i class="fas fa-chevron-left"></i>
          </Button>
          <Button
            variant="secondary"
            size="sm"
            @click="today"
          >
            Today
          </Button>
          <Button
            variant="secondary"
            size="sm"
            @click="nextMonth"
          >
            <i class="fas fa-chevron-right"></i>
          </Button>
        </div>
      </div>

      <!-- View Switcher -->
      <div class="flex items-center space-x-2">
        <Button
          v-for="view in availableViews"
          :key="view.value"
          :variant="currentView === view.value ? 'primary' : 'secondary'"
          size="sm"
          @click="changeView(view.value)"
        >
          {{ view.label }}
        </Button>
      </div>
    </div>

    <!-- Calendar Grid -->
    <div class="bg-white rounded-lg shadow">
      <!-- Week Days Header -->
      <div class="grid grid-cols-7 border-b border-gray-200">
        <div
          v-for="day in weekDays"
          :key="day"
          class="px-4 py-2 text-sm font-medium text-gray-900 text-center"
        >
          {{ day }}
        </div>
      </div>

      <!-- Calendar Days -->
      <div class="grid grid-cols-7 h-[600px]">
        <div
          v-for="(day, index) in calendarDays"
          :key="index"
          :class="[
            'border-b border-r border-gray-200 p-2 relative',
            {
              'bg-gray-50': !day.isCurrentMonth,
              'bg-primary-50': isToday(day.date),
              'cursor-pointer hover:bg-gray-50': !day.isDisabled
            }
          ]"
          @click="!day.isDisabled && selectDate(day)"
        >
          <!-- Day Number -->
          <div
            :class="[
              'text-sm font-medium',
              {
                'text-gray-900': day.isCurrentMonth,
                'text-gray-400': !day.isCurrentMonth,
                'text-primary-600': isToday(day.date)
              }
            ]"
          >
            {{ day.date.getDate() }}
          </div>

          <!-- Events -->
          <div class="mt-1 space-y-1">
            <div
              v-for="event in day.events"
              :key="event.id"
              :class="[
                'text-xs px-2 py-1 rounded-full truncate',
                getEventClass(event)
              ]"
              @click.stop="selectEvent(event)"
            >
              {{ event.title }}
            </div>
          </div>

          <!-- More Events Indicator -->
          <div
            v-if="day.events?.length > maxEventsPerDay"
            class="text-xs text-gray-500 mt-1 cursor-pointer"
            @click.stop="showMoreEvents(day)"
          >
            +{{ day.events.length - maxEventsPerDay }} more
          </div>
        </div>
      </div>
    </div>

    <!-- Event Modal -->
    <Modal
      v-model="showEventModal"
      :title="selectedEvent ? 'Edit Event' : 'New Event'"
    >
      <form @submit.prevent="handleEventSubmit">
        <div class="space-y-4">
          <FormInput
            v-model="eventForm.title"
            label="Title"
            required
          />
          <div class="grid grid-cols-2 gap-4">
            <FormInput
              v-model="eventForm.startDate"
              label="Start Date"
              type="date"
              required
            />
            <FormInput
              v-model="eventForm.endDate"
              label="End Date"
              type="date"
              required
            />
          </div>
          <FormInput
            v-model="eventForm.description"
            label="Description"
            type="textarea"
          />
          <FormInput
            v-model="eventForm.type"
            label="Event Type"
            type="select"
            :options="eventTypes"
          />
        </div>
        <div class="mt-4 flex justify-end space-x-2">
          <Button
            variant="secondary"
            @click="showEventModal = false"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            :loading="saving"
          >
            {{ selectedEvent ? 'Update' : 'Create' }}
          </Button>
        </div>
      </form>
    </Modal>

    <!-- More Events Modal -->
    <Modal
      v-model="showMoreEventsModal"
      title="Events"
    >
      <div class="space-y-2">
        <div
          v-for="event in selectedDayEvents"
          :key="event.id"
          :class="[
            'p-2 rounded-lg cursor-pointer hover:bg-gray-50',
            getEventClass(event)
          ]"
          @click="selectEvent(event)"
        >
          <div class="font-medium">{{ event.title }}</div>
          <div class="text-sm text-gray-500">
            {{ formatEventTime(event) }}
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import dayjs from 'dayjs'
import Button from './Button.vue'
import Modal from './Modal.vue'
import FormInput from './FormInput.vue'

const props = defineProps({
  events: {
    type: Array,
    default: () => []
  },
  maxEventsPerDay: {
    type: Number,
    default: 3
  },
  disabledDates: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['select-date', 'select-event', 'create-event', 'update-event'])

// State
const currentDate = ref(new Date())
const currentView = ref('month')
const showEventModal = ref(false)
const showMoreEventsModal = ref(false)
const selectedEvent = ref(null)
const selectedDate = ref(null)
const saving = ref(false)

const eventForm = ref({
  title: '',
  startDate: '',
  endDate: '',
  description: '',
  type: 'default'
})

// Constants
const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const availableViews = [
  { value: 'month', label: 'Month' },
  { value: 'week', label: 'Week' },
  { value: 'day', label: 'Day' }
]
const eventTypes = [
  { value: 'default', label: 'Default' },
  { value: 'meeting', label: 'Meeting' },
  { value: 'holiday', label: 'Holiday' },
  { value: 'birthday', label: 'Birthday' }
]

// Computed
const currentMonthYear = computed(() => {
  return dayjs(currentDate.value).format('MMMM YYYY')
})

const calendarDays = computed(() => {
  const days = []
  const start = dayjs(currentDate.value).startOf('month').startOf('week')
  const end = dayjs(currentDate.value).endOf('month').endOf('week')

  let current = start
  while (current.isBefore(end)) {
    days.push({
      date: current.toDate(),
      isCurrentMonth: current.month() === currentDate.value.getMonth(),
      isDisabled: isDateDisabled(current.toDate()),
      events: getEventsForDate(current.toDate())
    })
    current = current.add(1, 'day')
  }

  return days
})

const selectedDayEvents = computed(() => {
  if (!selectedDate.value) return []
  return getEventsForDate(selectedDate.value)
})

// Methods
const isToday = (date) => {
  return dayjs(date).isSame(dayjs(), 'day')
}

const isDateDisabled = (date) => {
  return props.disabledDates.some(disabledDate =>
    dayjs(date).isSame(dayjs(disabledDate), 'day')
  )
}

const getEventsForDate = (date) => {
  return props.events.filter(event =>
    dayjs(date).isBetween(event.startDate, event.endDate, 'day', '[]')
  )
}

const getEventClass = (event) => {
  const classes = {
    default: 'bg-blue-100 text-blue-800',
    meeting: 'bg-purple-100 text-purple-800',
    holiday: 'bg-red-100 text-red-800',
    birthday: 'bg-green-100 text-green-800'
  }
  return classes[event.type] || classes.default
}

const formatEventTime = (event) => {
  return `${dayjs(event.startDate).format('MMM D')} - ${dayjs(event.endDate).format('MMM D')}`
}

const previousMonth = () => {
  currentDate.value = dayjs(currentDate.value).subtract(1, 'month').toDate()
}

const nextMonth = () => {
  currentDate.value = dayjs(currentDate.value).add(1, 'month').toDate()
}

const today = () => {
  currentDate.value = new Date()
}

const changeView = (view) => {
  currentView.value = view
}

const selectDate = (day) => {
  emit('select-date', day.date)
  selectedDate.value = day.date
  showEventModal.value = true
  resetEventForm()
}

const selectEvent = (event) => {
  emit('select-event', event)
  selectedEvent.value = event
  showEventModal.value = true
  showMoreEventsModal.value = false
  populateEventForm(event)
}

const showMoreEvents = (day) => {
  selectedDate.value = day.date
  showMoreEventsModal.value = true
}

const resetEventForm = () => {
  eventForm.value = {
    title: '',
    startDate: dayjs(selectedDate.value).format('YYYY-MM-DD'),
    endDate: dayjs(selectedDate.value).format('YYYY-MM-DD'),
    description: '',
    type: 'default'
  }
}

const populateEventForm = (event) => {
  eventForm.value = {
    ...event,
    startDate: dayjs(event.startDate).format('YYYY-MM-DD'),
    endDate: dayjs(event.endDate).format('YYYY-MM-DD')
  }
}

const handleEventSubmit = async () => {
  try {
    saving.value = true
    if (selectedEvent.value) {
      await emit('update-event', { ...selectedEvent.value, ...eventForm.value })
    } else {
      await emit('create-event', eventForm.value)
    }
    showEventModal.value = false
  } catch (error) {
    console.error('Error saving event:', error)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.calendar {
  @apply bg-white rounded-lg shadow;
}

.calendar-day {
  min-height: 100px;
}

.event-item {
  @apply truncate cursor-pointer transition-colors duration-200;
}

.event-item:hover {
  @apply opacity-80;
}
</style>
