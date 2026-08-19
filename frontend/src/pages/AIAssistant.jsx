import { useState } from "react";
import { askHRAI } from "../services/hrAIService";
import EmployeeLayout from "../components/EmployeeLayout";

function AIAssistant() {

    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleAsk() {

        if (!prompt.trim()) return;

        setLoading(true);

        try {

            const result = await askHRAI(prompt);

setResponse(
                typeof result === "string"
                    ? result.replace(/\\n/g, "\n")
                    : result
            );

        }

        catch (error) {

    console.log("FULL ERROR:", error);
    console.log("STATUS:", error.response?.status);
    console.log("DATA:", error.response?.data);

    alert(JSON.stringify(error.response?.data || error.message));

}

        setLoading(false);

    }

    return (

        <EmployeeLayout>

            <div className="container mt-4">

                <div className="card shadow">

                    <div className="card-header bg-primary text-white">

                        <h3 className="mb-0">
                            AI HR Assistant
                        </h3>

                    </div>

                    <div className="card-body">

                        <textarea
                            className="form-control"
                            rows="5"
                            placeholder="Ask any HR related question..."
                            value={prompt}
                            onChange={(e) =>
                                setPrompt(e.target.value)
                            }
                        />

                        <button
                            className="btn btn-primary mt-3"
                            onClick={handleAsk}
                            disabled={loading}
                        >
                            {loading ? "Thinking..." : "Ask AI"}
                        </button>

                        {response && (

                            <div className="alert alert-light mt-4">

                                <h5>AI Response</h5>

                                <hr />

                                <p style={{ whiteSpace: "pre-wrap" }}>
                                    {response}
                                </p>

                            </div>

                        )}

                    </div>

                </div>

            </div>

        </EmployeeLayout>

    );

}

export default AIAssistant;