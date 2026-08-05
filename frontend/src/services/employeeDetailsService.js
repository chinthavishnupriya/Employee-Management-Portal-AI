import api from "./api";

export async function getEmployeeDetails() {

    const response = await api.get("/employee/details");

    return response.data;

}