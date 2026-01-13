<template>
  <div class="book-detail">
    <div class="back-nav">
      <router-link to="/books" class="back-link"> ← Назад к каталогу</router-link>
    </div>

    <div v-if="loading" class="loading">Загрузка информации о книге...</div>

    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="book" class="book-content">
      <div class="book-layout">
        <!-- Левая часть — основная обложка (берём первую) -->
        <div class="book-cover">
          <img
            v-if="mainCover"
            :src="mainCover"
            :alt="book.title"
            @error="handleImageError"
            @load="handleImageLoad"
            :class="{ loaded: imageLoaded, error: imageError }"
          />
          <div v-else-if="!imageLoaded && !imageError" class="image-placeholder">
            📖 Загрузка обложки...
          </div>
          <div v-if="imageError || !mainCover" class="image-placeholder error">
            ❌ Обложка недоступна
          </div>
        </div>

        <div class="book-info">
          <h1 class="book-title">{{ book.title }}</h1>

          <p class="book-author">
            {{ book.authors.length ? book.authors.join(', ') : 'Автор не указан' }}
          </p>

          <div class="book-meta">
            <div class="meta-item">
              <strong>Жанр{{ book.genres.length > 1 ? 'ы' : '' }}:</strong>
              <span>{{ book.genres.join(', ') || '—' }}</span>
            </div>
            <div class="meta-item">
              <strong>ID публикации:</strong>
              <span>{{ book.publication_id }}</span>
            </div>
          </div>

          <div v-if="annotation" class="book-description">
            <h3>Аннотация</h3>
            <p>{{ annotation }}</p>
          </div>

          <!-- Блок изданий -->
          <div class="editions-section" v-if="book.publication_site_info.length">
            <h3>Доступные издания</h3>
            <div class="editions-list">
              <div
                v-for="(site, index) in book.publication_site_info"
                :key="index"
                class="edition-card"
              >
                <div class="edition-header">
                  <h4>{{ site.site_name }}</h4>
                  <span class="year">{{ site.year }}</span>
                </div>

                <div class="edition-meta">
                  <div>
                    Страниц: <strong>{{ site.page_count || '—' }}</strong>
                  </div>
                  <div>
                    Цена: <strong>{{ site.price ? site.price + ' ₽' : '—' }}</strong>
                  </div>
                  <div v-if="site.illustration_type">
                    Иллюстрации: <strong>{{ site.illustration_type }}</strong>
                  </div>
                  <div v-if="site.coverages_type">
                    Переплёт: <strong>{{ site.coverages_type }}</strong>
                  </div>
                  <div v-if="site.dim_x && site.dim_y">
                    Размер:
                    <strong
                      >{{ site.dim_x }} × {{ site.dim_y }}
                      {{ site.dim_z ? '× ' + site.dim_z : '' }} мм</strong
                    >
                  </div>
                </div>

                <a
                  v-if="site.site_url"
                  :href="site.site_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn btn-small btn-primary"
                >
                  Перейти на сайт
                </a>
              </div>
            </div>
          </div>

          <div class="action-buttons">
            <button @click="goBack" class="btn btn-secondary">← Назад</button>
            <router-link to="/books" class="btn btn-primary">К каталогу</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bookApi } from '@/services/api'
import type { BookFull } from '@/types/book'

const route = useRoute()
const router = useRouter()

const book = ref<BookFull | null>(null)
const loading = ref(true)
const error = ref('')
const imageLoaded = ref(false)
const imageError = ref(false)

const bookId = computed(() => Number(route.params.publication_id))

const mainCover = computed(() => {
  if (!book.value?.publication_site_info?.length) return ''
  // Берём первую обложку, либо можно выбрать самую свежую по году
  return book.value.publication_site_info[0].image_url || ''
})

const annotation = computed(() => book.value?.annotation || '')

const loadBook = async () => {
  loading.value = true
  error.value = ''
  imageLoaded.value = false
  imageError.value = false

  try {
    book.value = await bookApi.getBook(bookId.value)
    console.log('Book loaded:', book.value)
  } catch (err: any) {
    console.error('Ошибка загрузки книги:', err)
    error.value = err.response?.status === 404 ? 'Книга не найдена' : 'Ошибка при загрузке данных'
  } finally {
    loading.value = false
  }
}

const handleImageError = () => {
  imageError.value = true
  imageLoaded.value = false
}

const handleImageLoad = () => {
  imageLoaded.value = true
  imageError.value = false
}

const goBack = () => {
  router.back()
}

onMounted(loadBook)
</script>

<style scoped>
.book-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.back-nav {
  margin-bottom: 1.5rem;
}

.back-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}

.back-link:hover {
  text-decoration: underline;
}

.book-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 2.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
}

.book-cover {
  position: relative;
  height: 520px;
  background: #f8fafc;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

.book-title {
  font-size: 2.4rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.15;
}

.book-author {
  font-size: 1.35rem;
  color: #6366f1;
  margin: 0.25rem 0 1rem;
}

.book-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem 2rem;
  margin-bottom: 0.5rem;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-item strong {
  font-weight: 600;
  color: #1f2937;
}

.book-description {
  margin: 1.5rem 0;
  line-height: 1.65;
  color: #374151;
}

.editions-section {
  margin: 2rem 0;
}

.editions-section h3 {
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  color: #111827;
}

.editions-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.edition-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  transition: all 0.18s;
}

.edition-card:hover {
  border-color: #c7d2fe;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
  transform: translateY(-2px);
}

.edition-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.9rem;
}

.edition-header h4 {
  margin: 0;
  font-size: 1.25rem;
  color: #1e40af;
}

.year {
  font-size: 1.1rem;
  color: #4b5563;
  font-weight: 500;
}

.edition-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.8rem 1.5rem;
  margin-bottom: 1.2rem;
  font-size: 0.98rem;
  color: #4b5563;
}

.edition-meta strong {
  color: #111827;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn {
  padding: 0.75rem 1.6rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: #6366f1;
  color: white;
}

.btn-primary:hover {
  background: #4f46e5;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}

.btn-small {
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
}

.loading,
.error {
  text-align: center;
  padding: 4rem 1rem;
  font-size: 1.2rem;
}

.error {
  color: #dc2626;
  background: #fef2f2;
  border-radius: 12px;
}

@media (max-width: 992px) {
  .book-layout {
    grid-template-columns: 1fr;
    padding: 2rem;
  }
  .book-cover {
    height: 420px;
    max-width: 340px;
    margin: 0 auto;
  }
}

@media (max-width: 640px) {
  .book-title {
    font-size: 2rem;
  }
  .action-buttons {
    flex-direction: column;
  }
}
</style>
