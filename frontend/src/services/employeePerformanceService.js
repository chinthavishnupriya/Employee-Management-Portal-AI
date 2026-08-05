import api from "./api";

// ==========================
// My Performance
// ==========================
export async function getMyPerformance() {

    const response = await api.get("/performance/me");

    return response.data;

}