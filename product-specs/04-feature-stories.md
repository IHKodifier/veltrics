# Veltrics Fleet & Vehicle Management — Feature Stories

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md)  
> **Status:** ✅ Approved  
> **Author:** SaaS Founder × Product Designer Persona (App Architect)  
> **Stage:** STAGE 4 — Feature Stories

---

## 1. Feature Story Structure

Every feature story in this document follows a consistent structure for machine-parseability and sprint-readability:

- **Story ID:** `FS-{EPIC}-{NNN}` — globally unique, cross-referenced in downstream artifacts.
- **As a:** The persona performing the action.
- **I want to:** The atomic action.
- **So that:** The value delivered.
- **Priority:** `IN` (ships in MVP) · `POST` (post-MVP) · `OUT` (not part of product).
- **Journey Ref:** Links to User Journey IDs (UJ-XXX) and Screen IDs (SCR-XXX-XXX) from Stage 3.
- **Acceptance Criteria:** Given/When/Then (BDD-style), testable and unambiguous.

### Priority Definitions

| Tag | Meaning | Build Implication |
|:---|:---|:---|
| `IN` | Ships in MVP. The product does not launch without this. | Must be completed before v1 release. |
| `POST` | Post-MVP. Planned for future releases after v1 launch. | Designed for extensibility but not built in v1. |
| `OUT` | Not part of the product vision. Explicitly descoped. | Will not be built. Prevents scope creep. |

---

## 2. Epic Overview

Epics map 1:1 to the backend's domain modules (Architecture Section 2.2) and the frontend's feature modules.

| Epic ID | Epic Name | Module | Story Count | IN | POST |
|:---|:---|:---|:---|:---|:---|
| EP-AUTH | Authentication & Profile | `auth` | 12 | 12 | 0 |
| EP-ORG | Organization & Multi-Tenancy | `organizations` | 10 | 10 | 0 |
| EP-VEH | Vehicle Management | `vehicles` | 10 | 10 | 0 |
| EP-MNT | Maintenance Engine | `maintenance` | 12 | 12 | 0 |
| EP-FUEL | Fuel Logging | `fuel` | 6 | 6 | 0 |
| EP-TRIP | Trip Logging | `trips` | 6 | 6 | 0 |
| EP-EXP | Expense Recording | `expenses` | 6 | 6 | 0 |
| EP-DASH | Dashboards | `dashboard` | 8 | 8 | 0 |
| EP-NOTIF | Notifications | `notifications` | 8 | 8 | 0 |
| EP-PAY | Payments & Subscriptions | `payments` | 10 | 10 | 0 |
| EP-SYNC | Offline Sync | `common` / client | 8 | 8 | 0 |
| EP-AD | Advertising (Free Tier) | `ads` | 5 | 5 | 0 |
| EP-DRV | Driver Scoring | — | 4 | 4 | 0 |
| EP-THEME | Dark Mode & Theming | client | 3 | 3 | 0 |
| EP-EXPORT | Data Export (Pro) | — | 3 | 3 | 0 |
| EP-SET | Settings & Account | — | 6 | 6 | 0 |
| **Total** | | | **117** | **117** | **0** |

> All 117 stories are tagged `IN`. Post-MVP and Out-of-scope items are listed in Section 19.

---

## 3. EP-AUTH — Authentication & Profile

### FS-AUTH-001: Sign up with Google One-Tap

- **As a** new user (consumer)
- **I want to** create an account using my Google account with a single tap
- **So that** I can start using the app in under 10 seconds without creating a new password.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 3) · SCR-AUTH-003, SCR-AUTH-004
- **Acceptance Criteria:**
  - GIVEN I am on the login/register screen, WHEN I tap "Continue with Google", THEN the Google One-Tap prompt appears.
  - GIVEN I select my Google account, WHEN authentication succeeds, THEN my profile is created on the backend (`POST /api/v1/auth/register`) with name and email pre-filled from Google.
  - GIVEN registration succeeds, THEN a personal pseudo-organization is created for me with `is_personal = true`.
  - GIVEN registration succeeds, THEN Firebase custom claims are set: `{role: "consumer", tier: "free"}`.
  - GIVEN registration succeeds, THEN I am navigated to the Profile Setup screen (SCR-AUTH-007).

### FS-AUTH-001b: Sign up with Facebook Login

- **As a** new user (consumer or fleet manager)
- **I want to** create an account using my Facebook account
- **So that** I can register quickly using my existing social profile.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 3) · SCR-AUTH-003, SCR-AUTH-004
- **Acceptance Criteria:**
  - GIVEN I am on the login/register screen, WHEN I tap "Continue with Facebook", THEN the Facebook OAuth sign-in flow initiates via Firebase Auth SDK.
  - GIVEN I grant permission, WHEN authentication succeeds, THEN my profile is created on the backend (`POST /api/v1/auth/register`) with name, email, and avatar pre-filled from Facebook.
  - GIVEN registration succeeds, THEN a personal pseudo-organization is created for me with `is_personal = true`.
  - GIVEN registration succeeds, THEN Firebase custom claims are set: `{role: "consumer", tier: "free"}`.
  - GIVEN registration succeeds, THEN I am navigated to the Profile Setup screen (SCR-AUTH-007).

### FS-AUTH-002: Sign up with Email and Password

- **As a** new user (consumer)
- **I want to** create an account using my email address and a password
- **So that** I can use the app without linking a Google account.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 3) · SCR-AUTH-003, SCR-AUTH-004
- **Acceptance Criteria:**
  - GIVEN I am on the register screen, WHEN I enter a valid email and password (min 8 characters, 1 uppercase, 1 number), THEN Firebase Auth creates the account.
  - GIVEN registration succeeds, THEN the backend creates my profile and personal pseudo-organization.
  - GIVEN registration succeeds, THEN I am navigated to the Profile Setup screen.
  - GIVEN I enter an email already in use, WHEN I tap "Create Account", THEN I see an inline error: "An account with this email already exists. [Sign in instead]".
  - GIVEN registration succeeds, THEN email verification is NOT required to proceed. A subtle banner appears later: "Verify your email to enable password recovery."

### FS-AUTH-003: Sign up with Phone OTP

- **As a** new user (driver or consumer)
- **I want to** create an account using my phone number with OTP verification
- **So that** I can use the app without an email address (common for drivers in Pakistan).
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 3), UJ-003 · SCR-AUTH-005
- **Acceptance Criteria:**
  - GIVEN I am on the register screen, WHEN I enter a valid phone number with country code (e.g., +92 3XX XXXXXXX), THEN Firebase Auth sends an SMS OTP.
  - GIVEN I receive the OTP, WHEN I enter the correct 6-digit code within 60 seconds, THEN my account is created.
  - GIVEN the OTP expires (60s), WHEN I tap "Resend Code", THEN a new OTP is sent (max 3 retries).
  - GIVEN the phone number is already registered, THEN I see: "This phone number is already in use. [Sign in instead]".

### FS-AUTH-004: Sign in (all methods)

- **As a** returning user
- **I want to** sign in using my previously registered method (Google, Facebook, email/password, or phone OTP)
- **So that** I can access my vehicles and data.
- **Priority:** `IN`
- **Journey Ref:** UJ-010 · SCR-AUTH-003
- **Acceptance Criteria:**
  - GIVEN I am on the login screen, WHEN I authenticate with valid credentials, THEN I receive a Firebase ID Token and am navigated to my dashboard.
  - GIVEN I enter incorrect email/password, THEN I see: "Invalid email or password. [Forgot password?]".
  - GIVEN I have a valid cached token on app launch, THEN I skip the login screen and go directly to the dashboard (splash screen auto-navigates).
  - GIVEN my cached token is expired but the refresh token is valid, THEN Firebase SDK silently refreshes the token and I proceed without interruption.

### FS-AUTH-005: Forgot password

- **As a** user who forgot their password
- **I want to** reset my password via email
- **So that** I can regain access to my account.
- **Priority:** `IN`
- **Journey Ref:** UJ-010 · SCR-AUTH-006
- **Acceptance Criteria:**
  - GIVEN I am on the login screen, WHEN I tap "Forgot Password", THEN I see an email input field.
  - GIVEN I enter my registered email, WHEN I tap "Send Reset Link", THEN Firebase Auth sends a password reset email within 30 seconds.
  - GIVEN I click the reset link in the email, THEN I am taken to a Firebase-hosted page where I can set a new password.
  - GIVEN I enter an unregistered email, THEN I see: "No account found with this email."

### FS-AUTH-006: Complete profile setup

- **As a** new user
- **I want to** set my display name and optional city after registration
- **So that** my profile is personalized.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 4) · SCR-AUTH-007
- **Acceptance Criteria:**
  - GIVEN I just registered, WHEN I land on Profile Setup, THEN my name is pre-filled (from Google if applicable).
  - GIVEN I enter a display name (required, 2-50 chars) and optional city, WHEN I tap "Continue", THEN my profile is updated via `PATCH /api/v1/users/me`.
  - GIVEN I skip city, THEN the field is stored as null — no error.
  - GIVEN profile setup completes, THEN I am navigated to "Add Your First Vehicle" (SCR-VEH-001).

### FS-AUTH-007: View and edit profile

- **As a** registered user
- **I want to** view and update my display name, city, and avatar
- **So that** my profile stays current.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Profile, THEN I see my current display name, email/phone, city, and avatar.
  - GIVEN I edit my display name and tap "Save", THEN the backend updates via `PATCH /api/v1/users/me` and I see a success toast.
  - GIVEN I tap my avatar, THEN I can choose a new photo from the device gallery. The photo uploads to Firebase Storage via signed URL.

### FS-AUTH-008: Silent token refresh

- **As a** user with an expired session token
- **I want to** have my token refreshed automatically without any visible interruption
- **So that** my app experience is seamless.
- **Priority:** `IN`
- **Journey Ref:** UJ-010
- **Acceptance Criteria:**
  - GIVEN my Firebase ID Token has expired (1-hour TTL), WHEN I make an API request, THEN the Flutter HTTP interceptor detects the 401, triggers Firebase SDK token refresh, and retries the original request.
  - GIVEN the refresh succeeds, THEN I see no error, no modal, no interruption — the request completes as if nothing happened.
  - GIVEN the refresh token is also invalid (inactive for weeks), THEN I see a "Session expired" modal with a "Sign in again" button, and my email is pre-filled on the login screen.

### FS-AUTH-009: Role-based navigation rendering

- **As a** user with a specific role (consumer/driver/fleet_manager/admin)
- **I want to** see only the navigation items and screens relevant to my role
- **So that** I am not confused by features I cannot use.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-001, SCR-DASH-002, SCR-DASH-003
- **Acceptance Criteria:**
  - GIVEN I am a `consumer`, THEN I see: Dashboard, My Vehicles, Settings. I do NOT see: Drivers, Organization Settings.
  - GIVEN I am a `driver`, THEN I see: My Assignments, Quick Log (Fuel/Trip/Odometer), Settings. I do NOT see: Add Vehicle, Payments, Organization.
  - GIVEN I am a `fleet_manager`, THEN I see: Fleet Dashboard, Vehicles, Drivers, Expenses, Payments, Organization Settings, Settings.
  - GIVEN I am an `admin`, THEN I see everything a `fleet_manager` sees PLUS Audit Logs and User Management.

