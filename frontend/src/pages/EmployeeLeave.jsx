import { useEffect, useState } from "react";

import EmployeeLayout from "../components/EmployeeLayout";
import LeaveBalance from "../components/leave/LeaveBalance";
import LeaveHistoryCard from "../components/leave/LeaveHistoryCard";

import {
    applyLeave,
    getMyLeaves,
    cancelLeave
} from "../services/employeeLeaveService";

function EmployeeLeave() {

    const [leaves, setLeaves] = useState([]);

    const [form, setForm] = useState({
        leave_type: "",
        start_date: "",
        end_date: "",
        reason: ""
    });

    useEffect(() => {

        loadLeaves();

    }, []);

    async function loadLeaves() {

        try {

            const data = await getMyLeaves();

            setLeaves(data);

        }

        catch {

            alert("Unable to load leave history.");

        }

    }

    async function handleSubmit(e) {

        e.preventDefault();

        try {

            await applyLeave(form);

            alert("Leave Applied Successfully");

            setForm({

                leave_type: "",
                start_date: "",
                end_date: "",
                reason: ""

            });

            loadLeaves();

        }

        catch {

            alert("Unable to apply leave.");

        }

    }

    async function handleCancel(id) {

        if (!window.confirm("Cancel this leave request?")) {

            return;

        }

        try {

            await cancelLeave(id);

            alert("Leave Cancelled Successfully");

            loadLeaves();

        }

        catch {

            alert("Unable to cancel leave.");

        }

    }

    return (

        <EmployeeLayout>

            <h2 className="mb-4">

                My Leave

            </h2>

            <hr />

            {/* Leave Balance */}

            <LeaveBalance

                summary={{

                    annual: 10,

                    casual: 5,

                    medical: 7

                }}

            />

            {/* Apply Leave */}

            <div className="card shadow border-0 mb-5">

                <div className="card-header bg-primary text-white">

                    Apply Leave

                </div>

                <div className="card-body">

                    <form onSubmit={handleSubmit}>

                        <div className="mb-3">

                            <label className="form-label">

                                Leave Type

                            </label>

                            <input

                                className="form-control"

                                placeholder="Annual / Casual / Medical"

                                value={form.leave_type}

                                onChange={(e) =>

                                    setForm({

                                        ...form,

                                        leave_type: e.target.value

                                    })

                                }

                                required

                            />

                        </div>

                        <div className="row">

                            <div className="col-md-6 mb-3">

                                <label className="form-label">

                                    Start Date

                                </label>

                                <input

                                    type="date"

                                    className="form-control"

                                    value={form.start_date}

                                    onChange={(e) =>

                                        setForm({

                                            ...form,

                                            start_date: e.target.value

                                        })

                                    }

                                    required

                                />

                            </div>

                            <div className="col-md-6 mb-3">

                                <label className="form-label">

                                    End Date

                                </label>

                                <input

                                    type="date"

                                    className="form-control"

                                    value={form.end_date}

                                    onChange={(e) =>

                                        setForm({

                                            ...form,

                                            end_date: e.target.value

                                        })

                                    }

                                    required

                                />

                            </div>

                        </div>

                        <div className="mb-3">

                            <label className="form-label">

                                Reason

                            </label>

                            <textarea

                                className="form-control"

                                rows="4"

                                placeholder="Reason for leave"

                                value={form.reason}

                                onChange={(e) =>

                                    setForm({

                                        ...form,

                                        reason: e.target.value

                                    })

                                }

                                required

                            />

                        </div>

                        <button

                            type="submit"

                            className="btn btn-primary"

                        >

                            Apply Leave

                        </button>

                    </form>

                </div>

            </div>

            {/* Leave History */}

            <h4 className="mb-4">

                My Leave Requests

            </h4>

            {

                leaves.length === 0 ? (

                    <div className="card shadow border-0">

                        <div className="card-body text-center p-5">

                            <h2>🏖</h2>

                            <h4>

                                No Leave Requests

                            </h4>

                            <p className="text-muted">

                                You haven't applied for any leave yet.

                            </p>

                        </div>

                    </div>

                ) : (

                    leaves.map((leave) => (

                        <LeaveHistoryCard

                            key={leave.id}

                            leave={leave}

                            onCancel={handleCancel}

                        />

                    ))

                )

            }

        </EmployeeLayout>

    );

}

export default EmployeeLeave;