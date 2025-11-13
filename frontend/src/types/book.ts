export interface Book {
  id: number
  title: string
  author: string
  year: number
  genre: string
  description: string
  image_filename: string
}

export interface BookFilters {
  genre?: string
  author?: string
  year_from?: number
  year_to?: number
  limit?: number
  offset?: number
}
