import { useEffect, useState } from "react";

import DocumentUpload from "../documents/DocumentUpload";
import DocumentList from "../documents/DocumentList";

import {

    getMyDocuments

} from "../../services/employeeDocumentService";

function DocumentsTab() {

    const [documents, setDocuments] = useState([]);

    useEffect(() => {

        loadDocuments();

    }, []);

    async function loadDocuments() {

        try {

            const data = await getMyDocuments();

            setDocuments(data);

        }

        catch (error) {

            console.log(error);

        }

    }

    return (

        <>

            <DocumentUpload

                refresh={loadDocuments}

            />

            <DocumentList

    documents={documents}

    refresh={loadDocuments}

/>

        </>

    );

}

export default DocumentsTab;