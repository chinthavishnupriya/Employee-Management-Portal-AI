import {
    FaPlaneDeparture,
    FaFileAlt,
    FaStar,
    FaUserPlus,
    FaUserMinus,
    FaArrowRight
} from "react-icons/fa";

function PendingTasks() {

    const tasks = [

        {
            title: "Leave Requests",
            count: 2,
            color: "warning",
            icon: <FaPlaneDeparture />
        },

        {
            title: "Pending Documents",
            count: 5,
            color: "danger",
            icon: <FaFileAlt />
        },

        {
            title: "Performance Reviews",
            count: 3,
            color: "primary",
            icon: <FaStar />
        },

        {
            title: "Onboarding",
            count: 1,
            color: "success",
            icon: <FaUserPlus />
        },

        {
            title: "Offboarding",
            count: 1,
            color: "secondary",
            icon: <FaUserMinus />
        }

    ];

    return (

        <div className="card border-0 shadow rounded-4 h-100">

            <div className="card-header bg-white border-0">

                <h5 className="fw-bold">

                    📋 Pending Tasks

                </h5>

            </div>

            <div className="card-body">

                {

                    tasks.map((task, index) => (

                        <div
                            key={index}
                            className="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom"
                        >

                            <div className="d-flex align-items-center">

                                <div
                                    className={`bg-${task.color} text-white rounded-circle d-flex justify-content-center align-items-center me-3`}
                                    style={{
                                        width: "45px",
                                        height: "45px"
                                    }}
                                >

                                    {task.icon}

                                </div>

                                <div>

                                    <strong>

                                        {task.title}

                                    </strong>

                                    <br />

                                    <small className="text-muted">

                                        Needs Attention

                                    </small>

                                </div>

                            </div>

                            <div className="text-end">

                                <span
                                    className={`badge bg-${task.color} fs-6`}
                                >

                                    {task.count}

                                </span>

                                <br />

                                <FaArrowRight className="mt-2 text-secondary" />

                            </div>

                        </div>

                    ))

                }

            </div>

        </div>

    );

}

export default PendingTasks;