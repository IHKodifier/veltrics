# Veltrics Fleet Management — Sprint 01 Manual Testing Guide

> **Document Version:** 1.0.0  
> **Target Release:** Sprint 01 Baseline (Phase 1 MVP)  
> **Master Spec:** [`product-specs/08-master-prd.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/08-master-prd.md)  
> **Sprint Backlog Tracker:** [`trackers/stage-01/sprints/07.01.01-tracker.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/stage-01/sprints/07.01.01-tracker.md)

---

## 1. Executive Summary & Test Environment Setup

This document provides a comprehensive, step-by-step manual testing guide for all **27 Use Cases** implemented in **Sprint 01**. Quality Assurance (QA) testers, developers, and product owners can follow this guide to systematically verify front-end screen flows, form validations, organization switching, vehicle management, maintenance logging, and backend API contracts.

### 1.1 Local Environment Setup Instructions

Before commencing manual testing, ensure the local development environment and backend services are active:

1. **Launch Backend Service (FastAPI + SQLite `dev.db` + Auth Emulator):**
   Open a PowerShell terminal in the repository root and execute:
   ```powershell
   .\scripts\start_backend.ps1
   ```
   *Backend API target address:* `http://localhost:8000`  
   *Interactive API Docs (Swagger UI):* `http://localhost:8000/docs`

2. **Launch Mobile/Web Client App (Flutter):**
   Open a secondary PowerShell terminal and run:
   ```powershell
   cd src/frontend
   flutter run -d chrome  # Or desktop/emulator
   ```

3. **Verify Database Seeding (UC-118):**
   The application initializes with pre-populated demo records for vehicles, maintenance schedules, and organizations (`org-demo-101`).

---

## 2. Global Navigation & Screen Architecture Map

The Veltrics Flutter client is structured around three primary bottom navigation tabs and contextual dialog overlays:

```
+-----------------------------------------------------------------------------------+
| Top App Bar: [ Org Selector Dropdown (UC-015) ]    [ Invite Member (UC-016) ]     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Tab 0: Dashboard ]          [ Tab 1: Fleet Directory ]       [ Tab 2: Auth ]   |
|  - Consumer Dashboard Cards    - Vehicle Grid & Search          - Sign In / Up    |
|    (UC-064)                      (UC-025)                         (UC-001 - 005)  |
|  - Fleet Health Overview       - FAB: Add Vehicle               - Reset Password  |
|  - Quick Action Buttons          (UC-024)                         (UC-006)        |
|                                - Tap Vehicle Card -> Detail     - Profile Setup   |
|                                  (UC-026)                         (UC-007)        |
|                                  ├── Edit Info (UC-027)        - Profile View    |
|                                  ├── Schedule (UC-034,035,038)   (UC-008)        |
|                                  ├── Service Log (UC-036)      - Security & Logs |
|                                  └── History (UC-037)           (UC-010-013)    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
| Bottom Navigation Bar: [ 📊 Dashboard ]   [ 🚗 Fleet Directory ]   [ 🛡️ Auth/Profile ] |
+-----------------------------------------------------------------------------------+
```

---

## 3. Step-by-Step Manual Test Protocols (UC-001 to UC-118)

---

### Module A: Authentication & Identity Management

#### UC-001: Sign Up with Google One-Tap
* **Target Screen:** Auth Tab (`AuthScreen` / `LoginScreen`) -> Google One-Tap Modal
* **Navigation Path:** Tap **Auth** icon (3rd tab on bottom nav) -> Click **"Continue with Google"** button.
* **Pre-conditions:** App launched, backend running.
* **Execution Steps:**
  1. Navigate to the **Auth** tab.
  2. Locate the **"Continue with Google"** button with the Google logo.
  3. Click **"Continue with Google"**.
* **Expected Outcome:**
  * One-tap authentication completes instantly.
  * User is authenticated as `Alex Rivera` (`alex.driver@veltrics.com`).
  * Profile banner displays "Signed in as Alex Rivera" with active JWT bearer token session.
  * Personal organization `Alex Rivera's Org` is automatically provisioned (UC-014).
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc001.py`

---

#### UC-002: Sign Up with Facebook Login
* **Target Screen:** Auth Tab -> Facebook OAuth Modal
* **Navigation Path:** Tap **Auth** icon -> Click **"Continue with Facebook"** button.
* **Pre-conditions:** App active in Auth tab.
* **Execution Steps:**
  1. Click the **"Continue with Facebook"** button.
* **Expected Outcome:**
  * Facebook OAuth handler completes session exchange.
  * User profile initializes with Facebook UID (`fb-uid-alex-rivera-fb`).
  * JWT access token & refresh token are stored in secure session storage.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc002.py`

