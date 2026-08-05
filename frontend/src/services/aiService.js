import api from "./api";

export const askAI = async (question) => {
    const response = await api.post("/hr-ai/ask", {
        question
    });

    return response.data.answer;
};