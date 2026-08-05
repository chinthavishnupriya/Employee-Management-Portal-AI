function AnnouncementCard() {

    return (

        <div className="card border-0 shadow mt-4">

            <div className="card-header bg-info text-white">

                Company Announcements

            </div>

            <div className="card-body">

                <ul className="list-group list-group-flush">

                    <li className="list-group-item">
                        📢 Company meeting on Friday at 10:00 AM
                    </li>

                    <li className="list-group-item">
                        🎉 Independence Day holiday on 15 August
                    </li>

                    <li className="list-group-item">
                        📄 Upload all pending documents this week
                    </li>

                </ul>

            </div>

        </div>

    );

}

export default AnnouncementCard;