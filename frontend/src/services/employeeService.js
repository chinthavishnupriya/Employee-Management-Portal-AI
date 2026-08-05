import api from "./api";

// ===========================
// Get All Employees
// ===========================
export const getEmployees = async () => {
  const token = localStorage.getItem("access_token");

  const response = await api.get("/employees", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Create Employee
// ===========================
export const createEmployee = async (employee) => {
  const token = localStorage.getItem("access_token");

  const response = await api.post("/employees", employee, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Get Employee By ID
// ===========================
export const getEmployee = async (id) => {
  const token = localStorage.getItem("access_token");

  const response = await api.get(`/employees/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Update Employee
// ===========================
export const updateEmployee = async (id, employee) => {
  const token = localStorage.getItem("access_token");

  const response = await api.put(`/employees/${id}`, employee, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Delete Employee
// ===========================
export const deleteEmployee = async (id) => {
  const token = localStorage.getItem("access_token");

  const response = await api.delete(`/employees/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Get Employee Details
// ===========================
export const getEmployeeDetails = async () => {
  const token = localStorage.getItem("access_token");

  const response = await api.get("/employees/details", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ===========================
// Get Employees By Department
// ===========================
export const getEmployeesByDepartment = async (departmentId) => {
  const token = localStorage.getItem("access_token");

  const response = await api.get(
    `/employees/department/${departmentId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};