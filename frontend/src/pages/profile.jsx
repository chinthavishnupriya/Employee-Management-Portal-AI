import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Layout from "../components/Layout";
import { getProfile } from "../services/profileService";

import {
    FaEnvelope,
    FaUserShield,
    FaCircle,
    FaBuilding,
    FaPhone,
    FaCalendarAlt,
    FaEdit
} from "react-icons/fa";

function Profile() {

    const navigate = useNavigate();

    const [profile, setProfile] = useState({});

    useEffect(() => {
        loadProfile();
    }, []);

    async function loadProfile() {

        try {

            const data = await getProfile();

            setProfile(data);

        } catch (error) {

            console.log(error);

            alert("Unable to load profile.");

        }

    }

    return (

        <Layout>

            <div className="container-fluid mt-4">

                {/* Profile Card */}

                <div className="card shadow border-0 rounded-4 mb-4">

                    <div className="card-body text-center">

                        <img
                            src={
                                profile.profile_photo
                                    ? `http://127.0.0.1:8000${profile.profile_photo}`
                                    : "/images/admin.png"
                            }
                            alt="Admin"
                            className="rounded-circle shadow"
                            style={{
                                width: "180px",
                                height: "180px",
                                objectFit: "cover",
                                border: "5px solid #0d6efd"
                            }}
                        />

                        <h2 className="fw-bold mt-4">
                            {profile.username || "Admin"}
                        </h2>

                        <p className="text-muted fs-5">
                            {profile.designation || "HR Manager"}
                        </p>

                        <span className="badge bg-success px-4 py-2 fs-6">
                            Active
                        </span>

                        <hr />

                        <button
                            className="btn btn-primary px-4"
                            onClick={() => navigate("/edit-profile")}
                        >
                            <FaEdit className="me-2" />
                            Edit Profile
                        </button>

                    </div>

                </div>

                {/* Personal Information */}

                <div className="card shadow border-0 rounded-4 mb-4">

                    <div className="card-header bg-primary text-white">
                        <h4 className="mb-0">Personal Information</h4>
                    </div>

                    <div className="card-body">

                        <div className="row mb-4">

                            <div className="col-md-3 fw-bold">
                                <FaEnvelope className="me-2" />
                                Email
                            </div>

                            <div className="col-md-9">
                                {profile.email || "-"}
                            </div>

                        </div>

                        <div className="row mb-4">

                            <div className="col-md-3 fw-bold">
                                <FaPhone className="me-2" />
                                Phone
                            </div>

                            <div className="col-md-9">
                                {profile.phone || "-"}
                            </div>

                        </div>

                        <div className="row mb-4">

                            <div className="col-md-3 fw-bold">
                                <FaBuilding className="me-2" />
                                Department
                            </div>

                            <div className="col-md-9">
                                {profile.department || "-"}
                            </div>

                        </div>

                        <div className="row">

                            <div className="col-md-3 fw-bold">
                                <FaCalendarAlt className="me-2" />
                                Joined Date
                            </div>

                            <div className="col-md-9">
                                01 January 2025
                            </div>

                        </div>

                    </div>

                </div>

                {/* Account Information */}

                <div className="card shadow border-0 rounded-4">

                    <div className="card-header bg-dark text-white">
                        <h4 className="mb-0">Account Information</h4>
                    </div>

                    <div className="card-body">

                        <div className="row mb-4">

                            <div className="col-md-3 fw-bold">
                                <FaUserShield className="me-2" />
                                Role
                            </div>

                            <div className="col-md-9">
                                {profile.role || "-"}
                            </div>

                        </div>

                        <div className="row">

                            <div className="col-md-3 fw-bold">
                                <FaCircle className="me-2 text-success" />
                                Status
                            </div>

                            <div className="col-md-9">

                                <span className="badge bg-success px-3 py-2">
                                    Active
                                </span>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </Layout>

    );

}

export default Profile;