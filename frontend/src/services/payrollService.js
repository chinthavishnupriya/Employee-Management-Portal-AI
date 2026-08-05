import api from "./api";

// Create
export async function createPayroll(data) {
    const response = await api.post("/payroll", data);
    return response.data;
}

// Get All
export async function getPayrolls() {
    const response = await api.get("/payroll");
    return response.data;
}

// Get One
export async function getPayroll(id) {
    const response = await api.get(`/payroll/${id}`);
    return response.data;
}

// Update
export async function updatePayroll(id, data) {
    const response = await api.put(`/payroll/${id}`, data);
    return response.data;
}

// Delete
export async function deletePayroll(id) {
    const response = await api.delete(`/payroll/${id}`);
    return response.data;
}

// Employee
export async function getMyPayroll() {
    const response = await api.get("/payroll/me");
    return response.data;
}