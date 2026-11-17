# BusSaathi – Smart & Reliable Public Transport Assistant

A hackathon starter prototype demonstrating:
- Driver/browser GPS location sharing
- Passenger map view
- GPS freshness states: LIVE (<=30 sec), DELAYED (31–120 sec), STALE (>120 sec)
- Basic issue reporting
- SQLite storage

## Important scope note
This is a demonstration prototype using a browser/phone GPS source. It is **not connected to KSRTC, BMTC, Chalo, or any official transport operator**. Bus IDs and route names are demo values. The freshness thresholds are configurable prototype rules, not a validated real-world reliability score. ETA prediction and alternative-route recommendations are not implemented yet.

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start:
   `python app.py`
5. Open `http://127.0.0.1:5000`
6. Open `http://127.0.0.1:5000/driver` in another browser tab/device that can reach the server.
7. Allow location access. Browser geolocation generally requires localhost or HTTPS.

## Demo
- Start sharing in Driver Demo Mode.
- Return to Passenger view and observe the map/status.
- Stop sharing or wait long enough to see the status change to DELAYED/STALE.

For a phone on the same Wi-Fi network, run Flask on an accessible development host and use HTTPS for browser geolocation where required. Do not expose the Flask debug server publicly.

## Suggested next tasks
- Add route/stop tables and route selection.
- Implement ETA using route distance and measured travel-time data.
- Add a proper authentication and role system.
- Validate GPS freshness thresholds with real observations.
- Add tests and deployment configuration.
- Obtain permission and a legitimate data feed before any real transport integration.

## Team
Add team members, institution and contact details before submission.
