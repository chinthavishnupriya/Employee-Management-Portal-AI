import api from "./api";

export async function getEmployeeDashboard() {

    const response = await api.get("/employee/dashboard");

    return response.data;

}