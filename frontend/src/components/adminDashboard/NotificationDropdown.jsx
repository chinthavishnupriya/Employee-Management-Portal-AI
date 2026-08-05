import {
    FaPlaneDeparture,
    FaUserPlus,
    FaFileAlt,
    FaStar
} from "react-icons/fa";

function NotificationDropdown() {

    const notifications = [

        {
            icon: <FaPlaneDeparture />,
            title: "Leave Request",
            message: "Harshita applied for leave.",
            color: "warning"
        },

        {
            icon: <FaUserPlus />,
            title: "New Employee",
            message: "Rahul joined the IT Department.",
            color: "success"
        },

        {
            icon: <FaFileAlt />,
            title: "Document Uploaded",
            message: "Shyam uploaded Aadhaar.",
            color: "primary"
        },

        {
            icon: <FaStar />,
            title: "Performance Review",
            message: "2 reviews are pending.",
            color: "danger"
        }

    ];

    return (

        <div
            className="card shadow border-0"
            style={{
                width: "320px",
                position: "absolute",
                top: "65px",
                right: "0",
                zIndex: "1000"
            }}
        >

            <div className="card-header bg-primary text-white">

                <strong>Notifications</strong>

            </div>

            <div className="card-body p-0">

                {

                    notifications.map((item, index) => (

                        <div
                            key={index}
                            className="d-flex p-3 border-bottom"
                        >

                            <div
                                className={`text-${item.color} fs-4 me-3`}
                            >

                                {item.icon}

                            </div>

                            <div>

                                <strong>

                                    {item.title}

                                </strong>

                                <br />

                                <small>

                                    {item.message}

                                </small>

                            </div>

                        </div>

                    ))

                }

            </div>

        </div>

    );

}

export default NotificationDropdown;