### FS-AUTH-010: Session-expired forced re-authentication

- **As a** user whose refresh token has expired
- **I want to** be prompted to sign in again with minimal friction
- **So that** I can resume using the app quickly.
- **Priority:** `IN`
- **Journey Ref:** UJ-010 · SCR-AUTH-003
- **Acceptance Criteria:**
  - GIVEN my refresh token is invalid, WHEN I attempt any API action, THEN I see a modal: "Your session has expired. Please sign in again."
  - GIVEN I tap "Sign In", THEN I am navigated to the login screen with my email pre-filled.
  - GIVEN I re-authenticate successfully, THEN I am returned to the screen I was on before the session expired.

### FS-AUTH-011: Splash screen with auto-navigation

- **As a** user launching the app
- **I want to** see a brief branded splash screen that automatically navigates me to the right place
- **So that** I don't waste time on login if I'm already authenticated.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 1) · SCR-AUTH-001
- **Acceptance Criteria:**
  - GIVEN I have a valid cached token, WHEN the app launches, THEN the splash screen displays for ≤ 1.5 seconds and I am navigated to my dashboard.
  - GIVEN I have no cached token, WHEN the app launches, THEN I am navigated to the Welcome screen (SCR-AUTH-002).
  - GIVEN the token check fails (network error), THEN the app navigates to the dashboard in offline mode (if cached data exists) or the login screen.

### FS-AUTH-012: Welcome / onboarding carousel

- **As a** first-time user
- **I want to** see a brief 2-3 card carousel explaining the app's value before signing up
- **So that** I understand what Veltrics does and am motivated to register.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 2) · SCR-AUTH-002
- **Acceptance Criteria:**
  - GIVEN I am a first-time user (no cached token), WHEN I pass the splash screen, THEN I see a horizontal carousel with 2-3 value proposition cards.
  - GIVEN I swipe through all cards OR tap "Get Started", THEN I am navigated to the auth screen (SCR-AUTH-003).
  - GIVEN I have seen the carousel before (flag stored locally), THEN the carousel is skipped on subsequent launches — I go directly to login.

---

## 4. EP-ORG — Organization & Multi-Tenancy

### FS-ORG-001: Auto-create personal pseudo-organization on registration

- **As a** new consumer
- **I want to** have a personal organization created automatically when I register
- **So that** all my data is organization-scoped from Day 1 (consistent query paths).
- **Priority:** `IN`
- **Journey Ref:** UJ-001 · Architecture Section 6.2
- **Acceptance Criteria:**
  - GIVEN I complete registration (any method), THEN the backend creates an `Organization` record with `is_personal = true`, `name = "{user's display name}'s Vehicles"`, and `max_vehicles = X` (free tier limit).
  - GIVEN the personal org is created, THEN I am added as the sole `Membership` with role `consumer`.
  - GIVEN the personal org exists, THEN all my vehicle, fuel, trip, expense, and maintenance queries are scoped to this org's `organization_id`.

### FS-ORG-002: Convert personal org to full organization on Pro upgrade

- **As a** consumer upgrading to Pro
- **I want to** have my personal organization automatically converted into a full organization
- **So that** my existing vehicles and data carry over seamlessly.
- **Priority:** `IN`
- **Journey Ref:** UJ-002, UJ-012 · Architecture Section 5.4
- **Acceptance Criteria:**
  - GIVEN my Pro subscription is activated (payment webhook confirmed), THEN my personal org's `is_personal` flag is set to `false`.
  - GIVEN the conversion completes, THEN `max_vehicles` is raised to the Pro tier limit and `max_drivers` is set to the Pro driver limit.
  - GIVEN the conversion completes, THEN my Firebase custom claims are updated to `{role: "fleet_manager", org_id: "...", tier: "pro"}`.
  - GIVEN the conversion completes, THEN all my existing vehicles remain in the organization — no data loss, no re-entry.

### FS-ORG-003: Edit organization details

- **As a** fleet manager or admin
- **I want to** update my organization's business name, logo, and industry type
- **So that** my organization profile is accurate and professional.
- **Priority:** `IN`
- **Journey Ref:** UJ-002 · SCR-ORG-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Organization Settings, THEN I see fields for Business Name, Logo (image upload), and Industry Type (dropdown: Logistics, Rental, Hotel Transport, Other).
  - GIVEN I update the business name and tap "Save", THEN `PATCH /api/v1/organizations/{id}` updates the record and I see a success toast.
  - GIVEN I upload a logo, THEN the image is stored via Firebase Storage signed URL and the org record is updated with the logo URI.

### FS-ORG-004: View organization members

- **As a** fleet manager or admin
- **I want to** see a list of all members (drivers, other managers) in my organization
- **So that** I can manage my team.
- **Priority:** `IN`
- **Journey Ref:** SCR-ORG-002
- **Acceptance Criteria:**
  - GIVEN I navigate to Drivers, THEN I see a list of all organization members with: Name, Phone, Role, Status (Active/Invited/Inactive), Assigned Vehicles count.
  - GIVEN the list has > 20 members, THEN pagination is applied (`GET /api/v1/organizations/{id}/members?page=1&per_page=20`).

### FS-ORG-005: Invite a driver by phone number

- **As a** fleet manager or admin
- **I want to** invite a driver to join my organization by entering their phone number
- **So that** they can log fuel, trips, and odometer readings for assigned vehicles.
- **Priority:** `IN`
- **Journey Ref:** UJ-003 · SCR-ORG-003
- **Acceptance Criteria:**
  - GIVEN I am on the Invite Driver screen, WHEN I enter a valid phone number (+92 format) and tap "Send Invitation", THEN `POST /api/v1/organizations/{id}/invitations` creates an invitation with a 6-character invite code (e.g., `VLT-A3K`), status `pending`, and 7-day expiry.
  - GIVEN the invited phone number belongs to an existing app user, THEN they receive an FCM push notification: "You've been invited to join [Business Name] as a driver."
  - GIVEN the invited phone number does NOT belong to an existing user, THEN they receive an SMS with a Play Store deep link and the invite code.
  - GIVEN I have reached the driver limit for my tier, THEN I see the quota exceeded prompt (UJ-011) instead of the invitation form.

### FS-ORG-006: Invite a driver by email

- **As a** fleet manager or admin
- **I want to** invite a driver by email as an alternative to phone
- **So that** I have flexibility in how I reach team members.
- **Priority:** `IN`
- **Journey Ref:** UJ-003 · SCR-ORG-003
- **Acceptance Criteria:**
  - GIVEN I am on the Invite Driver screen, WHEN I enter a valid email and tap "Send Invitation", THEN an invitation is created and an email is sent with the invite code and app download link.
  - GIVEN the invited email belongs to an existing user, THEN they receive an FCM push notification in-app.

### FS-ORG-007: Accept invitation (existing user, in-app)

- **As a** driver who received an invitation
- **I want to** accept the invitation from within the app
- **So that** I join the organization and see my assigned vehicles.
- **Priority:** `IN`
- **Journey Ref:** UJ-003 · SCR-ORG-005
- **Acceptance Criteria:**
  - GIVEN I open the app and have a pending invitation, THEN I see a banner: "You've been invited to join [Business Name] as a driver."
  - GIVEN I tap "Accept", THEN `PATCH /api/v1/invitations/{id}/accept` processes the acceptance, adds me to the organization, and updates my Firebase custom claims to `{role: "driver", org_id: "...", tier: "pro"}`.
  - GIVEN I tap "Decline", THEN the invitation is dismissed and I remain in my current state.
  - GIVEN my token is refreshed, THEN my navigation updates to show the Driver Dashboard (SCR-DASH-003).

### FS-ORG-008: Redeem invite code (new user)

- **As a** new user who received an invite code
- **I want to** enter the code after signing up to join an organization
- **So that** I can start logging data for my fleet immediately.
- **Priority:** `IN`
- **Journey Ref:** UJ-003 · SCR-ORG-006
- **Acceptance Criteria:**
  - GIVEN I just completed registration, WHEN I see the "Do you have an invite code?" prompt, THEN I can enter the 6-character code (e.g., `VLT-A3K`).
  - GIVEN I enter a valid, non-expired code, WHEN I tap "Join", THEN `POST /api/v1/invitations/redeem` adds me to the organization as a driver.
  - GIVEN I enter an expired or invalid code, THEN I see: "This invitation has expired or is invalid. Please ask your fleet manager to resend."

### FS-ORG-009: Remove a member from organization

- **As a** fleet manager or admin
- **I want to** remove a driver or member from my organization
- **So that** I can manage team access when someone leaves.
- **Priority:** `IN`
- **Journey Ref:** SCR-ORG-004
- **Acceptance Criteria:**
  - GIVEN I am on a driver's detail page, WHEN I tap "Remove from Organization" and confirm, THEN `DELETE /api/v1/organizations/{id}/members/{member_id}` removes the membership.
  - GIVEN the member is removed, THEN their Firebase custom claims revert to `{role: "consumer", tier: "free"}` and they lose access to org-scoped data.
  - GIVEN the member had a personal pseudo-org before joining, THEN they return to their personal org with their personal vehicles.

### FS-ORG-010: Cancel a pending invitation

- **As a** fleet manager or admin
- **I want to** cancel a pending invitation that hasn't been accepted
- **So that** I can revoke access before someone joins.
- **Priority:** `IN`
- **Journey Ref:** SCR-ORG-002
- **Acceptance Criteria:**
  - GIVEN I see a member with status "Invited" in the driver list, WHEN I tap "Cancel Invitation", THEN `DELETE /api/v1/invitations/{id}` invalidates the invitation.
  - GIVEN the invitation is cancelled, THEN the invite code can no longer be redeemed. The invited person sees "This invitation has been cancelled" if they try.

---

## 5. EP-VEH — Vehicle Management

### FS-VEH-001: Add a vehicle with typeahead

- **As a** consumer or fleet manager
- **I want to** add a vehicle by searching Make → Model → Year with typeahead auto-suggestions
- **So that** I can quickly register my vehicle without manual text entry errors.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 5) · SCR-VEH-001
- **Acceptance Criteria:**
  - GIVEN I am on the Add Vehicle screen, WHEN I start typing a make (e.g., "Toy"), THEN a dropdown suggests matching makes ("Toyota").
  - GIVEN I select a make, WHEN I start typing a model, THEN suggestions are filtered to that make ("Corolla", "Camry", "Hilux").
  - GIVEN I select make, model, and year, WHEN I enter the current odometer reading, license plate, and optionally VIN and color, THEN tapping "Save" calls `POST /api/v1/vehicles`.
  - GIVEN the vehicle is saved, THEN a pre-populated maintenance schedule is returned and displayed (SCR-MNT-001).
  - GIVEN I have reached my tier's vehicle limit (X), THEN I see the quota exceeded upgrade prompt (UJ-011) instead of the Add Vehicle form.

