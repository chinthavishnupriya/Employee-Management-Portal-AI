import { Link } from "react-router-dom";
import EmployeeSidebar from "./EmployeeSidebar";
import EmployeeTopNavbar from "./EmployeeTopNavbar";
function EmployeeLayout({ children }) {

    return (

        <div className="d-flex">

            <EmployeeSidebar />

            <div
                className="flex-grow-1 p-4"
                style={{
                    backgroundColor: "#f8f9fa",
                    minHeight: "100vh",
                }}
            >

                <div className="mb-3">

                    <Link to="/employee/attendance">
                        My Attendance
                    </Link>

                </div>
                <EmployeeTopNavbar />
                {children}

            </div>

        </div>

    );
}

export default EmployeeLayout;