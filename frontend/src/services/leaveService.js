import api from "./api";

// ==========================
// Apply Leave
// ==========================
export const applyLeave = async (leaveData) => {
  const token = localStorage.getItem("access_token");

  const response = await api.post(
    "/leave/apply",
    leaveData,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};

// ==========================
// Get Leave Requests
// ==========================
export const getLeaves = async () => {
  const token = localStorage.getItem("access_token");

  const response = await api.get("/leave", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ==========================
// Approve Leave
// ==========================
export const approveLeave = async (leaveId) => {
  const token = localStorage.getItem("access_token");

  const response = await api.put(
    `/leave/approve/${leaveId}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};

// ==========================
// Reject Leave
// ==========================
export const rejectLeave = async (leaveId) => {
  const token = localStorage.getItem("access_token");

  const response = await api.put(
    `/leave/reject/${leaveId}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};