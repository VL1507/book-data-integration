<template>
  <div class="books-view">
    <div class="page-header">
      <h1>Каталог книг</h1>
      <p>Найдите свою следующую любимую книгу</p>
    </div>

    <BookFilter
      :filters="filters"
      :loading="loading"
      @update:filters="updateFilters"
      @reset="resetFilters"
      @apply="applyFilters"
    />

    <div v-if="loading && books.length === 0" class="loading">
      <div class="spinner"></div>
      <p>Поиск книг...</p>
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="books.length === 0" class="no-results">
      <div class="no-results-icon">📚</div>
      <h3>Книги не найдены</h3>
      <p>Попробуйте изменить параметры поиска или сбросить фильтры</p>
      <button @click="resetFilters" class="btn-primary">Сбросить фильтры</button>
    </div>

    <div v-else>
      <!-- <div class="books-header">
        <div class="books-stats">
          Найдено книг: <strong>{{ books.length }}</strong>
          <span v-if="hasMore" class="more-available">(есть еще)</span>
        </div>
        <div class="sort-controls" v-if="books.length > 0">
          <label>Сортировка:</label>
          <select v-model="sortBy" @change="applySorting" class="sort-select">
            <option value="title">По названию</option>
            <option value="year">По году</option>
          </select>
        </div>
      </div> -->

      <div class="books-grid">
        <BookCard v-for="book in sortedBooks" :key="book.publication_id" :book="book" />
      </div>

      <div class="pagination" v-if="hasMore">
        <button @click="loadMore" class="load-more-btn" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Загрузить еще' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import BookCard from '@/components/BookCard.vue'
import BookFilter from '@/components/BookFilter.vue'
import { bookApi } from '@/services/api'
import type { Book, BookFilters } from '@/types/book'

const books = ref<Book[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const sortBy = ref<'title' | 'year' | 'author' | null>(null)
const appliedFilters = ref<BookFilters>({})

const filters = ref<BookFilters>({
  limit: 10,
  offset: 0,
})

const hasMore = computed(() => {
  return books.value.length >= (filters.value.limit || 10)
})

const sortedBooks = computed(() => {
  const sorted = [...books.value]

  switch (sortBy.value) {
    case 'title':
      return sorted.sort((a, b) => a.title.localeCompare(b.title))
    case 'year':
      return sorted.sort((a, b) => Math.min(...b.years) - Math.min(...a.years))
    default:
      return sorted
  }
})

const applyFilters = async () => {
  appliedFilters.value = { ...filters.value }
  await loadBooks(true)
}

const updateFilters = (newFilters: BookFilters) => {
  if (typeof newFilters.year_from !== 'undefined' && newFilters.year_from < 1000) {
    newFilters.year_from = 1000
  }
  filters.value = { ...newFilters }
}

const resetFilters = async () => {
  filters.value = { limit: 10, offset: 0 }
  appliedFilters.value = { limit: 10, offset: 0 }
  await loadBooks(true)
}

const loadBooks = async (reset: boolean = false) => {
  if (reset) {
    filters.value.offset = 0
  }

  loading.value = true
  error.value = null

  try {
    const newBooks = await bookApi.getBooks(appliedFilters.value)

    if (reset) {
      books.value = newBooks
    } else {
      books.value = [...books.value, ...newBooks]
    }
  } catch (err) {
    // error.value = 'Ошибка при загрузке книг'
    console.error('Ошибка:', err)
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  if (!hasMore.value) return

  filters.value.offset = books.value.length
  appliedFilters.value.offset = books.value.length
  await loadBooks(false)
}

// const applySorting = () => {
// }

onMounted(async () => {
  await loadBooks(true)
})
</script>

<style scoped>
.books-view {
  max-width: 100%;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.page-header p {
  font-size: 1.1rem;
  color: #666;
}

.loading {
  text-align: center;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error {
  background: #fee;
  color: #c33;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 1rem 0;
  border: 1px solid #fcc;
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.no-results p {
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.books-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 2rem 0;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.books-stats {
  font-size: 1rem;
  color: #555;
}

.more-available {
  color: #667eea;
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-controls label {
  font-size: 0.9rem;
  color: #555;
  font-weight: 500;
}

.sort-select {
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: white;
  font-size: 0.9rem;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.pagination {
  text-align: center;
  margin-top: 3rem;
}

.load-more-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 150px;
}

.load-more-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.load-more-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@media (max-width: 768px) {
  .books-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .sort-controls {
    justify-content: space-between;
  }
}
</style>
