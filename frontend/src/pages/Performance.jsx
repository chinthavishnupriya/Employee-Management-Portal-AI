import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
    getPerformance,
    createPerformance,
    deletePerformance
} from "../services/performanceService";

import { getEmployees } from "../services/employeeService";

function Performance() {

    const [reviews, setReviews] = useState([]);
    const [employees, setEmployees] = useState([]);

    const [form, setForm] = useState({
        employee_id: "",
        rating: "",
        reviewer: "",
        promotion_status: "",
        goals: "",
        strengths: "",
        weaknesses: "",
        feedback: ""
    });

    useEffect(() => {

        loadData();

    }, []);

    async function loadData() {

        try {

            const reviewData = await getPerformance();
            const employeeData = await getEmployees();

            setReviews(reviewData);
            setEmployees(employeeData);

        }

        catch (error) {

            console.log(error);
            alert("Unable to load performance data.");

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

            await createPerformance(form);

            alert("Performance review added.");

            setForm({
                employee_id: "",
                rating: "",
                reviewer: "",
                promotion_status: "",
                goals: "",
                strengths: "",
                weaknesses: "",
                feedback: ""
            });

            loadData();

        }

        catch (error) {

            console.log(error);
            alert("Unable to create performance review.");

        }

    }

    async function handleDelete(id) {

        if (!window.confirm("Delete this review?")) return;

        await deletePerformance(id);

        loadData();

    }

    return (

        <Layout>

            <h2 className="mb-4">

                Performance Management

            </h2>

            <div className="card shadow mb-4">

                <div className="card-header bg-primary text-white">

                    Add Performance Review

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

                                <label>Rating</label>

                                <input
                                    type="number"
                                    className="form-control"
                                    name="rating"
                                    value={form.rating}
                                    onChange={handleChange}
                                    min="1"
                                    max="10"
                                    required
                                />

                            </div>

                            <div className="col-md-6 mb-3">

                                <label>Reviewer</label>

                                <input
                                    className="form-control"
                                    name="reviewer"
                                    value={form.reviewer}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-6 mb-3">

                                <label>Promotion Status</label>

                                <input
                                    className="form-control"
                                    name="promotion_status"
                                    value={form.promotion_status}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-12 mb-3">

                                <label>Goals</label>

                                <textarea
                                    className="form-control"
                                    rows="2"
                                    name="goals"
                                    value={form.goals}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-6 mb-3">

                                <label>Strengths</label>

                                <textarea
                                    className="form-control"
                                    rows="2"
                                    name="strengths"
                                    value={form.strengths}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-6 mb-3">

                                <label>Weaknesses</label>

                                <textarea
                                    className="form-control"
                                    rows="2"
                                    name="weaknesses"
                                    value={form.weaknesses}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-12 mb-3">

                                <label>Feedback</label>

                                <textarea
                                    className="form-control"
                                    rows="3"
                                    name="feedback"
                                    value={form.feedback}
                                    onChange={handleChange}
                                />

                            </div>

                        </div>

                        <button
                            className="btn btn-primary"
                        >
                            Save Review
                        </button>

                    </form>

                </div>

            </div>

            <div className="card shadow">

                <div className="card-header bg-dark text-white">

                    Performance Reviews

                </div>

                <div className="card-body">

                    <table className="table table-bordered table-hover">

                        <thead>

                            <tr>

                                <th>Employee</th>
                                <th>Rating</th>
                                <th>Reviewer</th>
                                <th>Promotion</th>
                                <th>Action</th>

                            </tr>

                        </thead>

                        <tbody>

                            {

                                reviews.length === 0 ? (

                                    <tr>

                                        <td
                                            colSpan="5"
                                            className="text-center"
                                        >

                                            No Reviews Found

                                        </td>

                                    </tr>

                                ) : (

                                    reviews.map(review => (

                                        <tr key={review.id}>

                                            <td>{review.employee}</td>

                                            <td>{review.rating}/10</td>

                                            <td>{review.reviewer}</td>

                                            <td>{review.promotion_status}</td>

                                            <td>

                                                <button
                                                    className="btn btn-danger btn-sm"
                                                    onClick={() => handleDelete(review.id)}
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

export default Performance;