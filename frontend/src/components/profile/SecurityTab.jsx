import { Link } from "react-router-dom";

function SecurityTab() {

    return (

        <div className="text-center">

            <h4>

                Security Settings

            </h4>

            <p>

                Keep your account secure.

            </p>

            <Link
                className="btn btn-danger"
                to="/employee/change-password"
            >

                Change Password

            </Link>

        </div>

    );

}

export default SecurityTab;