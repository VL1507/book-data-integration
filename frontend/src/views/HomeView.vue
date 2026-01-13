<template>
  <div class="home">
    <DebugInfo />

    <div class="hero-section">
      <h1>Добро пожаловать в BookStore</h1>
      <p>Откройте для себя мир удивительных книг</p>
      <router-link to="/books" class="cta-button"> Смотреть все книги </router-link>
    </div>

    <div class="featured-books">
      <h2>Популярные книги</h2>
      <div v-if="loading" class="loading">Загрузка книг...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="books-grid">
        <BookCard
          v-for="book in featuredBooks"
          :key="book.id"
          :book="book"
          @click="openBookModal(book)"
        />
      </div>
    </div>

    <BookModal v-if="selectedBook" :book="selectedBook" @close="selectedBook = null" />
  </div>
</template>

<!-- ----------------------------------------------------------------------------------------------------------------------------- -->
<!-- ----------------------------------------------------------------------------------------------------------------------------- -->
<!-- ----------------------------------------------------------------------------------------------------------------------------- -->

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BookCard from '@/components/BookCard.vue'
import DebugInfo from '@/components/DebugInfo.vue'
import { bookApi } from '@/services/api'
import type { Book } from '@/types/book'

const featuredBooks = ref<Book[]>([])
const loading = ref(false)
const error = ref<string>('')

const loadFeaturedBooks = async () => {
  loading.value = true
  error.value = ''

  try {
    featuredBooks.value = await bookApi.getBooks({ limit: 3 })
  } catch (err) {
    console.error('Ошибка при загрузке книг:', err)
    error.value = 'Не удалось загрузить книги. Проверьте подключение к бэкенду.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadFeaturedBooks()
})
</script>

<!-- ----------------------------------------------------------------------------------------------------------------------------- -->
<!-- ----------------------------------------------------------------------------------------------------------------------------- -->
<!-- ----------------------------------------------------------------------------------------------------------------------------- -->

<style scoped>
.home {
  max-width: 100%;
}

.hero-section {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  margin-bottom: 3rem;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  display: inline-block;
  background: white;
  color: #667eea;
  padding: 12px 30px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.featured-books h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
  color: #333;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}
</style>
