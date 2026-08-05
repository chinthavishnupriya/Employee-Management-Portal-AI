function AttendanceHistory({ history }) {

    return (

        <div className="card border-0 shadow">

            <div className="card-header bg-dark text-white">

                Attendance History

            </div>

            <div className="card-body">

                <table className="table table-hover">

                    <thead>

                        <tr>

                            <th>Date</th>

                            <th>Status</th>

                            <th>Check In</th>

                            <th>Check Out</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            history.map((item) => (

                                <tr key={item.id}>

                                    <td>{item.date}</td>

                                    <td>{item.status}</td>

                                    <td>{item.check_in}</td>

                                    <td>{item.check_out}</td>

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

            </div>

        </div>

    );

}

export default AttendanceHistory;