---

#### UC-003: Sign Up with Email and Password
* **Target Screen:** Auth Tab -> Email Form Overlay
* **Navigation Path:** Tap **Auth** icon -> Click **"Sign Up with Email"** link to expand registration form.
* **Pre-conditions:** User logged out.
* **Execution Steps:**
  1. Tap **"Don't have an account? Sign Up"** toggle on the Auth screen.
  2. Enter Full Name: `Jane Doe`.
  3. Enter Email Address: `jane.doe@example.com`.
  4. Enter Password: `SecurePassword123!` (Must contain ≥8 chars, 1 uppercase, 1 digit).
  5. Click **"Create Account"** button.
* **Expected Outcome:**
  * System validates password strength regex.
  * Account is registered in backend database.
  * User session is established and onboarding Profile Setup prompt appears.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc003.py`

---

#### UC-004: User Password Authentication & Session Initiation
* **Target Screen:** Auth Tab -> Sign In Form
* **Navigation Path:** Tap **Auth** icon -> Select **"Sign In"** mode.
* **Pre-conditions:** Account created via UC-003.
* **Execution Steps:**
  1. Enter Registered Email: `jane.doe@example.com`.
  2. Enter Password: `SecurePassword123!`.
  3. Click **"Sign In"**.
* **Expected Outcome:**
  * Password hash is verified against bcrypt seed.
  * Session payload with `access_token` and `refresh_token` is generated.
  * Audit log event `USER_LOGIN_SUCCESS` is written (UC-012).
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc004.py`

---

#### UC-005: Unified Sign In (All Social & Credentials Methods)
* **Target Screen:** Auth Tab (`LoginScreen`)
* **Navigation Path:** Tap **Auth** icon.
* **Pre-conditions:** Backend initialized.
* **Execution Steps:**
  1. Test invalid credential entry (e.g., email `wrong@domain.com` / password `badpass`).
  2. Verify error message banner: `"Invalid email or password"`.
  3. Re-enter valid credentials and sign in successfully.
* **Expected Outcome:**
  * Clean error handling for unauthorized attempts.
  * Smooth auth state transition upon successful validation.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc005.py`

---

#### UC-006: Forgot Password & Reset Flow
* **Target Screen:** Auth Tab -> Forgot Password Dialog
* **Navigation Path:** Tap **Auth** icon -> Click **"Forgot Password?"** link text below password input.
* **Pre-conditions:** User on Auth screen.
* **Execution Steps:**
  1. Click **"Forgot Password?"**.
  2. In the popup dialog, enter email: `alex.driver@veltrics.com`.
  3. Click **"Request Reset"**.
  4. Notice system generates reset token automatically into token field.
  5. Enter New Password: `NewStrongPass123!`.
  6. Click **"Reset Password"**.
* **Expected Outcome:**
  * Reset token validation succeeds.
  * Success toast notification displays `"Password reset successfully"`.
  * User can now sign in with the new password `NewStrongPass123!`.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc006.py`

---

#### UC-007: Complete Profile Setup (Initial Onboarding)
* **Target Screen:** Auth Tab -> `ProfileSetupScreen`
* **Navigation Path:** Authenticate as new user -> Redirected automatically or click **"Complete Profile Setup"**.
* **Pre-conditions:** User signed up without completing profile metadata.
* **Execution Steps:**
  1. On Profile Setup form, fill out:
     * Full Name: `Alex Rivera`
     * Phone Number: `+1 (555) 234-5678`
     * City / Region: `Austin, TX`
     * Primary Role Dropdown: Select `Fleet Manager`
  2. Click **"Complete Setup & Save"**.
