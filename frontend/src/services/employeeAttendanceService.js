import api from "./api";

// ==========================
// Check In
// ==========================
export async function checkIn() {
    const response = await api.post("/attendance/check-in");
    return response.data;
}

// ==========================
// Check Out
// ==========================
export async function checkOut() {
    const response = await api.put("/attendance/check-out");
    return response.data;
}

// ==========================
// My Attendance
// ==========================
export async function getMyAttendance() {
    const response = await api.get("/attendance/me");
    return response.data;
}

// ==========================
// Attendance Summary
// ==========================
export async function getAttendanceSummary() {
    const response = await api.get("/attendance/my-summary");
    return response.data;
}

// ==========================
// Admin - All Attendance
// ==========================
export async function getAttendance() {
    const response = await api.get("/attendance");
    return response.data;
}

// ==========================
// Admin - Employee Attendance
// ==========================
export async function getEmployeeAttendance(employee_id) {
    const response = await api.get(`/attendance/${employee_id}`);
    return response.data;
}