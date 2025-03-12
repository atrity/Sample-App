<template>
  <div
    :class="[
      'flex',
      direction && `flex-${direction}`,
      wrap && 'flex-wrap',
      justify && `justify-${justify}`,
      items && `items-${items}`,
      content && `content-${content}`,
      gap && `gap-${gap}`,
      { 'flex-1': grow },
      { 'flex-shrink-0': !shrink },
      { 'inline-flex': inline },
      className
    ]"
  >
    <slot></slot>
  </div>
</template>

<script setup>
const props = defineProps({
  direction: {
    type: String,
    default: 'row',
    validator: (value) => [
      'row',
      'row-reverse',
      'col',
      'col-reverse'
    ].includes(value)
  },
  wrap: {
    type: Boolean,
    default: false
  },
  justify: {
    type: String,
    default: '',
    validator: (value) => [
      '',
      'start',
      'end',
      'center',
      'between',
      'around',
      'evenly'
    ].includes(value)
  },
  items: {
    type: String,
    default: '',
    validator: (value) => [
      '',
      'start',
      'end',
      'center',
      'baseline',
      'stretch'
    ].includes(value)
  },
  content: {
    type: String,
    default: '',
    validator: (value) => [
      '',
      'start',
      'end',
      'center',
      'between',
      'around',
      'evenly'
    ].includes(value)
  },
  gap: {
    type: [Number, String],
    default: ''
  },
  grow: {
    type: Boolean,
    default: false
  },
  shrink: {
    type: Boolean,
    default: true
  },
  inline: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
/* Optional: Add responsive flex direction */
@screen sm {
  .flex-responsive {
    @apply flex-row;
  }
}

@screen lg {
  .flex-responsive {
    @apply flex-col;
  }
}

/* Optional: Add flex container animations */
.flex-enter-active,
.flex-leave-active {
  @apply transition-all duration-300;
}

.flex-enter-from,
.flex-leave-to {
  @apply opacity-0;
}

/* Optional: Add gap responsive utilities */
.gap-responsive {
  @apply gap-2 sm:gap-4 lg:gap-6;
}

/* Optional: Add flex item animations */
.flex-item-enter-active,
.flex-item-leave-active {
  @apply transition-all duration-200;
}

.flex-item-enter-from,
.flex-item-leave-to {
  @apply opacity-0 transform scale-95;
}

/* Optional: Add flex order utilities */
.flex-order-first {
  @apply order-first;
}

.flex-order-last {
  @apply order-last;
}

/* Optional: Add flex basis utilities */
.flex-basis-auto {
  @apply basis-auto;
}

.flex-basis-full {
  @apply basis-full;
}

/* Optional: Add flex alignment self utilities */
.flex-self-auto {
  @apply self-auto;
}

.flex-self-start {
  @apply self-start;
}

.flex-self-end {
  @apply self-end;
}

.flex-self-center {
  @apply self-center;
}

.flex-self-stretch {
  @apply self-stretch;
}
</style>