### FS-VEH-002: View vehicle list

- **As a** consumer or fleet manager
- **I want to** see all my vehicles in a scrollable list with status indicators
- **So that** I can quickly identify which vehicles need attention.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-003
- **Acceptance Criteria:**
  - GIVEN I navigate to Vehicles, THEN I see a list of vehicle cards showing: Make/Model/Year, license plate, current odometer, and status badge (🟢 Healthy / 🟡 Attention / 🔴 Overdue).
  - GIVEN a vehicle has overdue maintenance, THEN its status badge is 🔴 Overdue.
  - GIVEN a vehicle has maintenance due within 7 days or 500 km, THEN its badge is 🟡 Attention.
  - GIVEN a vehicle has no upcoming maintenance issues, THEN its badge is 🟢 Healthy.

### FS-VEH-003: View vehicle detail

- **As a** user
- **I want to** view a vehicle's complete profile with tabs for Overview, Maintenance, Fuel, Trips, and Expenses
- **So that** I can see all data related to a single vehicle in one place.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-002
- **Acceptance Criteria:**
  - GIVEN I tap a vehicle card, THEN I see the Vehicle Detail screen with a header (make/model/year, photo, odometer, status) and tabs: Overview, Maintenance, Fuel, Trips, Expenses.
  - GIVEN I tap the Maintenance tab, THEN I see the maintenance schedule + service history for this vehicle.
  - GIVEN I tap the Fuel tab, THEN I see the fuel log history with a fuel efficiency trend indicator.

### FS-VEH-004: Edit vehicle

- **As a** consumer or fleet manager
- **I want to** update a vehicle's details (license plate, color, photo, odometer)
- **So that** I can keep vehicle information accurate.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-004
- **Acceptance Criteria:**
  - GIVEN I am on the Vehicle Detail screen, WHEN I tap "Edit", THEN I see the vehicle form pre-filled with current values.
  - GIVEN I update the license plate and tap "Save", THEN `PATCH /api/v1/vehicles/{id}` updates the record and I see a success toast.
  - GIVEN I update the odometer reading, THEN the maintenance schedule recalculates next-due dates based on the new odometer value.

### FS-VEH-005: Delete vehicle (soft delete)

- **As a** consumer or fleet manager
- **I want to** remove a vehicle from my list
- **So that** I can clean up vehicles I no longer own.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-002
- **Acceptance Criteria:**
  - GIVEN I am on the Vehicle Detail screen, WHEN I tap "Delete Vehicle" and confirm, THEN `DELETE /api/v1/vehicles/{id}` soft-deletes the vehicle.
  - GIVEN the vehicle is soft-deleted, THEN it no longer appears in my vehicle list or dashboard.
  - GIVEN the vehicle is soft-deleted, THEN it can be recovered within 30 days via Settings → Deleted Vehicles.

### FS-VEH-006: Log odometer reading

- **As a** consumer or driver
- **I want to** record the current odometer reading without logging a fuel or trip entry
- **So that** maintenance schedule calculations stay accurate.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-002
- **Acceptance Criteria:**
  - GIVEN I am on the Vehicle Detail screen, WHEN I tap "Update Odometer", THEN I see a numeric input pre-filled with the last known reading.
  - GIVEN I enter a new reading (must be ≥ last known), WHEN I tap "Save", THEN `POST /api/v1/vehicles/{id}/odometer-readings` records the reading with a timestamp.
  - GIVEN the new reading triggers a maintenance item (e.g., passed 90,000 km), THEN the maintenance schedule updates the item to "Due Now" or "Overdue".

### FS-VEH-007: Assign vehicle to driver

- **As a** fleet manager or admin
- **I want to** assign a vehicle to a specific driver in my organization
- **So that** the driver sees only their assigned vehicles and can log data for them.
- **Priority:** `IN`
- **Journey Ref:** SCR-ORG-004, SCR-VEH-002
- **Acceptance Criteria:**
  - GIVEN I am on the Vehicle Detail screen (as fleet manager), WHEN I tap "Assign Driver", THEN I see a list of organization drivers.
  - GIVEN I select a driver and confirm, THEN `POST /api/v1/vehicles/{id}/assignments` creates the assignment.
  - GIVEN the assignment is made, THEN the driver sees this vehicle in their Driver Dashboard (SCR-DASH-003).

### FS-VEH-008: Unassign vehicle from driver

- **As a** fleet manager or admin
- **I want to** remove a vehicle assignment from a driver
- **So that** I can reassign vehicles when needed.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-002
- **Acceptance Criteria:**
  - GIVEN a vehicle is assigned to a driver, WHEN I tap "Unassign" and confirm, THEN `DELETE /api/v1/vehicles/{id}/assignments/{assignment_id}` removes the assignment.
  - GIVEN the assignment is removed, THEN the vehicle no longer appears in the driver's dashboard.

### FS-VEH-009: Upload vehicle photo

- **As a** consumer or fleet manager
- **I want to** upload a photo of my vehicle
- **So that** I can visually identify vehicles in my list.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-001, SCR-VEH-004
- **Acceptance Criteria:**
  - GIVEN I am adding or editing a vehicle, WHEN I tap the photo area, THEN I can select a photo from my device gallery or take a new photo.
  - GIVEN I select a photo, THEN it is uploaded to Firebase Storage via a signed URL. The vehicle record stores the photo URI.
  - GIVEN no photo is uploaded, THEN a default vehicle silhouette icon is displayed.

### FS-VEH-010: Recover deleted vehicle

- **As a** consumer or fleet manager
- **I want to** recover a vehicle I deleted within the last 30 days
- **So that** I can undo accidental deletions.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Deleted Vehicles, THEN I see a list of soft-deleted vehicles with deletion dates.
  - GIVEN I tap "Restore" on a vehicle deleted < 30 days ago, THEN the vehicle and all its associated data (fuel logs, maintenance, trips, expenses) are restored.
  - GIVEN a vehicle was deleted > 30 days ago, THEN it is permanently purged and not shown.

---

## 6. EP-MNT — Maintenance Engine

### FS-MNT-001: View pre-populated maintenance schedule after adding vehicle

- **As a** consumer
- **I want to** see a maintenance schedule automatically generated for my vehicle based on Make/Model/Year and current odometer
- **So that** I know immediately what maintenance is coming up without configuring anything manually.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 6, Aha Moment) · SCR-MNT-001
- **Acceptance Criteria:**
  - GIVEN I just added a vehicle with Make, Model, Year, and Odometer, WHEN the vehicle is saved, THEN the backend returns a pre-populated maintenance schedule based on the vehicle category's default template.
  - GIVEN the schedule is returned, THEN I see a list of maintenance items with: Item Name, Interval (km and/or days), Next Due Date, Next Due Odometer.
  - GIVEN my current odometer is 85,000 km and the oil change interval is every 5,000 km, THEN the next oil change is shown as "Due at 90,000 km".
  - GIVEN I see the schedule, THEN I can tap "Accept All" to activate all reminders, or tap individual items to customize.

### FS-MNT-002: Customize maintenance schedule items

- **As a** consumer or fleet manager
- **I want to** edit individual maintenance items (toggle on/off, change intervals, adjust next-due values)
- **So that** the schedule matches my actual vehicle needs and driving habits.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 7) · SCR-MNT-004
- **Acceptance Criteria:**
  - GIVEN I am viewing a maintenance schedule, WHEN I tap an item, THEN I see editable fields: Enabled (toggle), Interval (km), Interval (days), Next Due Date, Next Due Odometer.
  - GIVEN I change the oil change interval from 5,000 km to 3,000 km, WHEN I tap "Save", THEN the next-due odometer recalculates.
  - GIVEN I toggle an item OFF, THEN it is hidden from the schedule and no reminders are sent for it.

### FS-MNT-003: Log a service record

- **As a** consumer or driver
- **I want to** log a maintenance service with multiple service items, costs, and an optional receipt photo
- **So that** my maintenance history is complete and my schedule auto-advances.
- **Priority:** `IN`
- **Journey Ref:** UJ-005 · SCR-MNT-002
- **Acceptance Criteria:**
  - GIVEN I am on the Log Service screen, WHEN I select service items from the multi-select picker (e.g., Engine Oil Change, Oil Filter), THEN each item appears with optional fields: Cost, Notes.
  - GIVEN I select "Engine Oil Change" with odometer 90,000 km, WHEN I save, THEN the maintenance schedule advances: "Next Oil Change: 95,000 km" (or based on configured interval).
  - GIVEN I enter per-item costs, THEN the Total Cost field auto-sums. I can override the total.
  - GIVEN I attach a receipt photo (optional), THEN it uploads to Firebase Storage via signed URL.
  - GIVEN I save the service record, THEN `POST /api/v1/maintenance/service-records` stores the record with all items.

### FS-MNT-004: Add custom service item

- **As a** consumer or fleet manager
- **I want to** add a service item not in the standard list
- **So that** I can track any type of service.
- **Priority:** `IN`
- **Journey Ref:** UJ-005 · SCR-MNT-002
- **Acceptance Criteria:**
  - GIVEN I am on the service item picker, WHEN I scroll to the bottom and tap "Custom Item...", THEN I see a text field for the item name.
  - GIVEN I enter a custom item name (e.g., "Windshield Replacement") and optional cost, THEN it is included in the service record.
  - GIVEN the custom item is saved, THEN it does NOT trigger any schedule recalculation (no known interval).

### FS-MNT-005: View service history for a vehicle

- **As a** user
- **I want to** see all past service records for a specific vehicle in chronological order
- **So that** I have a complete maintenance history.
- **Priority:** `IN`
- **Journey Ref:** SCR-MNT-003
- **Acceptance Criteria:**
  - GIVEN I am on the Vehicle Detail → Maintenance tab, WHEN I scroll past the schedule, THEN I see a chronological list of service records with: Date, Odometer, Items serviced, Total cost, Mechanic name.
  - GIVEN I tap a service record, THEN I see the full detail including per-item costs, notes, and receipt photo (if attached).

### FS-MNT-006: Edit a service record

- **As a** consumer or fleet manager
- **I want to** edit a previously logged service record
- **So that** I can correct errors.
- **Priority:** `IN`
- **Journey Ref:** SCR-MNT-003
- **Acceptance Criteria:**
  - GIVEN I tap a service record and then "Edit", THEN I see the service form pre-filled with existing values.
  - GIVEN I update the cost and tap "Save", THEN `PATCH /api/v1/maintenance/service-records/{id}` updates the record.
  - GIVEN I change the odometer reading, THEN the maintenance schedule recalculates.

### FS-MNT-007: Delete a service record

