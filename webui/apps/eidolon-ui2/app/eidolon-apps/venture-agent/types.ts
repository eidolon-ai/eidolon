export interface Company {
  name: string
  url: string
  category?: string
  loading: boolean
  should_research: boolean
  researched_details?: CompanyDetails
  error?: string
}

export interface CompanyDetails {
  process_id: string
  description: string
  stage: string
  market_size: string
  business_model: string
  logo_url: string
  relevance: number
  other_information?: string
}

export interface Thesis {
  parent_process_id: string
  companyFinderPID: string
}
