import api from "./api";

export async function uploadProfilePhoto(file) {

    const formData = new FormData();

    formData.append("photo", file);

    const response = await api.post(
        "/employee/profile-photo",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
}