- **As a** consumer or fleet manager
- **I want to** delete a service record
- **So that** I can remove erroneous entries.
- **Priority:** `IN`
- **Journey Ref:** SCR-MNT-003
- **Acceptance Criteria:**
  - GIVEN I tap a service record and then "Delete" and confirm, THEN `DELETE /api/v1/maintenance/service-records/{id}` soft-deletes the record.
  - GIVEN the record is deleted, THEN the maintenance schedule does NOT revert (the service was performed; only the record is removed).

### FS-MNT-008: View overdue maintenance alerts

- **As a** user
- **I want to** see a prominent alert when a maintenance item is overdue
- **So that** I take immediate action.
- **Priority:** `IN`
- **Journey Ref:** SCR-MNT-005, SCR-DASH-001, SCR-DASH-002
- **Acceptance Criteria:**
  - GIVEN a maintenance item's next-due date has passed OR the vehicle's current odometer exceeds the next-due odometer, THEN the item is flagged as "Overdue" with a 🔴 red badge.
  - GIVEN the item is overdue, THEN it appears in the Dashboard's Alerts & Actions panel with a "Log Service" CTA.
  - GIVEN the item is overdue and push notifications are enabled, THEN a push notification was sent (see EP-NOTIF).

### FS-MNT-009: View upcoming maintenance alerts

- **As a** user
- **I want to** see maintenance items coming due in the next 7 days or 500 km
- **So that** I can plan ahead.
- **Priority:** `IN`
- **Journey Ref:** SCR-MNT-005, SCR-DASH-001
- **Acceptance Criteria:**
  - GIVEN a maintenance item's next-due date is within 7 days OR the vehicle's odometer is within 500 km of the next-due reading, THEN the item is flagged as "Upcoming" with a 🟡 yellow badge.
  - GIVEN the item is upcoming, THEN it appears in the Dashboard's Alerts panel.

### FS-MNT-010: Bulk accept maintenance schedule

- **As a** consumer
- **I want to** accept all pre-populated maintenance items at once during onboarding
- **So that** I can quickly set up reminders without reviewing each item individually.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 7) · SCR-MNT-001
- **Acceptance Criteria:**
  - GIVEN I see the pre-populated schedule, WHEN I tap "Accept All", THEN `POST /api/v1/maintenance/schedules/bulk` saves all items as active.
  - GIVEN all items are active, THEN I am navigated to the FCM permission prompt.

### FS-MNT-011: View maintenance schedule timeline

- **As a** user
- **I want to** see a visual timeline of all upcoming maintenance items for a vehicle
- **So that** I can plan service visits efficiently.
- **Priority:** `IN`
- **Journey Ref:** SCR-MNT-001
- **Acceptance Criteria:**
  - GIVEN I am on the Vehicle Detail → Maintenance tab, THEN I see a timeline view of scheduled items ordered by next-due date/odometer.
  - GIVEN each item shows: Item name, Due date (or odometer), Status (OK / Upcoming / Overdue), Last serviced date.

### FS-MNT-012: Create maintenance schedule for additional vehicles

- **As a** consumer or fleet manager
- **I want to** get a pre-populated maintenance schedule when I add subsequent vehicles (not just the first one)
- **So that** every vehicle gets the same intelligent setup experience.
- **Priority:** `IN`
- **Journey Ref:** SCR-VEH-001
- **Acceptance Criteria:**
  - GIVEN I add a 2nd (or subsequent) vehicle, WHEN the vehicle is saved, THEN a pre-populated schedule is generated and displayed, just like the first vehicle.

---

## 7. EP-FUEL — Fuel Logging

### FS-FUEL-001: Log a fuel entry

- **As a** consumer or driver
- **I want to** log a fuel entry with liters, cost, odometer, and optional station name
- **So that** I track fuel consumption and spending.
- **Priority:** `IN`
- **Journey Ref:** UJ-004 · SCR-FUEL-001
- **Acceptance Criteria:**
  - GIVEN I tap "⛽ Log Fuel" on the dashboard, THEN I see a form with: Vehicle (pre-selected if single), Liters/Gallons (numeric keypad), Total Cost (numeric keypad), Odometer (pre-filled from last reading), Station Name (optional), Date (pre-filled: today).
  - GIVEN I enter valid values and tap "Save", THEN `POST /api/v1/fuel-logs` stores the entry.
  - GIVEN I am offline, THEN the entry is saved to Hive local storage and enqueued for sync. A yellow "pending" badge appears on the entry.

### FS-FUEL-002: View fuel log history for a vehicle

- **As a** user
- **I want to** see all fuel entries for a vehicle in chronological order with a fuel efficiency trend
- **So that** I can monitor consumption over time.
- **Priority:** `IN`
- **Journey Ref:** SCR-FUEL-002
- **Acceptance Criteria:**
  - GIVEN I am on Vehicle Detail → Fuel tab, THEN I see a list of fuel entries with: Date, Liters, Cost, Odometer, Station Name.
  - GIVEN I have ≥ 3 fuel entries, THEN a fuel efficiency indicator is displayed (km/liter or liters/100km, calculated from consecutive odometer/fuel readings).

### FS-FUEL-003: Edit a fuel entry

- **As a** consumer or driver
- **I want to** edit a fuel log entry to correct errors
- **So that** my records remain accurate.
- **Priority:** `IN`
- **Journey Ref:** SCR-FUEL-002
- **Acceptance Criteria:**
  - GIVEN I tap a fuel entry and then "Edit", THEN I see the form pre-filled with existing values.
  - GIVEN I update the cost and tap "Save", THEN `PATCH /api/v1/fuel-logs/{id}` updates the record and the dashboard cost summary refreshes.

### FS-FUEL-004: Delete a fuel entry

- **As a** consumer or fleet manager
- **I want to** delete a fuel log entry
- **So that** I can remove erroneous entries.
- **Priority:** `IN`
- **Journey Ref:** SCR-FUEL-002
- **Acceptance Criteria:**
  - GIVEN I tap a fuel entry and then "Delete" and confirm, THEN `DELETE /api/v1/fuel-logs/{id}` soft-deletes the record and the dashboard cost summary updates.

### FS-FUEL-005: Calculate fuel efficiency

- **As a** user
- **I want to** see my vehicle's calculated fuel efficiency based on fuel logs
- **So that** I can identify unusual consumption patterns.
- **Priority:** `IN`
- **Journey Ref:** SCR-FUEL-002, SCR-DASH-001
- **Acceptance Criteria:**
  - GIVEN a vehicle has ≥ 2 consecutive fuel entries with odometer readings, THEN the system calculates km/liter (or liters/100km based on user preference) for each interval.
  - GIVEN ≥ 3 data points exist, THEN a simple trend indicator shows whether efficiency is improving (↑ green), stable (→ gray), or declining (↓ red).

### FS-FUEL-006: Quick-log fuel from dashboard

- **As a** consumer or driver
- **I want to** tap a single "⛽ Fuel" button on my dashboard to jump directly to the fuel log form
- **So that** logging is fast (< 15 seconds total flow).
- **Priority:** `IN`
- **Journey Ref:** UJ-004 · SCR-DASH-001, SCR-DASH-003
- **Acceptance Criteria:**
  - GIVEN I am on my dashboard, WHEN I tap the "⛽ Fuel" quick-log button, THEN I navigate to SCR-FUEL-001 with the vehicle pre-selected (if single vehicle) and date pre-filled.

---

## 8. EP-TRIP — Trip Logging

### FS-TRIP-001: Log a trip entry

- **As a** consumer or driver
- **I want to** log a trip with start/end odometer, purpose, and optional notes
- **So that** I track vehicle usage and distance.
- **Priority:** `IN`
- **Journey Ref:** UJ-007 · SCR-TRIP-001
- **Acceptance Criteria:**
  - GIVEN I tap "🛣️ Log Trip" on the dashboard, THEN I see a form with: Vehicle (pre-selected), Date (today), Start Odometer (pre-filled from last reading), End Odometer (numeric), Purpose (dropdown: Business / Personal / Delivery), Notes (optional).
  - GIVEN I enter a valid end odometer (≥ start), THEN the distance is auto-calculated and displayed: "Distance: XX km".
  - GIVEN I tap "Save", THEN `POST /api/v1/trips` stores the entry. The vehicle's odometer is updated to the end reading.
  - GIVEN I am offline, THEN the entry saves to Hive and syncs later.

### FS-TRIP-002: View trip history for a vehicle

- **As a** user
- **I want to** see all trips for a vehicle in chronological order
- **So that** I can review usage history.
- **Priority:** `IN`
- **Journey Ref:** SCR-TRIP-002
- **Acceptance Criteria:**
  - GIVEN I am on Vehicle Detail → Trips tab, THEN I see a list of trip entries with: Date, Distance (km), Purpose, Notes.
  - GIVEN I have multiple trips, THEN a monthly distance total is displayed at the top.

### FS-TRIP-003: Edit a trip entry

- **As a** consumer or driver
- **I want to** edit a trip log entry to correct errors
- **So that** my records remain accurate.
- **Priority:** `IN`
- **Journey Ref:** SCR-TRIP-002
- **Acceptance Criteria:**
  - GIVEN I tap a trip entry and then "Edit", THEN I see the form pre-filled with existing values.
  - GIVEN I update the end odometer and tap "Save", THEN `PATCH /api/v1/trips/{id}` updates the record and distance recalculates.

### FS-TRIP-004: Delete a trip entry

- **As a** consumer or fleet manager
- **I want to** delete a trip log entry
- **So that** I can remove erroneous entries.
- **Priority:** `IN`
- **Journey Ref:** SCR-TRIP-002
- **Acceptance Criteria:**
  - GIVEN I tap a trip entry and then "Delete" and confirm, THEN `DELETE /api/v1/trips/{id}` soft-deletes the record.

### FS-TRIP-005: Quick-log trip from dashboard

- **As a** consumer or driver
- **I want to** tap a single "🛣️ Trip" button on my dashboard to jump to the trip log form
- **So that** logging is fast.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-001, SCR-DASH-003
- **Acceptance Criteria:**
  - GIVEN I am on my dashboard, WHEN I tap the "🛣️ Trip" quick-log button, THEN I navigate to SCR-TRIP-001 with vehicle pre-selected and date pre-filled.

### FS-TRIP-006: View distance summary

- **As a** user
- **I want to** see total distance traveled per vehicle per month
- **So that** I can track usage trends.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-001, SCR-TRIP-002
- **Acceptance Criteria:**
  - GIVEN a vehicle has trip entries, THEN the trip history header shows: "This Month: XXX km · Last Month: XXX km".

---

## 9. EP-EXP — Expense Recording

### FS-EXP-001: Log an expense

