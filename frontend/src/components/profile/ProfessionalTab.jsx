function ProfessionalTab({ profile }) {

    return (

        <div className="row">

            <div className="col-md-6 mb-3">

                <label>Department</label>

                <input
                    className="form-control"
                    value={profile.department || ""}
                    disabled
                />

            </div>

            <div className="col-md-6 mb-3">

                <label>Designation</label>

                <input
                    className="form-control"
                    value={profile.designation || ""}
                    disabled
                />

            </div>

            <div className="col-md-6">

                <label>Joining Date</label>

                <input
                    className="form-control"
                    value={profile.joining_date || ""}
                    disabled
                />

            </div>

            <div className="col-md-6">

                <label>Salary</label>

                <input
                    className="form-control"
                    value={profile.salary || ""}
                    disabled
                />

            </div>

        </div>

    );

}

export default ProfessionalTab;