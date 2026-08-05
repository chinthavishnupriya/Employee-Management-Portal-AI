import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    PointElement,
    LineElement,
    Tooltip,
    Legend
} from "chart.js";

import { Bar, Pie, Line } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    PointElement,
    LineElement,
    Tooltip,
    Legend
);

function DashboardCharts() {

    const employeeData = {

        labels: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ],

        datasets: [

            {

                label: "Employees",

                data: [18, 25, 32, 41, 48, 56],

                backgroundColor: "#0d6efd"

            }

        ]

    };

    const attendanceData = {

        labels: [

            "Present",
            "Leave",
            "Absent"

        ],

        datasets: [

            {

                data: [82, 10, 8],

                backgroundColor: [

                    "#198754",
                    "#ffc107",
                    "#dc3545"

                ]

            }

        ]

    };

    

    return (

        <div className="row">

            <div className="col-lg-6 mb-4">

                <div className="card shadow border-0 rounded-4">

                    <div className="card-header bg-white">

                        <h5 className="fw-bold">

                            📈 Employee Growth

                        </h5>

                    </div>

                    <div className="card-body">

                        <Bar data={employeeData} />

                    </div>

                </div>

            </div>

            <div className="col-lg-6 mb-4">

                <div className="card shadow border-0 rounded-4">

                    <div className="card-header bg-white">

                        <h5 className="fw-bold">

                            🥧 Attendance Overview

                        </h5>

                    </div>

                    <div className="card-body">

                        <Pie data={attendanceData} />

                    </div>

                </div>

            </div>

        </div>

    );

}

export default DashboardCharts;