- **As a** consumer or fleet manager
- **I want to** record a non-fuel, non-maintenance expense (toll, parking, insurance, registration, repair, other)
- **So that** I have a complete cost picture.
- **Priority:** `IN`
- **Journey Ref:** UJ-008 · SCR-EXP-001
- **Acceptance Criteria:**
  - GIVEN I tap "💳 Log Expense", THEN I see a form with: Vehicle (or "General/Fleet"), Category (dropdown: Toll, Parking, Insurance, Registration, Repair, Other), Amount (numeric), Date (today), Description (optional), Receipt Photo (optional).
  - GIVEN I save the expense, THEN `POST /api/v1/expenses` stores the record. Dashboard cost summary updates.
  - GIVEN I am offline, THEN the entry saves to Hive and syncs later.

### FS-EXP-002: View expense history

- **As a** consumer or fleet manager
- **I want to** see all expenses filterable by vehicle, category, and date range
- **So that** I can audit spending.
- **Priority:** `IN`
- **Journey Ref:** SCR-EXP-002
- **Acceptance Criteria:**
  - GIVEN I navigate to Expenses, THEN I see a list of expenses with: Date, Category icon, Amount, Vehicle name, Description.
  - GIVEN I apply filters (vehicle, category, date range), THEN the list updates to show only matching expenses.
  - GIVEN expenses are shown, THEN monthly totals are displayed at the top.

### FS-EXP-003: Edit an expense

- **As a** consumer or fleet manager
- **I want to** edit an expense entry
- **So that** I can correct errors.
- **Priority:** `IN`
- **Journey Ref:** SCR-EXP-002
- **Acceptance Criteria:**
  - GIVEN I tap an expense and then "Edit", THEN I see the form pre-filled with existing values.
  - GIVEN I update the amount and tap "Save", THEN `PATCH /api/v1/expenses/{id}` updates the record.

### FS-EXP-004: Delete an expense

- **As a** consumer or fleet manager
- **I want to** delete an expense entry
- **So that** I can remove erroneous entries.
- **Priority:** `IN`
- **Journey Ref:** SCR-EXP-002
- **Acceptance Criteria:**
  - GIVEN I tap an expense and then "Delete" and confirm, THEN `DELETE /api/v1/expenses/{id}` soft-deletes the record and cost summaries update.

### FS-EXP-005: Quick-log expense from dashboard

- **As a** consumer or fleet manager
- **I want to** tap a "💳 Expense" button on my dashboard to jump to the expense form
- **So that** logging is fast.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-001
- **Acceptance Criteria:**
  - GIVEN I am on my dashboard, WHEN I tap the "💳 Expense" quick-log button, THEN I navigate to SCR-EXP-001 with date pre-filled.

### FS-EXP-006: Attach receipt photo to expense

- **As a** consumer or fleet manager
- **I want to** optionally attach a photo of a receipt to an expense entry
- **So that** I have visual proof of the expense.
- **Priority:** `IN`
- **Journey Ref:** SCR-EXP-001
- **Acceptance Criteria:**
  - GIVEN I am logging or editing an expense, WHEN I tap "Add Receipt Photo", THEN I can select a photo from my gallery or take a new photo.
  - GIVEN I select a photo, THEN it uploads to Firebase Storage via signed URL. The expense record stores the photo URI.
  - GIVEN I view the expense later, THEN I can tap the receipt thumbnail to view the full image.

---

## 10. EP-DASH — Dashboards

### FS-DASH-001: Consumer dashboard with vehicle cards and quick-log buttons

- **As a** consumer
- **I want to** see a dashboard with my vehicle card(s), upcoming maintenance alerts, and quick-log buttons
- **So that** I have a single home screen for all vehicle activities.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 9), UJ-006 · SCR-DASH-001
- **Acceptance Criteria:**
  - GIVEN I am a consumer, WHEN I open the app or navigate to Dashboard, THEN I see: Vehicle card(s) with status badges, Upcoming maintenance alerts (ordered by urgency), Quick-log buttons: ⛽ Fuel, 🔧 Service, 🛣️ Trip, 💳 Expense.
  - GIVEN I have 1 vehicle, THEN the vehicle card is expanded with summary stats (fuel this month, next maintenance due).
  - GIVEN I have multiple vehicles, THEN I see a scrollable list of vehicle cards.

### FS-DASH-002: Fleet manager dashboard with panels

- **As a** fleet manager
- **I want to** see a dashboard with Fleet Overview, Alerts & Actions, Cost Summary, and Recent Activity panels
- **So that** I have a comprehensive operational view.
- **Priority:** `IN`
- **Journey Ref:** UJ-006 · SCR-DASH-002
- **Acceptance Criteria:**
  - GIVEN I am a fleet manager on the web dashboard, THEN I see 4 panels:
    - 🚗 Fleet Overview: Total vehicles, Active, In Service, Vehicles-by-status donut chart.
    - ⚠️ Alerts & Actions: Overdue (red), Upcoming (yellow), Low efficiency warnings. Each with a CTA.
    - 💰 Cost Summary: This month's total spend, Fuel vs. Maintenance breakdown, Per-vehicle cost ranking.
    - 📊 Recent Activity: Latest fuel logs, service records, trip logs across all vehicles.
  - GIVEN I click a vehicle in the Fleet Overview, THEN I navigate to that vehicle's detail page.
  - GIVEN I click an alert, THEN I navigate to the relevant vehicle's Maintenance tab.

### FS-DASH-003: Dashboard auto-refresh via FCM silent push

- **As a** fleet manager on the web dashboard
- **I want to** see data updates appear automatically within 2-5 seconds when a driver logs an entry
- **So that** I don't need to manually refresh.
- **Priority:** `IN`
- **Journey Ref:** UJ-006 · Architecture Section 9
- **Acceptance Criteria:**
  - GIVEN a driver logs a fuel entry, WHEN the backend publishes a `fleet.event` to Pub/Sub, THEN the Pub/Sub handler sends an FCM data-only message to my web session.
  - GIVEN my Flutter Web `onMessage` handler receives the FCM message, THEN the dashboard widget triggers a re-fetch of `GET /api/v1/dashboard/summary`.
  - GIVEN the re-fetch completes, THEN the dashboard panels update with the new data without page reload.
  - GIVEN the update occurs, THEN a subtle animation indicates new data (e.g., new activity item slides in).

### FS-DASH-004: Dashboard catch-up on tab focus

- **As a** fleet manager who switched away from the dashboard tab
- **I want to** have the dashboard automatically refresh when I return to the tab
- **So that** I see up-to-date data after being away.
- **Priority:** `IN`
- **Journey Ref:** UJ-006 · Architecture Section 9.4
- **Acceptance Criteria:**
  - GIVEN the browser tab was inactive, WHEN I return to the tab (triggering `visibilitychange` event), THEN the Flutter Web app polls `GET /api/v1/dashboard/summary`.
  - GIVEN the poll returns new data, THEN the dashboard updates with the latest information.

### FS-DASH-005: Driver dashboard with assigned vehicles

- **As a** driver
- **I want to** see a simplified dashboard showing only my assigned vehicles and quick-log buttons
- **So that** I can log data without navigating complex menus.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-003
- **Acceptance Criteria:**
  - GIVEN I am a driver, WHEN I open the app, THEN I see: Assigned vehicle list (read-only — I cannot add/remove vehicles), Quick-log buttons: ⛽ Fuel, 🛣️ Trip, 📏 Odometer.
  - GIVEN I tap a vehicle, THEN I can view its details (read-only maintenance, fuel history) but cannot edit the maintenance schedule or vehicle profile.
  - GIVEN I have no assigned vehicles, THEN I see: "No vehicles assigned. Please contact your fleet manager."

### FS-DASH-006: Cost summary per vehicle

- **As a** consumer or fleet manager
- **I want to** see total fuel, maintenance, and expense costs per vehicle for the current month
- **So that** I understand per-vehicle spending.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-001, SCR-DASH-002
- **Acceptance Criteria:**
  - GIVEN I am viewing my dashboard, THEN each vehicle card shows: "This month: PKR/$ XXX" combining fuel, maintenance, and expense costs.
  - GIVEN I tap the cost figure, THEN I see a breakdown: Fuel: XXX, Maintenance: XXX, Expenses: XXX.

### FS-DASH-007: Fleet cost ranking (fleet manager)

- **As a** fleet manager
- **I want to** see my vehicles ranked by total cost (highest to lowest) in the dashboard's Cost Summary panel
- **So that** I can identify the most expensive vehicles.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-002
- **Acceptance Criteria:**
  - GIVEN the Cost Summary panel on the fleet dashboard, THEN I see a ranked list of vehicles by total cost (fuel + maintenance + expenses) for the current month.
  - GIVEN each vehicle in the list shows: Vehicle name, Total cost, and a horizontal bar indicating relative cost.

### FS-DASH-008: Fleet availability overview

- **As a** fleet manager
- **I want to** see how many vehicles are available, in service, or needing attention
- **So that** I can plan operations.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-002
- **Acceptance Criteria:**
  - GIVEN the Fleet Overview panel, THEN I see a donut chart with: 🟢 Healthy (X%), 🟡 Attention (X%), 🔴 Overdue (X%).
  - GIVEN I tap a segment of the donut chart, THEN the vehicle list filters to show only vehicles with that status.

---

## 11. EP-NOTIF — Notifications

### FS-NOTIF-001: Request FCM push notification permission

- **As a** new user
- **I want to** be prompted for notification permission AFTER seeing the value of the app (after the aha moment)
- **So that** I understand why notifications are useful before granting permission.
- **Priority:** `IN`
- **Journey Ref:** UJ-001 (Step 8) · SCR-MNT-001
- **Acceptance Criteria:**
  - GIVEN I have just accepted my maintenance schedule, THEN the app shows a contextual prompt: "Stay on top of your car's health. Allow notifications for maintenance reminders?"
  - GIVEN I tap "Allow", THEN the Android system notification permission dialog appears. If granted, the FCM device token is registered via `POST /api/v1/notifications/devices`.
  - GIVEN I tap "Not Now", THEN the prompt is dismissed and I can enable notifications later from Settings.

### FS-NOTIF-002: Send maintenance overdue push notification

- **As a** user with a vehicle that has overdue maintenance
- **I want to** receive a push notification alerting me
- **So that** I don't miss critical service.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 12.1
- **Acceptance Criteria:**
  - GIVEN the scheduled Maintenance Due Check (Cloud Tasks, every 6 hours) identifies an overdue item, THEN a `maintenance.overdue` event is published to Pub/Sub.
  - GIVEN the Pub/Sub handler processes the event, THEN an FCM notification+data message is sent: "⚠️ [Vehicle Name]: Oil Change is overdue by 500 km. [Tap to log service]".
  - GIVEN I tap the notification, THEN the app opens to the vehicle's maintenance tab.

### FS-NOTIF-003: Send maintenance upcoming push notification

- **As a** user with maintenance due in the next 7 days or 500 km
- **I want to** receive a reminder push notification
- **So that** I can schedule the service.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 12.1
- **Acceptance Criteria:**
  - GIVEN the Maintenance Due Check identifies an upcoming item, THEN a `maintenance.upcoming` event is published.
  - GIVEN the event is processed, THEN an FCM notification is sent: "🔔 [Vehicle Name]: Brake Pads due in 3 days. [Plan your visit]".

