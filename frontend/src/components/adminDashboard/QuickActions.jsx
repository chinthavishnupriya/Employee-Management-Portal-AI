import {
    FaUserPlus,
    FaBuilding,
    FaMoneyCheckAlt,
    FaPlaneDeparture,
    FaChartBar,
    FaStar
} from "react-icons/fa";

function QuickActions() {

    const actions = [

        {
            title: "Add Employee",
            icon: <FaUserPlus />,
            color: "primary"
        },

        {
            title: "Add Department",
            icon: <FaBuilding />,
            color: "success"
        },

        {
            title: "Process Payroll",
            icon: <FaMoneyCheckAlt />,
            color: "warning"
        },

        {
            title: "Approve Leave",
            icon: <FaPlaneDeparture />,
            color: "danger"
        },

        {
            title: "Generate Report",
            icon: <FaChartBar />,
            color: "info"
        },

        {
            title: "Performance Review",
            icon: <FaStar />,
            color: "secondary"
        }

    ];

    return (

        <div className="card shadow rounded-4 border-0 h-100">

            <div className="card-header bg-white border-0">

                <h5 className="fw-bold">

                    ⚡ Quick Actions

                </h5>

            </div>

            <div className="card-body">

                <div className="row">

                    {

                        actions.map((action, index) => (

                            <div
                                className="col-md-6 mb-3"
                                key={index}
                            >

                                <button
                                    className={`btn btn-${action.color} w-100 py-3 rounded-3`}
                                >

                                    <div className="fs-3 mb-2">

                                        {action.icon}

                                    </div>

                                    {action.title}

                                </button>

                            </div>

                        ))

                    }

                </div>

            </div>

        </div>

    );

}

export default QuickActions;