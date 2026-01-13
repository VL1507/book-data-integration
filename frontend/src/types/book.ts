export interface Book {
  id: number
  title: string
  authors: string[]
  years: number[]
  genres: string[]
  image_url: string
}

export interface BookFilters {
  genre?: string
  author?: string
  title?: string
  year_from?: number
  year_to?: number
  limit?: number
  offset?: number
}