### FS-NOTIF-004: Send silent refresh FCM to fleet managers

- **As the** system
- **I want to** send a data-only FCM message to fleet managers when their fleet data changes
- **So that** their web/mobile dashboard auto-refreshes.
- **Priority:** `IN`
- **Journey Ref:** UJ-006 · Architecture Section 9
- **Acceptance Criteria:**
  - GIVEN a driver logs a fuel entry, WHEN the `fuel.logged` event is published, THEN the Pub/Sub handler sends an FCM data-only message to all fleet manager device tokens for that organization.
  - GIVEN the fleet manager's web session receives the FCM message, THEN the dashboard re-fetches summary data.
  - GIVEN the fleet manager's app is in the background (Android), THEN no visible notification is shown — the data is queued for the next app open.

### FS-NOTIF-005: View notification center

- **As a** user
- **I want to** see a chronological list of all my notifications in-app
- **So that** I can review past alerts.
- **Priority:** `IN`
- **Journey Ref:** SCR-NOTIF-001
- **Acceptance Criteria:**
  - GIVEN I tap the notification bell icon, THEN I see a list of notifications: maintenance reminders, sync confirmations, payment alerts, invitation updates.
  - GIVEN I have unread notifications, THEN a badge count appears on the bell icon.
  - GIVEN I tap a notification, THEN I navigate to the relevant screen (e.g., vehicle maintenance tab, payment status).

### FS-NOTIF-006: Configure notification preferences

- **As a** user
- **I want to** toggle notification categories on/off and set quiet hours
- **So that** I control what alerts I receive and when.
- **Priority:** `IN`
- **Journey Ref:** SCR-NOTIF-002
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Notifications, THEN I see toggles for: Maintenance reminders, Payment alerts, Fleet activity (fleet managers only), Sync status.
  - GIVEN I turn off "Maintenance reminders", THEN I stop receiving push notifications for upcoming/overdue maintenance (but the alerts still show in the dashboard).
  - GIVEN I set Quiet Hours (e.g., 10 PM – 7 AM), THEN notifications are held and delivered after quiet hours end.

### FS-NOTIF-007: Send payment-related notifications

- **As a** subscriber (Pro/Enterprise)
- **I want to** receive push notifications for payment events (subscription activated, renewal reminder, payment failed)
- **So that** I stay informed about my billing status.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 12.2
- **Acceptance Criteria:**
  - GIVEN a `subscription.activated` event is published, THEN I receive: "✅ Your Pro subscription is active! Welcome to the fleet."
  - GIVEN a subscription is expiring in 7 days, THEN I receive: "🔔 Your Pro subscription renews in 7 days."
  - GIVEN a `payment.failed` event is published, THEN I receive: "⚠️ Payment failed. Update your payment method to keep Pro features."

### FS-NOTIF-008: Remove stale FCM device tokens

- **As the** system
- **I want to** automatically remove FCM device tokens that have failed delivery > 3 times
- **So that** the token registry stays clean and notification delivery is efficient.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 12.1
- **Acceptance Criteria:**
  - GIVEN the weekly Stale Token Cleanup task runs, THEN device tokens with > 3 consecutive delivery failures are deleted from the `notification_devices` table.

---

## 12. EP-PAY — Payments & Subscriptions

### FS-PAY-001: Initiate Pro subscription via Stripe

- **As a** consumer upgrading to Pro
- **I want to** start a Pro subscription using Stripe (international)
- **So that** I can pay with an international card.
- **Priority:** `IN`
- **Journey Ref:** UJ-002, UJ-012 · SCR-PAY-001
- **Acceptance Criteria:**
  - GIVEN I am on the Upgrade screen and tap "Upgrade via Stripe", THEN `POST /api/v1/payments/subscribe` with `{tier: "pro", gateway: "stripe"}` is called.
  - GIVEN the server creates a Stripe Checkout Session, THEN I am returned a `checkout_url` and redirected to the Stripe-hosted checkout page in an in-app browser.
  - GIVEN I complete payment on the Stripe page, THEN Stripe sends a `checkout.session.completed` webhook to the backend.
  - GIVEN the webhook is verified, THEN my subscription is activated (see FS-ORG-002 for org conversion).

### FS-PAY-002: Initiate Pro subscription via Safepay

- **As a** consumer upgrading to Pro (Pakistan domestic)
- **I want to** start a Pro subscription using Safepay (Cards + Easypaisa + JazzCash)
- **So that** I can pay with local Pakistani payment methods.
- **Priority:** `IN`
- **Journey Ref:** UJ-002, UJ-012 · SCR-PAY-001
- **Acceptance Criteria:**
  - GIVEN I am on the Upgrade screen and tap "Upgrade via Safepay", THEN `POST /api/v1/payments/subscribe` with `{tier: "pro", gateway: "safepay"}` is called.
  - GIVEN the server creates a Safepay checkout session, THEN I am redirected to the Safepay checkout page.
  - GIVEN I complete payment (Visa/MC, Easypaisa, or JazzCash), THEN Safepay sends a webhook to the backend.
  - GIVEN the webhook is verified, THEN my subscription is activated.

### FS-PAY-003: Handle payment failure

- **As a** user whose payment was declined
- **I want to** see a clear error message and be able to retry with the same or different payment method
- **So that** I can resolve the issue and complete my upgrade.
- **Priority:** `IN`
- **Journey Ref:** UJ-011 · SCR-PAY-004
- **Acceptance Criteria:**
  - GIVEN I return from the checkout page without completing payment, THEN I see: "Payment could not be processed."
  - GIVEN the error screen shows, THEN I see options: "Try Again" (returns to checkout), "Use Different Payment Method" (returns to gateway selection).
  - GIVEN the error screen shows, THEN no subscription is created — my account remains on the free tier.

### FS-PAY-004: View subscription status

- **As a** paid subscriber (Pro/Enterprise)
- **I want to** see my current subscription details (tier, renewal date, payment method)
- **So that** I can manage my billing.
- **Priority:** `IN`
- **Journey Ref:** SCR-PAY-003
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Subscription, THEN I see: Current Tier (Pro/Enterprise), Next Renewal Date, Payment Gateway (Stripe/Safepay), "Manage Subscription" link.
  - GIVEN I tap "Manage Subscription" and my gateway is Stripe, THEN I am redirected to Stripe Customer Portal for self-service billing management.
  - GIVEN my gateway is Safepay, THEN I see in-app options to update payment method or cancel.

### FS-PAY-005: Process Stripe webhook

- **As the** system
- **I want to** verify and process incoming Stripe webhooks (subscription created, renewed, cancelled, payment failed)
- **So that** subscription state stays synchronized.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 10.2
- **Acceptance Criteria:**
  - GIVEN a Stripe webhook arrives at `POST /api/v1/payments/webhooks/stripe`, THEN the signature is verified using `stripe.Webhook.construct_event()`.
  - GIVEN the event type is `checkout.session.completed`, THEN a `Subscription` record is created, org tier is updated, and Firebase custom claims are refreshed.
  - GIVEN the event type is `invoice.payment_failed`, THEN a `payment.failed` event is published to Pub/Sub and the user is notified via FCM.
  - GIVEN the event type is `customer.subscription.deleted`, THEN the subscription is cancelled, org tier reverts to free, and Firebase claims are updated.

### FS-PAY-006: Process Safepay webhook

- **As the** system
- **I want to** verify and process incoming Safepay webhooks
- **So that** Pakistan domestic payment events are handled correctly.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 10.3
- **Acceptance Criteria:**
  - GIVEN a Safepay webhook arrives at `POST /api/v1/payments/webhooks/safepay`, THEN the HMAC signature is verified.
  - GIVEN payment is confirmed, THEN the same downstream flow as Stripe applies — subscription created, claims updated.

### FS-PAY-007: Display upgrade prompt at vehicle quota wall

- **As a** consumer who tries to add vehicle (X+1)
- **I want to** see a clear upgrade prompt explaining why I can't add more vehicles and what Pro offers
- **So that** I understand the value of upgrading.
- **Priority:** `IN`
- **Journey Ref:** UJ-011, UJ-012 · SCR-PAY-001
- **Acceptance Criteria:**
  - GIVEN I attempt to add a vehicle beyond my tier limit, WHEN the API returns `403 QUOTA_EXCEEDED`, THEN I see the Upgrade Prompt screen with: Feature comparison (Free vs. Pro), Vehicle limit increase, Gateway selection buttons, "Maybe later" dismiss option.
  - GIVEN I tap "Maybe later", THEN the prompt dismisses and a subtle "⭐ Upgrade" badge remains in the navigation.

### FS-PAY-008: Display upgrade prompt at driver quota wall

- **As a** fleet manager who tries to invite driver (Y+1)
- **I want to** see an upgrade prompt explaining Enterprise benefits
- **So that** I understand how to grow my team.
- **Priority:** `IN`
- **Journey Ref:** UJ-011 · SCR-PAY-002
- **Acceptance Criteria:**
  - GIVEN I attempt to invite a driver beyond my tier's driver limit, WHEN the API returns `403 QUOTA_EXCEEDED`, THEN I see the Enterprise upgrade prompt with feature comparison.

### FS-PAY-009: Welcome to Pro celebration screen

- **As a** consumer who just upgraded to Pro
- **I want to** see a celebratory screen confirming my upgrade with next-step suggestions
- **So that** I feel excited about my new capabilities.
- **Priority:** `IN`
- **Journey Ref:** UJ-012 · SCR-PAY-005
- **Acceptance Criteria:**
  - GIVEN my subscription is activated and my token refreshes with the new claims, THEN I see a "🎉 Welcome to Pro!" screen with confetti animation.
  - GIVEN the screen shows, THEN I see three suggested next steps: "Add more vehicles", "Invite your first driver", "Set up maintenance schedules".
  - GIVEN I tap a suggestion, THEN I navigate to the relevant screen. I can also dismiss with "Go to Dashboard".

### FS-PAY-010: Persistent upgrade badge in navigation (Free tier)

- **As a** free tier consumer
- **I want to** see a subtle "⭐ Upgrade" badge in the navigation
- **So that** I always know the upgrade option exists without being aggressively prompted.
- **Priority:** `IN`
- **Journey Ref:** UJ-012
- **Acceptance Criteria:**
  - GIVEN I am on the free tier, THEN a subtle "⭐ Upgrade" badge is visible in the navigation drawer/sidebar.
  - GIVEN I tap the badge, THEN I navigate to the Upgrade Prompt screen (SCR-PAY-001).
  - GIVEN I upgrade to Pro, THEN the badge disappears permanently.

---

## 13. EP-SYNC — Offline Sync

### FS-SYNC-001: Save data entry offline when no connectivity

