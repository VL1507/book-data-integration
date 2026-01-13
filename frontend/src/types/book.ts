export interface Book {
  publication_id: number
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

export interface PublicationSiteInfo {
  year: number
  page_count: number
  price: number
  image_url: string
  site_name: string
  site_url: string
  illustration_type?: string
  coverages_type?: string
  dim_x?: number
  dim_y?: number
  dim_z?: number
}

export interface BookFull {
  publication_id: number
  title: string
  authors: string[]
  genres: string[]
  isbn: string[]
  annotation?: string
  publication_site_info: PublicationSiteInfo[]
}
