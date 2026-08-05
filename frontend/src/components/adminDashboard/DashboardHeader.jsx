import {
    FaUsers,
    FaArrowUp
} from "react-icons/fa";

function DashboardHeader({ dashboard }) {

    return (

        <div className="bg-primary text-white rounded-4 shadow p-4 mb-4">

            <div className="row align-items-center">

                <div className="col-md-8">

                    <h2 className="fw-bold">
                        Welcome Back, Admin 👋
                    </h2>

                    <p className="mb-0 fs-5">
                        Manage employees, attendance, payroll,
                        performance and HR operations from one place.
                    </p>

                </div>

                <div className="col-md-4 text-end">

                    <div className="bg-white text-dark rounded-4 p-3 d-inline-block shadow">

                        <FaUsers className="text-primary fs-1 mb-2" />

                        <h4 className="mb-0">
                            HR Dashboard
                        </h4>

                        <small className="text-muted">
                            Enterprise Management Portal
                        </small>

                    </div>

                </div>

            </div>

            <hr className="my-4" />

            <div className="row">

                <div className="col-md-4">

                    <h6>Total Employees</h6>

                    <h3>
                        {dashboard.total_employees ?? 0}
                    </h3>

                </div>

                <div className="col-md-4">

                    <h6>Monthly Growth</h6>

                    <h3 className="text-warning">

                        <FaArrowUp />

                        {" "}12%

                    </h3>

                </div>

                <div className="col-md-4">

                    <h6>System Status</h6>

                    <h3 className="text-success">
                        Online
                    </h3>

                </div>

            </div>

        </div>

    );

}

export default DashboardHeader;