* **Expected Outcome:**
  * Profile record is updated with phone, city, and role metadata.
  * User profile badge updates to display `Fleet Manager`.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc007.py`

---

#### UC-008: View and Edit Profile
* **Target Screen:** Auth Tab -> `ProfileScreen`
* **Navigation Path:** Tap **Auth** icon -> Tap **"View Profile & Settings"**.
* **Pre-conditions:** User authenticated.
* **Execution Steps:**
  1. Observe current profile info card (Name, Phone, City, Job Role).
  2. Click **"Edit Profile"** button (pencil icon).
  3. Change City from `Austin, TX` to `Dallas, TX`.
  4. Change Job Role to `Fleet Owner`.
  5. Click **"Save Changes"**.
* **Expected Outcome:**
  * Profile updates without screen reload.
  * Confirmation snackbar appears: `"Profile updated successfully"`.
  * Changes persist across app restarts.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc008.py`

---

#### UC-009: Silent Token Refresh
* **Target Screen:** App-wide API Layer (Background Service)
* **Navigation Path:** Background interaction during active session.
* **Pre-conditions:** Active JWT session established.
* **Execution Steps:**
  1. Trigger an API call when access token has expired (or click **"Trigger Token Refresh"** in Security section of Profile screen).
  2. Observe network request logs in developer console.
* **Expected Outcome:**
  * Refresh token payload `/api/v1/auth/refresh` is sent automatically.
  * New access token issued seamlessly without interrupting user UX or logging user out.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc009.py`

---

#### UC-010: User Sign Out & Token Revocation
* **Target Screen:** `ProfileScreen` -> Security Actions Section
* **Navigation Path:** Tap **Auth** tab -> Scroll down to Security Actions -> Click **"Sign Out"** button.
* **Pre-conditions:** User signed in.
* **Execution Steps:**
  1. Click **"Sign Out"**.
  2. Confirm sign out in popup modal.
* **Expected Outcome:**
  * Bearer token is revoked on backend blacklist.
  * Local session state cleared.
  * UI redirects to unauthenticated Auth Sign In screen.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc010.py`

---

#### UC-011: Account Deletion (GDPR Right to be Forgotten)
* **Target Screen:** `ProfileScreen` -> Danger Zone Section
* **Navigation Path:** Tap **Auth** tab -> Scroll to Danger Zone -> Click **"Delete Account"**.
* **Pre-conditions:** User signed in.
* **Execution Steps:**
  1. Scroll down to Danger Zone on Profile screen.
  2. Click red **"Delete Account"** button.
  3. In confirmation modal, type `DELETE` to confirm irreversible action.
  4. Click **"Confirm Permanent Deletion"**.
* **Expected Outcome:**
  * User profile, session keys, and associated personal assets are purged.
  * Account state marked as soft-deleted/anonymized in DB.
  * App returns to default unauthenticated state with success notification.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc011.py`

---

#### UC-012: Audit Log Recording for Authentication Events
* **Target Screen:** `ProfileScreen` -> Security & Audit History Section
* **Navigation Path:** Tap **Auth** tab -> Click **"View Audit Logs"** panel.
* **Pre-conditions:** User performed login, profile edit, or password reset events.
* **Execution Steps:**
  1. Open Audit Log drawer/section.
  2. Review recorded security events list.
* **Expected Outcome:**
  * Audit entries display: Event Type (e.g., `LOGIN_SUCCESS`, `PROFILE_UPDATE`), Timestamp, IP Address, Device User-Agent.
  * Logs are immutable and ordered chronologically.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc012.py`

---

#### UC-013: Active Session Management & Device Tracking
* **Target Screen:** `ProfileScreen` -> Active Sessions Panel
* **Navigation Path:** Tap **Auth** tab -> Click **"Active Sessions"**.
* **Pre-conditions:** User logged in from one or more devices.
* **Execution Steps:**
  1. Inspect list of active sessions (Current Browser / Flutter Client / Mobile device).
  2. Click **"Revoke Session"** next to a secondary device session.
* **Expected Outcome:**
  * Targeted device session token is invalidated in backend.
  * Session entry vanishes from active session list.
* **Automated Test Ref:** `pytest src/tests/unit/test_auth_uc013.py`

---

### Module B: Multi-Tenant Organization Management

#### UC-014: Auto-Create Personal Organization
* **Target Screen:** App Header / Dashboard Top Bar
* **Navigation Path:** Auto-triggered upon initial sign up (UC-001/UC-003).
* **Pre-conditions:** New user registration.
* **Execution Steps:**
  1. Sign up as a new user.
  2. Check organization dropdown menu on Top App Bar.
* **Expected Outcome:**
  * Default personal organization (e.g., `Alex Rivera's Org`) is created with owner role assigned to new user.
  * Tenant isolation UUID is provisioned.
