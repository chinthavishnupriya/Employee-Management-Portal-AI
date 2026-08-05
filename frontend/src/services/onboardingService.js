import api from "./api";

// Get all onboarding records
export async function getOnboarding() {
    const response = await api.get("/onboarding");
    return response.data;
}

// Create onboarding record
export async function createOnboarding(data) {
    const response = await api.post("/onboarding", data);
    return response.data;
}

// Delete onboarding record
export async function deleteOnboarding(id) {
    const response = await api.delete(`/onboarding/${id}`);
    return response.data;
}