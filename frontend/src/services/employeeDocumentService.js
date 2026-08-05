import api from "./api";

// Upload Document
export async function uploadDocument(formData) {

    const response = await api.post(
        "/employee/documents/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );

    return response.data;
}

// Get My Documents
export async function getMyDocuments() {

    const response = await api.get(
        "/employee/documents"
    );

    return response.data;
}
// Delete Document

export async function deleteDocument(documentId) {

    const response = await api.delete(

        `/employee/documents/${documentId}`

    );

    return response.data;

}