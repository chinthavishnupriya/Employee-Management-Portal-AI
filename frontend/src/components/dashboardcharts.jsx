import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar, Pie } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function DashboardCharts({ analytics }) {
  const leaveChart = {
    labels: ["Approved", "Pending", "Rejected"],
    datasets: [
      {
        label: "Leave Requests",
        data: [
          analytics.approved_leaves || 0,
          analytics.pending_leaves || 0,
          analytics.rejected_leaves || 0,
        ],
        backgroundColor: [
          "#198754",
          "#ffc107",
          "#dc3545",
        ],
      },
    ],
  };

  const employeeChart = {
    labels: [
      "Employees",
      "Departments",
      "Attendance",
      "Payroll",
    ],
    datasets: [
      {
        label: "System Summary",
        data: [
          analytics.total_employees || 0,
          analytics.total_departments || 0,
          analytics.total_attendance || 0,
          analytics.total_payroll_records || 0,
        ],
        backgroundColor: [
          "#0d6efd",
          "#20c997",
          "#ffc107",
          "#6610f2",
        ],
      },
    ],
  };

  return (
    <div className="row mt-4">

      <div className="col-lg-6 mb-4">
        <div className="card shadow">
          <div className="card-header">
            Employees Overview
          </div>

          <div className="card-body">
            <Bar data={employeeChart} />
          </div>
        </div>
      </div>

      <div className="col-lg-6 mb-4">
        <div className="card shadow">
          <div className="card-header">
            Leave Requests
          </div>

          <div className="card-body">
            <Pie data={leaveChart} />
          </div>
        </div>
      </div>

    </div>
  );
}

export default DashboardCharts;