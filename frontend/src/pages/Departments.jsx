import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
  getDepartments,
  createDepartment,
  updateDepartment,
  deleteDepartment,
} from "../services/departmentService";

function Departments() {
  const [departments, setDepartments] = useState([]);
  const [search, setSearch] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    department_name: "",
    description: "",
  });

  useEffect(() => {
    loadDepartments();
  }, []);

  const loadDepartments = async () => {
    try {
      const data = await getDepartments();
      setDepartments(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load departments");
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
      if (editingId) {
        await updateDepartment(editingId, form);
        alert("Department Updated Successfully");
      } else {
        await createDepartment(form);
        alert("Department Added Successfully");
      }

      setEditingId(null);

      setForm({
        department_name: "",
        description: "",
      });

      loadDepartments();
    } catch (error) {
      console.error(error);
      alert("Operation Failed");
    }
  };

  const handleEdit = (department) => {
    setEditingId(department.id);

    setForm({
      department_name: department.department_name,
      description: department.description,
    });
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this department?")) return;

    try {
      await deleteDepartment(id);
      alert("Department Deleted");
      loadDepartments();
    } catch (error) {
      console.error(error);
      alert("Delete Failed");
    }
  };

  const filteredDepartments = departments.filter((dept) =>
    dept.department_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Layout>

      <h2 className="mb-4">Department Management</h2>

      <div className="card shadow mb-4">

        <div className="card-header bg-primary text-white">
          <h5 className="mb-0">
            {editingId ? "Edit Department" : "Add Department"}
          </h5>
        </div>

        <div className="card-body">

          <form onSubmit={handleSubmit}>

            <div className="row">

              <div className="col-md-6 mb-3">
                <label>Department Name</label>

                <input
                  className="form-control"
                  name="department_name"
                  value={form.department_name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="col-md-6 mb-3">
                <label>Description</label>

                <input
                  className="form-control"
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  required
                />
              </div>

            </div>

            <button
              className={
                editingId
                  ? "btn btn-warning"
                  : "btn btn-success"
              }
            >
              {editingId ? "Update Department" : "Add Department"}
            </button>

          </form>

        </div>

      </div>

      <div className="card shadow">

        <div className="card-header bg-dark text-white">
          <h5 className="mb-0">Departments</h5>
        </div>

        <div className="card-body">

          <div className="mb-3">
            <input
              className="form-control"
              placeholder="Search Department..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <table className="table table-bordered table-hover">

            <thead className="table-dark">

              <tr>
                <th>ID</th>
                <th>Department</th>
                <th>Description</th>
                <th>Actions</th>
              </tr>

            </thead>

            <tbody>

              {filteredDepartments.length === 0 ? (

                <tr>
                  <td colSpan="4" className="text-center">
                    No Departments Found
                  </td>
                </tr>

              ) : (

                filteredDepartments.map((dept) => (

                  <tr key={dept.id}>

                    <td>{dept.id}</td>
                    <td>{dept.department_name}</td>
                    <td>{dept.description}</td>

                    <td>

                      <button
                        className="btn btn-warning btn-sm me-2"
                        onClick={() => handleEdit(dept)}
                      >
                        Edit
                      </button>

                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(dept.id)}
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

    </Layout>
  );
}

export default Departments;