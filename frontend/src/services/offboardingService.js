import api from "./api";

export async function getOffboarding() {
    const response = await api.get("/offboarding");
    return response.data;
}

export async function createOffboarding(data) {
    const response = await api.post("/offboarding", data);
    return response.data;
}

export async function deleteOffboarding(id) {
    const response = await api.delete(`/offboarding/${id}`);
    return response.data;
}