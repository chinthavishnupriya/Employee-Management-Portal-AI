import { Link } from "react-router-dom";

function QuickActions() {

    return (

        <div className="card border-0 shadow mt-4">

            <div className="card-header bg-dark text-white">

                Quick Actions

            </div>

            <div className="card-body">

                <div className="row g-3">

                    <div className="col-md-3">
                        <Link
                            className="btn btn-primary w-100"
                            to="/employee/profile"
                        >
                            👤 Profile
                        </Link>
                    </div>

                    <div className="col-md-3">
                        <Link
                            className="btn btn-success w-100"
                            to="/employee/attendance"
                        >
                            📅 Attendance
                        </Link>
                    </div>

                    <div className="col-md-3">
                        <Link
                            className="btn btn-warning w-100"
                            to="/employee/leave"
                        >
                            🏖 Leave
                        </Link>
                    </div>

                    <div className="col-md-3">
                        <Link
                            className="btn btn-danger w-100"
                            to="/employee/payroll"
                        >
                            💰 Payroll
                        </Link>
                    </div>

                </div>

            </div>

        </div>

    );

}

export default QuickActions;