import Navbar from "../components/navbar";
import Footer from "../components/footer";
import { useEffect, useState } from "react";
import { getHomeData } from "../services/homeService";
function Home() {
    const [home, setHome] = useState(null);

useEffect(() => {

    loadHome();

}, []);

async function loadHome() {

    try {

        const data = await getHomeData();

        setHome(data);

    }

    catch (error) {

        console.log(error);

    }

}
    return (
        <>
            <Navbar />

            <section
                id="home"
                className="container-fluid"
                style={{
                    background:
                        "linear-gradient(135deg,#2563eb,#0f172a)",
                    minHeight: "90vh",
                    color: "white"
                }}
            >
                <div className="container">

                    <div
                        className="row align-items-center"
                        style={{ minHeight: "90vh" }}
                    >

                        <div className="col-lg-6">

                            <h1 className="display-2 fw-bold">
                               {home?.portal_name || "Employee Management Portal"}
                            </h1>

                            <p className="fs-4 mt-4">
                                {home?.hero?.title}
                            </p>

                            <p
                                className="lead mt-3"
                                style={{ maxWidth: "600px" }}
                            >
                                {home?.hero?.subtitle}
                            </p>

                            <a
                                href="/login"
                                className="btn btn-light btn-lg mt-3 me-3"
                            >
                                Get Started
                            </a>

                            <a
                                href="#features"
                                className="btn btn-outline-light btn-lg mt-3"
                            >
                                Learn More
                            </a>

                        </div>

                        <div className="col-lg-6 text-center">

                            <div className="row mt-5">

    <div className="col-md-6 mb-4">
        <div className="card shadow border-0 p-4 h-100">
            <h3>👨‍💼 Employee Management</h3>
            <p>
                Store employee profiles, departments,
                documents and personal information.
            </p>
        </div>
    </div>

    <div className="col-md-6 mb-4">
        <div className="card shadow border-0 p-4 h-100">
            <h3>⏰ Attendance</h3>
            <p>
                Track daily check-in,
                check-out and attendance history.
            </p>
        </div>
    </div>

    <div className="col-md-6 mb-4">
        <div className="card shadow border-0 p-4 h-100">
            <h3>💰 Payroll</h3>
            <p>
                Generate salaries,
                reports and payroll records.
            </p>
        </div>
    </div>

    <div className="col-md-6 mb-4">
        <div className="card shadow border-0 p-4 h-100">
            <h3>🤖 AI Analytics</h3>
            <p>
                Visualize company performance
                using AI-powered insights.
            </p>
        </div>
    </div>

</div>

                        </div>

                    </div>

                </div>

            </section>
{/* ================= Features ================= */}

<section
    id="features"
    className="py-5 bg-light"
>
    <div className="container">

        <div className="text-center mb-5">

            <h2 className="fw-bold">
                Our Features
            </h2>

            <p className="text-muted">
                Everything your organization needs to manage employees efficiently.
            </p>

        </div>

        <div className="row g-4">

            <div className="col-md-4">
                <div className="card shadow border-0 h-100 text-center p-4">

                    <div className="display-4 mb-3">
                        👨‍💼
                    </div>

                    <h4>Employee Management</h4>

                    <p className="text-muted">
                        Add, edit and manage employee records with ease.
                    </p>

                </div>
            </div>

            <div className="col-md-4">
                <div className="card shadow border-0 h-100 text-center p-4">

                    <div className="display-4 mb-3">
                        ⏰
                    </div>

                    <h4>Attendance</h4>

                    <p className="text-muted">
                        Track employee check-in, check-out and attendance history.
                    </p>

                </div>
            </div>

            <div className="col-md-4">
                <div className="card shadow border-0 h-100 text-center p-4">

                    <div className="display-4 mb-3">
                        💰
                    </div>

                    <h4>Payroll</h4>

                    <p className="text-muted">
                        Generate payroll reports and salary records automatically.
                    </p>

                </div>
            </div>

            <div className="col-md-4">
                <div className="card shadow border-0 h-100 text-center p-4">

                    <div className="display-4 mb-3">
                        📈
                    </div>

                    <h4>Performance</h4>

                    <p className="text-muted">
                        Monitor employee performance and growth over time.
                    </p>

                </div>
            </div>

            <div className="col-md-4">
                <div className="card shadow border-0 h-100 text-center p-4">

                    <div className="display-4 mb-3">
                        📄
                    </div>

                    <h4>Documents</h4>

                    <p className="text-muted">
                        Store employee documents securely in one place.
                    </p>

                </div>
            </div>

            <div className="col-md-4">
                <div className="card shadow border-0 h-100 text-center p-4">

                    <div className="display-4 mb-3">
                        🤖
                    </div>

                    <h4>AI Analytics</h4>

                    <p className="text-muted">
                        View intelligent insights through analytics and reports.
                    </p>

                </div>
            </div>

        </div>

    </div>
</section>
{/* ================= Statistics ================= */}

<section
    className="py-5"
    style={{
        background: "#0f172a",
        color: "white"
    }}
>

    <div className="container">

        <div className="text-center mb-5">

            <h2 className="fw-bold">

                Portal Statistics

            </h2>

            <p className="text-light">

                Powerful HR management trusted by organizations.

            </p>

        </div>

        <div className="row text-center">

            <div className="col-md-3 mb-4">

                <h1 className="display-4 fw-bold text-info">

                    {home?.statistics?.employees ?? 0}

                </h1>

                <h5>

                    Employees

                </h5>

            </div>

            <div className="col-md-3 mb-4">

                <h1 className="display-4 fw-bold text-success">

                    {home?.statistics?.departments ?? 0}

                </h1>

                <h5>

                    Departments

                </h5>

            </div>

            <div className="col-md-3 mb-4">

                <h1 className="display-4 fw-bold text-warning">

                    {home?.statistics?.attendance ?? 0}99%

                </h1>

                <h5>

                    Attendance Accuracy

                </h5>

            </div>

            <div className="col-md-3 mb-4">

                <h1 className="display-4 fw-bold text-danger">

                   {home?.statistics?.leave_requests ?? 0}

                </h1>

                <h5>

                    System Availability

                </h5>

            </div>

        </div>

    </div>

</section>
{/* ================= Why Choose Us ================= */}

<section
    id="about"
    className="py-5 bg-white"
>

    <div className="container">

        <div className="text-center mb-5">

            <h2 className="fw-bold">

                Why Choose Our Portal?

            </h2>

            <p className="text-muted">

                Built for organizations that need a secure, scalable and efficient HR management solution.

            </p>

        </div>

        <div className="row g-4">

            <div className="col-md-4">

                <div className="card border-0 shadow h-100 p-4 text-center">

                    <div className="display-4 mb-3">🔒</div>

                    <h4>Secure Authentication</h4>

                    <p className="text-muted">

                        Role-based access ensures administrators and employees only access authorized features.

                    </p>

                </div>

            </div>

            <div className="col-md-4">

                <div className="card border-0 shadow h-100 p-4 text-center">

                    <div className="display-4 mb-3">⚡</div>

                    <h4>Fast Performance</h4>

                    <p className="text-muted">

                        Optimized workflows help HR teams complete daily tasks efficiently.

                    </p>

                </div>

            </div>

            <div className="col-md-4">

                <div className="card border-0 shadow h-100 p-4 text-center">

                    <div className="display-4 mb-3">🤖</div>

                    <h4>AI Insights</h4>

                    <p className="text-muted">

                        Analyze workforce data and generate meaningful reports with AI-powered analytics.

                    </p>

                </div>

            </div>

            <div className="col-md-4">

                <div className="card border-0 shadow h-100 p-4 text-center">

                    <div className="display-4 mb-3">☁️</div>

                    <h4>Cloud Ready</h4>

                    <p className="text-muted">

                        Designed to support modern deployment and future scalability.

                    </p>

                </div>

            </div>

            <div className="col-md-4">

                <div className="card border-0 shadow h-100 p-4 text-center">

                    <div className="display-4 mb-3">📱</div>

                    <h4>Responsive Design</h4>

                    <p className="text-muted">

                        Works seamlessly across desktops, tablets and mobile devices.

                    </p>

                </div>

            </div>

            <div className="col-md-4">

                <div className="card border-0 shadow h-100 p-4 text-center">

                    <div className="display-4 mb-3">🛡️</div>

                    <h4>Data Protection</h4>

                    <p className="text-muted">

                        Employee records are managed with secure access and organized storage.

                    </p>

                </div>

            </div>

        </div>

    </div>

</section>
{/* ================= Dashboard Preview ================= */}

<section className="py-5 bg-light">

    <div className="container">

        <div className="text-center mb-5">

            <h2 className="fw-bold">

                Dashboard Preview

            </h2>

            <p className="text-muted">

                Explore the intuitive dashboards designed for administrators and employees.

            </p>

        </div>

        <div className="row justify-content-center mt-4">

    {/* Admin Dashboard */}

    <div className="col-lg-5 col-md-6 mb-4">

        <div className="card shadow border-0 h-100">

            <img
                src="/images/admin-dashboard.jpg"
                className="card-img-top"
                alt="Admin Dashboard"
                style={{
                    height: "260px",
                    objectFit: "cover"
                }}
            />

            <div className="card-body">

                <h4 className="fw-bold">
                    Admin Dashboard
                </h4>

                <p className="text-muted">
                    Manage employees, payroll,
                    departments, reports and analytics.
                </p>

            </div>

        </div>

    </div>

    {/* Employee Dashboard */}

    <div className="col-lg-5 col-md-6 mb-4">

        <div className="card shadow border-0 h-100">

            <img
                src="/images/employee-dashboard.jpg"
                className="card-img-top"
                alt="Employee Dashboard"
                style={{
                    height: "260px",
                    objectFit: "cover"
                }}
            />

            <div className="card-body">

                <h4 className="fw-bold">
                    Employee Dashboard
                </h4>

                <p className="text-muted">
                    Attendance, leave requests,
                    documents, payroll and profile management.
                </p>

            </div>

        </div>

    </div>

</div>

    </div>

</section>
{/* ================= Testimonials ================= */}

<section className="py-5 bg-white">

    <div className="container">

        <div className="text-center mb-5">

            <h2 className="fw-bold">

                What Organizations Say

            </h2>

            <p className="text-muted">

                Feedback from organizations using our HR Management Platform.

            </p>

        </div>

        <div className="row g-4">

            <div className="col-lg-4">

                <div className="card shadow border-0 h-100 p-4">

                    <h5 className="fw-bold">

                        Rahul Sharma

                    </h5>

                    <small className="text-primary">

                        HR Manager

                    </small>

                    <hr />

                    <p className="text-muted">

                        "The attendance and payroll modules reduced our manual work significantly."

                    </p>

                </div>

            </div>

            <div className="col-lg-4">

                <div className="card shadow border-0 h-100 p-4">

                    <h5 className="fw-bold">

                        Priya Reddy

                    </h5>

                    <small className="text-primary">

                        Operations Head

                    </small>

                    <hr />

                    <p className="text-muted">

                        "The employee dashboard is intuitive and makes leave management simple."

                    </p>

                </div>

            </div>

            <div className="col-lg-4">

                <div className="card shadow border-0 h-100 p-4">

                    <h5 className="fw-bold">

                        Arjun Kumar

                    </h5>

                    <small className="text-primary">

                        IT Administrator

                    </small>

                    <hr />

                    <p className="text-muted">

                        "Role-based authentication and centralized management improve security."

                    </p>

                </div>

            </div>

        </div>

    </div>

</section>
{/* ================= FAQ ================= */}

<section className="py-5 bg-light">

    <div className="container">

        <div className="text-center mb-5">

            <h2 className="fw-bold">

                Frequently Asked Questions

            </h2>

        </div>

        <div className="accordion" id="faqAccordion">

            <div className="accordion-item">

                <h2 className="accordion-header">

                    <button
                        className="accordion-button"
                        data-bs-toggle="collapse"
                        data-bs-target="#faq1"
                    >
                        Can employees mark attendance online?
                    </button>

                </h2>

                <div
                    id="faq1"
                    className="accordion-collapse collapse show"
                    data-bs-parent="#faqAccordion"
                >

                    <div className="accordion-body">

                        Yes. Employees can securely check in and check out through their dashboard.

                    </div>

                </div>

            </div>

            <div className="accordion-item">

                <h2 className="accordion-header">

                    <button
                        className="accordion-button collapsed"
                        data-bs-toggle="collapse"
                        data-bs-target="#faq2"
                    >
                        Does the system support payroll management?
                    </button>

                </h2>

                <div
                    id="faq2"
                    className="accordion-collapse collapse"
                    data-bs-parent="#faqAccordion"
                >

                    <div className="accordion-body">

                        Yes. Administrators can manage payroll records and salary reports.

                    </div>

                </div>

            </div>

            <div className="accordion-item">

                <h2 className="accordion-header">

                    <button
                        className="accordion-button collapsed"
                        data-bs-toggle="collapse"
                        data-bs-target="#faq3"
                    >
                        Is the portal secure?
                    </button>

                </h2>

                <div
                    id="faq3"
                    className="accordion-collapse collapse"
                    data-bs-parent="#faqAccordion"
                >

                    <div className="accordion-body">

                        Yes. Authentication and role-based authorization protect employee data.

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>
{/* ================= FAQ ================= */}

<section className="py-5 bg-light">

    <div className="container">

        <div className="text-center mb-5">

            <h2 className="fw-bold">

                Frequently Asked Questions

            </h2>

        </div>

        <div className="accordion" id="faqAccordion">

            <div className="accordion-item">

                <h2 className="accordion-header">

                    <button
                        className="accordion-button"
                        data-bs-toggle="collapse"
                        data-bs-target="#faq1"
                    >
                        Can employees mark attendance online?
                    </button>

                </h2>

                <div
                    id="faq1"
                    className="accordion-collapse collapse show"
                    data-bs-parent="#faqAccordion"
                >

                    <div className="accordion-body">

                        Yes. Employees can securely check in and check out through their dashboard.

                    </div>

                </div>

            </div>

            <div className="accordion-item">

                <h2 className="accordion-header">

                    <button
                        className="accordion-button collapsed"
                        data-bs-toggle="collapse"
                        data-bs-target="#faq2"
                    >
                        Does the system support payroll management?
                    </button>

                </h2>

                <div
                    id="faq2"
                    className="accordion-collapse collapse"
                    data-bs-parent="#faqAccordion"
                >

                    <div className="accordion-body">

                        Yes. Administrators can manage payroll records and salary reports.

                    </div>

                </div>

            </div>

            <div className="accordion-item">

                <h2 className="accordion-header">

                    <button
                        className="accordion-button collapsed"
                        data-bs-toggle="collapse"
                        data-bs-target="#faq3"
                    >
                        Is the portal secure?
                    </button>

                </h2>

                <div
                    id="faq3"
                    className="accordion-collapse collapse"
                    data-bs-parent="#faqAccordion"
                >

                    <div className="accordion-body">

                        Yes. Authentication and role-based authorization protect employee data.

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>
{/* ================= CTA ================= */}

<section
    className="py-5 text-center bg-primary text-white"
>

    <div className="container">

        <h2 className="fw-bold">

            Ready to Transform Your HR Management?

        </h2>

        <p className="lead mt-3">

            Join organizations that streamline employee management with our secure platform.

        </p>

        <a
            href="/login"
            className="btn btn-light btn-lg mt-3 px-5"
        >

            Get Started

        </a>

    </div>

</section>
            <Footer />
        </>
    );
}

export default Home;