* **Automated Test Ref:** `pytest src/tests/unit/test_organizations_uc014.py`

---

#### UC-015: View & Switch Active Organization
* **Target Screen:** App Top Bar / Global Header -> Org Selector Dropdown
* **Navigation Path:** Click **Organization Selector Dropdown** on top bar of Dashboard or Fleet screen.
* **Pre-conditions:** User belongs to multiple organizations (e.g. `Demo Fleet Org` and `Personal Fleet`).
* **Execution Steps:**
  1. Click **Org Selector Dropdown** on top app bar.
  2. Observe list of available organizations.
  3. Select **"Apex Logistics Fleet"**.
* **Expected Outcome:**
  * Active tenant context updates across client app.
  * Dashboard cards and vehicle list filter dynamically to show only vehicles belonging to `Apex Logistics Fleet`.
* **Automated Test Ref:** `pytest src/tests/unit/test_organizations_uc015.py`

---

#### UC-016: Invite Team Member to Organization
* **Target Screen:** Dashboard / Header -> Invite Team Member Modal
* **Navigation Path:** Click **"Invite Member"** icon/button on top app bar.
* **Pre-conditions:** User has `Owner` or `Manager` role in active org.
* **Execution Steps:**
  1. Click **"Invite Member"** button.
  2. Enter Invitee Email: `colleague@veltrics.com`.
  3. Select Role: `Driver` (Options: Owner, Manager, Driver, Dispatcher).
  4. Click **"Send Invitation"**.
* **Expected Outcome:**
  * Invitation payload created with pending status.
  * Snackbar displays `"Invitation sent to colleague@veltrics.com"`.
* **Automated Test Ref:** `pytest src/tests/unit/test_organizations_uc016.py`

---

### Module C: Fleet Vehicle Management

#### UC-024: Add Vehicle with Typeahead VIN Lookup
* **Target Screen:** Fleet Directory Tab -> `AddVehicleScreen`
* **Navigation Path:** Tap **Fleet Directory** (Tab 1 on bottom nav) -> Click **"+ Add Vehicle"** Floating Action Button (FAB).
* **Pre-conditions:** User in active organization context.
* **Execution Steps:**
  1. Navigate to Fleet tab and click **"+ Add Vehicle"**.
  2. Enter VIN in typeahead input field: `1FTFW1ED4MFC12345`.
  3. Click **"Decode VIN / Search Typeahead"**.
  4. Observe auto-filled fields:
     * Make: `Ford`
     * Model: `F-150`
     * Year: `2021`
     * Engine: `3.5L V6 EcoBoost`
  5. Fill in remaining required fields:
     * Current Mileage: `45000`
     * License Plate: `TX-8921-FL`
     * Vehicle Nickname: `Red Hauler 01`
     * Vehicle Type: `Truck`
  6. Click **"Save Vehicle"** button.
* **Expected Outcome:**
  * Vehicle is saved to database.
  * System automatically seeds default baseline maintenance schedule (Oil Change, Tire Rotation, Brake Inspection) for this vehicle (UC-034).
  * Screen closes and returns to Vehicle Directory list containing the new vehicle.
* **Automated Test Ref:** `pytest src/tests/unit/test_vehicles_uc024.py`

---

#### UC-025: View Vehicle List (Search & Filter)
* **Target Screen:** Fleet Directory Tab (`VehicleListScreen`)
* **Navigation Path:** Tap **Fleet Directory** icon (Tab 1 on bottom nav).
* **Pre-conditions:** Vehicles exist in current organization.
* **Execution Steps:**
  1. View overall vehicle grid/list cards.
  2. Type `Ford` into Search bar at top.
  3. Observe list updates to show only Ford vehicles.
  4. Filter by status pill: Click **"MAINTENANCE"** tab.
* **Expected Outcome:**
  * Instant search filtering by Make, Model, License Plate, or Nickname.
  * Status chips (All, Active, Maintenance, Inactive) accurately isolate matching vehicles.
  * Vehicle summary card displays Thumbnail image, Year/Make/Model, Plate, Current Mileage, and Status Badge.
* **Automated Test Ref:** `pytest src/tests/unit/test_vehicles_uc025.py`

---

