function WelcomeBanner({ employee }) {

    const hour = new Date().getHours();

    let greeting = "Good Evening";

    if (hour < 12) {
        greeting = "Good Morning";
    } else if (hour < 17) {
        greeting = "Good Afternoon";
    }

    const today = new Date().toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        }
    );

    return (

        <div
            className="card border-0 shadow mb-4"
            style={{
                borderRadius: "20px",
                background:
                    "linear-gradient(135deg,#2563EB,#1D4ED8)",
                color: "white"
            }}
        >

            <div className="card-body p-4">

                <h2 className="fw-bold">

                    {greeting},

                    {" "}

                    {employee.full_name}

                    👋

                </h2>

                <h5 className="mb-3">

                    {employee.designation}

                </h5>

                <p>

                    Welcome back to the Employee Management Portal.

                </p>

                <small>

                    {today}

                </small>

            </div>

        </div>

    );

}

export default WelcomeBanner;
