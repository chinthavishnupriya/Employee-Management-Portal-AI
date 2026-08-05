import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import {
  getEmployees,
  createEmployee,
  updateEmployee,
  deleteEmployee,
} from "../services/employeeService";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    employee_id: "",
    full_name: "",
    email: "",
    department_id: "",
    designation: "",
    salary: "",
  });

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      const data = await getEmployees();
      setEmployees(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load employees");
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
      const employeeData = {
  employee_id: form.employee_id,
  full_name: form.full_name,
  email: form.email,
  department_id: Number(form.department_id),
  designation: form.designation,
  salary: Number(form.salary),
};

if (editingId) {
  await updateEmployee(editingId, employeeData);
  alert("Employee Updated Successfully");
} else {
  await createEmployee(employeeData);
  alert("Employee Added Successfully");
}

      setEditingId(null);

setForm({
        employee_id: "",
        full_name: "",
        email: "",
        department_id: "",
        designation: "",
        salary: "",
      });

      loadEmployees();
    } catch (error) {
      console.error(error);
      alert("Failed to add employee");
    }
  };

  const handleEdit = (employee) => {
  setEditingId(employee.id);

  setForm({
    employee_id: employee.employee_id,
    full_name: employee.full_name,
    email: employee.email,
    department_id: employee.department_id,
    designation: employee.designation,
    salary: employee.salary,
  });
};

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this employee?"
    );

    if (!confirmDelete) return;

    try {
      await deleteEmployee(id);

      alert("Employee deleted successfully.");

      loadEmployees();
    } catch (error) {
      console.error(error);
      alert("Failed to delete employee.");
    }
  };

  const filteredEmployees = employees.filter(
    (emp) =>
      emp.full_name.toLowerCase().includes(search.toLowerCase()) ||
      emp.employee_id.toLowerCase().includes(search.toLowerCase()) ||
      emp.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Layout>
      <div className="container">

        <h2 className="mb-4">Employee Management</h2>

        {/* Add Employee */}
        <div className="card shadow mb-4">

          <div className="card-header bg-primary text-white">
            <h5 className="mb-0">Add Employee</h5>
          </div>

          <div className="card-body">

            <form onSubmit={handleSubmit}>

              <div className="row">

                <div className="col-md-4 mb-3">
                  <label>Employee ID</label>
                  <input
                    type="text"
                    className="form-control"
                    name="employee_id"
                    value={form.employee_id}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-md-4 mb-3">
                  <label>Full Name</label>
                  <input
                    type="text"
                    className="form-control"
                    name="full_name"
                    value={form.full_name}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-md-4 mb-3">
                  <label>Email</label>
                  <input
                    type="email"
                    className="form-control"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-md-4 mb-3">
                  <label>Department ID</label>
                  <input
                    type="number"
                    className="form-control"
                    name="department_id"
                    value={form.department_id}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-md-4 mb-3">
                  <label>Designation</label>
                  <input
                    type="text"
                    className="form-control"
                    name="designation"
                    value={form.designation}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-md-4 mb-3">
                  <label>Salary</label>
                  <input
                    type="number"
                    className="form-control"
                    name="salary"
                    value={form.salary}
                    onChange={handleChange}
                    required
                  />
                </div>

              </div>

              <button
  type="submit"
  className={
    editingId
      ? "btn btn-warning"
      : "btn btn-success"
  }
>
  {editingId ? "Update Employee" : "Add Employee"}
</button>

            </form>

          </div>

        </div>

        {/* Employee List */}
        <div className="card shadow">

          <div className="card-header bg-dark text-white">
            <h5 className="mb-0">Employee List</h5>
          </div>

          <div className="card-body">

            <div className="mb-3">
              <input
                type="text"
                className="form-control"
                placeholder="Search Employee..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <table className="table table-bordered table-hover">

              <thead className="table-dark">

                <tr>
                  <th>ID</th>
                  <th>Employee ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Department</th>
                  <th>Designation</th>
                  <th>Salary</th>
                  <th>Actions</th>
                </tr>

              </thead>

              <tbody>

                {filteredEmployees.length === 0 ? (

                  <tr>
                    <td colSpan="8" className="text-center">
                      No Employees Found
                    </td>
                  </tr>

                ) : (

                  filteredEmployees.map((emp) => (

                    <tr key={emp.id}>

                      <td>{emp.id}</td>
                      <td>{emp.employee_id}</td>
                      <td>{emp.full_name}</td>
                      <td>{emp.email}</td>
                      <td>{emp.department_id}</td>
                      <td>{emp.designation}</td>
                      <td>₹ {emp.salary}</td>

                      <td>

                        <button
  className="btn btn-warning btn-sm me-2"
  onClick={() => handleEdit(emp)}
>
  Edit
</button>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDelete(emp.id)}
                        >
                          Delete
                        </button>

                      </td>

                    </tr>

                  ))

                )}

              </tbody>

            </table>

          </div>

        </div>

      </div>
    </Layout>
  );
}

export default Employees;