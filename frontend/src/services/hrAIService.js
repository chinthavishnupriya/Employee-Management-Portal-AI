import api from "./api";

export const askHRAI = async (question) => {

    console.log("Sending request...");

    const response = await api.post("/hr-ai/ask", {
        question,
    });

    console.log("Response:", response.data);

    return response.data.answer;
};