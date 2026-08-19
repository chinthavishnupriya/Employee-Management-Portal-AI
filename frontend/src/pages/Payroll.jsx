import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import {
    createPayroll,
    getPayrolls
} from "../services/payrollService";

function Payroll() {

    const [payrolls, setPayrolls] = useState([]);

    const [form, setForm] = useState({
        employee_id: "",
        basic_salary: "",
        bonus: "",
        allowances: "",
        deductions: "",
        pay_date: ""
    });

    useEffect(() => {
        loadPayrolls();
    }, []);

    async function loadPayrolls() {

        try {

            const data = await getPayrolls();

            setPayrolls(data);

        } catch (error) {

            console.error(error);

            alert("Unable to load payrolls");

        }

    }

    function handleChange(e) {

        setForm({
            ...form,
            [e.target.name]: e.target.value
        });

    }

    async function handleSubmit(e) {

        e.preventDefault();

        const basic = Number(form.basic_salary);
        const bonus = Number(form.bonus);
        const allowances = Number(form.allowances);
        const deductions = Number(form.deductions);

        try {

            await createPayroll({

                employee_id: Number(form.employee_id),

                basic_salary: basic,

                bonus: bonus,

                allowances: allowances,

                deductions: deductions,

                net_salary:
                    basic +
                    bonus +
                    allowances -
                    deductions,

                pay_date: form.pay_date

            });

            alert("Payroll Created Successfully");

            setForm({

                employee_id: "",
                basic_salary: "",
                bonus: "",
                allowances: "",
                deductions: "",
                pay_date: ""

            });

            loadPayrolls();

        } catch (error) {

            console.error(error);

            alert("Unable to create payroll");

        }

    }

    return (

        <Layout>

            <h2 className="mb-4">
                Payroll Management
            </h2>

            <div className="card shadow mb-4">

                <div className="card-header">
                    <h5>Create Payroll</h5>
                </div>

                <div className="card-body">

                    <form onSubmit={handleSubmit}>

                        <div className="row">

                            <div className="col-md-4 mb-3">

                                <label>Employee ID</label>

                                <input
                                    className="form-control"
                                    name="employee_id"
                                    value={form.employee_id}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="col-md-4 mb-3">

                                <label>Basic Salary</label>

                                <input
                                    type="number"
                                    className="form-control"
                                    name="basic_salary"
                                    value={form.basic_salary}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="col-md-4 mb-3">

                                <label>Bonus</label>

                                <input
                                    type="number"
                                    className="form-control"
                                    name="bonus"
                                    value={form.bonus}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-4 mb-3">

                                <label>Allowances</label>

                                <input
                                    type="number"
                                    className="form-control"
                                    name="allowances"
                                    value={form.allowances}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-4 mb-3">

                                <label>Deductions</label>

                                <input
                                    type="number"
                                    className="form-control"
                                    name="deductions"
                                    value={form.deductions}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="col-md-4 mb-3">

                                <label>Pay Date</label>

                                <input
                                    type="date"
                                    className="form-control"
                                    name="pay_date"
                                    value={form.pay_date}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                        </div>

                        <button
                            className="btn btn-primary"
                        >
                            Create Payroll
                        </button>

                    </form>

                </div>

            </div>

            <div className="card shadow">

                <div className="card-header">
                    <h5>Payroll Records</h5>
                </div>

                <div className="card-body">

                    <table className="table table-bordered">

                        <thead>

                            <tr>

                                <th>ID</th>
                                <th>Employee</th>
                                <th>Department</th>
                                <th>Basic</th>
                                <th>Bonus</th>
                                <th>Allowances</th>
                                <th>Deductions</th>
                                <th>Net Salary</th>
                                <th>Pay Date</th>

                            </tr>

                        </thead>

                        <tbody>

                            {

                                payrolls.map((payroll) => (

                                    <tr key={payroll.id}>

                                        <td>{payroll.id}</td>

                                        <td>{payroll.employee}</td>

                                        <td>{payroll.department}</td>

                                        <td>₹ {payroll.basic_salary}</td>

                                        <td>₹ {payroll.bonus}</td>

                                        <td>₹ {payroll.allowances}</td>

                                        <td>₹ {payroll.deductions}</td>

                                        <td>
                                            <strong>
                                                ₹ {payroll.net_salary}
                                            </strong>
                                        </td>

                                        <td>{payroll.pay_date}</td>

                                    </tr>

                                ))

                            }

                        </tbody>

                    </table>

                </div>

            </div>

        </Layout>

    );

}

export default Payroll;