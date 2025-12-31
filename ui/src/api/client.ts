import axios from "axios";

// Relative path for Nginx proxy interaction
const API_BASE_URL = "/api/v1/agent";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(request => {
  console.log('Starting Request', request)
  return request
})

apiClient.interceptors.response.use(response => {
  console.log('Response:', response)
  return response
})

export const analyzeProfile = async (formData: FormData) => {
  const response = await apiClient.post("/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

export const generateRecovery = async (context: string, jobDescription: string, githubUsername?: string) => {
  const formData = new FormData();
  formData.append("context", context);
  formData.append("job_description", jobDescription);
  if (githubUsername) formData.append("github_username", githubUsername);

  const response = await apiClient.post("/recover", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};
