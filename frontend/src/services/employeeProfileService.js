import api from "./api";

export async function getProfile() {

    const response = await api.get(
        "/employee/profile"
    );

    return response.data;

}

export async function updateProfile(profile) {

    const response = await api.put(
        "/employee/profile",
        profile
    );

    return response.data;

}