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

import { Bar, Line, Pie } from "react-chartjs-2";

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

function AnalyticsCharts() {

    const employeeGrowth = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [
            {
                label: "Employees",
                data: [18, 25, 32, 41, 48, 56],
                backgroundColor: "#0d6efd"
            }
        ]
    };

    const attendance = {
        labels: ["Present", "Leave", "Absent"],
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

    const payroll = {
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
                label: "Payroll",
                data: [
                    8,
                    10,
                    12,
                    14,
                    16,
                    18
                ],
                borderColor: "#6f42c1",
                backgroundColor: "#6f42c1",
                fill: false
            }
        ]
    };

    return (

        <div className="row">

            <div className="col-lg-6 mb-4">

                <div className="card shadow">

                    <div className="card-header">

                        Employee Growth

                    </div>

                    <div className="card-body">

                        <Bar data={employeeGrowth} />

                    </div>

                </div>

            </div>

            <div className="col-lg-6 mb-4">

                <div className="card shadow">

                    <div className="card-header">

                        Attendance Overview

                    </div>

                    <div className="card-body">

                        <Pie data={attendance} />

                    </div>

                </div>

            </div>

            <div className="col-12">

                <div className="card shadow">

                    <div className="card-header">

                        Monthly Payroll Trend

                    </div>

                    <div className="card-body">

                        <Line data={payroll} />

                    </div>

                </div>

            </div>

        </div>

    );

}

export default AnalyticsCharts;