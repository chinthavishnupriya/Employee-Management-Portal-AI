import { useEffect, useState } from "react";

import EmployeeLayout from "../components/EmployeeLayout";

import {
    getMyAttendance,
    getAttendanceSummary,
    checkIn,
    checkOut
} from "../services/employeeAttendanceService";

import TodayStatus from "../components/attendance/TodayStatus";
import AttendanceSummary from "../components/attendance/AttendanceSummary";
import AttendanceHistory from "../components/attendance/AttendanceHistory";

function EmployeeAttendance() {

    const [attendance, setAttendance] = useState(null);

    useEffect(() => {

        loadAttendance();

    }, []);

    async function loadAttendance() {

        try {

            const history = await getMyAttendance();

            const summary = await getAttendanceSummary();

            setAttendance({

                today:

                    history.length > 0

                        ? history[0]

                        : {

                              check_in: "--",

                              check_out: "--"

                          },

                summary: {

                    present: summary.present || 0,

                    absent: summary.absent || 0,

                    leave: summary.leave || 0,

                    late: summary.late || 0

                },

                history: history

            });

        }

        catch (error) {

            console.log(error);

            alert("Unable to load attendance.");

        }

    }
async function handleCheckIn() {

    try {

        const employeeId = localStorage.getItem("employee_id");

        await checkIn(employeeId);

        alert("Checked In Successfully");

        loadAttendance();

    }

    catch (error) {

        console.log(error);

        alert("Unable to Check In");

    }

}

async function handleCheckOut() {

    try {

        const employeeId = localStorage.getItem("employee_id");

        await checkOut(employeeId);

        alert("Checked Out Successfully");

        loadAttendance();

    }

    catch (error) {

        console.log(error);

        alert("Unable to Check Out");

    }

}
    if (!attendance) {

        return (

            <EmployeeLayout>

                <div className="text-center mt-5">

                    <div className="spinner-border text-primary"></div>

                    <h5 className="mt-3">

                        Loading Attendance...

                    </h5>

                </div>

            </EmployeeLayout>

        );

    }

    return (

        <EmployeeLayout>

            <h2 className="mb-4">

                Attendance Dashboard

            </h2>

            <div className="mb-4">

    <button
        className="btn btn-success me-3"
        onClick={handleCheckIn}
    >

        Check In

    </button>

    <button
        className="btn btn-danger"
        onClick={handleCheckOut}
    >

        Check Out

    </button>

</div>

            <AttendanceSummary

                summary={attendance.summary}

            />

            <AttendanceHistory

                history={attendance.history}

            />

        </EmployeeLayout>

    );

}

export default EmployeeAttendance;