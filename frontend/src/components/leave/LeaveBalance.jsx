function LeaveBalance({ summary }) {

    const cards = [

        {
            title: "Annual Leave",
            value: summary?.annual || 0,
            color: "primary"
        },

        {
            title: "Casual Leave",
            value: summary?.casual || 0,
            color: "success"
        },

        {
            title: "Medical Leave",
            value: summary?.medical || 0,
            color: "danger"
        }

    ];

    return (

        <div className="row mb-4">

            {

                cards.map((card, index) => (

                    <div
                        className="col-md-4"
                        key={index}
                    >

                        <div className={`card bg-${card.color} text-white shadow border-0`}>

                            <div className="card-body text-center">

                                <h5>{card.title}</h5>

                                <h2>{card.value}</h2>

                                <small>Days Remaining</small>

                            </div>

                        </div>

                    </div>

                ))

            }

        </div>

    );

}

export default LeaveBalance;