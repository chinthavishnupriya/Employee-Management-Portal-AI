import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
  getAttendance,
} from "../services/attendanceService";

function Attendance() {
  const [attendance, setAttendance] = useState([]);
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

  const filteredAttendance = attendance.filter((record) =>
    String(record.employee_name ?? "")
      .toLowerCase()
      .includes(search.toLowerCase()) ||
    String(record.employee_id ?? "")
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <Layout>

      <h2 className="mb-4">
        Attendance Management
      </h2>

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

                    <td>{record.check_in || "-"}</td>

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
