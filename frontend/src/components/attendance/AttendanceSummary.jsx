function AttendanceSummary({ summary }) {

    const cards = [

        {
            title: "Present",
            value: summary.present,
            color: "success"
        },

        {
            title: "Absent",
            value: summary.absent,
            color: "danger"
        },

        {
            title: "Leave",
            value: summary.leave,
            color: "warning"
        },

        {
            title: "Late",
            value: summary.late,
            color: "primary"
        }

    ];

    return (

        <div className="row g-4 mb-4">

            {

                cards.map((card, index) => (

                    <div
                        className="col-md-3"
                        key={index}
                    >

                        <div
                            className={`card border-0 shadow bg-${card.color} text-white`}
                        >

                            <div className="card-body text-center">

                                <h5>

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

export default AttendanceSummary;