- **As a** consumer or driver on Android without internet
- **I want to** log fuel, trip, maintenance, and expense entries that are saved locally
- **So that** I can log data anywhere, regardless of connectivity.
- **Priority:** `IN`
- **Journey Ref:** UJ-004, UJ-005, UJ-007, UJ-008 · SCR-SYNC-003
- **Acceptance Criteria:**
  - GIVEN I am offline, WHEN I submit a fuel/trip/maintenance/expense form, THEN the entry is saved to Hive local storage with a client-generated UUID and status `pending`.
  - GIVEN the entry is saved locally, THEN it appears in the relevant list with a yellow "pending sync" badge.
  - GIVEN the entry is saved locally, THEN I see a toast: "Saved offline — will sync when connection returns."

### FS-SYNC-002: Background sync on connectivity restoration

- **As a** user whose device regains internet connectivity
- **I want to** have my pending offline entries automatically synced to the server
- **So that** my data is persisted without manual intervention.
- **Priority:** `IN`
- **Journey Ref:** UJ-004 · Architecture Section 8
- **Acceptance Criteria:**
  - GIVEN my device regains connectivity (or the app is foregrounded), THEN the background sync isolate processes the sync queue in FIFO order.
  - GIVEN pending entries exist, THEN `POST /api/v1/sync/batch` sends the entire queue as an array.
  - GIVEN the server returns per-item results, THEN successfully synced items have their badges removed and status updated to `synced`.
  - GIVEN the sync completes, THEN a subtle toast appears: "✅ X entries synced."

### FS-SYNC-003: Display offline indicator banner

- **As a** user who is currently offline
- **I want to** see a clear but non-alarming indicator that I'm offline
- **So that** I understand why some features are unavailable.
- **Priority:** `IN`
- **Journey Ref:** SCR-SYNC-003
- **Acceptance Criteria:**
  - GIVEN my device is offline, THEN a persistent banner appears at the top of the screen: "📡 You're offline — entries will be saved locally."
  - GIVEN connectivity is restored, THEN the banner fades out with a brief "Back online" confirmation.
  - GIVEN the banner is present, THEN data entry forms remain fully functional (save to Hive).

### FS-SYNC-004: View pending sync queue

- **As a** user with pending offline entries
- **I want to** see a list of all entries waiting to sync
- **So that** I know what data hasn't reached the server yet.
- **Priority:** `IN`
- **Journey Ref:** SCR-SYNC-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Sync Status (or tap the "pending" badge), THEN I see a list of pending entries with: Type (Fuel/Trip/Maintenance/Expense), Vehicle name, Created date, Status (Pending/Syncing/Conflict).

### FS-SYNC-005: Handle sync conflict with side-by-side resolution

- **As a** user whose offline entry conflicts with a server update
- **I want to** see both versions side-by-side and choose how to resolve the conflict
- **So that** I don't lose data and I control the resolution.
- **Priority:** `IN`
- **Journey Ref:** UJ-009 · SCR-SYNC-002
- **Acceptance Criteria:**
  - GIVEN the sync response includes a conflict for an entry, THEN the entry's status changes to "Conflict" (orange badge).
  - GIVEN I tap the conflicting entry, THEN I see a side-by-side comparison: "📱 Your version" vs. "🌐 Server version" with differences highlighted.
  - GIVEN I choose "Keep mine", THEN `PATCH /{entity}/{id}` with `force_overwrite=true` sends my version to the server.
  - GIVEN I choose "Accept server", THEN local storage updates to match the server version.
  - GIVEN I choose "Edit manually", THEN a pre-filled form opens with both values visible for reconciliation.

### FS-SYNC-006: Idempotent sync via client-generated UUIDs

- **As the** system
- **I want to** use client-generated UUIDs as deduplication keys on the server
- **So that** re-syncing the same entry multiple times is safe and does not create duplicates.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 8.4
- **Acceptance Criteria:**
  - GIVEN every offline entry has a client-generated UUID (`client_id`), WHEN the sync batch sends the entry, THEN the server checks for an existing record with the same `client_id`.
  - GIVEN a matching `client_id` exists, THEN the server returns `{status: "already_exists"}` and does not create a duplicate.
  - GIVEN no matching `client_id` exists, THEN the entry is inserted and `{status: "created"}` is returned.

### FS-SYNC-007: Offline sync does not block non-conflicting items

- **As a** user with multiple pending entries (some conflicting, some not)
- **I want to** have non-conflicting entries sync immediately while conflicts are queued for review
- **So that** most of my data syncs without delay.
- **Priority:** `IN`
- **Journey Ref:** UJ-009
- **Acceptance Criteria:**
  - GIVEN a sync batch contains 5 entries, of which 1 has a conflict, THEN the 4 non-conflicting entries sync immediately and their badges are removed.
  - GIVEN the 1 conflicting entry remains, THEN it shows an orange "Conflict" badge and waits for user resolution.

### FS-SYNC-008: Sync on app foreground

- **As a** user who backgrounds and then re-opens the app
- **I want to** have any pending entries sync when the app is foregrounded
- **So that** data syncs at every opportunity.
- **Priority:** `IN`
- **Journey Ref:** Architecture Section 8.4
- **Acceptance Criteria:**
  - GIVEN the app is brought to the foreground and connectivity is available, THEN the sync queue is processed automatically.
  - GIVEN no pending entries exist, THEN no sync request is made.

---

## 14. EP-AD — Advertising (Free Tier)

### FS-AD-001: Display banner ad on dashboard (Android, Free tier)

- **As a** free tier consumer on Android
- **I want to** see a non-intrusive banner ad at the bottom of my dashboard
- **So that** Veltrics generates revenue from my free usage.
- **Priority:** `IN`
- **Journey Ref:** SCR-AD-001
- **Acceptance Criteria:**
  - GIVEN I am on the free tier AND on the dashboard screen (Android), THEN an AdMob banner ad loads at the bottom of the screen.
  - GIVEN I am on any data entry form (Log Fuel, Log Service, Log Trip, Log Expense), THEN no ad is displayed.
  - GIVEN I am a Pro or Enterprise subscriber, THEN no ads are displayed anywhere.
  - GIVEN the ad fails to load, THEN the space is collapsed — no empty placeholder shown.

### FS-AD-002: Display native ad card in vehicle list (Android, Free tier)

- **As a** free tier consumer on Android
- **I want to** see a styled native ad card in the vehicle list or activity feed
- **So that** ads feel integrated rather than intrusive.
- **Priority:** `IN`
- **Journey Ref:** SCR-AD-002
- **Acceptance Criteria:**
  - GIVEN I am on the free tier AND viewing my vehicle list or dashboard activity feed, THEN an AdMob native ad card appears between content items (every 5th item or after the 3rd item if fewer).
  - GIVEN the native ad card is styled to match the app's card design, THEN it includes a small "Ad" label for transparency.

### FS-AD-003: Display AdSense ad on web dashboard (Free tier)

- **As a** free tier consumer on Flutter Web
- **I want to** see a display ad in the dashboard sidebar
- **So that** Veltrics generates revenue from my free web usage.
- **Priority:** `IN`
- **Journey Ref:** SCR-AD-003
- **Acceptance Criteria:**
  - GIVEN I am on the free tier AND viewing the web dashboard, THEN an AdSense responsive display ad appears in the sidebar.
  - GIVEN I am a Pro or Enterprise subscriber, THEN no ads are displayed.

### FS-AD-004: Rewarded video ad for permanent bonus vehicle/driver slot

- **As a** free tier consumer who has hit the vehicle or driver quota (X or Y)
- **I want to** watch rewarded video ads to permanently unlock a bonus slot
- **So that** I can add one more vehicle or driver without upgrading to Pro right away.
- **Priority:** `IN`
- **Journey Ref:** UJ-012
- **Acceptance Criteria:**
  - GIVEN I hit the vehicle quota wall (X) or driver quota wall (Y), WHEN the upgrade prompt appears, THEN I also see an option: "🎬 Watch 3 videos to permanently unlock 1 bonus slot."
  - GIVEN I tap the option, THEN I must watch 3 consecutive full rewarded video ads (back-to-back, no skip). A progress indicator shows "Ad 1 of 3 / 2 of 3 / 3 of 3".
  - GIVEN all 3 ads complete successfully, THEN my quota permanently increases by 1. The bonus resource is tagged `ad_rewarded = true` and shown with a "🎬 Ad" badge.
  - GIVEN I abandon the ad sequence before all 3 complete, THEN no slot is unlocked and I return to the quota wall.
  - GIVEN I have an ad-rewarded vehicle or driver, THEN every action involving that resource requires watching 1 video ad before the action completes.
  - GIVEN a rewarded video ad fails to load during a per-action gate, THEN the action is blocked with: "Ad unavailable. Try again later or upgrade to Pro for ad-free access."
  - GIVEN the maximum bonus slots (2 per resource type) are already unlocked, THEN the "Watch to unlock" option is hidden and only the "Upgrade to Pro" path is shown.
  - GIVEN I upgrade to Pro, THEN all ad-rewarded resources convert to standard resources and per-action ad gates are removed.

### FS-AD-005: Ad-free zone on data entry forms

- **As a** free tier user logging data (fuel, service, trip, expense)
- **I want to** have zero ads visible during the data entry process
- **So that** logging is fast and uninterrupted.
- **Priority:** `IN`
- **Journey Ref:** Product Brief Risk #1
- **Acceptance Criteria:**
  - GIVEN I am on any data entry form (SCR-FUEL-001, SCR-MNT-002, SCR-TRIP-001, SCR-EXP-001), THEN no banner, native, or interstitial ads are displayed.
  - GIVEN I submit the form and return to the dashboard, THEN ads resume (banner at bottom, native in feed).

---

## 15. EP-DRV — Driver Scoring

### FS-DRV-001: Calculate driver score based on logging consistency

- **As a** fleet manager
- **I want to** see a score for each driver based on how consistently they log fuel and trip entries
- **So that** I can identify drivers who are reliably recording data.
- **Priority:** `IN`
- **Journey Ref:** SCR-ORG-004
- **Acceptance Criteria:**
  - GIVEN a driver has been active for ≥ 7 days, THEN their score is calculated as: (days with at least 1 log entry / total active days) × 100.
  - GIVEN the score is ≥ 80%, THEN the driver is labeled "Consistent" (🟢).
  - GIVEN the score is 50-79%, THEN the driver is labeled "Moderate" (🟡).
  - GIVEN the score is < 50%, THEN the driver is labeled "Needs Attention" (🔴).

### FS-DRV-002: View driver score on driver list

- **As a** fleet manager
- **I want to** see each driver's consistency score on the driver list screen
- **So that** I can quickly assess team performance.
- **Priority:** `IN`
- **Journey Ref:** SCR-ORG-002
- **Acceptance Criteria:**
  - GIVEN I am on the Driver List screen, THEN each driver card shows: Name, Phone, Assigned vehicles count, Consistency Score (percentage + color label).

### FS-DRV-003: View driver activity detail

