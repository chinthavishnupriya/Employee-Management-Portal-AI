import api from "./api";

// Get all performance reviews
export async function getPerformance() {
    const response = await api.get("/performance");
    return response.data;
}

// Create performance review
export async function createPerformance(data) {
    const response = await api.post("/performance", data);
    return response.data;
}

// Delete performance review
export async function deletePerformance(id) {
    const response = await api.delete(`/performance/${id}`);
    return response.data;
}