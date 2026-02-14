const API_BASE_URL = 'http://localhost:8000';

export interface Plant {
  id: number;
  name: string;
  species: string;
  careLevel: string;
  wateringFrequency: string;
  sunlight: string;
  description: string;
  lastWatered: string;
}

export interface TestUploadResponse {
  message: string;
  filename: string;
  content_type: string;
  size_kb: number;
  dimensions: string;
  format: string;
}

export interface DiseaseInfo {
  name: string;
  severity: string;
  symptoms: string[];
  remedies: string[];
}

export interface PredictionResponse {
  scientific_name: string;
  common_name: string;
  confidence: number;
  medicinal_properties: string[];
  plant_health_status: string;
  detected_diseases?: DiseaseInfo[] | null;
  care_recommendations: string[];
}

export const api = {
  // Test image upload
  testUpload: async (file: File): Promise<TestUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/test-upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload image');
    }

    return response.json();
  },

  // Analyze plant disease
  analyze: async (file: File): Promise<PredictionResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      // Try to extract error message from response
      let errorMessage = 'Failed to analyze image';
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // If response is not JSON, use status text
        errorMessage = response.statusText || errorMessage;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  },

  // Get all plants
  getPlants: async (): Promise<Plant[]> => {
    const response = await fetch(`${API_BASE_URL}/api/plants`);
    if (!response.ok) {
      throw new Error('Failed to fetch plants');
    }
    return response.json();
  },

  // Get single plant
  getPlant: async (id: number): Promise<Plant> => {
    const response = await fetch(`${API_BASE_URL}/api/plants/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch plant');
    }
    return response.json();
  },

  // Add new plant
  addPlant: async (plant: Omit<Plant, 'id'>): Promise<Plant> => {
    const response = await fetch(`${API_BASE_URL}/api/plants`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(plant),
    });
    if (!response.ok) {
      throw new Error('Failed to add plant');
    }
    return response.json();
  },

  // Update plant
  updatePlant: async (id: number, plant: Partial<Plant>): Promise<Plant> => {
    const response = await fetch(`${API_BASE_URL}/api/plants/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(plant),
    });
    if (!response.ok) {
      throw new Error('Failed to update plant');
    }
    return response.json();
  },

  // Delete plant
  deletePlant: async (id: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/api/plants/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete plant');
    }
  },

  // Mark plant as watered
  waterPlant: async (id: number): Promise<Plant> => {
    const response = await fetch(`${API_BASE_URL}/api/plants/${id}/water`, {
      method: 'PATCH',
    });
    if (!response.ok) {
      throw new Error('Failed to water plant');
    }
    return response.json();
  },
};

