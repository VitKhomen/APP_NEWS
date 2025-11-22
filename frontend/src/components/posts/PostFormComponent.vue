<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Заголовок -->
    <div>
      <label class="block text-sm font-medium text-gray-700">
        Заголовок <span class="text-red-500">*</span>
      </label>
      <input
        v-model="formData.title"
        type="text"
        required
        class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
        placeholder="Введите заголовок..."
      />
    </div>

    <!-- Категория -->
    <div>
      <label class="block text-sm font-medium text-gray-700">Категория</label>
      <select
        v-model="formData.category"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="">Выберите категорию</option>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
    </div>

    <!-- Изображение -->
    <div>
      <label class="block text-sm font-medium text-gray-700">Изображение</label>
      
      <!-- Превью -->
      <div v-if="imagePreview" class="mb-3">
        <img :src="imagePreview" class="w-full max-w-md h-48 object-cover rounded-md" />
        <button type="button" @click="removeImage" class="text-red-600 text-sm mt-2">
          Удалить изображение
        </button>
      </div>
      
      <!-- Загрузка -->
      <input
        type="file"
        accept="image/*"
        @change="handleImageChange"
        class="block w-full text-sm text-gray-500"
      />
    </div>

    <!-- Содержимое -->
    <div>
      <label class="block text-sm font-medium text-gray-700">
        Содержимое <span class="text-red-500">*</span>
      </label>
      <textarea
        v-model="formData.content"
        required
        rows="10"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
        placeholder="Напишите текст статьи..."
      ></textarea>
    </div>

    <!-- Статус -->
    <div>
      <label class="block text-sm font-medium text-gray-700">Статус</label>
      <select
        v-model="formData.status"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md"
      >
        <option value="published">Опубликовать</option>
        <option value="draft">Черновик</option>
      </select>
    </div>

    <!-- Кнопки -->
    <div class="flex justify-end space-x-3">
      <button
        type="button"
        @click="$emit('cancel')"
        class="py-2 px-4 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
      >
        Отмена
      </button>
      <button
        type="submit"
        :disabled="isSubmitting"
        class="py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {{ isSubmitting ? 'Сохранение...' : (isEditing ? 'Обновить' : 'Создать') }}
      </button>
    </div>
  </form>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { usePostsStore } from '@/stores/posts'

export default {
  name: 'PostFormComponent',
  props: {
    initialData: {
      type: Object,
      default: null
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const postsStore = usePostsStore()
    const isSubmitting = ref(false)
    const imagePreview = ref(null)
    const imageFile = ref(null)
    
    const formData = reactive({
      title: '',
      content: '',
      category: '',
      status: 'published'
    })
    
    const categories = computed(() => postsStore.categories)
    
    // Инициализация данных при редактировании
    onMounted(() => {
      if (props.initialData) {
        formData.title = props.initialData.title || ''
        formData.content = props.initialData.content || ''
        formData.category = props.initialData.category || ''
        formData.status = props.initialData.status || 'published'
        
        if (props.initialData.image) {
          imagePreview.value = props.initialData.image
        }
      }
      
      // Загружаем категории если их нет
      if (categories.value.length === 0) {
        postsStore.fetchCategories()
      }
    })
    
    const handleImageChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 10 * 1024 * 1024) {
          alert('Размер файла не должен превышать 10MB')
          return
        }
        
        imageFile.value = file
        
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const removeImage = () => {
      imagePreview.value = null
      imageFile.value = null
    }
    
    const handleSubmit = async () => {
      if (!formData.title.trim() || !formData.content.trim()) {
        alert('Заполните обязательные поля')
        return
      }
      
      isSubmitting.value = true
      
      try {
        // Создаем FormData если есть изображение
        let submitData
        if (imageFile.value) {
          submitData = new FormData()
          submitData.append('title', formData.title.trim())
          submitData.append('content', formData.content.trim())
          submitData.append('status', formData.status)
          
          if (formData.category) {
            submitData.append('category', formData.category)
          }
          
          submitData.append('image', imageFile.value)
        } else {
          submitData = {
            title: formData.title.trim(),
            content: formData.content.trim(),
            status: formData.status
          }
          
          if (formData.category) {
            submitData.category = formData.category
          }
        }
        
        emit('submit', submitData)
      } catch (error) {
        console.error('Ошибка отправки формы:', error)
      } finally {
        isSubmitting.value = false
      }
    }
    
    return {
      formData,
      categories,
      isSubmitting,
      imagePreview,
      handleImageChange,
      removeImage,
      handleSubmit
    }
  }
}
</script>