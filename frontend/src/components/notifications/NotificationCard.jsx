import {
    FaPlaneDeparture,
    FaFileAlt,
    FaBirthdayCake,
    FaMoneyCheckAlt,
    FaUserPlus,
    FaExclamationTriangle
} from "react-icons/fa";

function NotificationCard() {

    const notifications = [

        {
            title: "2 Leave Requests Pending",
            type: "warning",
            icon: <FaPlaneDeparture />
        },

        {
            title: "5 Documents Awaiting Verification",
            type: "danger",
            icon: <FaFileAlt />
        },

        {
            title: "Payroll Processing Tomorrow",
            type: "primary",
            icon: <FaMoneyCheckAlt />
        },

        {
            title: "3 Employee Birthdays This Week",
            type: "success",
            icon: <FaBirthdayCake />
        },

        {
            title: "1 New Employee Joining",
            type: "info",
            icon: <FaUserPlus />
        },

        {
            title: "Attendance Alert Detected",
            type: "secondary",
            icon: <FaExclamationTriangle />
        }

    ];

    return (

        <div className="card shadow border-0 rounded-4">

            <div className="card-header bg-white">

                <h4 className="fw-bold">
                    🔔 HR Notifications
                </h4>

            </div>

            <div className="card-body">

                {

                    notifications.map((item, index) => (

                        <div
                            key={index}
                            className={`alert alert-${item.type} d-flex align-items-center`}
                        >

                            <span className="fs-4 me-3">
                                {item.icon}
                            </span>

                            <strong>
                                {item.title}
                            </strong>

                        </div>

                    ))

                }

            </div>

        </div>

    );

}

export default NotificationCard;