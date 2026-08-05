import { Navigate } from "react-router-dom";

function EmployeeRoute({ children }) {

    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    
    if (!token) {
        return <Navigate to="/" />;
    }

    if (role !== "Employee") {
        return <Navigate to="/dashboard" />;
    }

    return children;
}

export default EmployeeRoute;