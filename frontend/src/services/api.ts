import axios from 'axios'
import type { Book, BookFilters, BookFull } from '@/types/book'

// TODO: добавить путь в env
// const API_BASE_URL = 'http://book_backend:8000'
const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Добавляем интерцептор для логирования
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`)
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  },
)

api.interceptors.response.use(
  (response) => {
    console.log(`Response received:`, response.status)
    return response
  },
  (error) => {
    console.error('Response error:', error)
    if (error.response) {
      console.error('Error data:', error.response.data)
      console.error('Error status:', error.response.status)
    } else if (error.request) {
      console.error('No response received:', error.request)
    } else {
      console.error('Error message:', error.message)
    }
    return Promise.reject(error)
  },
)

export const bookApi = {
  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await api.get('/health')
    return response.data
  },

  async pingPong(): Promise<{ ping: string }> {
    const response = await api.get('/health')
    return response.data
  },

  async getBooks(filters: BookFilters = {}): Promise<Book[]> {
    try {
      console.log('Fetching books with filters:', filters)

      const params: Record<string, string> = {}

      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params[key] = value.toString()
        }
      })

      const response = await api.get<Book[]>('/books/', { params })
      console.log('Books received:', response.data.length)
      return response.data
    } catch (error) {
      console.error('Error fetching books:', error)
      throw error
    }
  },

  async getBook(id: number): Promise<BookFull> {
    try {
      console.log(`Fetching book with id: ${id}`)
      const response = await api.get<BookFull>(`/books/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error fetching book ${id}:`, error)
      throw error
    }
  },
}
