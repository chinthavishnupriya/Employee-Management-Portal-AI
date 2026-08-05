import Layout from "../components/Layout";
import AnalyticsCards from "../components/analytics/AnalyticsCards";
import AnalyticsCharts from "../components/analytics/AnalyticsCharts";

function Analytics() {

    return (

        <Layout>

            <div className="mb-4">

                <h2 className="fw-bold">
                    📊 HR Analytics Dashboard
                </h2>

                <p className="text-muted">
                    Employee Management Analytics & Business Insights
                </p>

            </div>

            <AnalyticsCards />

            <AnalyticsCharts />

        </Layout>

    );

}

export default Analytics;