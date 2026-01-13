<template>
  <div class="debug-info">
    <h3>Отладочная информация</h3>
    <div class="debug-content">
      <div class="status">
        <strong>Статус API:</strong>
        <span :class="apiStatus">{{ apiStatusText }}</span>
      </div>

      <div class="connection-test">
        <button @click="testConnection" :disabled="testing">Проверить подключение</button>
        <div v-if="connectionResults.length > 0" class="test-results">
          <div v-for="result in connectionResults" :key="result.endpoint" class="test-result">
            <span class="endpoint-name">{{ result.endpoint }}:</span>
            <span :class="result.status">{{ result.message }}</span>
          </div>
        </div>
      </div>

      <div class="last-error" v-if="lastError">
        <strong>Последняя ошибка:</strong> {{ lastError }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { bookApi } from '@/services/api'

const apiStatus = ref<'checking' | 'online' | 'offline'>('checking')
const apiStatusText = ref('Проверка...')
const testing = ref(false)
const connectionResults = ref<
  Array<{ endpoint: string; status: 'success' | 'error'; message: string }>
>([])
const lastError = ref<string>('')

const testConnection = async () => {
  testing.value = true
  connectionResults.value = []
  lastError.value = ''

  const tests = [
    { name: 'Health Check', test: async () => await bookApi.healthCheck() },
    { name: 'Список книг', test: async () => await bookApi.getBooks({ limit: 1 }) },
    { name: 'Информация о книге', test: async () => await bookApi.getBook(1) },
  ]

  for (const test of tests) {
    try {
      await test.test()
      connectionResults.value.push({
        endpoint: test.name,
        status: 'success',
        message: '✅ Успешно',
      })
    } catch (error: any) {
      connectionResults.value.push({
        endpoint: test.name,
        status: 'error',
        message: `❌ Ошибка: ${error.message || 'Неизвестная ошибка'}`,
      })
      lastError.value = `Ошибка в ${test.name}: ${error.message}`
    }
  }

  // Проверяем общий статус
  const hasErrors = connectionResults.value.some((result) => result.status === 'error')
  apiStatus.value = hasErrors ? 'offline' : 'online'
  apiStatusText.value = hasErrors ? 'Есть проблемы' : 'Всё работает'

  testing.value = false
}
</script>

<style scoped>
.debug-info {
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  font-family: monospace;
  font-size: 0.9rem;
}

.debug-info h3 {
  margin-top: 0;
  color: #333;
}

.status .online {
  color: green;
  font-weight: bold;
}

.status .offline {
  color: red;
  font-weight: bold;
}

.status .checking {
  color: orange;
  font-weight: bold;
}

.connection-test {
  margin: 1rem 0;
}

.connection-test button {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.connection-test button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.connection-test button:hover:not(:disabled) {
  background: #0056b3;
}

.test-results {
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.test-result {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.5rem 0;
  padding: 0.25rem 0;
}

.endpoint-name {
  font-weight: bold;
}

.test-result .success {
  color: green;
}

.test-result .error {
  color: red;
}

.last-error {
  color: red;
  background: #ffe6e6;
  padding: 0.5rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.8rem;
}
</style>