- **As a** fleet manager
- **I want to** see a driver's recent activity (fuel logs, trip logs, odometer updates) on their detail page
- **So that** I can verify they are logging accurately.
- **Priority:** `IN`
- **Journey Ref:** SCR-ORG-004
- **Acceptance Criteria:**
  - GIVEN I tap a driver on the Driver List, THEN I see: Driver profile, Consistency Score, Assigned vehicles, Recent activity feed (last 30 days of logs).

### FS-DRV-004: Fleet manager receives alert for inactive driver

- **As a** fleet manager
- **I want to** receive a notification when a driver hasn't logged any entry for 3+ consecutive days
- **So that** I can follow up.
- **Priority:** `IN`
- **Journey Ref:** SCR-NOTIF-001
- **Acceptance Criteria:**
  - GIVEN a driver has 0 log entries for 3 consecutive days, THEN the fleet manager receives an FCM notification: "📊 [Driver Name] hasn't logged any data in 3 days."
  - GIVEN the notification is tapped, THEN the fleet manager navigates to the driver's detail page.

---

## 16. EP-THEME — Dark Mode & Theming

### FS-THEME-001: Toggle dark mode in settings

- **As a** user
- **I want to** switch between light mode, dark mode, and system-default theme
- **So that** I can use the app comfortably in any lighting condition.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Theme, THEN I see three options: Light, Dark, System Default.
  - GIVEN I select "Dark", THEN the entire app immediately switches to a dark color scheme.
  - GIVEN I select "System Default", THEN the app follows the device's system theme setting.
  - GIVEN I change the theme, THEN my preference is persisted locally and applied on next launch.

### FS-THEME-002: Dark mode color scheme

- **As a** user in dark mode
- **I want to** see a properly designed dark color scheme (not just inverted colors)
- **So that** the app is readable and aesthetically pleasing at night.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN dark mode is active, THEN all backgrounds use dark surface colors (e.g., #121212, #1E1E1E).
  - GIVEN dark mode is active, THEN text uses light colors with appropriate contrast ratios (≥ 4.5:1 for body text, ≥ 3:1 for large text).
  - GIVEN dark mode is active, THEN status badges (🟢🟡🔴), charts, and icons remain distinguishable.
  - GIVEN dark mode is active, THEN AdMob banner ads and native ads render correctly without visual conflicts.

### FS-THEME-003: Persist theme preference across sessions

- **As a** user who selected a theme
- **I want to** have my preference remembered when I reopen the app
- **So that** I don't need to reconfigure every time.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I selected "Dark" mode, WHEN I close and reopen the app, THEN dark mode is applied from the splash screen onward.
  - GIVEN the preference is stored in Hive local storage, THEN it persists across app updates.

---

## 17. EP-EXPORT — Data Export (Pro-Gated)

### FS-EXPORT-001: Export vehicle maintenance history as PDF

- **As a** Pro or Enterprise subscriber
- **I want to** export a vehicle's complete maintenance history as a PDF document
- **So that** I can share it with buyers, insurers, or auditors.
- **Priority:** `IN`
- **Journey Ref:** Product Brief Section 4.1 (Pro features)
- **Acceptance Criteria:**
  - GIVEN I am on a vehicle's Maintenance tab (as a Pro subscriber), WHEN I tap "Export PDF", THEN the server generates a PDF with: Vehicle details, Complete service history, Per-service costs, Total maintenance spend.
  - GIVEN the PDF is generated, THEN it downloads to my device (Android) or opens in a new tab (Web).
  - GIVEN I am on the free tier, THEN the "Export PDF" button shows a lock icon and tapping it navigates to the upgrade prompt.

### FS-EXPORT-002: Export fuel and expense data as CSV

- **As a** Pro or Enterprise subscriber
- **I want to** export fuel logs and expenses as CSV files
- **So that** I can import them into spreadsheets or accounting software.
- **Priority:** `IN`
- **Journey Ref:** Product Brief Section 4.1
- **Acceptance Criteria:**
  - GIVEN I am on the Fuel History or Expense History screen, WHEN I tap "Export CSV", THEN the server generates a CSV file with all entries for the selected vehicle and date range.
  - GIVEN the CSV is generated, THEN it downloads to my device.
  - GIVEN I am on the free tier, THEN the "Export CSV" button shows a lock icon.

### FS-EXPORT-003: Export fleet summary report as PDF (fleet manager)

- **As a** fleet manager (Pro or Enterprise)
- **I want to** export a fleet-wide summary report as PDF
- **So that** I can share operational reports with management.
- **Priority:** `IN`
- **Journey Ref:** SCR-DASH-002
- **Acceptance Criteria:**
  - GIVEN I am on the Fleet Dashboard, WHEN I tap "Export Report", THEN the server generates a PDF with: Fleet overview, Per-vehicle cost breakdown, Maintenance compliance summary, Driver activity scores.
  - GIVEN the PDF is generated, THEN it downloads or opens in a new tab.

---

## 18. EP-SET — Settings & Account

### FS-SET-001: View app settings

- **As a** user
- **I want to** access all settings from a single screen
- **So that** I can manage my preferences in one place.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings, THEN I see sections: Profile, Notifications, Theme, Units, Subscription (if applicable), Sync Status, About, Account Deletion, Logout.

### FS-SET-002: Configure measurement units

- **As a** user
- **I want to** choose between km/miles and liters/gallons
- **So that** the app displays measurements in my preferred units.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Units, THEN I see options: Distance (Kilometers / Miles), Volume (Liters / Gallons).
  - GIVEN I select Miles and Gallons, THEN all distances display in miles and fuel volumes in gallons throughout the app.
  - GIVEN my preference is saved, THEN it persists across sessions and applies to all data entry forms, lists, and dashboards.

### FS-SET-003: Logout

- **As a** user
- **I want to** sign out of the app
- **So that** I can switch accounts or secure my session.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I tap "Logout" in Settings, THEN Firebase Auth signs out, cached tokens are cleared, and I am navigated to the login screen.
  - GIVEN I was offline when logging out, THEN a warning appears: "You have X pending entries. Logging out will NOT delete them — they'll sync when you sign back in."

### FS-SET-004: Request account deletion

- **As a** user
- **I want to** request deletion of my account and all associated data
- **So that** I can exercise my data privacy rights.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-002 · Architecture Section 13.2
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → Delete Account, THEN I see a warning: "This will permanently delete your account and all vehicle, maintenance, fuel, trip, and expense data after a 30-day grace period."
  - GIVEN I type "DELETE" and tap "Confirm", THEN `POST /api/v1/users/me/delete` initiates a cascading soft-delete of all associated data.
  - GIVEN the 30-day grace period is active, THEN I can re-sign-in to cancel the deletion.
  - GIVEN 30 days pass without cancellation, THEN all data is permanently hard-deleted (except payment records, retained 7 years per compliance).

### FS-SET-005: Download my data before deletion

- **As a** user about to delete their account
- **I want to** download all my data (vehicles, fuel logs, maintenance, trips, expenses) before deletion
- **So that** I retain my records.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-002
- **Acceptance Criteria:**
  - GIVEN I am on the Delete Account screen, THEN I see a "Download My Data" button before the deletion CTA.
  - GIVEN I tap "Download My Data", THEN the server generates a ZIP file containing CSV exports of all my data + receipt photos.

### FS-SET-006: View app version and about info

- **As a** user
- **I want to** see the app version, terms of service, and privacy policy links
- **So that** I can verify the version and access legal documents.
- **Priority:** `IN`
- **Journey Ref:** SCR-SET-001
- **Acceptance Criteria:**
  - GIVEN I navigate to Settings → About, THEN I see: App version number, Build number, Terms of Service link, Privacy Policy link, "Made with ❤️ by Veltrics" branding.

---

## 19. Out-of-Scope & Post-MVP Items

### `OUT` — Not Part of the Product

These features are explicitly excluded from the product vision:

| Feature | Rationale |
|:---|:---|
| **OCR Receipt Scanning** | Adds mobile vision SDK complexity. Photos attached to entries are sufficient. Manual entry is the core loop. |
| **Multi-Language / i18n Support** | Product launches in English. Pakistan's tech-literate SMB market is comfortable with English UI. Evaluate post-PMF. |
| **OBD-II / Telematics Integration** | Hardware dependency. Not part of the product vision. GPS tracking (without hardware) is POST. |

### `POST` — Post-MVP (Planned for Future Releases)

| Feature | Priority After MVP | Notes |
|:---|:---|:---|
| **AI-Powered Predictive Maintenance** | Immediate after MVP | Leverage accumulated service history + Make/Model data to predict failures before they occur. Requires sufficient historical dataset from MVP usage. |
| **iOS App** | Immediate after MVP | Flutter compiles to iOS natively. Primary effort is App Store listing, iOS-specific testing, and Apple IAP integration. |
| **Transactional Email (SendGrid/Mailgun)** | Immediate after MVP | Email invoices, onboarding drips, subscription reminders, maintenance alerts via email. User-toggleable in notification preferences (Settings → Notifications → Email Alerts). |
| **GPS Trip Tracking** | High | Automatic trip logging via GPS (start/stop detection) without OBD-II hardware. Reduces manual data entry. |
| **Feature Flags (Remote Config)** | Medium | Enables A/B testing and gradual rollouts. Use Firebase Remote Config. |
| **QuickBooks/Xero Integration** | Low | Distantly post-MVP. Useful for Enterprise customers who need accounting sync. API-based integration via backend module. |
| **Full-Text Search (PostgreSQL `tsvector`)** | Low | Vehicle/maintenance search. PostgreSQL native search is sufficient for MVP; can add Typesense later. |
| **Cloud CDN for API** | Low | Not needed until API traffic exceeds regional capacity. |

---

## 20. Story Count Summary

| Epic | Stories (IN) |
|:---|:---|
| EP-AUTH — Authentication & Profile | 12 |
| EP-ORG — Organization & Multi-Tenancy | 10 |
| EP-VEH — Vehicle Management | 10 |
| EP-MNT — Maintenance Engine | 12 |
| EP-FUEL — Fuel Logging | 6 |
| EP-TRIP — Trip Logging | 6 |
| EP-EXP — Expense Recording | 6 |
| EP-DASH — Dashboards | 8 |
| EP-NOTIF — Notifications | 8 |
| EP-PAY — Payments & Subscriptions | 10 |
| EP-SYNC — Offline Sync | 8 |
| EP-AD — Advertising (Free Tier) | 5 |
| EP-DRV — Driver Scoring | 4 |
| EP-THEME — Dark Mode & Theming | 3 |
| EP-EXPORT — Data Export (Pro) | 3 |
| EP-SET — Settings & Account | 6 |
| **Total** | **117** |

---

## 21. Next Steps & Approval Gate

- **Next Stage:** `★ MVP SCOPING GATE` (`04b-mvp-scope.md`) led by the *Technical Product Strategist* persona.
- **Gate Confirmation:** Please review this Feature Stories document (`product-specs/04-feature-stories.md`).

> Does this look right, or shall we refine anything before moving on?
