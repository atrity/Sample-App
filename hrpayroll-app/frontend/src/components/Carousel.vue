<template>
  <div
    class="relative"
    :class="className"
    @mouseenter="autoplay && pause()"
    @mouseleave="autoplay && resume()"
  >
    <!-- Slides Container -->
    <div
      ref="container"
      class="overflow-hidden relative"
      :class="{ 'rounded-lg': rounded }"
    >
      <!-- Slides -->
      <div
        class="flex transition-transform duration-300 ease-in-out"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <div
          v-for="(slide, index) in slides"
          :key="getSlideKey(slide, index)"
          class="flex-shrink-0 w-full"
        >
          <!-- Custom Slide Content -->
          <slot
            :name="'slide-' + index"
            :slide="slide"
            :index="index"
            :active="currentIndex === index"
          >
            <!-- Default Slide Content -->
            <div class="relative">
              <!-- Image -->
              <img
                :src="getSlideImage(slide)"
                :alt="getSlideTitle(slide)"
                class="w-full h-full object-cover"
                :style="{ height }"
              >

              <!-- Caption -->
              <div
                v-if="captions && (getSlideTitle(slide) || getSlideDescription(slide))"
                class="absolute bottom-0 left-0 right-0 p-4 bg-black bg-opacity-50 text-white"
              >
                <h3
                  v-if="getSlideTitle(slide)"
                  class="text-lg font-medium"
                >
                  {{ getSlideTitle(slide) }}
                </h3>
                <p
                  v-if="getSlideDescription(slide)"
                  class="mt-1 text-sm"
                >
                  {{ getSlideDescription(slide) }}
                </p>
              </div>
            </div>
          </slot>
        </div>
      </div>

      <!-- Navigation Arrows -->
      <template v-if="arrows && slides.length > 1">
        <!-- Previous -->
        <button
          class="absolute top-1/2 left-4 -translate-y-1/2 p-2 rounded-full bg-black bg-opacity-50 text-white hover:bg-opacity-75 focus:outline-none"
          @click="previous"
        >
          <i class="fas fa-chevron-left"></i>
        </button>

        <!-- Next -->
        <button
          class="absolute top-1/2 right-4 -translate-y-1/2 p-2 rounded-full bg-black bg-opacity-50 text-white hover:bg-opacity-75 focus:outline-none"
          @click="next"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </template>
    </div>

    <!-- Indicators -->
    <div
      v-if="indicators && slides.length > 1"
      class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2"
    >
      <button
        v-for="(_, index) in slides"
        :key="index"
        class="w-2 h-2 rounded-full transition-all duration-200 focus:outline-none"
        :class="[
          currentIndex === index
            ? 'bg-white scale-125'
            : 'bg-white bg-opacity-50 hover:bg-opacity-75'
        ]"
        @click="goTo(index)"
      ></button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  slides: {
    type: Array,
    required: true
  },
  height: {
    type: String,
    default: '400px'
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  interval: {
    type: Number,
    default: 5000
  },
  arrows: {
    type: Boolean,
    default: true
  },
  indicators: {
    type: Boolean,
    default: true
  },
  captions: {
    type: Boolean,
    default: true
  },
  rounded: {
    type: Boolean,
    default: true
  },
  imageKey: {
    type: String,
    default: 'image'
  },
  titleKey: {
    type: String,
    default: 'title'
  },
  descriptionKey: {
    type: String,
    default: 'description'
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['change'])

// State
const currentIndex = ref(0)
const autoplayInterval = ref(null)
const container = ref(null)

// Methods
const getSlideKey = (slide, index) => {
  return slide.id || index
}

const getSlideImage = (slide) => {
  return typeof slide === 'string' ? slide : slide[props.imageKey]
}

const getSlideTitle = (slide) => {
  return typeof slide === 'object' ? slide[props.titleKey] : null
}

const getSlideDescription = (slide) => {
  return typeof slide === 'object' ? slide[props.descriptionKey] : null
}

const next = () => {
  currentIndex.value = (currentIndex.value + 1) % props.slides.length
  emit('change', currentIndex.value)
}

const previous = () => {
  currentIndex.value = currentIndex.value === 0
    ? props.slides.length - 1
    : currentIndex.value - 1
  emit('change', currentIndex.value)
}

const goTo = (index) => {
  currentIndex.value = index
  emit('change', currentIndex.value)
}

const startAutoplay = () => {
  if (props.autoplay && props.slides.length > 1) {
    autoplayInterval.value = setInterval(next, props.interval)
  }
}

const pause = () => {
  if (autoplayInterval.value) {
    clearInterval(autoplayInterval.value)
    autoplayInterval.value = null
  }
}

const resume = () => {
  startAutoplay()
}

// Touch handling
let touchStartX = 0
let touchEndX = 0

const handleTouchStart = (e) => {
  touchStartX = e.touches[0].clientX
}

const handleTouchMove = (e) => {
  touchEndX = e.touches[0].clientX
}

const handleTouchEnd = () => {
  const diff = touchStartX - touchEndX
  if (Math.abs(diff) > 50) { // Minimum swipe distance
    if (diff > 0) {
      next()
    } else {
      previous()
    }
  }
}

// Lifecycle
onMounted(() => {
  startAutoplay()
  
  // Add touch event listeners
  if (container.value) {
    container.value.addEventListener('touchstart', handleTouchStart)
    container.value.addEventListener('touchmove', handleTouchMove)
    container.value.addEventListener('touchend', handleTouchEnd)
  }
})

onBeforeUnmount(() => {
  pause()
  
  // Remove touch event listeners
  if (container.value) {
    container.value.removeEventListener('touchstart', handleTouchStart)
    container.value.removeEventListener('touchmove', handleTouchMove)
    container.value.removeEventListener('touchend', handleTouchEnd)
  }
})
</script>

<style scoped>
/* Optional: Add fade transition for slides */
.slide-fade-enter-active,
.slide-fade-leave-active {
  @apply transition-opacity duration-300;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  @apply opacity-0;
}

/* Optional: Add scale animation for active indicator */
.indicator-scale {
  @apply transition-transform duration-200;
}

.indicator-scale.active {
  @apply transform scale-125;
}

/* Optional: Add hover effect for navigation arrows */
.nav-arrow {
  @apply transition-all duration-200;
}

.nav-arrow:hover {
  @apply bg-opacity-75 transform scale-110;
}

/* Optional: Add gradient overlay for captions */
.caption-gradient {
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0) 100%
  );
}

/* Optional: Add loading state */
.carousel-loading {
  @apply animate-pulse bg-gray-200;
}

/* Optional: Add focus styles */
.carousel-focus {
  @apply focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2;
}
</style>
