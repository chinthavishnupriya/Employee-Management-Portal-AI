import { useEffect, useState } from "react";
import EmployeeLayout from "../components/EmployeeLayout";
import { getMyPerformance } from "../services/employeePerformanceService";

function EmployeePerformance() {

    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadPerformance();

    }, []);

    async function loadPerformance() {

        try {

            const data = await getMyPerformance();

            setReviews(data);

        }

        catch (error) {

            console.error(error);

            alert("Unable to load performance.");

        }

        finally {

            setLoading(false);

        }

    }

    if (loading) {

        return (

            <EmployeeLayout>

                <div className="text-center mt-5">

                    <div className="spinner-border text-primary"></div>

                    <h5 className="mt-3">

                        Loading Performance...

                    </h5>

                </div>

            </EmployeeLayout>

        );

    }

    return (

        <EmployeeLayout>

            <h2 className="mb-4">

                My Performance

            </h2>

            <hr />

            {

                reviews.length === 0 ? (

                    <div className="card shadow border-0">

                        <div className="card-body text-center p-5">

                            <h2>⭐</h2>

                            <h4>No Performance Reviews</h4>

                            <p className="text-muted">

                                Your manager hasn't submitted any
                                performance reviews yet.

                            </p>

                        </div>

                    </div>

                ) : (

                    <div className="row">

                        {

                            reviews.map((review) => (

                                <div
                                    className="col-lg-6 mb-4"
                                    key={review.id}
                                >

                                    <div className="card shadow border-0 h-100">

                                        <div className="card-header bg-primary text-white d-flex justify-content-between">

                                            <strong>

                                                ⭐ Rating

                                            </strong>

                                            <strong>

                                                {review.rating}/5

                                            </strong>

                                        </div>

                                        <div className="card-body">

                                            <div className="row mb-3">

                                                <div className="col-6">

                                                    <strong>

                                                        Review Date

                                                    </strong>

                                                    <br />

                                                    {review.review_date}

                                                </div>

                                                <div className="col-6">

                                                    <strong>

                                                        Reviewer

                                                    </strong>

                                                    <br />

                                                    {review.reviewer}

                                                </div>

                                            </div>

                                            <div className="mb-3">

                                                <strong>

                                                    Promotion

                                                </strong>

                                                <br />

                                                <span className={
                                                    review.promotion_status === "Yes"
                                                        ? "badge bg-success"
                                                        : "badge bg-secondary"
                                                }>

                                                    {review.promotion_status}

                                                </span>

                                            </div>

                                            <div className="mb-3">

                                                <strong>

                                                    🎯 Goals

                                                </strong>

                                                <div className="border rounded p-2 mt-2 bg-light">

                                                    {

                                                        review.goals || "N/A"

                                                    }

                                                </div>

                                            </div>

                                            <div className="mb-3">

                                                <strong>

                                                    💪 Strengths

                                                </strong>

                                                <div className="border rounded p-2 mt-2 bg-light">

                                                    {

                                                        review.strengths || "N/A"

                                                    }

                                                </div>

                                            </div>

                                            <div className="mb-3">

                                                <strong>

                                                    ⚠ Weaknesses

                                                </strong>

                                                <div className="border rounded p-2 mt-2 bg-light">

                                                    {

                                                        review.weaknesses || "N/A"

                                                    }

                                                </div>

                                            </div>

                                            <div>

                                                <strong>

                                                    💬 Feedback

                                                </strong>

                                                <div className="border rounded p-3 mt-2 bg-light">

                                                    {

                                                        review.feedback || "No feedback."

                                                    }

                                                </div>

                                            </div>

                                        </div>

                                    </div>

                                </div>

                            ))

                        }

                    </div>

                )

            }

        </EmployeeLayout>

    );

}

export default EmployeePerformance;