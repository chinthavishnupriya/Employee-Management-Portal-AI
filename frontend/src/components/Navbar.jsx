import { Link } from "react-router-dom";

function Navbar() {
    return (
        <nav
            className="navbar navbar-expand-lg navbar-dark shadow-sm"
            style={{
                background: "linear-gradient(90deg,#2563eb,#1e3a8a)"
            }}
        >
            <div className="container">

                {/* Logo */}
                <Link
                    className="navbar-brand fw-bold fs-3"
                    to="/"
                >
                    Employee Management Portal
                </Link>

                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div
                    className="collapse navbar-collapse"
                    id="navbarNav"
                >

                    <ul className="navbar-nav ms-auto align-items-lg-center">

                        <li className="nav-item">
                            <a
                                className="nav-link text-white"
                                href="#home"
                            >
                                Home
                            </a>
                        </li>

                        <li className="nav-item">
                            <a
                                className="nav-link text-white"
                                href="#features"
                            >
                                Features
                            </a>
                        </li>

                        <li className="nav-item">
                            <a
                                className="nav-link text-white"
                                href="#about"
                            >
                                About
                            </a>
                        </li>

                        <li className="nav-item">
                            <a
                                className="nav-link text-white"
                                href="#contact"
                            >
                                Contact
                            </a>
                        </li>

                        <li className="nav-item ms-lg-3">
                            <Link
                                to="/login"
                                className="btn btn-light fw-bold px-4"
                            >
                                Login
                            </Link>
                        </li>

                    </ul>

                </div>

            </div>
        </nav>
    );
}

export default Navbar;