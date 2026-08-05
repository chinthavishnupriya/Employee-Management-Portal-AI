function PayrollCard({ payroll }) {

    return (

        <div className="card shadow border-0 mb-4">

            <div className="card-header bg-success text-white d-flex justify-content-between">

                <strong>

                    💰 Net Salary

                </strong>

                <strong>

                    ₹ {payroll.net_salary}

                </strong>

            </div>

            <div className="card-body">

                <div className="row">

                    <div className="col-md-6 mb-3">

                        <strong>

                            Pay Date

                        </strong>

                        <br />

                        {payroll.pay_date}

                    </div>

                </div>

                <hr />

                <div className="row">

                    <div className="col-md-6 mb-3">

                        <strong>Basic Salary</strong>

                        <br />

                        ₹ {payroll.basic_salary}

                    </div>

                    <div className="col-md-6 mb-3">

                        <strong>Bonus</strong>

                        <br />

                        ₹ {payroll.bonus}

                    </div>

                    <div className="col-md-6">

                        <strong>Allowances</strong>

                        <br />

                        ₹ {payroll.allowances}

                    </div>

                    <div className="col-md-6">

                        <strong>Deductions</strong>

                        <br />

                        ₹ {payroll.deductions}

                    </div>

                </div>

            </div>

        </div>

    );

}

export default PayrollCard;