#### UC-026: View Vehicle Detail Screen
* **Target Screen:** Fleet Directory -> `VehicleDetailScreen`
* **Navigation Path:** Tap **Fleet Directory** (Tab 1) -> Tap on any **Vehicle Card** (e.g. `2021 Ford F-150`).
* **Pre-conditions:** At least one vehicle in fleet list.
* **Execution Steps:**
  1. Tap the vehicle card for `Ford F-150`.
  2. Inspect Detail Header & Spec Cards (VIN, Mileage, Fuel Type, License Plate, Org Owner).
  3. Inspect Quick Action Grid:
     * **Edit Vehicle Info**
     * **Maintenance Schedule**
     * **Log Service Record**
     * **Service History**
* **Expected Outcome:**
  * Vehicle detail page renders cleanly with spec overview, health stats, and operational status badge.
  * Navigation links to schedule, service logging, and history function seamlessly.
* **Automated Test Ref:** `pytest src/tests/unit/test_vehicles_uc026.py`

---

#### UC-027: Edit Vehicle Information
* **Target Screen:** Vehicle Detail -> `EditVehicleScreen`
* **Navigation Path:** Fleet Directory -> Tap Vehicle Card -> Click **"Edit Vehicle"** button (or pencil icon).
* **Pre-conditions:** Viewing Vehicle Detail screen.
* **Execution Steps:**
  1. Click **"Edit Vehicle Information"**.
  2. Update Current Mileage to `48500`.
  3. Change Primary Status to `MAINTENANCE`.
  4. Update License Plate to `TX-9900-NEW`.
  5. Click **"Update Vehicle"**.
* **Expected Outcome:**
  * Form validates input numeric bounds.
  * Vehicle detail updates immediately reflecting new mileage (`48,500 mi`) and status badge (`IN MAINTENANCE`).
  * Changes persist in SQLite backend database.
* **Automated Test Ref:** `pytest src/tests/unit/test_vehicles_uc027.py`

---

### Module D: Vehicle Maintenance & Service Logging

#### UC-034: View Pre-Populated Maintenance Schedule
* **Target Screen:** Vehicle Detail -> `MaintenanceScheduleScreen`
* **Navigation Path:** Fleet Directory -> Tap Vehicle Card -> Click **"Maintenance Schedule"** quick action card.
* **Pre-conditions:** Vehicle added via UC-024.
* **Execution Steps:**
  1. Open Maintenance Schedule screen for the vehicle.
  2. Review pre-populated schedule items generated at vehicle creation:
     * *Oil & Filter Change* (Interval: 5,000 miles / 6 months)
     * *Tire Rotation & Alignment* (Interval: 7,500 miles / 6 months)
     * *Brake Pad & Rotor Inspection* (Interval: 15,000 miles / 12 months)
  3. Observe status color badges (**DUE SOON**, **UPCOMING**, **OVERDUE**).
* **Expected Outcome:**
  * Pre-populated schedule items display interval specifications, last performed date, and next due mileage threshold.
  * Sort options allow viewing by Urgency or Due Date.
* **Automated Test Ref:** `pytest src/tests/unit/test_maintenance_uc034.py`

---

#### UC-035: Customize Maintenance Schedule Items
* **Target Screen:** Maintenance Schedule Screen -> Customize Modal
* **Navigation Path:** Maintenance Schedule -> Tap **Settings/Customize** icon on an item card (e.g. *Oil Change*).
* **Pre-conditions:** Viewing Maintenance Schedule.
* **Execution Steps:**
  1. Click edit/customize icon on **Oil & Filter Change** schedule card.
  2. Change Mileage Interval from `5,000` to `7,500` miles.
  3. Change Time Interval from `6 months` to `9 months`.
  4. Enable custom reminder alert toggle.
  5. Click **"Save Custom Schedule"**.
* **Expected Outcome:**
  * Schedule item updates interval calculations dynamically.
  * Next Due Mileage recalculates instantly based on vehicle's current odometer.
* **Automated Test Ref:** `pytest src/tests/unit/test_maintenance_uc035.py`

---

