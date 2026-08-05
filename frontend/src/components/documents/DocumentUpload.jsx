import { useState } from "react";
import { uploadDocument } from "../../services/employeeDocumentService";

function DocumentUpload({ refresh }) {

    const [documentType, setDocumentType] = useState("");
    const [file, setFile] = useState(null);

    async function handleUpload(e) {

        e.preventDefault();

        if (!documentType || !file) {

            alert("Select document type and file.");

            return;

        }

        const formData = new FormData();

        formData.append(
            "document_type",
            documentType
        );

        formData.append(
            "file",
            file
        );

        try {

            await uploadDocument(formData);

            alert("Document uploaded successfully.");

            setDocumentType("");

            setFile(null);

            refresh();

        }

        catch (error) {

            console.log(error);

            alert("Upload failed.");

        }

    }

    return (

        <div className="card shadow mb-4">

            <div className="card-header bg-primary text-white">

                Upload Document

            </div>

            <div className="card-body">

                <form onSubmit={handleUpload}>

                    <select
                        className="form-select mb-3"
                        value={documentType}
                        onChange={(e) =>
                            setDocumentType(
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Select Document
                        </option>

                        <option>
                            Aadhaar
                        </option>

                        <option>
                            PAN
                        </option>

                        <option>
                            Resume
                        </option>

                        <option>
                            Certificate
                        </option>

                    </select>

                    <input
                        type="file"
                        className="form-control mb-3"
                        onChange={(e) =>
                            setFile(
                                e.target.files[0]
                            )
                        }
                    />

                    <button
                        className="btn btn-primary"
                    >
                        Upload
                    </button>

                </form>

            </div>

        </div>

    );

}

export default DocumentUpload;