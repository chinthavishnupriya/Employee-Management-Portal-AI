import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
  checkIn,
  checkOut,
  getAttendance,
} from "../services/attendanceService";

function Attendance() {
  const [attendance, setAttendance] = useState([]);
  const [employeeId, setEmployeeId] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadAttendance();
  }, []);

  const loadAttendance = async () => {
    try {
      const data = await getAttendance();
      setAttendance(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load attendance");
    }
  };

  const handleCheckIn = async () => {
    if (!employeeId) {
      alert("Enter Employee ID");
      return;
    }

    try {
      await checkIn(Number(employeeId));
      alert("Check-In Successful");
      setEmployeeId("");
      loadAttendance();
    } catch (error) {
      console.error(error);
      alert("Check-In Failed");
    }
  };

  const handleCheckOut = async () => {
    if (!employeeId) {
      alert("Enter Employee ID");
      return;
    }

    try {
      await checkOut(Number(employeeId));
      alert("Check-Out Successful");
      setEmployeeId("");
      loadAttendance();
    } catch (error) {
      console.error(error);
      alert("Check-Out Failed");
    }
  };

  const filteredAttendance = attendance.filter((record) =>
    record.employee_name
      .toLowerCase()
      .includes(search.toLowerCase()) ||
    record.employee_id
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <Layout>

      <h2 className="mb-4">
        Attendance Management
      </h2>

      <div className="card shadow mb-4">

        <div className="card-header bg-primary text-white">
          <h5 className="mb-0">
            Attendance
          </h5>
        </div>

        <div className="card-body">

          <div className="row">

            <div className="col-md-6">

              <label>Employee ID</label>

              <input
                className="form-control"
                value={employeeId}
                onChange={(e) =>
                  setEmployeeId(e.target.value)
                }
              />

            </div>

          </div>

          <button
            className="btn btn-success mt-3 me-2"
            onClick={handleCheckIn}
          >
            Check In
          </button>

          <button
            className="btn btn-danger mt-3"
            onClick={handleCheckOut}
          >
            Check Out
          </button>

        </div>

      </div>

      <div className="card shadow">

        <div className="card-header bg-dark text-white">
          <h5 className="mb-0">
            Attendance History
          </h5>
        </div>

        <div className="card-body">

          <input
            className="form-control mb-3"
            placeholder="Search Employee..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />

          <table className="table table-bordered table-hover">

            <thead className="table-dark">

              <tr>

                <th>ID</th>
                <th>Name</th>
                <th>Department</th>
                <th>Date</th>
                <th>Check In</th>
                <th>Check Out</th>
                <th>Status</th>

              </tr>

            </thead>

            <tbody>

              {filteredAttendance.length === 0 ? (

                <tr>

                  <td
                    colSpan="7"
                    className="text-center"
                  >
                    No Attendance Found
                  </td>

                </tr>

              ) : (

                filteredAttendance.map((record) => (

                  <tr key={record.id}>

                    <td>{record.employee_id}</td>

                    <td>{record.employee_name}</td>

                    <td>{record.department}</td>

                    <td>{record.date}</td>

                    <td>{record.check_in}</td>

                    <td>{record.check_out || "-"}</td>

                    <td>

                      <span
                        className={
                          record.status === "Present"
                            ? "badge bg-success"
                            : "badge bg-danger"
                        }
                      >
                        {record.status}
                      </span>

                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </div>

    </Layout>
  );
}

export default Attendance;