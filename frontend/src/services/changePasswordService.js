import api from "./api";

export async function changePassword(data) {
    const response = await api.put("/change-password", data);
    return response.data;
}