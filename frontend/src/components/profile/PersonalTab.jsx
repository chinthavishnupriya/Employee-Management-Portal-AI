function PersonalTab({ profile, handleChange }) {

    return (

        <div className="row">

            <div className="col-md-6 mb-3">

                <label>Phone</label>

                <input
                    className="form-control"
                    name="phone"
                    value={profile.phone || ""}
                    onChange={handleChange}
                />

            </div>

            <div className="col-md-6 mb-3">

                <label>Email</label>

                <input
                    className="form-control"
                    value={profile.email || ""}
                    disabled
                />

            </div>

            <div className="col-12 mb-3">

                <label>Address</label>

                <textarea
                    className="form-control"
                    rows="3"
                    name="address"
                    value={profile.address || ""}
                    onChange={handleChange}
                />

            </div>

            <div className="col-md-6">

                <label>Date of Birth</label>

                <input
                    type="date"
                    className="form-control"
                    name="date_of_birth"
                    value={profile.date_of_birth || ""}
                    onChange={handleChange}
                />

            </div>

            <div className="col-md-6">

                <label>Nationality</label>

                <input
                    className="form-control"
                    name="nationality"
                    value={profile.nationality || ""}
                    onChange={handleChange}
                />

            </div>

        </div>

    );

}

export default PersonalTab;