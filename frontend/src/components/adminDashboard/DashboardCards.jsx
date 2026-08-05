import {
    FaUsers,
    FaBuilding,
    FaCalendarCheck,
    FaPlaneDeparture,
    FaMoneyCheckAlt,
    FaStar,
    FaFileAlt,
    FaUserPlus,
    FaUserMinus
} from "react-icons/fa";

function DashboardCards({ dashboard }) {

    const cards = [

        {
            title: "Employees",
            value: dashboard.total_employees ?? 0,
            color: "primary",
            icon: <FaUsers />
        },

        {
            title: "Departments",
            value: dashboard.total_departments ?? 0,
            color: "success",
            icon: <FaBuilding />
        },

        {
            title: "Present Today",
            value: dashboard.total_attendance ?? 0,
            color: "warning",
            icon: <FaCalendarCheck />
        },

        {
            title: "Leave Requests",
            value: dashboard.total_leave_requests ?? 0,
            color: "danger",
            icon: <FaPlaneDeparture />
        },

        {
            title: "Payroll",
            value: dashboard.total_payroll_records ?? 0,
            color: "info",
            icon: <FaMoneyCheckAlt />
        },

        {
            title: "Performance",
            value: dashboard.total_performance ?? 0,
            color: "secondary",
            icon: <FaStar />
        },

        {
            title: "Documents",
            value: dashboard.total_documents ?? 0,
            color: "dark",
            icon: <FaFileAlt />
        },

        {
            title: "Onboarding",
            value: dashboard.total_onboarding ?? 0,
            color: "success",
            icon: <FaUserPlus />
        },

        {
            title: "Offboarding",
            value: dashboard.total_offboarding ?? 0,
            color: "danger",
            icon: <FaUserMinus />
        }

    ];

    return (

        <div className="row">

            {
                cards.map((card, index) => (

                    <div
                        className="col-xl-4 col-lg-4 col-md-6 mb-4"
                        key={index}
                    >

                        <div className={`card border-0 shadow rounded-4 bg-${card.color} text-white`}>

                            <div className="card-body">

                                <div className="d-flex justify-content-between align-items-center">

                                    <div>

                                        <h6>{card.title}</h6>

                                        <h2 className="fw-bold">
                                            {card.value}
                                        </h2>

                                        <small>
                                            Updated Today
                                        </small>

                                    </div>

                                    <div
                                        style={{
                                            fontSize: "42px"
                                        }}
                                    >
                                        {card.icon}
                                    </div>

                                </div>

                            </div>

                        </div>

                    </div>

                ))
            }

        </div>

    );

}

export default DashboardCards;