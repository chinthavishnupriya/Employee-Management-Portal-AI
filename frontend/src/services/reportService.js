import api from "./api";

function downloadFile(data, filename) {
  const blob = new Blob([data], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename);

  document.body.appendChild(link);
  link.click();

  link.remove();
  window.URL.revokeObjectURL(url);
}

// Employee Report
export const downloadEmployeeReport = async () => {
  const response = await api.get("/reports/employees/csv", {
    responseType: "blob",
  });

  downloadFile(response.data, "employees_report.csv");
};

// Attendance Report
export const downloadAttendanceReport = async () => {
  const response = await api.get("/reports/attendance/csv", {
    responseType: "blob",
  });

  downloadFile(response.data, "attendance_report.csv");
};

// Leave Report
export const downloadLeaveReport = async () => {
  const response = await api.get("/reports/leave/csv", {
    responseType: "blob",
  });

  downloadFile(response.data, "leave_report.csv");
};

// Payroll Report
export const downloadPayrollReport = async () => {
  const response = await api.get("/reports/payroll/csv", {
    responseType: "blob",
  });

  downloadFile(response.data, "payroll_report.csv");
};