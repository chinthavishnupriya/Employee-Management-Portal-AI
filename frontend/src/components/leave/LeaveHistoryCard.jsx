function LeaveHistoryCard({

    leave,

    onCancel

}) {

    const badge =

        leave.status === "Approved"

            ? "success"

            : leave.status === "Rejected"

            ? "danger"

            : "warning";

    return (

        <div className="card shadow border-0 mb-3">

            <div className="card-body">

                <div className="d-flex justify-content-between">

                    <h5>

                        {leave.leave_type}

                    </h5>

                    <span
                        className={`badge bg-${badge}`}
                    >

                        {leave.status}

                    </span>

                </div>

                <hr />

                <div className="row">

                    <div className="col-md-6">

                        <strong>

                            Start Date

                        </strong>

                        <br />

                        {leave.start_date}

                    </div>

                    <div className="col-md-6">

                        <strong>

                            End Date

                        </strong>

                        <br />

                        {leave.end_date}

                    </div>

                </div>

                <br />

                <strong>

                    Reason

                </strong>

                <div
                    className="border rounded p-3 mt-2 bg-light"
                >

                    {leave.reason}

                </div>

                {

                    leave.status === "Pending"

                    &&

                    <div className="text-end mt-3">

                        <button

                            className="btn btn-danger"

                            onClick={() =>
                                onCancel(leave.id)
                            }

                        >

                            Cancel Request

                        </button>

                    </div>

                }

            </div>

        </div>

    );

}

export default LeaveHistoryCard;