#### UC-036: Log Service Record
* **Target Screen:** Maintenance Schedule / Vehicle Detail -> `LogMaintenanceScreen`
* **Navigation Path:** Maintenance Schedule -> Click **"Log Service"** button on a schedule item OR Vehicle Detail -> Click **"Log Service Record"**.
* **Pre-conditions:** Vehicle exists.
* **Execution Steps:**
  1. Tap **"Log Service Record"**.
  2. Select Service Task: `Oil & Filter Change`.
  3. Enter Service Date: Today's Date (`2026-08-10`).
  4. Enter Odometer at Service: `45200`.
  5. Enter Service Cost ($): `89.50`.
  6. Enter Service Provider / Shop: `Jiffy Lube Express #402`.
  7. Enter Technician Notes: `Replaced synthetic 5W-30 oil and OEM filter. Topped off washer fluid.`
  8. Click **"Submit Service Log"**.
* **Expected Outcome:**
  * Service record logged successfully.
  * Schedule item status for *Oil Change* updates to **COMPLETED / UP TO DATE**.
  * Vehicle's current mileage updates to `45,200` if higher than prior value.
  * Entry added to Service History list (UC-037).
* **Automated Test Ref:** `pytest src/tests/unit/test_maintenance_uc036.py`

---

#### UC-037: View Service History & Cost Breakdown
* **Target Screen:** Vehicle Detail -> `ServiceHistoryScreen`
* **Navigation Path:** Fleet Directory -> Tap Vehicle Card -> Click **"Service History"** button.
* **Pre-conditions:** Service records logged for vehicle.
* **Execution Steps:**
  1. Open Service History screen.
  2. Inspect Cumulative Cost Summary Card at top (e.g. `Total Maintenance Spent: $425.00`).
  3. Scroll down chronological timeline of logged services.
  4. Tap a service item card to view full detail popup (Invoice notes, provider name, logged mileage).
* **Expected Outcome:**
  * Total maintenance spending calculation is accurate across all historical records.
  * Filters for Date Range and Category (Routine, Repair, Inspection) function properly.
* **Automated Test Ref:** `pytest src/tests/unit/test_maintenance_uc037.py`

---

#### UC-038: Bulk Accept Maintenance Schedule
* **Target Screen:** Maintenance Schedule Screen
* **Navigation Path:** Fleet Directory -> Tap Vehicle -> Maintenance Schedule -> Click **"Accept All Recommended"** banner button.
* **Pre-conditions:** Newly added vehicle with unconfirmed OEM maintenance recommendations.
* **Execution Steps:**
  1. Open Maintenance Schedule screen for a new vehicle.
  2. Click **"Bulk Accept Recommended Schedule"** button at top of schedule list.
  3. Confirm bulk approval in dialog popup.
* **Expected Outcome:**
  * All recommended OEM maintenance items transition from `RECOMMENDED` to `ACTIVE SCHEDULED`.
  * Success toast confirms: `"All 6 recommended schedule items accepted into active maintenance plan"`.
* **Automated Test Ref:** `pytest src/tests/unit/test_maintenance_uc038.py`

---

### Module E: Consumer Dashboard & Metrics

#### UC-064: Consumer Dashboard with Vehicle Summary Cards
* **Target Screen:** Dashboard Tab (`DashboardScreen`)
* **Navigation Path:** Tap **Dashboard** icon (1st tab on bottom nav).
* **Pre-conditions:** Vehicles & service logs exist in active organization.
* **Execution Steps:**
  1. Navigate to **Dashboard** tab.
  2. Inspect Metric KPI Cards across top:
     * **Total Fleet Vehicles** (e.g. `4 Vehicles`)
     * **Vehicles Needing Service** (e.g. `1 Overdue`)
     * **Total Monthly Spent** (e.g. `$340.50`)
     * **Fleet Operational Rate** (e.g. `92%`)
  3. Scroll down to **Vehicle Summary Cards Carousel/Grid**.
  4. Verify each card displays vehicle status, upcoming due item, and quick **Log Service** button.
  5. Pull down to refresh screen.
* **Expected Outcome:**
  * Metrics recalculate dynamically from backend database values.
  * Summary cards provide immediate visual status indicators (Green = Healthy, Yellow = Due Soon, Red = Overdue).
* **Automated Test Ref:** `pytest src/tests/unit/test_dashboard_uc064.py`

---

### Module F: Backend Infrastructure & Data Seeding

#### UC-118: Database Migration & Schema Seeding Infrastructure
* **Target Screen:** Backend Terminal / CLI & System Baseline
* **Navigation Path:** Terminal Command Execution.
* **Pre-conditions:** Terminal access to repository root.
* **Execution Steps:**
  1. Open PowerShell terminal.
  2. Execute unit test suite for DB Seeding:
     ```powershell
     pytest src/tests/integration/test_db_seeding_uc118.py -v
     ```
