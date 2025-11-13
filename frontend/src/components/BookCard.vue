<template>
  <div class="book-card" @click="goToBookDetail">
    <div class="book-image">
      <img
        :src="coverUrl"
        :alt="book.title"
        @error="handleImageError"
        @load="handleImageLoad"
        :class="{ loaded: imageLoaded, error: imageError }"
      />
      <div v-if="!imageLoaded && !imageError" class="image-placeholder">📖 Загрузка...</div>
      <div v-if="imageError" class="image-placeholder error">❌ Нет обложки</div>
    </div>
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-author">{{ book.author }}</p>
      <div class="book-meta">
        <span class="book-year">{{ book.year }}</span>
        <span class="book-genre">{{ book.genre }}</span>
      </div>
      <p class="book-description">{{ truncatedDescription }}</p>
      <div class="book-link">
        <span class="link-text">Подробнее →</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { bookApi } from '@/services/api'
import type { Book } from '@/types/book'

interface Props {
  book: Book
}

const props = defineProps<Props>()
const router = useRouter()

const imageLoaded = ref(false)
const imageError = ref(false)

const coverUrl = computed(() => bookApi.getBookCoverUrl(props.book.id))

const truncatedDescription = computed(() => {
  const desc = props.book.description
  return desc.length > 100 ? desc.substring(0, 100) + '...' : desc
})

const handleImageError = (event: Event) => {
  console.error(
    `Ошибка загрузки изображения для книги ${props.book.id}:`,
    props.book.image_filename,
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

const goToBookDetail = () => {
  router.push(`/books/${props.book.id}`)
}
</script>

<style scoped>
.book-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  cursor: pointer;
  position: relative;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.book-card:hover .book-link .link-text {
  color: #667eea;
  transform: translateX(5px);
}

.book-image {
  width: 100%;
  height: 250px;
  overflow: hidden;
  position: relative;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.book-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.book-image img.loaded {
  display: block;
}

.book-image img.error {
  display: none;
}

.book-card:hover .book-image img {
  transform: scale(1.05);
}

.image-placeholder {
  color: #666;
  font-size: 1rem;
  text-align: center;
  padding: 1rem;
}

.image-placeholder.error {
  color: #dc3545;
}

.book-info {
  padding: 1.5rem;
}

.book-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
  line-height: 1.3;
}

.book-author {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.book-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.book-year {
  background: #f0f0f0;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  color: #666;
}

.book-genre {
  background: #e3f2fd;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  color: #1976d2;
}

.book-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.book-link {
  display: flex;
  justify-content: flex-end;
}

.link-text {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s;
}
</style>
