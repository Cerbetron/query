import axios from 'axios';

// Base Axios instance configured for the backend API.
// The base URL can be overridden with the REACT_APP_API_URL env variable
// when building the React application.
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

export interface SearchFilters {
  keyword?: string;
  filters?: string[];
}

export interface Resource {
  id: number;
  name: string;
  url?: string;
  description?: string;
  tags?: string[];
}

/**
 * Perform a search request using the provided filters.
 * Returns a list of resources that match the query.
 */
export async function searchResources(
  filters: SearchFilters
): Promise<Resource[]> {
  const response = await apiClient.post<Resource[]>('/search', filters);
  return response.data;
}

/**
 * Fetch details about a single resource by id.
 */
export async function getDetails(id: number): Promise<Resource> {
  const response = await apiClient.get<Resource>(`/details/${id}`);
  return response.data;
}

export default apiClient;