* **Expected Outcome:**
  * Migration scripts create all SQLite tables: `users`, `auth_sessions`, `audit_logs`, `organizations`, `organization_members`, `vehicles`, `maintenance_schedules`, `service_records`.
  * Pre-populated seed records insert cleanly without foreign key violations.
  * Test outputs `27 passed`.
* **Automated Test Ref:** `pytest src/tests/integration/test_db_seeding_uc118.py`

---

## 4. Manual QA Execution Scorecard & Checklist Matrix

Testers can print or copy this section to track pass/fail results during manual test execution:

| Module | Use Case | Description | Target Screen | Status | Tester Initial | Comments / Issues |
|:---|:---|:---|:---|:---:|:---:|:---|
| **Auth** | **UC-001** | Sign Up with Google One-Tap | Auth Tab | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-002** | Sign Up with Facebook Login | Auth Tab | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-003** | Sign Up with Email & Password | Auth Tab -> Form | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-004** | Password Auth & Session Start | Auth Tab | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-005** | Unified Sign In (All Methods) | Auth Tab | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-006** | Forgot Password & Reset Flow | Auth -> Reset Dialog | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-007** | Complete Profile Setup | Profile Onboarding | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-008** | View and Edit Profile | Profile Screen | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-009** | Silent Token Refresh | Background / Security | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-010** | Sign Out & Token Revocation | Profile -> Security | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-011** | Account Deletion (GDPR) | Profile -> Danger Zone | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-012** | Audit Log Recording | Profile -> Audit History | `[ ] PASS / [ ] FAIL` | | |
| **Auth** | **UC-013** | Session & Device Tracking | Profile -> Sessions | `[ ] PASS / [ ] FAIL` | | |
| **Org** | **UC-014** | Auto-Create Personal Org | App Header | `[ ] PASS / [ ] FAIL` | | |
| **Org** | **UC-015** | View & Switch Active Org | Top Bar Dropdown | `[ ] PASS / [ ] FAIL` | | |
| **Org** | **UC-016** | Invite Team Member | Header -> Modal | `[ ] PASS / [ ] FAIL` | | |
| **Vehicle** | **UC-024** | Add Vehicle (VIN Typeahead) | Fleet -> Add Screen | `[ ] PASS / [ ] FAIL` | | |
| **Vehicle** | **UC-025** | View Vehicle List & Filter | Fleet Directory Tab | `[ ] PASS / [ ] FAIL` | | |
| **Vehicle** | **UC-026** | View Vehicle Detail Screen | Fleet -> Vehicle Detail | `[ ] PASS / [ ] FAIL` | | |
| **Vehicle** | **UC-027** | Edit Vehicle Information | Detail -> Edit Screen | `[ ] PASS / [ ] FAIL` | | |
| **Maint** | **UC-034** | View Maintenance Schedule | Detail -> Schedule | `[ ] PASS / [ ] FAIL` | | |
| **Maint** | **UC-035** | Customize Schedule Items | Schedule -> Edit Dialog | `[ ] PASS / [ ] FAIL` | | |
| **Maint** | **UC-036** | Log Service Record | Log Service Screen | `[ ] PASS / [ ] FAIL` | | |
| **Maint** | **UC-037** | View Service History | Detail -> History Screen | `[ ] PASS / [ ] FAIL` | | |
| **Maint** | **UC-038** | Bulk Accept Schedule | Schedule Screen | `[ ] PASS / [ ] FAIL` | | |
| **Dash** | **UC-064** | Consumer Dashboard Cards | Dashboard Tab | `[ ] PASS / [ ] FAIL` | | |
| **Infra** | **UC-118** | DB Migration & Schema Seeding | Backend CLI / pytest | `[ ] PASS / [ ] FAIL` | | |

---

## 5. Summary & Troubleshooting Tips

* **Backend Connection Issues:** Ensure `.\scripts\start_backend.ps1` is running on `http://localhost:8000`. If port 8000 is occupied, verify using `Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess`.
* **State Reset / Seed Reload:** To reset the manual test state back to default seed data, delete `src/backend/dev.db` and restart the backend script.
* **Automated Regression Check:** Run all 27 unit/integration tests in sequence:
  ```powershell
  pytest src/tests/ -v
  ```
