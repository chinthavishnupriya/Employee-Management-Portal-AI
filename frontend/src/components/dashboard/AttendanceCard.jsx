function AttendanceCard({ attendance }) {

    return (

        <div className="card border-0 shadow h-100">

            <div className="card-header bg-primary text-white">

                Today's Attendance

            </div>

            <div className="card-body">

                <h4 className="text-success">

                    {attendance.status}

                </h4>

                <hr />

                <p>

                    <strong>Check In:</strong>

                    {" "}

                    {attendance.check_in || "--"}

                </p>

                <p>

                    <strong>Check Out:</strong>

                    {" "}

                    {attendance.check_out || "--"}

                </p>

            </div>

        </div>

    );

}

export default AttendanceCard;