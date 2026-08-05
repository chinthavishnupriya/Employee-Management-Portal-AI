function PerformanceCard({ score = 92 }) {

    return (

        <div className="card border-0 shadow h-100">

            <div className="card-header bg-warning">

                Performance

            </div>

            <div className="card-body">

                <h3>

                    {score}%

                </h3>

                <div className="progress">

                    <div
                        className="progress-bar bg-success"
                        style={{
                            width: `${score}%`
                        }}
                    >

                        {score}%

                    </div>

                </div>

                <p className="mt-3 text-muted">

                    Keep up the great work!

                </p>

            </div>

        </div>

    );

}

export default PerformanceCard;