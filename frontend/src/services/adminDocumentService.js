import api from "./api";

// Get all uploaded documents
export async function getAllDocuments() {
    const response = await api.get("/admin/documents");
    return response.data;
}

// Approve document
export async function approveDocument(id) {
    const response = await api.put(`/admin/documents/${id}/approve`);
    return response.data;
}

// Reject document
export async function rejectDocument(id) {
    const response = await api.put(`/admin/documents/${id}/reject`);
    return response.data;
}