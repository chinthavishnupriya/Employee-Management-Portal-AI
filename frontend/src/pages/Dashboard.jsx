import { useEffect, useState } from "react";

import Layout from "../components/Layout";
import DashboardHeader from "../components/adminDashboard/DashboardHeader";
import DashboardCards from "../components/adminDashboard/DashboardCards";

import {
    getDashboardAnalytics
} from "../services/dashboardService";

function Dashboard() {

    const [dashboard, setDashboard] = useState({});

    useEffect(() => {

        loadDashboard();

    }, []);

    async function loadDashboard() {

        try {

            const data = await getDashboardAnalytics();

            console.log(data);

            setDashboard(data);

        } catch (error) {

            console.log(error);

        }

    }

    return (

        <Layout>

            <DashboardHeader dashboard={dashboard} />

<DashboardCards dashboard={dashboard} />

        </Layout>

    );

}

export default Dashboard;