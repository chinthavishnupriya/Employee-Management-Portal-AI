function TodayStatus({ attendance }) {

    return (

        <div className="card border-0 shadow mb-4">

            <div className="card-header bg-success text-white">

                Today's Attendance

            </div>

            <div className="card-body">

                <div className="row text-center">

                    <div className="col-md-6">

                        <h5>Check In</h5>

                        <h4>

                            {attendance?.check_in || "--"}

                        </h4>

                    </div>

                    <div className="col-md-6">

                        <h5>Check Out</h5>

                        <h4>

                            {attendance?.check_out || "--"}

                        </h4>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default TodayStatus;