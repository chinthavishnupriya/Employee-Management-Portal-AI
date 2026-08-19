import { useState } from "react";
import Layout from "../components/Layout";

function Settings() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleTheme = () => {
    setDarkMode(!darkMode);

    document.body.className = darkMode
      ? "bg-white text-dark"
      : "bg-dark text-white";
  };

  return (
    <Layout>

      <h2 className="mb-4">Settings</h2>

      <div className="card shadow">

        <div className="card-body">

          <h5>Appearance</h5>

          <button
            className="btn btn-primary mb-3"
            onClick={toggleTheme}
          >
            {darkMode ? "Light Mode" : "Dark Mode"}
          </button>

          <hr />

          <h5>Application</h5>

          <p>
            Employee Management Portal
          </p>

          <p>
            Version: 1.0.0
          </p>

          <p>
            Developed using React, FastAPI & PostgreSQL.
          </p>

        </div>

      </div>

    </Layout>
  );
}

export default Settings;