import Layout from "../components/Layout";

import {
  downloadEmployeeReport,
  downloadAttendanceReport,
  downloadLeaveReport,
  downloadPayrollReport,
} from "../services/reportService";

function Reports() {
  return (
    <Layout>

      <h2 className="mb-4">
        Reports
      </h2>

      <div className="row">

        <div className="col-md-6 mb-3">

          <div className="card shadow">

            <div className="card-body">

              <h4>Employee Report</h4>

              <button
                className="btn btn-primary"
                onClick={downloadEmployeeReport}
              >
                Download CSV
              </button>

            </div>

          </div>

        </div>

        <div className="col-md-6 mb-3">

          <div className="card shadow">

            <div className="card-body">

              <h4>Attendance Report</h4>

              <button
                className="btn btn-success"
                onClick={downloadAttendanceReport}
              >
                Download CSV
              </button>

            </div>

          </div>

        </div>

        <div className="col-md-6 mb-3">

          <div className="card shadow">

            <div className="card-body">

              <h4>Leave Report</h4>

              <button
                className="btn btn-warning"
                onClick={downloadLeaveReport}
              >
                Download CSV
              </button>

            </div>

          </div>

        </div>

        <div className="col-md-6 mb-3">

          <div className="card shadow">

            <div className="card-body">

              <h4>Payroll Report</h4>

              <button
                className="btn btn-danger"
                onClick={downloadPayrollReport}
              >
                Download CSV
              </button>

            </div>

          </div>

        </div>

      </div>

    </Layout>
  );
}

export default Reports;