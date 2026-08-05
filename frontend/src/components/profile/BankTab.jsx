function BankTab() {

    return (

        <div className="row">

            <div className="col-md-6 mb-3">

                <label>Bank Name</label>

                <input
                    className="form-control"
                    placeholder="State Bank of India"
                />

            </div>

            <div className="col-md-6 mb-3">

                <label>Account Number</label>

                <input
                    className="form-control"
                />

            </div>

            <div className="col-md-6">

                <label>IFSC Code</label>

                <input
                    className="form-control"
                />

            </div>

            <div className="col-md-6">

                <label>Branch</label>

                <input
                    className="form-control"
                />

            </div>

        </div>

    );

}

export default BankTab;