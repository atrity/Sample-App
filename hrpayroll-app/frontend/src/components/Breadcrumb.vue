<template>
  <nav class="flex" aria-label="Breadcrumb">
    <ol class="flex items-center space-x-2">
      <!-- Home Link -->
      <li>
        <div>
          <router-link
            to="/"
            class="text-gray-400 hover:text-gray-500"
            :class="{ 'cursor-default': disableHome }"
            @click="disableHome && $event.preventDefault()"
          >
            <i class="fas fa-home text-gray-400"></i>
            <span class="sr-only">Home</span>
          </router-link>
        </div>
      </li>

      <!-- Breadcrumb Items -->
      <template v-for="(item, index) in items" :key="index">
        <!-- Separator -->
        <li class="flex items-center">
          <i
            :class="[
              'fas fa-chevron-right text-gray-300',
              separatorClass
            ]"
          ></i>
        </li>

        <!-- Item -->
        <li :class="{ 'truncate': truncate }">
          <template v-if="index === items.length - 1">
            <!-- Current Page (Last Item) -->
            <span
              class="text-gray-700 font-medium"
              :class="activeClass"
            >
              <slot :name="`item-${index}`" :item="item">
                {{ item.label }}
              </slot>
            </span>
          </template>
          <template v-else>
            <!-- Link -->
            <router-link
              v-if="item.to"
              :to="item.to"
              class="text-gray-500 hover:text-gray-700"
              :class="itemClass"
            >
              <slot :name="`item-${index}`" :item="item">
                {{ item.label }}
              </slot>
            </router-link>
            <!-- Text Only -->
            <span
              v-else
              class="text-gray-500"
              :class="itemClass"
            >
              <slot :name="`item-${index}`" :item="item">
                {{ item.label }}
              </slot>
            </span>
          </template>
        </li>
      </template>
    </ol>

    <!-- Actions Slot -->
    <div v-if="$slots.actions" class="ml-auto">
      <slot name="actions"></slot>
    </div>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    validator: (items) => {
      return items.every(item => 
        typeof item === 'object' && 
        'label' in item &&
        (!('to' in item) || typeof item.to === 'string' || typeof item.to === 'object')
      )
    }
  },
  disableHome: {
    type: Boolean,
    default: false
  },
  truncate: {
    type: Boolean,
    default: false
  },
  separatorClass: {
    type: String,
    default: 'mx-2'
  },
  itemClass: {
    type: String,
    default: ''
  },
  activeClass: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
/* Optional: Add custom separator styles */
.custom-separator {
  @apply mx-2 text-gray-400;
}

/* Optional: Add hover effect for links */
.breadcrumb-link {
  @apply transition-colors duration-200;
}

.breadcrumb-link:hover {
  @apply text-primary-600;
}

/* Optional: Add truncation styles */
.truncate {
  @apply max-w-xs;
}

/* Optional: Add responsive styles */
@media (max-width: 640px) {
  .truncate {
    @apply max-w-[150px];
  }
}
</style>
