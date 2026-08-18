import api from "./api";

export const askHRAI = async (question) => {

    console.log("Sending request to /ai/chat...");

    const response = await api.post("/ai/chat", {
        prompt: question,
    });

    console.log("Response:", response.data);

    return response.data.response;
};
