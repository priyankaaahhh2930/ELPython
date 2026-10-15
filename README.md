# Hospital Management System — Phase 3

A beginner-friendly web upgrade of the Phase 2 Python menu-driven Hospital Management System. It uses **Flask** for the Python web backend, **SQLite** for persistent records on a single running environment, and HTML/CSS/JavaScript for a responsive interface.

## Modules
- Dashboard and summary counts
- Patient registration, listing and deletion
- Doctor management
- Appointment booking and listing
- Medical records
- Billing with automatic total calculation
- Pharmacy stock management
- Reports, total billed amount and low-stock summary

## Run locally (Windows)
1. Extract this folder.
2. Open the folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment (optional but recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   py -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   py app.py
   ```
7. Open `http://127.0.0.1:5000` in the browser.

The SQLite database (`hospital.db`) is created automatically on first run.

## Deploy on Render
1. Create a GitHub repository and upload the contents of this folder (not the ZIP itself).
2. In Render, choose **New + → Blueprint** and connect that GitHub repository; Render will read `render.yaml`.
3. Wait for the build to finish and open the generated `onrender.com` URL.
4. Test each module with dummy/demo data.

**Important deployment note:** SQLite is suitable for a college prototype and local testing. On many free web hosting plans, the local filesystem may be temporary or reset during redeploys/restarts. For reliable persistent production data, use a managed database such as PostgreSQL and configure its connection separately. Do not store real patient/medical information in this demo without appropriate security, privacy controls, access management and backups.

## Current scope / limitations
- This is a college project prototype, not a certified hospital information system.
- There is no login/role-based access, audit trail, prescription workflow or patient data encryption in this version.
- Patient/doctor removal also removes linked appointments/records/bills because of the configured foreign-key relationships; use dummy data when testing.
- `Hospital_Management_Phase_2.py` is included as the original Phase 2 program for reference.
