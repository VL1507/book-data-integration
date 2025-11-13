<template>
  <div class="book-filter">
    <div class="filter-header">
      <h3>Фильтры</h3>
      <div class="filter-actions">
        <button @click="applyFilters" class="apply-btn" :disabled="loading">
          {{ loading ? 'Поиск...' : 'Найти' }}
        </button>
        <button @click="resetFilters" class="reset-btn" :disabled="loading">Сбросить</button>
      </div>
    </div>

    <div class="filter-grid">
      <div class="filter-group">
        <label>Жанр</label>
        <input
          v-model="localFilters.genre"
          type="text"
          placeholder="Введите жанр..."
          @keyup.enter="applyFilters"
        />
      </div>

      <div class="filter-group">
        <label>Автор</label>
        <input
          v-model="localFilters.author"
          type="text"
          placeholder="Введите автора..."
          @keyup.enter="applyFilters"
        />
      </div>

      <div class="filter-group">
        <label>Год от</label>
        <input
          v-model="localFilters.year_from"
          type="number"
          placeholder="От"
          @keyup.enter="applyFilters"
        />
      </div>

      <div class="filter-group">
        <label>Год до</label>
        <input
          v-model="localFilters.year_to"
          type="number"
          placeholder="До"
          @keyup.enter="applyFilters"
        />
      </div>
    </div>

    <div class="active-filters" v-if="hasActiveFilters">
      <h4>Активные фильтры:</h4>
      <div class="filter-tags">
        <span v-if="localFilters.genre" class="filter-tag">
          Жанр: {{ localFilters.genre }}
          <button @click="removeFilter('genre')" class="remove-tag">×</button>
        </span>
        <span v-if="localFilters.author" class="filter-tag">
          Автор: {{ localFilters.author }}
          <button @click="removeFilter('author')" class="remove-tag">×</button>
        </span>
        <span v-if="localFilters.year_from" class="filter-tag">
          Год от: {{ localFilters.year_from }}
          <button @click="removeFilter('year_from')" class="remove-tag">×</button>
        </span>
        <span v-if="localFilters.year_to" class="filter-tag">
          Год до: {{ localFilters.year_to }}
          <button @click="removeFilter('year_to')" class="remove-tag">×</button>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { BookFilters } from '@/types/book'

interface Props {
  filters: BookFilters
  loading?: boolean
}

interface Emits {
  (e: 'update:filters', filters: BookFilters): void
  (e: 'reset'): void
  (e: 'apply'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const localFilters = ref<BookFilters>({ ...props.filters })

const hasActiveFilters = computed(() => {
  return Object.values(localFilters.value).some(
    (value) => value !== undefined && value !== null && value !== '',
  )
})

const applyFilters = () => {
  // Очищаем пустые значения перед отправкой
  const cleanedFilters: BookFilters = {}

  Object.entries(localFilters.value).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      cleanedFilters[key as keyof BookFilters] = value
    }
  })

  cleanedFilters.offset = 0 // Сбрасываем пагинацию при новом поиске
  cleanedFilters.limit = props.filters.limit || 6

  emit('update:filters', cleanedFilters)
  emit('apply')
}

const resetFilters = () => {
  localFilters.value = { limit: 6, offset: 0 }
  emit('reset')
}

const removeFilter = (filterKey: keyof BookFilters) => {
  localFilters.value[filterKey] = undefined
  // Автоматически применяем фильтры после удаления тега
  applyFilters()
}

// Обновляем локальные фильтры при изменении пропсов
watch(
  () => props.filters,
  (newFilters) => {
    localFilters.value = { ...newFilters }
  },
  { deep: true },
)
</script>

<style scoped>
.book-filter {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.3rem;
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
}

.apply-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  min-width: 80px;
}

.apply-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.apply-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.reset-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.reset-btn:hover:not(:disabled) {
  background: #5a6268;
}

.reset-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
  font-size: 0.9rem;
}

.filter-group input {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.filter-group input:focus {
  outline: none;
  border-color: #667eea;
}

.filter-group input::placeholder {
  color: #999;
}

.active-filters {
  border-top: 1px solid #e0e0e0;
  padding-top: 1.5rem;
}

.active-filters h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: #555;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.remove-tag {
  background: none;
  border: none;
  color: #1976d2;
  margin-left: 0.5rem;
  cursor: pointer;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s;
}

.remove-tag:hover {
  background: rgba(25, 118, 210, 0.1);
}

@media (max-width: 768px) {
  .filter-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-actions {
    justify-content: stretch;
  }

  .apply-btn,
  .reset-btn {
    flex: 1;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }
}
</style>
