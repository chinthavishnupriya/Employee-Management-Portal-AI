import api from "./api";

// ===========================
// Get All Departments
// ===========================
export const getDepartments = async () => {
  const token = localStorage.getItem("access_token");

  const response = await api.get("/departments", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Create Department
// ===========================
export const createDepartment = async (department) => {
  const token = localStorage.getItem("access_token");

  const response = await api.post("/departments", department, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Update Department
// ===========================
export const updateDepartment = async (id, department) => {
  const token = localStorage.getItem("access_token");

  const response = await api.put(`/departments/${id}`, department, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Delete Department
// ===========================
export const deleteDepartment = async (id) => {
  const token = localStorage.getItem("access_token");

  const response = await api.delete(`/departments/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Get Department By ID (Optional)
// ===========================
export const getDepartment = async (id) => {
  const token = localStorage.getItem("access_token");

  const response = await api.get(`/departments/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};