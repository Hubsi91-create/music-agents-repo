const API_BASE_URL = 'http://localhost:5000'

export const useApi = () => {
  const fetchData = async (endpoint: string, options?: RequestInit) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }

    return response.json()
  }

  const postData = async (endpoint: string, data: any) => {
    return fetchData(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  return {
    fetchData,
    postData,
  }
}
