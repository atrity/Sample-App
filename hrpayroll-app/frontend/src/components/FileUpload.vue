<template>
  <div class="space-y-4">
    <!-- Upload Area -->
    <div
      class="relative border-2 border-dashed rounded-lg p-6"
      :class="[
        isDragging ? 'border-primary-500 bg-primary-50' : 'border-gray-300',
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-primary-400'
      ]"
      @dragenter.prevent="handleDragEnter"
      @dragleave.prevent="handleDragLeave"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="!disabled && triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        class="hidden"
        :accept="accept"
        :multiple="multiple"
        :disabled="disabled"
        @change="handleFileSelect"
      >

      <div class="text-center">
        <i class="fas fa-cloud-upload-alt text-4xl text-gray-400 mb-3"></i>
        <div class="text-sm text-gray-600">
          <label class="relative cursor-pointer rounded-md font-medium text-primary-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2 hover:text-primary-500">
            <span>Upload files</span>
          </label>
          <span class="pl-1">or drag and drop</span>
        </div>
        <p class="text-xs text-gray-500 mt-2">
          {{ acceptedFileTypes }}
        </p>
        <p v-if="maxSize" class="text-xs text-gray-500">
          Max file size: {{ formatSize(maxSize) }}
        </p>
      </div>
    </div>

    <!-- Error Message -->
    <p v-if="errorMessage" class="text-sm text-red-600">
      {{ errorMessage }}
    </p>

    <!-- File List -->
    <div v-if="files.length > 0" class="space-y-2">
      <div
        v-for="(file, index) in files"
        :key="index"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
      >
        <!-- File Info -->
        <div class="flex items-center space-x-3">
          <!-- Preview -->
          <div v-if="file.preview" class="h-10 w-10 flex-shrink-0">
            <img
              :src="file.preview"
              class="h-10 w-10 rounded object-cover"
              alt="File preview"
            />
          </div>
          <div v-else class="h-10 w-10 flex-shrink-0 flex items-center justify-center bg-gray-100 rounded">
            <i :class="getFileIcon(file)" class="text-gray-400"></i>
          </div>

          <!-- File Details -->
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ file.name }}
            </p>
            <p class="text-xs text-gray-500">
              {{ formatSize(file.size) }}
            </p>
          </div>

          <!-- Progress -->
          <div v-if="file.progress !== undefined" class="ml-4 flex-shrink-0">
            <div class="w-20">
              <div class="bg-gray-200 rounded-full h-2">
                <div
                  class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${file.progress}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="ml-4 flex-shrink-0">
          <button
            type="button"
            class="text-gray-400 hover:text-gray-500"
            @click.stop="removeFile(index)"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  accept: {
    type: String,
    default: '*'
  },
  multiple: {
    type: Boolean,
    default: false
  },
  maxSize: {
    type: Number,
    default: 0 // in bytes, 0 means no limit
  },
  maxFiles: {
    type: Number,
    default: 0 // 0 means no limit
  },
  disabled: {
    type: Boolean,
    default: false
  },
  preview: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'error'])

// State
const fileInput = ref(null)
const isDragging = ref(false)
const files = ref([])
const errorMessage = ref('')

// Computed
const acceptedFileTypes = computed(() => {
  if (props.accept === '*') return 'All file types accepted'
  return `Accepted file types: ${props.accept}`
})

// Methods
const triggerFileInput = () => {
  if (!props.disabled) {
    fileInput.value.click()
  }
}

const handleDragEnter = () => {
  if (!props.disabled) {
    isDragging.value = true
  }
}

const handleDragLeave = () => {
  isDragging.value = false
}

const validateFiles = (fileList) => {
  const validFiles = []
  errorMessage.value = ''

  for (const file of fileList) {
    // Check file type
    if (props.accept !== '*' && !file.type.match(props.accept)) {
      errorMessage.value = `File type not accepted: ${file.name}`
      continue
    }

    // Check file size
    if (props.maxSize > 0 && file.size > props.maxSize) {
      errorMessage.value = `File too large: ${file.name}`
      continue
    }

    validFiles.push(file)
  }

  // Check max files
  if (props.maxFiles > 0 && files.value.length + validFiles.length > props.maxFiles) {
    errorMessage.value = `Maximum ${props.maxFiles} files allowed`
    return []
  }

  return validFiles
}

const processFiles = async (fileList) => {
  const validFiles = validateFiles(fileList)
  if (!validFiles.length) return

  const processedFiles = await Promise.all(
    validFiles.map(async (file) => {
      const processedFile = {
        file,
        name: file.name,
        size: file.size,
        type: file.type,
        progress: 0
      }

      if (props.preview && file.type.startsWith('image/')) {
        processedFile.preview = await readFileAsDataURL(file)
      }

      return processedFile
    })
  )

  files.value = [...files.value, ...processedFiles]
  emit('update:modelValue', files.value.map(f => f.file))
}

const handleFileSelect = (event) => {
  const fileList = Array.from(event.target.files)
  processFiles(fileList)
  event.target.value = null // Reset input
}

const handleDrop = (event) => {
  isDragging.value = false
  const fileList = Array.from(event.dataTransfer.files)
  processFiles(fileList)
}

const removeFile = (index) => {
  files.value.splice(index, 1)
  emit('update:modelValue', files.value.map(f => f.file))
}

const readFileAsDataURL = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.readAsDataURL(file)
  })
}

const getFileIcon = (file) => {
  const icons = {
    'image/': 'fas fa-image',
    'video/': 'fas fa-video',
    'audio/': 'fas fa-music',
    'application/pdf': 'fas fa-file-pdf',
    'application/msword': 'fas fa-file-word',
    'application/vnd.ms-excel': 'fas fa-file-excel',
    'text/': 'fas fa-file-alt'
  }

  for (const [type, icon] of Object.entries(icons)) {
    if (file.type.startsWith(type)) return icon
  }

  return 'fas fa-file'
}

const formatSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}
</script>

<style scoped>
.upload-area {
  @apply transition-all duration-200;
}

.upload-area:hover {
  @apply border-primary-400;
}

.file-preview {
  @apply transition-all duration-200;
}

.file-preview:hover {
  @apply opacity-75;
}
</style>
