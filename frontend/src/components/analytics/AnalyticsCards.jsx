import {
    FaUsers,
    FaBuilding,
    FaCalendarCheck,
    FaMoneyCheckAlt,
    FaChartLine,
    FaPlaneDeparture
} from "react-icons/fa";

function AnalyticsCards() {

    const cards = [

        {
            title: "Employees",
            value: 156,
            icon: <FaUsers />,
            color: "primary"
        },

        {
            title: "Departments",
            value: 8,
            icon: <FaBuilding />,
            color: "success"
        },

        {
            title: "Attendance %",
            value: "92%",
            icon: <FaCalendarCheck />,
            color: "warning"
        },

        {
            title: "Monthly Payroll",
            value: "₹18.5L",
            icon: <FaMoneyCheckAlt />,
            color: "info"
        },

        {
            title: "Performance",
            value: "89%",
            icon: <FaChartLine />,
            color: "secondary"
        },

        {
            title: "Leave Rate",
            value: "6%",
            icon: <FaPlaneDeparture />,
            color: "danger"
        }

    ];

    return (

        <div className="row">

            {cards.map((card, index) => (

                <div className="col-lg-4 col-md-6 mb-4" key={index}>

                    <div className={`card bg-${card.color} text-white shadow border-0`}>

                        <div className="card-body">

                            <div className="d-flex justify-content-between align-items-center">

                                <div>

                                    <h6>{card.title}</h6>

                                    <h3>{card.value}</h3>

                                </div>

                                <div style={{ fontSize: "40px" }}>

                                    {card.icon}

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            ))}

        </div>

    );

}

export default AnalyticsCards;