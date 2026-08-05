import { Navigate } from "react-router-dom";

function AdminRoute({ children }) {

    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    console.log("TOKEN:", token);
    console.log("ROLE:", role);

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    if (role !== "Admin") {
        return <Navigate to="/employee/dashboard" replace />;
    }

    return children;
}

export default AdminRoute;