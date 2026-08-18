import api from "./api";

export const askAI = async (question) => {

    const response = await api.post("/ai/chat", {
        prompt: question,
    });

    return response.data.response;
};
