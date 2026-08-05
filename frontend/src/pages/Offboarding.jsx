import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
    getOffboarding,
    createOffboarding,
    deleteOffboarding
} from "../services/offboardingService";

import { getEmployees } from "../services/employeeService";

function Offboarding() {

    const [records, setRecords] = useState([]);

    const [employees, setEmployees] = useState([]);

    const [form, setForm] = useState({

        employee_id: "",

        resignation_date: "",

        last_working_day: "",

        exit_reason: "",

        laptop_returned: false,

        id_card_returned: false,

        account_disabled: false,

        exit_interview_completed: false,

        final_settlement_completed: false,

        status: "Pending"

    });

    useEffect(() => {

        loadData();

    }, []);

    async function loadData() {

        try {

            const offboardingData = await getOffboarding();

            const employeeData = await getEmployees();

            setRecords(offboardingData);

            setEmployees(employeeData);

        }

        catch (error) {

            console.log(error);

            alert("Unable to load offboarding records.");

        }

    }

    function handleChange(e) {

        const { name, value, type, checked } = e.target;

        setForm({

            ...form,

            [name]: type === "checkbox"
                ? checked
                : value

        });

    }

    async function handleSubmit(e) {

        e.preventDefault();

        try {

            await createOffboarding(form);

            alert("Offboarding record created successfully.");

            setForm({

                employee_id: "",

                resignation_date: "",

                last_working_day: "",

                exit_reason: "",

                laptop_returned: false,

                id_card_returned: false,

                account_disabled: false,

                exit_interview_completed: false,

                final_settlement_completed: false,

                status: "Pending"

            });

            loadData();

        }

        catch (error) {

            console.log(error);

            alert("Unable to create offboarding record.");

        }

    }

    async function handleDelete(id) {

        if (!window.confirm("Delete this offboarding record?")) {

            return;

        }

        try {

            await deleteOffboarding(id);

            loadData();

        }

        catch (error) {

            console.log(error);

            alert("Unable to delete record.");

        }

    }

    function getStatusBadge(status) {

        switch (status) {

            case "Completed":

                return "success";

            case "In Progress":

                return "warning";

            default:

                return "secondary";

        }

    }
        return (

        <Layout>

            <h2 className="mb-4">

                Employee Offboarding

            </h2>

            <div className="card shadow mb-4">

                <div className="card-header bg-danger text-white">

                    Add Offboarding Record

                </div>

                <div className="card-body">

                    <form onSubmit={handleSubmit}>

                        <div className="row">

                            <div className="col-md-6 mb-3">

                                <label className="form-label">

                                    Employee

                                </label>

                                <select
                                    className="form-control"
                                    name="employee_id"
                                    value={form.employee_id}
                                    onChange={handleChange}
                                    required
                                >

                                    <option value="">

                                        Select Employee

                                    </option>

                                    {

                                        employees.map(emp => (

                                            <option
                                                key={emp.id}
                                                value={emp.id}
                                            >

                                                {emp.full_name}

                                            </option>

                                        ))

                                    }

                                </select>

                            </div>

                            <div className="col-md-3 mb-3">

                                <label className="form-label">

                                    Resignation Date

                                </label>

                                <input
                                    type="date"
                                    className="form-control"
                                    name="resignation_date"
                                    value={form.resignation_date}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="col-md-3 mb-3">

                                <label className="form-label">

                                    Last Working Day

                                </label>

                                <input
                                    type="date"
                                    className="form-control"
                                    name="last_working_day"
                                    value={form.last_working_day}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                        </div>

                        <div className="row">

                            <div className="col-md-8 mb-3">

                                <label className="form-label">

                                    Exit Reason

                                </label>

                                <textarea
                                    className="form-control"
                                    rows="3"
                                    name="exit_reason"
                                    value={form.exit_reason}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-4 mb-3">

                                <label className="form-label">

                                    Status

                                </label>

                                <select
                                    className="form-control"
                                    name="status"
                                    value={form.status}
                                    onChange={handleChange}
                                >

                                    <option>Pending</option>

                                    <option>In Progress</option>

                                    <option>Completed</option>

                                </select>

                            </div>

                        </div>

                        <hr />

                        <h5 className="mb-3">

                            Offboarding Checklist

                        </h5>

                        <div className="row">

                            <div className="col-md-4 mb-3">

                                <div className="form-check">

                                    <input
                                        type="checkbox"
                                        className="form-check-input"
                                        name="laptop_returned"
                                        checked={form.laptop_returned}
                                        onChange={handleChange}
                                    />

                                    <label className="form-check-label">

                                        Laptop Returned

                                    </label>

                                </div>

                            </div>

                            <div className="col-md-4 mb-3">

                                <div className="form-check">

                                    <input
                                        type="checkbox"
                                        className="form-check-input"
                                        name="id_card_returned"
                                        checked={form.id_card_returned}
                                        onChange={handleChange}
                                    />

                                    <label className="form-check-label">

                                        ID Card Returned

                                    </label>

                                </div>

                            </div>

                            <div className="col-md-4 mb-3">

                                <div className="form-check">

                                    <input
                                        type="checkbox"
                                        className="form-check-input"
                                        name="account_disabled"
                                        checked={form.account_disabled}
                                        onChange={handleChange}
                                    />

                                    <label className="form-check-label">

                                        Account Disabled

                                    </label>

                                </div>

                            </div>

                            <div className="col-md-4 mb-3">

                                <div className="form-check">

                                    <input
                                        type="checkbox"
                                        className="form-check-input"
                                        name="exit_interview_completed"
                                        checked={form.exit_interview_completed}
                                        onChange={handleChange}
                                    />

                                    <label className="form-check-label">

                                        Exit Interview Completed

                                    </label>

                                </div>

                            </div>

                            <div className="col-md-4 mb-3">

                                <div className="form-check">

                                    <input
                                        type="checkbox"
                                        className="form-check-input"
                                        name="final_settlement_completed"
                                        checked={form.final_settlement_completed}
                                        onChange={handleChange}
                                    />

                                    <label className="form-check-label">

                                        Final Settlement Completed

                                    </label>

                                </div>

                            </div>

                        </div>

                        <button
                            className="btn btn-danger"
                            type="submit"
                        >

                            Save Offboarding Record

                        </button>

                    </form>

                </div>

            </div>
                        <div className="card shadow">

                <div className="card-header bg-dark text-white">

                    Offboarding Records

                </div>

                <div className="card-body">

                    <div className="table-responsive">

                        <table className="table table-hover table-bordered align-middle">

                            <thead className="table-light">

                                <tr>

                                    <th>Employee</th>

                                    <th>Resignation</th>

                                    <th>Last Working Day</th>

                                    <th>Laptop</th>

                                    <th>ID Card</th>

                                    <th>Settlement</th>

                                    <th>Status</th>

                                    <th>Action</th>

                                </tr>

                            </thead>

                            <tbody>

                                {

                                    records.length === 0 ? (

                                        <tr>

                                            <td
                                                colSpan="8"
                                                className="text-center"
                                            >

                                                No offboarding records found.

                                            </td>

                                        </tr>

                                    ) : (

                                        records.map(record => (

                                            <tr key={record.id}>

                                                <td>

                                                    {record.employee}

                                                </td>

                                                <td>

                                                    {record.resignation_date}

                                                </td>

                                                <td>

                                                    {record.last_working_day}

                                                </td>

                                                <td>

                                                    {

                                                        record.laptop_returned

                                                            ?

                                                            <span className="badge bg-success">

                                                                Returned

                                                            </span>

                                                            :

                                                            <span className="badge bg-danger">

                                                                Pending

                                                            </span>

                                                    }

                                                </td>

                                                <td>

                                                    {

                                                        record.id_card_returned

                                                            ?

                                                            <span className="badge bg-success">

                                                                Returned

                                                            </span>

                                                            :

                                                            <span className="badge bg-danger">

                                                                Pending

                                                            </span>

                                                    }

                                                </td>

                                                <td>

                                                    {

                                                        record.final_settlement_completed

                                                            ?

                                                            <span className="badge bg-success">

                                                                Completed

                                                            </span>

                                                            :

                                                            <span className="badge bg-warning">

                                                                Pending

                                                            </span>

                                                    }

                                                </td>

                                                <td>

                                                    <span
                                                        className={`badge bg-${getStatusBadge(record.status)}`}
                                                    >

                                                        {record.status}

                                                    </span>

                                                </td>

                                                <td>

                                                    <button
                                                        className="btn btn-danger btn-sm"
                                                        onClick={() => handleDelete(record.id)}
                                                    >

                                                        Delete

                                                    </button>

                                                </td>

                                            </tr>

                                        ))

                                    )

                                }

                            </tbody>

                        </table>

                    </div>

                </div>

            </div>
                    </Layout>

    );

}

export default Offboarding;