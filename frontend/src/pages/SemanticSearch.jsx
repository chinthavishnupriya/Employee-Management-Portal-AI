import { useState } from "react";
import api from "../services/api";

function SemanticSearch() {

    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);

    const search = async () => {

        if (!query.trim()) {
            alert("Enter search query");
            return;
        }

        try {

            const res = await api.post("/resume/search", {
                query
            });

            setResults(res.data.results);

        } catch (err) {

            console.error(err);
            alert("Search failed.");

        }

    };

    return (

        <div className="container mt-5">

            <h2>Resume Semantic Search</h2>

            <input
                className="form-control mt-4"
                placeholder="Search skills (Python, AI, React...)"
                value={query}
                onChange={(e)=>setQuery(e.target.value)}
            />

            <button
                className="btn btn-primary mt-3"
                onClick={search}
            >
                Search
            </button>

            <div className="mt-4">

                {results.map((resume,index)=>(

                    <div
                        key={index}
                        className="card mb-3"
                    >

                        <div className="card-body">

                            <h5>{resume.id}</h5>

                            <p>

                                Similarity Score :
                                {" "}
                                {resume.distance.toFixed(3)}

                            </p>

                            <pre
                                style={{
                                    whiteSpace:"pre-wrap"
                                }}
                            >
                                {resume.text.substring(0,500)}...
                            </pre>

                        </div>

                    </div>

                ))}

            </div>

        </div>

    );

}

export default SemanticSearch;