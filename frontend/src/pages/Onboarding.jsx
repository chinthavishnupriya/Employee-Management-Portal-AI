import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
    getOnboarding,
    createOnboarding,
    deleteOnboarding
} from "../services/onboardingService";

import { getEmployees } from "../services/employeeService";

function Onboarding() {

    const [records, setRecords] = useState([]);
    const [employees, setEmployees] = useState([]);

    const [form, setForm] = useState({
    employee_id: "",
    offer_status: "",
    documents_uploaded: false,
    email_created: false,
    id_card_issued: false,
    laptop_assigned: false,
    orientation_completed: false,
    manager_assigned: false,
    status: "",
    joining_date: "",
    mentor: "",
    training_status: "",
    welcome_kit: ""
});

    useEffect(() => {
        loadData();
    }, []);

    async function loadData() {

        try {

            const onboarding = await getOnboarding();
            const employeeData = await getEmployees();

            setRecords(onboarding);
            setEmployees(employeeData);

        } catch (error) {

            console.log(error);
            alert("Unable to load onboarding records.");

        }

    }

    function handleChange(e) {

        setForm({
            ...form,
            [e.target.name]: e.target.value
        });

    }

    async function handleSubmit(e) {

        e.preventDefault();

        try {

            await createOnboarding(form);

            alert("Onboarding record created.");

            setForm({
                employee_id: "",
    offer_status: "",
    documents_uploaded: false,
    email_created: false,
    id_card_issued: false,
    laptop_assigned: false,
    orientation_completed: false,
    manager_assigned: false,
    status: "",
    joining_date: "",
    mentor: "",
    training_status: "",
    welcome_kit: ""
            });

            loadData();

        } catch (error) {

            console.log(error);
            alert("Unable to create onboarding record.");

        }

    }

    async function handleDelete(id) {

        if (!window.confirm("Delete this onboarding record?")) return;

        await deleteOnboarding(id);

        loadData();

    }

    return (

        <Layout>

            <h2 className="mb-4">

                Employee Onboarding

            </h2>

            <div className="card shadow mb-4">

                <div className="card-header bg-primary text-white">

                    Add Onboarding Record

                </div>

                <div className="card-body">

                    <form onSubmit={handleSubmit}>

                        <div className="row">

                            <div className="col-md-6 mb-3">

                                <label>Employee</label>

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
<div className="col-md-6 mb-3">

    <label>Offer Status</label>

    <select
        className="form-control"
        name="offer_status"
        value={form.offer_status}
        onChange={handleChange}
        required
    >

        <option value="">Select</option>

        <option>Offer Sent</option>

        <option>Offer Accepted</option>

        <option>Offer Declined</option>

    </select>

</div>
                            <div className="col-md-6 mb-3">

                                <label>Joining Date</label>

                                <input
                                    type="date"
                                    className="form-control"
                                    name="joining_date"
                                    value={form.joining_date}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="col-md-6 mb-3">

                                <label>Mentor</label>

                                <input
                                    className="form-control"
                                    name="mentor"
                                    value={form.mentor}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-3 mb-3">

                                <select
    className="form-control"
    name="training_status"
    value={form.training_status}
    onChange={handleChange}
>
    <option value="">Select</option>
    <option>Not Started</option>
    <option>In Progress</option>
    <option>Completed</option>
</select>

                            </div>
<div className="row mt-3">

    <div className="col-md-4">

        <div className="form-check">

            <input
                type="checkbox"
                className="form-check-input"
                checked={form.documents_uploaded}
                onChange={(e)=>
                    setForm({
                        ...form,
                        documents_uploaded:e.target.checked
                    })
                }
            />

            <label className="form-check-label">

                Documents Uploaded

            </label>

        </div>

    </div>

</div>
                            <div className="col-md-3 mb-3">

                                <select
    className="form-control"
    name="welcome_kit"
    value={form.welcome_kit}
    onChange={handleChange}
>
    <option value="">Select</option>
    <option>Pending</option>
    <option>Issued</option>
</select>

                            </div>
                            <div className="col-md-6 mb-3">

    <label>Status</label>

    <select
        className="form-control"
        name="status"
        value={form.status}
        onChange={handleChange}
        required
    >

        <option value="">Select</option>

        <option>Pending</option>

        <option>In Progress</option>

        <option>Completed</option>

    </select>

</div>


                        </div>

                        <button className="btn btn-primary">

                            Save Record

                        </button>

                    </form>

                </div>

            </div>

            <div className="card shadow">

                <div className="card-header bg-dark text-white">

                    Onboarding Records

                </div>

                <div className="card-body">

                    <table className="table table-bordered table-hover">

                        <thead>

                            <tr>

                                <th>Employee</th>
                                <th>Joining Date</th>
                                <th>Mentor</th>
                                <th>Training</th>
                                <th>Welcome Kit</th>
                                <th>Action</th>

                            </tr>

                        </thead>

                        <tbody>

                            {

                                records.length === 0 ? (

                                    <tr>

                                        <td
                                            colSpan="6"
                                            className="text-center"
                                        >

                                            No onboarding records found.

                                        </td>

                                    </tr>

                                ) : (

                                    records.map(record => (

                                        <tr key={record.id}>

                                            <td>{record.employee}</td>

                                            <td>{record.joining_date}</td>

                                            <td>{record.mentor}</td>

                                            <td>{record.training_status}</td>

                                            <td>{record.welcome_kit}</td>

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

        </Layout>

    );

}

export default Onboarding;