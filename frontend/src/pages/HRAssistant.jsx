import { useState } from "react";
import Layout from "../components/Layout";
import { askHRAI } from "../services/hrAIService";

function HRAssistant() {

    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");

    const askAI = async () => {

        if (!question.trim()) return;

        try {

            setAnswer("🤖 Thinking...");

            const result = await askHRAI(question);

            setAnswer(result);

        } catch (error) {

    console.log("FULL ERROR:", error);

    console.log("Response:", error.response);

    console.log("Data:", error.response?.data);

    setAnswer("❌ Failed to get AI response.");

}
    };

    return (

        <Layout>

            <div className="card shadow border-0 rounded-4">

                <div className="card-header bg-primary text-white">

                    <h3>🤖 AI HR Assistant</h3>

                </div>

                <div className="card-body">

                    <textarea
                        className="form-control"
                        rows="4"
                        placeholder="Ask anything about employees, attendance, payroll, leave, reports..."
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                    />

                    <button
                        className="btn btn-primary mt-3"
                        onClick={askAI}
                    >
                        Ask AI
                    </button>

                    <div className="mt-4">

                        <h5>Response</h5>

                        <div
                            className="border rounded p-3"
                            style={{
                                minHeight: "150px",
                                whiteSpace: "pre-wrap"
                            }}
                        >
                            {answer || "No response yet."}
                        </div>

                    </div>

                </div>

            </div>

        </Layout>

    );

}

export default HRAssistant;