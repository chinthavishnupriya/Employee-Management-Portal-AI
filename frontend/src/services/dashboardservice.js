import api from "./api";

// Dashboard Summary
export const getDashboard = async () => {
  const token = localStorage.getItem("access_token");

  const response = await api.get("/dashboard", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// Dashboard Analytics
export const getDashboardAnalytics = async () => {
  const token = localStorage.getItem("access_token");

  const response = await api.get("/dashboard/analytics", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};