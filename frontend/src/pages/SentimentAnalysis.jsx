import { useState } from "react";
import api from "../services/api";

function SentimentAnalysis() {

    const [feedback, setFeedback] = useState("");
    const [result, setResult] = useState("");

    const analyze = async () => {

        if (!feedback.trim()) {
            alert("Enter employee feedback");
            return;
        }

        try {

            const res = await api.post("/sentiment/analyze", {
                feedback
            });

            setResult(res.data.result);

        } catch (error) {

            console.error(error);

            alert("Analysis failed.");

        }

    };

    return (

        <div className="container mt-5">

            <h2 className="mb-4">
                Employee Sentiment Analysis
            </h2>

            <textarea
                className="form-control"
                rows="6"
                placeholder="Enter employee feedback..."
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
            />

            <button
                className="btn btn-primary mt-3"
                onClick={analyze}
            >
                Analyze Sentiment
            </button>

            {result && (

                <div className="card mt-4">

                    <div className="card-body">

                        <h5>Result</h5>

                        <pre
                            style={{
                                whiteSpace: "pre-wrap"
                            }}
                        >
                            {result}
                        </pre>

                    </div>

                </div>

            )}

        </div>

    );

}

export default SentimentAnalysis;