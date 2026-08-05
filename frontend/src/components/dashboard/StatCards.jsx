function StatCards({ dashboard }) {

    const cards = [

        {
            title: "Attendance",
            value: dashboard.attendance_count,
            icon: "📅",
            color: "#2563EB"
        },

        {
            title: "Leave",
            value: dashboard.leave_count,
            icon: "🏖️",
            color: "#F59E0B"
        },

        {
            title: "Payroll",
            value: dashboard.payroll_count,
            icon: "💰",
            color: "#16A34A"
        },

        {
            title: "Performance",
            value: dashboard.performance_count,
            icon: "⭐",
            color: "#9333EA"
        }

    ];

    return (

        <div className="row g-4 mb-4">

            {

                cards.map((card, index) => (

                    <div
                        className="col-lg-3 col-md-6"
                        key={index}
                    >

                        <div
                            className="card border-0 shadow h-100"
                            style={{
                                borderRadius: "18px"
                            }}
                        >

                            <div className="card-body text-center">

                                <div
                                    style={{
                                        fontSize: "45px"
                                    }}
                                >
                                    {card.icon}
                                </div>

                                <h5
                                    className="mt-3"
                                    style={{
                                        color: card.color
                                    }}
                                >
                                    {card.title}
                                </h5>

                                <h2>

                                    {card.value}

                                </h2>

                            </div>

                        </div>

                    </div>

                ))

            }

        </div>

    );

}

export default StatCards;