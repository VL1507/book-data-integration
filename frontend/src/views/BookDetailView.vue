<template>
  <div class="book-detail">
    <div class="back-nav">
      <router-link to="/books" class="back-link"> ← Назад к каталогу </router-link>
    </div>

    <div v-if="loading" class="loading">Загрузка информации о книге...</div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="book" class="book-content">
      <div class="book-layout">
        <div class="book-cover">
          <img
            :src="book.image_url"
            :alt="book.title"
            @error="handleImageError"
            @load="handleImageLoad"
            :class="{ loaded: imageLoaded, error: imageError }"
          />
          <div v-if="!imageLoaded && !imageError" class="image-placeholder">
            📖 Загрузка обложки...
          </div>
          <div v-if="imageError" class="image-placeholder error">❌ Обложка недоступна</div>
        </div>

        <div class="book-info">
          <h1 class="book-title">{{ book.title }}</h1>
          <p class="book-author">Автор: {{ book.authors }}</p>

          <div class="book-meta-grid">
            <div class="meta-item">
              <strong>Год издания:</strong>
              <span>{{ book.years }}</span>
            </div>
            <div class="meta-item">
              <strong>Жанр:</strong>
              <span>{{ book.genres }}</span>
            </div>
            <div class="meta-item">
              <strong>ID:</strong>
              <span>{{ book.publication_id }}</span>
            </div>
          </div>

          <!-- <div class="book-description">
            <h3>Описание</h3>
            <p>{{ book.description }}</p>
          </div> -->

          <div class="action-buttons">
            <button @click="goBack" class="btn btn-secondary">← Назад</button>
            <router-link to="/books" class="btn btn-primary"> К каталогу </router-link>
          </div>
        </div>
      </div>

      <!-- <div class="related-books" v-if="relatedBooks.length > 0">
        <h2>Похожие книги</h2>
        <div class="related-grid">
          <BookCard
            v-for="relatedBook in relatedBooks"
            :key="relatedBook.id"
            :book="relatedBook"
            @click="goToBook(relatedBook.id)"
          />
        </div>
      </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// import BookCard from '@/components/BookCard.vue'
import { bookApi } from '@/services/api'
import type { BookFull } from '@/types/book'

const route = useRoute()
const router = useRouter()

const book = ref<BookFull | null>(null)
// const relatedBooks = ref<Book[]>([])
const loading = ref(false)
const error = ref<string>('')
const imageLoaded = ref(false)
const imageError = ref(false)

const bookId = computed(() => parseInt(route.params.publication_id as string))

// const coverUrl = computed(() => {
//   if (!book.value) return ''
//   return book.value.image_url
// })

const loadBook = async () => {
  loading.value = true
  error.value = ''
  imageLoaded.value = false
  imageError.value = false

  try {
    // Загружаем информацию о книге
    book.value = await bookApi.getBook(bookId.value)

    // Загружаем похожие книги (того же жанра)
    // const allBooks = await bookApi.getBooks()
    // relatedBooks.value = allBooks
    //   .filter((b) => b.id !== book.value!.id && b.genres === book.value!.genres)
    //   .slice(0, 3)
  } catch (err: any) {
    console.error('Ошибка загрузки книги:', err)
    error.value =
      err.response?.status === 404 ? 'Книга не найдена' : 'Ошибка при загрузке информации о книге'
  } finally {
    loading.value = false
  }
}

const handleImageError = (event: Event) => {
  console.error(
    `Ошибка загрузки обложки для книги ${book.value?.publication_id}:`,
    book.value?.image_url,
  )
  imageError.value = true
  imageLoaded.value = false

  const target = event.target as HTMLImageElement
  target.style.display = 'none'
}

const handleImageLoad = () => {
  imageLoaded.value = true
  imageError.value = false
}

// const goToBook = (id: number) => {
//   router.push(`/books/${id}`)
// }

const goBack = () => {
  router.back()
}

// Загружаем книгу при монтировании
onMounted(() => {
  loadBook()
})

// Реагируем на изменение ID в URL
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      loadBook()
    }
  },
)
</script>

<style scoped>
.book-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.back-nav {
  margin-bottom: 2rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.back-link:hover {
  color: #5a67d8;
}

.loading,
.error {
  text-align: center;
  padding: 3rem;
  font-size: 1.1rem;
}

.error {
  background: #fee;
  color: #c33;
  border-radius: 8px;
  border: 1px solid #fcc;
}

.book-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.book-layout {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 3rem;
  padding: 3rem;
}

.book-cover {
  width: 100%;
  height: 500px;
  position: relative;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.book-cover img.error {
  display: none;
}

.image-placeholder {
  color: #666;
  font-size: 1.2rem;
  text-align: center;
  padding: 2rem;
}

.image-placeholder.error {
  color: #dc3545;
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.book-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  line-height: 1.2;
  margin: 0;
}

.book-author {
  font-size: 1.3rem;
  color: #667eea;
  font-weight: 500;
  margin: 0;
}

.book-meta-grid {
  display: grid;
  gap: 1rem;
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e9ecef;
}

.meta-item:last-child {
  border-bottom: none;
}

.meta-item strong {
  color: #555;
}

.meta-item span {
  color: #333;
  font-weight: 500;
}

.book-description h3 {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 1rem;
}

.book-description p {
  line-height: 1.7;
  color: #555;
  font-size: 1.1rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: auto;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(108, 117, 125, 0.4);
}

.related-books {
  padding: 3rem;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.related-books h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

@media (max-width: 968px) {
  .book-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
    padding: 2rem;
  }

  .book-cover {
    height: 400px;
    max-width: 300px;
    margin: 0 auto;
  }

  .book-title {
    font-size: 2rem;
    text-align: center;
  }

  .book-author {
    text-align: center;
  }
}

@media (max-width: 768px) {
  .book-detail {
    padding: 1rem;
  }

  .book-layout {
    padding: 1.5rem;
  }

  .related-books {
    padding: 2rem 1.5rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    text-align: center;
  }
}
</style>
