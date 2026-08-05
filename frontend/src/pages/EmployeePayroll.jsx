import { useEffect, useState } from "react";

import EmployeeLayout from "../components/EmployeeLayout";
import PayrollCard from "../components/payroll/PayrollCard";

import { getMyPayroll } from "../services/payrollService";

function EmployeePayroll() {

    const [payrolls, setPayrolls] = useState([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadPayroll();

    }, []);

    async function loadPayroll() {

        try {

            const data = await getMyPayroll();

            setPayrolls(data);

        }

        catch (error) {

            console.error(error);

            alert("Unable to load payroll.");

        }

        finally {

            setLoading(false);

        }

    }

    if (loading) {

        return (

            <EmployeeLayout>

                <div className="text-center mt-5">

                    <div className="spinner-border text-success"></div>

                    <h5 className="mt-3">

                        Loading Payroll...

                    </h5>

                </div>

            </EmployeeLayout>

        );

    }

    return (

        <EmployeeLayout>

            <h2 className="mb-4">

                My Payroll

            </h2>

            <hr />

            {

                payrolls.length === 0 ? (

                    <div className="card shadow border-0">

                        <div className="card-body text-center p-5">

                            <h2>

                                💰

                            </h2>

                            <h4>

                                No Payroll Records

                            </h4>

                            <p className="text-muted">

                                Payroll has not been generated yet.

                            </p>

                        </div>

                    </div>

                ) : (

                    payrolls.map((payroll) => (

                        <PayrollCard

                            key={payroll.id}

                            payroll={payroll}

                        />

                    ))

                )

            }

        </EmployeeLayout>

    );

}

export default EmployeePayroll;