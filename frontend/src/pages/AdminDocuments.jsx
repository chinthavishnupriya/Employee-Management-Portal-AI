import { useEffect, useState } from "react";
import Layout from "../components/Layout";

import {
    getAllDocuments,
    approveDocument,
    rejectDocument
} from "../services/adminDocumentService";

function AdminDocuments() {

    const [documents, setDocuments] = useState([]);

    useEffect(() => {
        loadDocuments();
    }, []);

    async function loadDocuments() {

        try {

            const data = await getAllDocuments();

            setDocuments(data);

        } catch (error) {

            console.log(error);

        }

    }

    async function handleApprove(id) {

        await approveDocument(id);

        loadDocuments();

    }

    async function handleReject(id) {

        await rejectDocument(id);

        loadDocuments();

    }

    return (

        <Layout>

            <h2>Employee Documents</h2>

            <hr />

            <table className="table table-bordered">

                <thead>

                    <tr>

                        <th>Employee</th>

                        <th>Document</th>

                        <th>Status</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        documents.length === 0 ? (

                            <tr>

                                <td colSpan="4" className="text-center">

                                    No Documents Found

                                </td>

                            </tr>

                        ) : (

                            documents.map((doc) => (

                                <tr key={doc.id}>

                                    <td>{doc.employee_id}</td>

                                    <td>{doc.document_name}</td>

                                    <td>{doc.status}</td>

                                    <td>

                                        <button
                                            className="btn btn-success btn-sm me-2"
                                            onClick={() => handleApprove(doc.id)}
                                        >
                                            Approve
                                        </button>

                                        <button
                                            className="btn btn-danger btn-sm"
                                            onClick={() => handleReject(doc.id)}
                                        >
                                            Reject
                                        </button>

                                    </td>

                                </tr>

                            ))

                        )

                    }

                </tbody>

            </table>

        </Layout>

    );

}

export default AdminDocuments;