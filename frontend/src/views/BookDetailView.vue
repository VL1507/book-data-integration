<template>
  <div class="book-detail">
    <div class="back-nav">
      <router-link to="/books" class="back-link">← Назад к каталогу</router-link>
    </div>

    <div v-if="loading" class="loading">Загрузка информации о книге...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="book" class="book-content">
      <!-- Основная информация о книге -->
      <div class="book-header">
        <div class="main-cover" v-if="mainCoverUrl">
          <img
            :src="mainCoverUrl"
            :alt="book.title"
            @error="handleImageError"
            @load="handleImageLoad"
            :class="{ loaded: imageLoaded, error: imageError }"
          />
          <div v-if="imageError" class="image-placeholder error">Обложка недоступна</div>
        </div>

        <div class="book-main-info">
          <h1 class="book-title">{{ book.title }}</h1>

          <div class="book-authors" v-if="book.authors?.length">
            {{ book.authors.length > 1 ? 'Авторы' : 'Автор' }}:
            <span>{{ book.authors.join(', ') }}</span>
          </div>

          <div class="book-genres" v-if="book.genres?.length">
            Жанр{{ book.genres.length > 1 ? 'ы' : '' }}:
            <span v-for="(genre, i) in book.genres" :key="genre">
              {{ genre }}{{ i < book.genres.length - 1 ? ', ' : '' }}
            </span>
          </div>

          <div class="book-isbn" v-if="book.isbn?.length">ISBN: {{ book.isbn.join(' • ') }}</div>

          <div class="book-annotation" v-if="book.annotation">
            <h3>Аннотация</h3>
            <!-- <p>{{ book.annotation }}</p> -->
            <p>{{ shortAnnotation }}</p>
          </div>
        </div>
      </div>

      <!-- Блок изданий -->
      <div class="editions-section" v-if="book.publication_site_info?.length">
        <h2>Издания и где доступно</h2>

        <div class="editions-list">
          <div
            v-for="(site, index) in book.publication_site_info"
            :key="index"
            class="edition-item"
          >
            <div class="edition-cover" v-if="site.image_url">
              <img :src="site.image_url" :alt="`Обложка — ${site.site_name}`" />
            </div>
            <div v-else class="edition-cover placeholder">Нет обложки</div>

            <div class="edition-details">
              <h3 class="edition-site-name">
                <a :href="`https://${site.site_url}`" target="_blank" rel="noopener noreferrer">
                  {{ site.site_name }}
                </a>
              </h3>

              <div class="edition-meta">
                <div v-if="site.year">Год издания: {{ site.year }}</div>
                <div v-if="site.page_count">Страниц: {{ site.page_count }}</div>
                <div v-if="site.price">Цена: {{ formatPrice(site.price) }}</div>

                <div v-if="site.dim_x || site.dim_y" class="dimensions">
                  Формат: {{ formatDimensions(site.dim_x, site.dim_y, site.dim_z) }}
                </div>

                <div v-if="site.illustration_type || site.coverages_type" class="types">
                  <span v-if="site.illustration_type"
                    >Иллюстрации: {{ site.illustration_type }}</span
                  >
                  <span v-if="site.coverages_type">Переплёт: {{ site.coverages_type }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="goBack" class="btn btn-secondary">← Назад</button>
        <router-link to="/books" class="btn btn-primary">К каталогу</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
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

const MAX_ANNOTATION_LENGTH = 1300 // подбери под дизайн
const shortAnnotation = computed(() => {
  if (!book.value?.annotation) return ''
  const text = book.value.annotation.trim()

  const dotIndex = text.lastIndexOf('.')

  if (dotIndex >= 0) {
    return text.slice(0, dotIndex + 1) + '…'
  }

  // запасной вариант — просто по длине
  return text.slice(0, MAX_ANNOTATION_LENGTH).replace(/[.,!?;]$/, '') + '…'
})

const bookId = computed(() => Number(route.params.publication_id))

const mainCoverUrl = computed(() => {
  if (!book.value?.publication_site_info?.length) return ''
  const withImage = book.value.publication_site_info.find((s) => s.image_url)
  return withImage?.image_url || ''
})

const formatPrice = (price: number | undefined) =>
  price ? `${price.toLocaleString('ru-RU')} ₽` : '—'

const formatDimensions = (x?: number, y?: number, z?: number) => {
  if (!x || !y) return '—'
  let str = `${x}×${y} мм`
  if (z) str += `×${z} мм`
  return str
}

const loadBook = async () => {
  loading.value = true
  error.value = ''
  imageLoaded.value = false
  imageError.value = false

  try {
    const data = await bookApi.getBook(bookId.value)
    book.value = data
  } catch (err: any) {
    error.value = err.response?.status === 404 ? 'Книга не найдена' : 'Ошибка загрузки данных книги'
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
const goBack = () => router.back()

onMounted(loadBook)

watch(
  () => route.params.publication_id,
  () => {
    if (route.params.publication_id) loadBook()
  },
  { immediate: true },
)
</script>

<style scoped>
.book-detail {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
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

/* ── Основной блок книги ── */
.book-header {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2.5rem;
  margin-bottom: 3rem;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
}

.main-cover {
  position: relative;
  height: 480px;
  background: #f9fafb;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.main-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-main-info {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.book-title {
  margin: 0;
  font-size: 2.4rem;
  line-height: 1.15;
  color: #111827;
}

.book-authors {
  font-size: 1.25rem;
  color: #4f46e5;
  font-weight: 500;
}

.book-genres {
  font-size: 1.05rem;
  color: #6b7280;
}

.book-isbn {
  font-size: 0.95rem;
  color: #6b7280;
  font-family: monospace;
}

.book-annotation {
  margin-top: 1.5rem;
  line-height: 1.65;
  color: #374151;
}

.book-annotation h3 {
  margin: 0 0 0.8rem 0;
  font-size: 1.2rem;
  color: #1f2937;
}

/* ── Блок изданий ── */
.editions-section {
  margin-top: 3rem;
}

.editions-section h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.6rem;
  color: #111827;
}

.editions-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.edition-item {
  display: flex;
  gap: 1.25rem;
  padding: 1.25rem;
  background: #f9fafb;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  transition: all 0.15s;
}

.edition-item:hover {
  background: white;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
}

.edition-cover {
  width: 120px;
  height: 170px;
  flex-shrink: 0;
  border-radius: 6px;
  overflow: hidden;
  background: #e5e7eb;
}

.edition-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.edition-cover.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  color: #9ca3af;
  background: #f3f4f6;
}

.edition-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.edition-site-name {
  margin: 0;
  font-size: 1.25rem;
}

.edition-site-name a {
  color: #2563eb;
  text-decoration: none;
}

.edition-site-name a:hover {
  text-decoration: underline;
}

.edition-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem 2rem;
  font-size: 0.95rem;
  color: #4b5563;
}

.edition-meta > div {
  min-width: 120px;
}

.dimensions,
.types {
  color: #6b7280;
  font-size: 0.92rem;
}

/* кнопки */
.action-buttons {
  margin-top: 2.5rem;
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: #4f46e5;
  color: white;
}

.btn-primary:hover {
  background: #4338ca;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}

/* адаптив */
@media (max-width: 900px) {
  .book-header {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .main-cover {
    height: 420px;
    max-width: 340px;
    margin: 0 auto;
  }
}

@media (max-width: 600px) {
  .edition-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .edition-meta {
    justify-content: center;
  }
}
</style>
