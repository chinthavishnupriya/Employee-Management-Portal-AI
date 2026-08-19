import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
  applyLeave,
  getLeaves,
  approveLeave,
  rejectLeave,
} from "../services/leaveService";

function Leave() {
  const [leaves, setLeaves] = useState([]);
  const [search, setSearch] = useState("");

  const [form, setForm] = useState({
    employee_id: "",
    leave_type: "",
    start_date: "",
    end_date: "",
    reason: "",
  });

  useEffect(() => {
    loadLeaves();
  }, []);

  const loadLeaves = async () => {
    try {
      const data = await getLeaves();
      setLeaves(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load leave requests.");
    }
  };

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await applyLeave({
        employee_id: Number(form.employee_id),
        leave_type: form.leave_type,
        start_date: form.start_date,
        end_date: form.end_date,
        reason: form.reason,
      });

      alert("Leave request submitted.");

      setForm({
        employee_id: "",
        leave_type: "",
        start_date: "",
        end_date: "",
        reason: "",
      });

      loadLeaves();
    } catch (error) {
      console.error(error);
      alert("Failed to apply leave.");
    }
  };

  const handleApprove = async (id) => {
    try {
      await approveLeave(id);
      alert("Leave Approved");
      loadLeaves();
    } catch (error) {
      console.error(error);
      alert("Failed to approve leave.");
    }
  };

  const handleReject = async (id) => {
    try {
      await rejectLeave(id);
      alert("Leave Rejected");
      loadLeaves();
    } catch (error) {
      console.error(error);
      alert("Failed to reject leave.");
    }
  };

  const filteredLeaves = leaves.filter((leave) =>
    String(
      leave.employee_id ??
      leave.employee_name ??
      ""
    )
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <Layout>
      <h2 className="mb-4">
        Leave Management
      </h2>

      <div className="card shadow">

        <div className="card-header bg-dark text-white">
          <h5 className="mb-0">
            Leave Requests
          </h5>
        </div>

        <div className="card-body">

          <input
            className="form-control mb-3"
            placeholder="Search by Employee ID or Name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <table className="table table-bordered table-hover">

            <thead className="table-dark">
              <tr>
                <th>ID</th>
                <th>Employee</th>
                <th>Leave Type</th>
                <th>Start</th>
                <th>End</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              {filteredLeaves.length === 0 ? (

                <tr>
                  <td colSpan="8" className="text-center">
                    No Leave Requests
                  </td>
                </tr>

              ) : (

                filteredLeaves.map((leave, index) => (

                  <tr key={leave.id ?? index}>

                    <td>{leave.id ?? "-"}</td>

                    <td>
                      {leave.employee_name ?? leave.employee_id ?? "-"}
                    </td>

                    <td>{leave.leave_type}</td>

                    <td>{leave.start_date}</td>

                    <td>{leave.end_date}</td>

                    <td>{leave.reason ?? "-"}</td>

                    <td>
                      <span
                        className={
                          leave.status === "Approved"
                            ? "badge bg-success"
                            : leave.status === "Rejected"
                            ? "badge bg-danger"
                            : "badge bg-warning text-dark"
                        }
                      >
                        {leave.status}
                      </span>
                    </td>

                    <td>

                      <button
                        className="btn btn-success btn-sm me-2"
                        onClick={() => handleApprove(leave.id)}
                      >
                        Approve
                      </button>

                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleReject(leave.id)}
                      >
                        Reject
                      </button>

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

export default Leave;