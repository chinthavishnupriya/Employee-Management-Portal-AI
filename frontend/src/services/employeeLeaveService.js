import api from "./api";

// Apply Leave
export async function applyLeave(data) {

    const employeeId = localStorage.getItem("employee_id");

    const response = await api.post("/leave/apply", {
        employee_id: Number(employeeId),
        leave_type: data.leave_type,
        start_date: data.start_date,
        end_date: data.end_date,
        reason: data.reason,
    });

    return response.data;
}

// My Leave History
export async function getMyLeaves() {
    const response = await api.get("/leave/me");
    return response.data;
}

// Cancel Leave
export async function cancelLeave(id) {
    const response = await api.delete(`/leave/${id}`);
    return response.data;
}