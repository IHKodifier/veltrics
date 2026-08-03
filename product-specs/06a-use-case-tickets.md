# Use Case & Implementation Tickets: Veltrics Fleet & Vehicle Management

> **Reads from:** [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md) · [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md) · [06-data-model.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06-data-model.md)  
> **Scope:** Full Product Backlog (117 Feature Stories + 5 Core Technical Infrastructure Tickets = 122 Tickets)  
> **Status:** ✅ Approved  
> **Author:** Staff Engineer Persona (App Architect)  

---

## Executive Summary & Architecture Integration

This document defines the complete, implementation-ready backlog of 122 use case tickets for the Veltrics Fleet & Vehicle Management Platform. Every ticket is structured for immediate pickup by a coding agent without requiring mid-implementation product or architectural decisions.

### Mandatory Domain & Architectural Directives
1. **Domain Context:** Veltrics is a Fleet & Vehicle Management Platform supporting single-vehicle consumers, small commercial fleets, and enterprise logistics networks.
2. **Offline-First Transaction Ordering:** Mobile client generates UUID v4 identifiers locally for offline creation. Sync payload (`POST /api/v1/sync/batch`) is processed within a single database transaction in strict topological foreign-key order: `organizations` → `users` → `vehicles` → `drivers` → `fuel_logs` / `maintenance_logs` / `trips` / `expenses`.
3. **Ad-Rewarded Quota Lifecycle:** Free-tier users earn up to +2 bonus vehicle slots and +2 bonus driver slots via rewarded video ads. Bonus slots are permanently attached to the `organization` entity. Pro-to-Free subscription downgrades preserve earned bonus slots up to the 5-vehicle / 5-driver hard ceiling.
4. **Dual Payment Gateway Webhook Reconciliation:** Webhooks from Stripe (International) and Safepay (Pakistan) write to a unified `subscriptions` relational schema. Gateway-agnostic status (`ACTIVE`, `PAST_DUE`, `CANCELED`) is normalized while raw provider events are preserved in the `gateway_payload` JSON field.
5. **Ad-Gate Signature Enforcement:** Mutating endpoints for ad-rewarded entities require a cryptographically signed ad-completion token generated upon verified ad playback, validated by FastAPI middleware prior to DB mutation.

---

## 1. EP-AUTH — Authentication & Profile

### UC-001: Sign Up with Google One-Tap

**Linked story:** FS-AUTH-001  
**Actor(s):** Unauthenticated User (Consumer / Manager)  
**Trigger:** User taps "Continue with Google" on login/registration screen.  

**Preconditions**
- [ ] Google Play Services / Google Sign-In SDK is initialized on mobile app.
- [ ] App has valid Firebase Auth web client ID configured.

**Main flow**
1. User taps "Continue with Google".
2. Flutter app calls Google SDK and receives ID token.
3. Flutter app exchanges ID token with Firebase Auth for a Firebase JWT credential.
4. App sends Firebase JWT to FastAPI backend `POST /api/v1/auth/register`.
5. Backend verifies JWT, extracts email, full name, and photo URL.
6. Backend checks if `users` record exists by `firebase_uid`. If not, creates new `users` record with UUID v4 primary key.
7. Backend creates default personal `organizations` record with `is_personal = true`, `max_vehicles = 3`, `max_drivers = 3`.
8. Backend returns Auth Session DTO (Access JWT, Refresh Token, User DTO, Org DTO).
9. App stores tokens securely and navigates to Profile Setup screen (SCR-AUTH-007).

**Alternate flows**
- **A1 — Existing User Login:** If user record already exists, backend skips organization creation and returns existing session DTO.

**Edge cases & error handling**
- [ ] Google Auth canceled by user → App resets login UI to neutral state without error dialog.
- [ ] Invalid/Expired Google Token → API returns `HTTP 401 Unauthorized` with detail `"INVALID_GOOGLE_TOKEN"`.

**Postconditions**
- User record and default personal organization exist in database with soft-delete flags intact (`deleted_at IS NULL`).

**Data & API touchpoints**
- Entities touched: `users`, `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/auth/register`

**Acceptance criteria (testable)**
- WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL create a `users` row and a personal `organizations` row with `max_vehicles=3` in a single transaction.
- WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL return the user's existing organization and profile payload without creating duplicate DB records.

**Estimate:** S  
**Depends on:** none  

---

### UC-002: Sign Up with Facebook Login

**Linked story:** FS-AUTH-001b  
**Actor(s):** Unauthenticated User  
**Trigger:** User taps "Continue with Facebook" button.  

**Preconditions**
- [ ] Facebook SDK initialized in Flutter client.

**Main flow**
1. User initiates Facebook OAuth flow.
2. Flutter receives Facebook Access Token and authenticates with Firebase Auth.
3. App posts Firebase ID Token to `POST /api/v1/auth/register`.
4. Backend creates `users` entity with `auth_provider = "facebook"` and populates `linked_providers` JSON field.
5. Backend creates personal `organizations` entity (`is_personal = true`).
6. API returns Auth DTO and navigates to Profile Setup screen.

**Alternate flows**
- **A1 — Account Linking:** If email matches existing account with different provider, backend attaches Facebook provider to `linked_providers` JSON array.

**Edge cases & error handling**
- [ ] Facebook permission denied for email → API returns `HTTP 400 Bad Request` requiring email entry.

**Postconditions**
- User authenticated with linked Facebook provider ID.

**Data & API touchpoints**
- Entities touched: `users`, `organizations`
- Endpoint(s): `POST /api/v1/auth/register`

**Acceptance criteria (testable)**
- WHEN a user registers via Facebook THE SYSTEM SHALL store `"facebook"` inside the `linked_providers` JSON array of the `users` record.

**Estimate:** S  
**Depends on:** UC-001  

---

### UC-003: Sign Up with Email and Password

**Linked story:** FS-AUTH-002  
**Actor(s):** Unauthenticated User  
**Trigger:** User submits email, password, and confirmation on registration form.  

**Preconditions**
- [ ] User is on SCR-AUTH-003.

**Main flow**
1. User enters valid email and strong password (min 8 chars, 1 upper, 1 digit).
2. App creates Firebase Auth account via client SDK.
3. App calls FastAPI `POST /api/v1/auth/register` with Firebase ID token.
4. Backend provisions user and personal organization records.
5. Backend sends email verification link via background task.
6. API returns session DTO with `email_verified = false`.

**Alternate flows**
- **A1 — Duplicate Email:** Firebase Auth rejects registration; client displays "Email already registered".

**Edge cases & error handling**
- [ ] Weak Password → Client validation prevents submission; API enforces Regex pattern.

**Postconditions**
- Account created with unverified email state.

**Data & API touchpoints**
- Entities touched: `users`, `organizations`
- Endpoint(s): `POST /api/v1/auth/register`

**Acceptance criteria (testable)**
- WHEN valid email/password details are submitted THE SYSTEM SHALL return `HTTP 201 Created` containing user and organization IDs.

**Estimate:** S  
**Depends on:** UC-001  

---

### UC-004: User Password Authentication & Session Initiation

**Linked story:** FS-AUTH-003  
**Actor(s):** Registered User  
**Trigger:** User submits credentials on SCR-AUTH-001.  

**Preconditions**
- [ ] User account exists.

**Main flow**
1. User submits email and password.
2. Firebase Auth verifies credentials and issues Firebase ID Token.
3. App sends ID Token to `POST /api/v1/auth/login`.
4. Backend verifies token, fetches user and primary active organization, and generates session JWT pair.
5. App stores Access JWT (secure storage) and Refresh Token (HTTP-only cookie / secure storage).
6. App navigates to Dashboard (SCR-DASH-001).

**Alternate flows**
- **A1 — Disabled Account:** Backend checks `is_active == false` or `deleted_at IS NOT NULL` and returns `HTTP 403 Forbidden`.

**Edge cases & error handling**
- [ ] Incorrect Password → API returns `HTTP 401 Unauthorized`.

**Postconditions**
- Active access session established.

**Data & API touchpoints**
- Entities touched: `users`, `organizations`
- Endpoint(s): `POST /api/v1/auth/login`

**Acceptance criteria (testable)**
- WHEN valid login credentials are provided THE SYSTEM SHALL return an Access JWT with 15-minute expiration and Refresh Token with 30-day expiration.

**Estimate:** S  
**Depends on:** UC-003  

---

### UC-005: Phone Number OTP Authentication

**Linked story:** FS-AUTH-004  
**Actor(s):** Driver / Fleet Manager  
**Trigger:** User enters phone number and requests OTP code.  

**Preconditions**
- [ ] SMS Gateway / Firebase Phone Auth service configured.

**Main flow**
1. User enters E.164 phone number (e.g. `+923001234567`).
2. App calls Firebase Phone Auth to send 6-digit SMS code.
3. User enters 6-digit code.
4. Firebase verifies SMS code and returns credential token.
5. App posts token to `POST /api/v1/auth/phone-login`.
6. Backend provisions user if new, or fetches existing profile, and returns Auth session payload.

**Alternate flows**
- **A1 — OTP Expiration:** User requests resend after 60-second cooldown timer expires.

**Edge cases & error handling**
- [ ] Invalid OTP code → Backend returns `HTTP 400 Bad Request` with message `"INVALID_OTP"`.

**Postconditions**
- Phone number verified and session established.

**Data & API touchpoints**
- Entities touched: `users`, `organizations`
- Endpoint(s): `POST /api/v1/auth/phone-login`

**Acceptance criteria (testable)**
- WHEN a valid SMS verification code is submitted THE SYSTEM SHALL authenticate the user and link `phone_number` in `users` entity.

**Estimate:** M  
**Depends on:** UC-001  

---

### UC-006: Password Reset Request & Execution

**Linked story:** FS-AUTH-005  
**Actor(s):** User  
**Trigger:** User taps "Forgot Password?" and enters email address.  

**Preconditions**
- [ ] User is on SCR-AUTH-005.

**Main flow**
1. User inputs registered email and clicks "Send Reset Link".
2. Client calls Firebase Auth reset password trigger or FastAPI `POST /api/v1/auth/forgot-password`.
3. System dispatches password reset email containing one-time token (15-min TTL).
4. User clicks link in email, navigating to web reset page / app deep link (SCR-AUTH-006).
5. User enters new password and submits.
6. Backend invalidates all prior sessions/refresh tokens for user.

**Alternate flows**
- **A1 — Non-existent Email:** System returns standard success response to prevent email enumeration attacks.

**Edge cases & error handling**
- [ ] Expired Reset Token → Display "Reset link expired. Please request a new one."

**Postconditions**
- User password updated in Firebase Auth; existing API sessions revoked.

**Data & API touchpoints**
- Entities touched: `users`, `audit_logs`
- Endpoint(s): `POST /api/v1/auth/forgot-password`, `POST /api/v1/auth/reset-password`

**Acceptance criteria (testable)**
- WHEN a password reset is completed THE SYSTEM SHALL revoke all existing active refresh tokens for that user ID.

**Estimate:** S  
**Depends on:** UC-003  

---

### UC-007: Multi-Tenant Role-Based Authorization Enforcement

**Linked story:** FS-AUTH-006  
**Actor(s):** Authenticated User  
**Trigger:** User performs any API request to a tenant-scoped resource.  

**Preconditions**
- [ ] Valid Authorization Bearer header present.

**Main flow**
1. FastAPI Dependency (`get_current_user`) extracts user ID and target `organization_id` from request token / header.
2. Authorization Middleware queries `users_organizations` association table for `(user_id, organization_id)`.
3. Middleware checks user role (`owner`, `admin`, `manager`, `driver`, `viewer`) against route permissions.
4. If role is authorized, request proceeds to route handler.

**Alternate flows**
- **A1 — Cross-Tenant Access Attempt:** Request `organization_id` does not match user memberships → Middleware aborts immediately with `HTTP 403 Forbidden`.

**Edge cases & error handling**
- [ ] Soft-deleted organization → Returns `HTTP 404 Not Found`.

**Postconditions**
- Resource access strictly isolated per tenant boundary.

**Data & API touchpoints**
- Entities touched: `users`, `organizations`, `users_organizations`
- Endpoint(s): All authenticated endpoints (`/api/v1/*`)

**Acceptance criteria (testable)**
- WHEN a user attempts to read or mutate a resource belonging to an `organization_id` they do not belong to THE SYSTEM SHALL return `HTTP 403 Forbidden`.

**Estimate:** M  
**Depends on:** UC-004  

---

### UC-008: Profile Setup & Avatar Upload

**Linked story:** FS-AUTH-007  
**Actor(s):** Authenticated User  
**Trigger:** User updates full name, phone number, or profile picture on SCR-AUTH-007.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. User enters profile details and selects an avatar image.
2. Flutter app resizes image and uploads via `POST /api/v1/users/me/avatar` (multipart/form-data).
3. Backend saves image to Cloud Storage / local storage and generates public CDN URL.
4. App updates user profile with name and `avatar_url` via `PATCH /api/v1/users/me`.
5. Backend updates `users` record and returns updated User DTO.

**Alternate flows**
- **A1 — No Avatar Upload:** User updates text fields only; avatar endpoint is bypassed.

**Edge cases & error handling**
- [ ] Image file size > 5MB → API returns `HTTP 413 Payload Too Large`.

**Postconditions**
- User profile updated in DB.

**Data & API touchpoints**
- Entities touched: `users`
- Endpoint(s): `PATCH /api/v1/users/me`, `POST /api/v1/users/me/avatar`

**Acceptance criteria (testable)**
- WHEN an image over 5MB is uploaded THE SYSTEM SHALL reject the request with `HTTP 413` error code.

**Estimate:** S  
**Depends on:** UC-004  

---

### UC-009: Session Refresh & Access Token Renewal

**Linked story:** FS-AUTH-008  
**Actor(s):** Client App / Background HTTP Interceptor  
**Trigger:** Access JWT expires (HTTP 401 response on API call).  

**Preconditions**
- [ ] Refresh token stored on client.

**Main flow**
1. HTTP client catches 401 response.
2. Interceptor sends stored Refresh Token to `POST /api/v1/auth/refresh`.
3. Backend validates refresh token signature and checks database revocation list.
4. Backend issues new Access JWT (15-min TTL) and new Refresh Token (rotating refresh token pattern).
5. Interceptor retries original failed request with new Access JWT.

**Alternate flows**
- **A1 — Revoked Refresh Token:** Backend returns `HTTP 401`; app clears local storage and redirects user to Login screen.

**Edge cases & error handling**
- [ ] Concurrent refresh requests → Lock mechanism in client prevents multiple simultaneous refresh calls.

**Postconditions**
- Access JWT renewed seamlessly without interrupting user flow.

**Data & API touchpoints**
- Entities touched: `users`
- Endpoint(s): `POST /api/v1/auth/refresh`

**Acceptance criteria (testable)**
- WHEN a valid refresh token is submitted THE SYSTEM SHALL return a new access token and invalidate the previously used refresh token.

**Estimate:** S  
**Depends on:** UC-004  

---

### UC-010: User Sign Out & Token Revocation

**Linked story:** FS-AUTH-009  
**Actor(s):** Authenticated User  
**Trigger:** User taps "Sign Out" in Settings (SCR-SET-001).  

**Preconditions**
- [ ] User logged in.

**Main flow**
1. User confirms sign out prompt.
2. App sends refresh token to `POST /api/v1/auth/logout`.
3. Backend marks token family as revoked in database / Redis cache.
4. App clears secure storage (JWTs, local Hive encryption keys, cached user session).
5. App resets navigation stack to Login screen (SCR-AUTH-001).

**Alternate flows**
- **A1 — Offline Logout:** App clears local credentials immediately and queues token revocation call for next connection.

**Edge cases & error handling**
- [ ] Network failure during API logout → Client forces local credential purge regardless.

**Postconditions**
- Active tokens invalidated server-side and cleared client-side.

**Data & API touchpoints**
- Entities touched: `users`, `audit_logs`
- Endpoint(s): `POST /api/v1/auth/logout`

**Acceptance criteria (testable)**
- WHEN sign out is executed THE SYSTEM SHALL invalidate the active refresh token server-side so it cannot be reused.

**Estimate:** S  
**Depends on:** UC-004  

---

### UC-011: Account Deletion (GDPR Right to be Forgotten)

**Linked story:** FS-AUTH-010  
**Actor(s):** User  
**Trigger:** User requests account deletion in Privacy Settings.  

**Preconditions**
- [ ] User is account owner.

**Main flow**
1. User enters password / confirms deletion dialog.
2. App calls `DELETE /api/v1/users/me`.
3. Backend verifies user is not the sole owner of an active paid organization with other active members (must transfer ownership first).
4. Backend sets `deleted_at = NOW()` on `users` record (soft delete).
5. Backend anonymizes PII fields (`email = "deleted_user_UUID@anonymized.local"`, `name = "Deleted User"`).
6. Backend revokes all active auth sessions.

**Alternate flows**
- **A1 — Sole Owner:** Deletion blocked until organization is deleted or ownership transferred.

**Edge cases & error handling**
- [ ] Active subscription linked → API prompts user to cancel subscription prior to account deletion.

**Postconditions**
- User record soft-deleted and PII anonymized.

**Data & API touchpoints**
- Entities touched: `users`, `organizations`, `audit_logs`
- Endpoint(s): `DELETE /api/v1/users/me`

**Acceptance criteria (testable)**
- WHEN a user deletes their account THE SYSTEM SHALL soft-delete the record (`deleted_at NOT NULL`) and overwrite name and email fields with anonymized strings.

**Estimate:** M  
**Depends on:** UC-007, UC-010  

---

### UC-012: Audit Log Recording for Authentication Events

**Linked story:** FS-AUTH-011  
**Actor(s):** System  
**Trigger:** Any auth event occurs (login, failed login, password change, role change).  

**Preconditions**
- [ ] Auth event triggered.

**Main flow**
1. System captures event metadata (IP address, user agent, event type, timestamp, target user ID).
2. System inserts record into immutable `audit_logs` table (`action`, `actor_id`, `organization_id`, `payload`).
3. If event is high risk (e.g. 5 failed logins), system sends security alert notification.

**Alternate flows**
- **A1 — Unauthenticated Attempt:** `actor_id` is set to null, IP stored.

**Edge cases & error handling**
- [ ] Audit log DB write error → Handled asynchronously; user request is not blocked.

**Postconditions**
- Immutable audit record appended.

**Data & API touchpoints**
- Entities touched: `audit_logs`
- Endpoint(s): Internal middleware

**Acceptance criteria (testable)**
- WHEN an authentication failure or success occurs THE SYSTEM SHALL create an immutable entry in `audit_logs` within 500ms.

**Estimate:** S  
**Depends on:** UC-004  

---

### UC-013: Active Session Management & Device Tracking

**Linked story:** FS-AUTH-012  
**Actor(s):** Authenticated User  
**Trigger:** User views "Active Devices" in Security Settings.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. App calls `GET /api/v1/users/me/sessions`.
2. Backend returns list of active refresh token sessions (device model, OS, IP address, last active time).
3. User selects a session and taps "Revoke Device".
4. App calls `DELETE /api/v1/users/me/sessions/{session_id}`.
5. Backend revokes specified refresh token.

**Alternate flows**
- **A1 — Revoke All Other Devices:** User taps "Revoke All Other Sessions" → Backend revokes all refresh tokens except current session token.

**Edge cases & error handling**
- [ ] Revoking current session → Forces user to re-login immediately.

**Postconditions**
- Target session revoked.

**Data & API touchpoints**
- Entities touched: `users`, `audit_logs`
- Endpoint(s): `GET /api/v1/users/me/sessions`, `DELETE /api/v1/users/me/sessions/{session_id}`

**Acceptance criteria (testable)**
- WHEN a session is revoked via API THE SYSTEM SHALL block any subsequent refresh requests using that session's refresh token with `HTTP 401`.

**Estimate:** M  
**Depends on:** UC-009  

---

## 2. EP-ORG — Organization & Multi-Tenancy

### UC-014: Provision New Commercial Organization

**Linked story:** FS-ORG-001  
**Actor(s):** Fleet Owner  
**Trigger:** User taps "Create Fleet Organization" on SCR-ORG-001.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. User enters organization name, tax ID (optional), industry, and default currency (e.g. `PKR`, `USD`).
2. App sends payload to `POST /api/v1/organizations`.
3. Backend provisions `organizations` record with `is_personal = false`, `tier = "free"`, `max_vehicles = 3`, `max_drivers = 3`.
4. Backend creates record in `users_organizations` linking user as `owner`.
5. Backend returns Organization DTO.
6. App switches user active context to new organization.

**Alternate flows**
- **A1 — Personal Org Creation:** System auto-provisions `is_personal = true` during registration (UC-001).

**Edge cases & error handling**
- [ ] Blank Organization Name → Client/Server validation rejects with `HTTP 422 Unprocessable Entity`.

**Postconditions**
- New multi-tenant organization created; user assigned `owner` role.

**Data & API touchpoints**
- Entities touched: `organizations`, `users_organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/organizations`

**Acceptance criteria (testable)**
- WHEN a commercial organization is created THE SYSTEM SHALL assign the creator the `owner` role in `users_organizations`.

**Estimate:** M  
**Depends on:** UC-001, UC-007  

---

### UC-015: Switch Active Organization Context

**Linked story:** FS-ORG-002  
**Actor(s):** User belonging to multiple organizations  
**Trigger:** User selects an organization from the header context dropdown.  

**Preconditions**
- [ ] User belongs to > 1 active organization.

**Main flow**
1. App fetches organization list via `GET /api/v1/organizations`.
2. User selects target organization.
3. App stores selected `organization_id` in local session state and header configuration.
4. App clears local data cache and re-fetches dashboard data for new tenant context.

**Alternate flows**
- **A1 — Single Org User:** Dropdown is hidden; default organization context used.

**Edge cases & error handling**
- [ ] Membership revoked while active → Next API request returns `HTTP 403`, triggering force-switch to personal org.

**Postconditions**
- Application views scoped strictly to selected tenant.

**Data & API touchpoints**
- Entities touched: `organizations`, `users_organizations`
- Endpoint(s): `GET /api/v1/organizations`

**Acceptance criteria (testable)**
- WHEN active organization context is switched THE SYSTEM SHALL filter all subsequent data queries by the new `organization_id`.

**Estimate:** S  
**Depends on:** UC-007, UC-014  

---

### UC-016: Invite Team Member to Organization

**Linked story:** FS-ORG-003  
**Actor(s):** Owner / Admin  
**Trigger:** User submits invite form on SCR-ORG-002 with email and assigned role.  

**Preconditions**
- [ ] User has `owner` or `admin` role in active organization.

**Main flow**
1. User enters recipient email and selects role (`admin`, `manager`, `driver`, `viewer`).
2. App submits payload to `POST /api/v1/organizations/{org_id}/invitations`.
3. Backend verifies org member count limit (Pro vs Free limits).
4. Backend generates invitation token (7-day TTL) and writes to `organization_invitations` table.
5. Backend sends invitation email with sign-up / accept link.

**Alternate flows**
- **A1 — Existing User:** Recipient already has Veltrics account; email includes direct link to accept in-app.

**Edge cases & error handling**
- [ ] User already invited → API updates expiration and resends email without creating duplicate active token.

**Postconditions**
- Pending invitation record created.

**Data & API touchpoints**
- Entities touched: `organizations`, `organization_invitations`
- Endpoint(s): `POST /api/v1/organizations/{org_id}/invitations`

**Acceptance criteria (testable)**
- WHEN an invitation is created THE SYSTEM SHALL generate a secure 64-character token with a 7-day TTL.

**Estimate:** M  
**Depends on:** UC-007, UC-014  

---

### UC-017: Accept Organization Invitation

**Linked story:** FS-ORG-004  
**Actor(s):** Invited User  
**Trigger:** User clicks invitation link in email or enters token in-app.  

**Preconditions**
- [ ] Valid active invitation token exists.

**Main flow**
1. User opens link containing token `GET /api/v1/invitations/{token}`.
2. System validates token status and expiration.
3. If user is unauthenticated, prompts for registration/login.
4. Upon authentication, user confirms "Accept Invitation".
5. App posts to `POST /api/v1/invitations/{token}/accept`.
6. Backend inserts `users_organizations` record (`user_id`, `organization_id`, `role`).
7. Backend marks invitation status as `ACCEPTED`.

**Alternate flows**
- **A1 — Reject Invitation:** User clicks decline → Status updated to `REJECTED`.

**Edge cases & error handling**
- [ ] Expired Token → API returns `HTTP 410 Gone` with message `"INVITATION_EXPIRED"`.

**Postconditions**
- User linked to organization with assigned role.

**Data & API touchpoints**
- Entities touched: `organizations`, `users_organizations`, `organization_invitations`
- Endpoint(s): `GET /api/v1/invitations/{token}`, `POST /api/v1/invitations/{token}/accept`

**Acceptance criteria (testable)**
- WHEN an invitation is accepted THE SYSTEM SHALL create a `users_organizations` record and mark the invitation as `ACCEPTED` in a single transaction.

**Estimate:** M  
**Depends on:** UC-016  

---

### UC-018: Modify Team Member Role & Permissions

**Linked story:** FS-ORG-005  
**Actor(s):** Owner  
**Trigger:** Owner changes role dropdown for a member on Team Management screen (SCR-ORG-003).  

**Preconditions**
- [ ] Actor is `owner`. Target is member of same organization.

**Main flow**
1. Owner selects new role for target member (`admin` → `manager`).
2. App sends payload to `PATCH /api/v1/organizations/{org_id}/members/{user_id}`.
3. Backend checks caller role is `owner` (only owner can modify admin roles).
4. Backend updates `role` in `users_organizations`.
5. Backend creates audit log record.
6. API returns updated member list DTO.

**Alternate flows**
- **A1 — Change Owner:** Transfer ownership flow (UC-020).

**Edge cases & error handling**
- [ ] Admin attempts to modify Owner role → API returns `HTTP 403 Forbidden`.

**Postconditions**
- Member permissions updated immediately across all subsequent API requests.

**Data & API touchpoints**
- Entities touched: `users_organizations`, `audit_logs`
- Endpoint(s): `PATCH /api/v1/organizations/{org_id}/members/{user_id}`

**Acceptance criteria (testable)**
- WHEN a non-owner attempts to change a member's role THE SYSTEM SHALL reject the request with `HTTP 403 Forbidden`.

**Estimate:** S  
**Depends on:** UC-007, UC-014  

---

### UC-019: Remove Member from Organization

**Linked story:** FS-ORG-006  
**Actor(s):** Owner / Admin  
**Trigger:** Admin taps "Remove Member" button next to a user.  

**Preconditions**
- [ ] Actor has authority to remove target user.

**Main flow**
1. Admin confirms removal modal prompt.
2. App sends request to `DELETE /api/v1/organizations/{org_id}/members/{user_id}`.
3. Backend soft-deletes or deletes row in `users_organizations`.
4. Backend unassigns user from any assigned vehicles (`driver_id = null`).
5. Backend revokes active org session context for removed user.

**Alternate flows**
- **A1 — Self Removal:** Non-owner member clicks "Leave Organization" → Removes own membership.

**Edge cases & error handling**
- [ ] Attempting to remove Organization Owner → API returns `HTTP 400 Bad Request` ("Cannot remove organization owner").

**Postconditions**
- User access to organization revoked; driver assignments cleared.

**Data & API touchpoints**
- Entities touched: `users_organizations`, `vehicles`, `audit_logs`
- Endpoint(s): `DELETE /api/v1/organizations/{org_id}/members/{user_id}`

**Acceptance criteria (testable)**
- WHEN a member is removed THE SYSTEM SHALL clear their `driver_id` from all assigned vehicles in that organization.

**Estimate:** S  
**Depends on:** UC-018  

---

### UC-020: Transfer Organization Ownership

**Linked story:** FS-ORG-007  
**Actor(s):** Current Owner  
**Trigger:** Owner selects "Transfer Ownership" on Organization Settings screen.  

**Preconditions**
- [ ] Actor is current `owner`. Target recipient is an active `admin` or `manager`.

**Main flow**
1. Owner selects target member, enters password, and submits transfer request.
2. Backend validates password.
3. In a single transaction:
   - Updates target member role to `owner`.
   - Updates former owner role to `admin`.
4. Backend writes to `audit_logs`.
5. API notifies new owner via email and push notification.

**Alternate flows**
- **A1 — Transfer Cancelation:** Owner cancels modal before password verification.

**Edge cases & error handling**
- [ ] Invalid Password → API returns `HTTP 401 Unauthorized`.

**Postconditions**
- Primary ownership transferred; former owner demoted to admin.

**Data & API touchpoints**
- Entities touched: `organizations`, `users_organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/organizations/{org_id}/transfer-ownership`

**Acceptance criteria (testable)**
- WHEN ownership is transferred THE SYSTEM SHALL update both user roles in `users_organizations` within a single database transaction.

**Estimate:** M  
**Depends on:** UC-018  

---

### UC-021: Update Organization Profile & Currency Settings

**Linked story:** FS-ORG-008  
**Actor(s):** Owner / Admin  
**Trigger:** User updates organization name, address, tax ID, or currency preference.  

**Preconditions**
- [ ] Actor is owner or admin.

**Main flow**
1. User updates fields on SCR-ORG-004 and clicks "Save Changes".
2. App sends payload to `PATCH /api/v1/organizations/{org_id}`.
3. Backend validates currency code (e.g. ISO 4217 code `PKR`, `USD`, `EUR`).
4. Backend updates `organizations` table.
5. API returns updated Organization DTO.

**Alternate flows**
- **A1 — Currency Formatting Update:** Dashboard UI re-renders all monetary figures using new currency symbol and formatting rules.

**Edge cases & error handling**
- [ ] Invalid ISO Currency Code → API returns `HTTP 422 Unprocessable Entity`.

**Postconditions**
- Organization profile updated.

**Data & API touchpoints**
- Entities touched: `organizations`
- Endpoint(s): `PATCH /api/v1/organizations/{org_id}`

**Acceptance criteria (testable)**
- WHEN currency preference is updated THE SYSTEM SHALL validate the code against standard ISO 4217 currencies.

**Estimate:** S  
**Depends on:** UC-014  

---

### UC-022: Enforce Tier Slot Quotas (Vehicles & Drivers)

**Linked story:** FS-ORG-009  
**Actor(s):** System / User  
**Trigger:** User attempts to add a new vehicle or driver.  

**Preconditions**
- [ ] User initiating vehicle/driver creation.

**Main flow**
1. System queries active organization limits: `max_vehicles` (base + ad-rewarded bonus) and current active count `SELECT COUNT(*) FROM vehicles WHERE organization_id = :org_id AND deleted_at IS NULL`.
2. If `current_count < max_vehicles`, request proceeds.
3. If `current_count >= max_vehicles`, system blocks creation and triggers Quota Wall UI (SCR-PAY-001).

**Alternate flows**
- **A1 — Ad-Rewarded Unlock Available:** If user is on Free Tier and `ad_bonus_vehicles < 2`, Quota Wall offers "Watch Ads for +1 Bonus Slot" (UC-120).
- **A2 — Hard Cap Reached:** If user reached 5 vehicles on Free Tier, Quota Wall requires upgrading to Pro.

**Edge cases & error handling**
- [ ] Concurrent creation race condition → DB check / constraint prevents inserting vehicle beyond `max_vehicles`.

**Postconditions**
- Resource creation strictly bounded by active tier limits.

**Data & API touchpoints**
- Entities touched: `organizations`, `vehicles`, `drivers`
- Endpoint(s): `POST /api/v1/vehicles`, `POST /api/v1/drivers`

**Acceptance criteria (testable)**
- WHEN an organization at max quota attempts to add a vehicle without bonus slots THE SYSTEM SHALL return `HTTP 402 Payment Required` with detail `"QUOTA_EXCEEDED"`.

**Estimate:** M  
**Depends on:** UC-014, UC-120  

---

### UC-023: Soft Delete & Archive Organization

**Linked story:** FS-ORG-010  
**Actor(s):** Owner  
**Trigger:** Owner clicks "Delete Organization" in danger zone.  

**Preconditions**
- [ ] Actor is `owner`. Password re-verification completed.

**Main flow**
1. Owner submits confirmation phrase and password.
2. App calls `DELETE /api/v1/organizations/{org_id}`.
3. Backend sets `deleted_at = NOW()` on `organizations` record and cascading soft deletes on all child entities (`vehicles`, `drivers`, `fuel_logs`, `maintenance_logs`, `trips`, `expenses`).
4. Backend cancels active payment subscriptions via gateway API.
5. App switches user active context to personal organization.

**Alternate flows**
- **A1 — Restore Organization:** Super-admin can restore soft-deleted organization within 30 days by setting `deleted_at = NULL`.

**Edge cases & error handling**
- [ ] Personal Organization Deletion Attempt → API rejects with `HTTP 400` ("Personal organization cannot be deleted").

**Postconditions**
- Organization and child entities soft-deleted.

**Data & API touchpoints**
- Entities touched: `organizations`, `vehicles`, `drivers`, `subscriptions`, `audit_logs`
- Endpoint(s): `DELETE /api/v1/organizations/{org_id}`

**Acceptance criteria (testable)**
- WHEN an organization is deleted THE SYSTEM SHALL set `deleted_at` timestamps on the organization and all associated child entity rows within a single transaction.

**Estimate:** L  
**Depends on:** UC-007, UC-014  

---

## 3. EP-VEH — Vehicle Management

### UC-024: Register New Vehicle

**Linked story:** FS-VEH-001  
**Actor(s):** Fleet Manager / Consumer  
**Trigger:** User taps "Add Vehicle" and submits form on SCR-VEH-002.  

**Preconditions**
- [ ] Organization quota not exceeded (UC-022).

**Main flow**
1. User enters make, model, year, VIN, license plate, initial odometer, fuel type, and transmission.
2. Client generates local UUID v4 `vehicle_id`.
3. App posts payload to `POST /api/v1/vehicles`.
4. Backend validates VIN format and checks quota limits.
5. Backend creates `vehicles` record with `organization_id`, `sharding_key`, and `created_at`.
6. API returns created Vehicle DTO.
7. App updates local Hive cache and navigates to Vehicle Detail screen (SCR-VEH-003).

**Alternate flows**
- **A1 — Ad-Rewarded Vehicle:** If vehicle created under ad-rewarded slot 4 or 5, system attaches `is_ad_rewarded = true` flag.

**Edge cases & error handling**
- [ ] Duplicate VIN in same organization → API returns `HTTP 409 Conflict` ("VIN already exists in fleet").

**Postconditions**
- Vehicle added to fleet.

**Data & API touchpoints**
- Entities touched: `vehicles`, `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/vehicles`

**Acceptance criteria (testable)**
- WHEN a valid vehicle payload is submitted THE SYSTEM SHALL store the vehicle record with client-assigned UUID v4 primary key.

**Estimate:** M  
**Depends on:** UC-014, UC-022  

---

### UC-025: View Fleet Vehicle Directory & Filter

**Linked story:** FS-VEH-002  
**Actor(s):** User  
**Trigger:** User navigates to Vehicles tab (SCR-VEH-001).  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. App queries `GET /api/v1/vehicles?status=active&page=1&limit=20`.
2. Backend filters `vehicles` table by `organization_id` and `deleted_at IS NULL`.
3. Backend joins assigned driver details (`users.name`).
4. API returns paginated list of vehicle summary DTOs.
5. Flutter client renders vehicle grid/list with badge indicators (ad-rewarded badge, status color).

**Alternate flows**
- **A1 — Search & Filter:** User filters by status (`ACTIVE`, `MAINTENANCE`, `INACTIVE`), fuel type, or searches by plate string → App requests with corresponding query params.

**Edge cases & error handling**
- [ ] Offline Access → App reads cached vehicle list from local Hive `hive_vehicles` box.

**Postconditions**
- Vehicle list displayed.

**Data & API touchpoints**
- Entities touched: `vehicles`, `users`
- Endpoint(s): `GET /api/v1/vehicles`

**Acceptance criteria (testable)**
- WHEN query params `status=MAINTENANCE` are passed THE SYSTEM SHALL return only vehicles currently flagged in `MAINTENANCE` state.

**Estimate:** S  
**Depends on:** UC-024  

---

### UC-026: View Vehicle Detailed Overview

**Linked story:** FS-VEH-003  
**Actor(s):** User  
**Trigger:** User taps a vehicle card in the fleet directory.  

**Preconditions**
- [ ] Vehicle exists in active tenant context.

**Main flow**
1. App calls `GET /api/v1/vehicles/{vehicle_id}`.
2. Backend fetches vehicle entity, specs JSONB, primary assigned driver, and summary counts (latest fuel log, active maintenance tasks, total monthly expense).
3. API returns comprehensive Vehicle Detail DTO.
4. App renders tabs: Overview, Specs, Maintenance History, Fuel Logs, Expenses.

**Alternate flows**
- **A1 — Vehicle Not Found:** Returns `HTTP 404 Not Found`.

**Edge cases & error handling**
- [ ] Vehicle belongs to different organization → Returns `HTTP 403 Forbidden`.

**Postconditions**
- Vehicle detail state loaded.

**Data & API touchpoints**
- Entities touched: `vehicles`, `users`, `maintenance_logs`, `fuel_logs`, `expenses`
- Endpoint(s): `GET /api/v1/vehicles/{vehicle_id}`

**Acceptance criteria (testable)**
- WHEN fetching vehicle details THE SYSTEM SHALL return overall vehicle metadata along with latest fuel log and upcoming maintenance alert summary.

**Estimate:** S  
**Depends on:** UC-025  

---

### UC-027: Update Vehicle Metadata & Specifications

**Linked story:** FS-VEH-004  
**Actor(s):** Fleet Manager / Owner  
**Trigger:** User edits vehicle details on SCR-VEH-004 and taps Save.  

**Preconditions**
- [ ] User has edit permissions.

**Main flow**
1. User updates color, license plate, specs JSONB (engine size, tire pressure specs, oil type).
2. App sends payload to `PATCH /api/v1/vehicles/{vehicle_id}`.
3. Backend validates JSONB schema for custom specs.
4. Backend updates `vehicles` record and increments `updated_at`.
5. API returns updated Vehicle DTO.

**Alternate flows**
- **A1 — Odometer Manual Correction:** Updating odometer triggers audit log entry if discrepancy > 500km.

**Edge cases & error handling**
- [ ] Invalid JSONB structure in specs → Backend returns `HTTP 422 Unprocessable Entity`.

**Postconditions**
- Vehicle specifications updated.

**Data & API touchpoints**
- Entities touched: `vehicles`, `audit_logs`
- Endpoint(s): `PATCH /api/v1/vehicles/{vehicle_id}`

**Acceptance criteria (testable)**
- WHEN custom specs are submitted THE SYSTEM SHALL validate the structure against the Pydantic VehicleSpecs JSON schema.

**Estimate:** S  
**Depends on:** UC-026  

---

### UC-028: Assign Primary Driver to Vehicle

**Linked story:** FS-VEH-005  
**Actor(s):** Fleet Manager  
**Trigger:** User selects a driver from dropdown on Vehicle Assignment modal.  

**Preconditions**
- [ ] Target driver is an active member/driver in same organization.

**Main flow**
1. Manager selects driver from dropdown list (`GET /api/v1/drivers`).
2. App calls `POST /api/v1/vehicles/{vehicle_id}/assign-driver` with `driver_id`.
3. Backend updates `vehicles.primary_driver_id = driver_id`.
4. Backend logs assignment event in `audit_logs`.
5. API returns updated vehicle DTO.
6. Push notification sent to assigned driver's device.

**Alternate flows**
- **A1 — Unassign Driver:** Manager selects "None" → Backend sets `primary_driver_id = NULL`.

**Edge cases & error handling**
- [ ] Assigned driver from another organization → API returns `HTTP 403 Forbidden`.

**Postconditions**
- Driver linked to vehicle.

**Data & API touchpoints**
- Entities touched: `vehicles`, `users`, `audit_logs`
- Endpoint(s): `POST /api/v1/vehicles/{vehicle_id}/assign-driver`

**Acceptance criteria (testable)**
- WHEN a driver is assigned to a vehicle THE SYSTEM SHALL update `primary_driver_id` and create an audit log entry.

**Estimate:** S  
**Depends on:** UC-026  

---

### UC-029: Update Vehicle Odometer Reading

**Linked story:** FS-VEH-006  
**Actor(s):** Driver / Fleet Manager  
**Trigger:** User inputs current odometer reading on Quick Update modal.  

**Preconditions**
- [ ] Vehicle active.

**Main flow**
1. User enters new mileage (e.g. `45,250 km`).
2. App sends `POST /api/v1/vehicles/{vehicle_id}/odometer` with `{ current_odometer: 45250, reading_date: "2026-08-01" }`.
3. Backend validates `current_odometer >= vehicle.current_odometer` (mileage cannot decrease).
4. Backend updates `vehicles.current_odometer = 45250`.
5. Backend checks if any scheduled maintenance triggers are reached (e.g. 45,000km oil change) and generates alert if threshold crossed.

**Alternate flows**
- **A1 — Lower Odometer Entry (Correction):** Requires admin privilege and explicit flag `is_correction = true`.

**Edge cases & error handling**
- [ ] Odometer entry lower than current without correction flag → API returns `HTTP 400 Bad Request` ("New odometer reading cannot be lower than existing reading of 45,200 km").

**Postconditions**
- Vehicle odometer updated; maintenance threshold triggers evaluated.

**Data & API touchpoints**
- Entities touched: `vehicles`, `maintenance_schedules`, `notifications`
- Endpoint(s): `POST /api/v1/vehicles/{vehicle_id}/odometer`

**Acceptance criteria (testable)**
- WHEN a higher odometer reading is submitted THE SYSTEM SHALL update `current_odometer` and trigger any matching maintenance schedule alerts.

**Estimate:** M  
**Depends on:** UC-026  

---

### UC-030: Vehicle Status Lifecycle Management (Active / In Service / Decommissioned)

**Linked story:** FS-VEH-007  
**Actor(s):** Fleet Manager  
**Trigger:** Manager updates status dropdown on Vehicle Detail screen.  

**Preconditions**
- [ ] Manager permissions verified.

**Main flow**
1. Manager selects new status (`ACTIVE`, `IN_SERVICE`, `OUT_OF_SERVICE`, `SOLD`).
2. App calls `PATCH /api/v1/vehicles/{vehicle_id}/status`.
3. Backend updates `vehicles.status`.
4. If status set to `SOLD` or `OUT_OF_SERVICE`, driver assignment is cleared.
5. API returns updated Vehicle DTO.

**Alternate flows**
- **A1 — Maintenance Auto-Status:** Logging an active maintenance ticket auto-prompts to change status to `IN_SERVICE`.

**Edge cases & error handling**
- [ ] Attempting to log trip on `OUT_OF_SERVICE` vehicle → System blocks trip entry.

**Postconditions**
- Vehicle status transition recorded.

**Data & API touchpoints**
- Entities touched: `vehicles`, `audit_logs`
- Endpoint(s): `PATCH /api/v1/vehicles/{vehicle_id}/status`

**Acceptance criteria (testable)**
- WHEN vehicle status is changed to `SOLD` THE SYSTEM SHALL unassign the primary driver and exclude the vehicle from active fleet statistics.

**Estimate:** S  
**Depends on:** UC-026  

---

### UC-031: Upload & Manage Vehicle Documents (Registration / Insurance)

**Linked story:** FS-VEH-008  
**Actor(s):** Fleet Manager  
**Trigger:** User uploads PDF/image of registration or insurance card on Documents tab.  

**Preconditions**
- [ ] File selected (< 10MB PDF/JPEG/PNG).

**Main flow**
1. User enters document type (`INSURANCE`, `REGISTRATION`, `PERMIT`), expiration date, and attaches file.
2. App calls `POST /api/v1/vehicles/{vehicle_id}/documents` (multipart).
3. Backend uploads document to Cloud Storage and creates `vehicle_documents` record with expiration timestamp.
4. Backend schedules background notification 30 days prior to document expiration.
5. API returns created document DTO with download URL.

**Alternate flows**
- **A1 — Document Expiration Alert:** Nightly cron checks expiring documents and sends notification to fleet manager (UC-076).

**Edge cases & error handling**
- [ ] Unsupported format (e.g. `.exe`) → API rejects with `HTTP 400 Bad Request`.

**Postconditions**
- Vehicle document stored and expiration alert scheduled.

**Data & API touchpoints**
- Entities touched: `vehicles`, `vehicle_documents`
- Endpoint(s): `POST /api/v1/vehicles/{vehicle_id}/documents`, `GET /api/v1/vehicles/{vehicle_id}/documents`

**Acceptance criteria (testable)**
- WHEN a vehicle document with an expiration date is uploaded THE SYSTEM SHALL store the document and create a scheduled expiration alert task.

**Estimate:** M  
**Depends on:** UC-026  

---

### UC-032: Soft Delete & Archive Vehicle

**Linked story:** FS-VEH-009  
**Actor(s):** Fleet Owner / Admin  
**Trigger:** User clicks "Delete Vehicle" on SCR-VEH-004.  

**Preconditions**
- [ ] Admin permission.

**Main flow**
1. User confirms deletion prompt.
2. App sends `DELETE /api/v1/vehicles/{vehicle_id}`.
3. Backend sets `deleted_at = NOW()` on target `vehicles` row.
4. Backend frees up 1 vehicle slot in active organization quota.
5. API returns `HTTP 200 OK`.

**Alternate flows**
- **A1 — Soft Delete Recovery:** Vehicle can be restored within 30 days by setting `deleted_at = NULL`.

**Edge cases & error handling**
- [ ] Active maintenance tasks linked → System archives tasks alongside vehicle.

**Postconditions**
- Vehicle soft-deleted; quota slot released.

**Data & API touchpoints**
- Entities touched: `vehicles`, `organizations`, `audit_logs`
- Endpoint(s): `DELETE /api/v1/vehicles/{vehicle_id}`

**Acceptance criteria (testable)**
- WHEN a vehicle is soft-deleted THE SYSTEM SHALL set `deleted_at = NOW()` and reduce the active organization vehicle count by 1.

**Estimate:** S  
**Depends on:** UC-026  

---

### UC-033: Vehicle Cost-per-Kilometer & Total Cost Analytics

**Linked story:** FS-VEH-010  
**Actor(s):** User / Manager  
**Trigger:** User views Analytics section on Vehicle Detail screen.  

**Preconditions**
- [ ] Vehicle has logged fuel/expenses and odometer history.

**Main flow**
1. App calls `GET /api/v1/vehicles/{vehicle_id}/analytics?timeframe=30d`.
2. Backend sums `fuel_logs.total_cost` + `maintenance_logs.cost` + `expenses.amount` over period.
3. Backend calculates total distance traveled over period (`max_odometer - min_odometer`).
4. Backend computes `cost_per_km = total_cost / total_distance`.
5. API returns Analytics DTO (total cost breakdown, cost per km, fuel efficiency km/L).

**Alternate flows**
- **A1 — Zero Distance Traveled:** `cost_per_km` returned as 0.0 with warning `"INSUFFICIENT_DISTANCE_DATA"`.

**Edge cases & error handling**
- [ ] No logs exist for timeframe → Returns zeroes without error.

**Postconditions**
- Vehicle cost metrics computed and rendered.

**Data & API touchpoints**
- Entities touched: `vehicles`, `fuel_logs`, `maintenance_logs`, `expenses`
- Endpoint(s): `GET /api/v1/vehicles/{vehicle_id}/analytics`

**Acceptance criteria (testable)**
- WHEN analytics are requested THE SYSTEM SHALL calculate total cost and divide by distance delta to return `cost_per_km` rounded to 2 decimal places.

**Estimate:** M  
**Depends on:** UC-026, UC-040, UC-046  

---

## 4. EP-MNT — Maintenance Engine

### UC-034: Log Completed Maintenance Task

**Linked story:** FS-MNT-001  
**Actor(s):** Driver / Fleet Manager  
**Trigger:** User fills maintenance form on SCR-MNT-002 and submits.  

**Preconditions**
- [ ] Vehicle exists in organization.

**Main flow**
1. User selects vehicle, service type (`OIL_CHANGE`, `TIRE_ROTATION`, `BRAKE_INSPECTION`, `REPAIR`), cost, service date, odometer reading, service provider name, and notes.
2. User optionally attaches receipt image.
3. Client generates local UUID v4 `maintenance_id`.
4. App calls `POST /api/v1/maintenance`.
5. Backend creates `maintenance_logs` record.
6. Backend updates `vehicles.current_odometer` if logged odometer > current.
7. Backend resets corresponding scheduled maintenance interval timers/mileage counters.
8. API returns Maintenance Log DTO.

**Alternate flows**
- **A1 — Ad-Rewarded Vehicle Log:** If vehicle is ad-rewarded (Free tier), Flutter requires ad playback completion and signature token prior to submission (UC-122).

**Edge cases & error handling**
- [ ] Negative cost entry → Client/API validation rejects with `HTTP 422`.

**Postconditions**
- Maintenance entry saved; vehicle odometer updated; service schedule reset.

**Data & API touchpoints**
- Entities touched: `maintenance_logs`, `vehicles`, `maintenance_schedules`
- Endpoint(s): `POST /api/v1/maintenance`

**Acceptance criteria (testable)**
- WHEN a completed maintenance task is logged THE SYSTEM SHALL store the log, update vehicle odometer, and reset related maintenance schedule counters.

**Estimate:** M  
**Depends on:** UC-026  

---

### UC-035: Configure Recurring Maintenance Schedules

**Linked story:** FS-MNT-002  
**Actor(s):** Fleet Manager  
**Trigger:** Manager configures service rule (e.g. "Oil Change every 5,000 km or 6 months") on SCR-MNT-004.  

**Preconditions**
- [ ] Manager permissions.

**Main flow**
1. Manager enters task name, interval distance (km), interval time (months), and target vehicle / fleet-wide template flag.
2. App sends payload to `POST /api/v1/maintenance/schedules`.
3. Backend creates record in `maintenance_schedules`.
4. Backend calculates next due odometer (`current_odometer + interval_km`) and next due date (`current_date + interval_months`).
5. API returns Schedule DTO.

**Alternate flows**
- **A1 — Fleet Template:** If `is_template = true`, schedule automatically applies to all newly registered vehicles in organization.

**Edge cases & error handling**
- [ ] Both interval distance and time set to zero → API rejects with `HTTP 400 Bad Request`.

**Postconditions**
- Recurring maintenance rule established.

**Data & API touchpoints**
- Entities touched: `maintenance_schedules`, `vehicles`
- Endpoint(s): `POST /api/v1/maintenance/schedules`

**Acceptance criteria (testable)**
- WHEN a recurring schedule is configured THE SYSTEM SHALL compute and store the `next_due_odometer` and `next_due_date` fields.

**Estimate:** M  
**Depends on:** UC-026  

---

### UC-036: Generate Scheduled Maintenance Due Notifications

**Linked story:** FS-MNT-003  
**Actor(s):** System Cron / Background Worker  
**Trigger:** Daily scheduled maintenance evaluator job runs.  

**Preconditions**
- [ ] Active maintenance schedules exist.

**Main flow**
1. Worker queries active `maintenance_schedules` where `next_due_date <= CURRENT_DATE + 7 DAYS` OR `vehicles.current_odometer >= next_due_odometer - 500`.
2. Worker creates alert records in `notifications` for assigned drivers and fleet managers.
3. System dispatches FCM push notifications: `"Maintenance Due: Vehicle [Plate] is due for Oil Change in 200 km"`.
4. Updates schedule status to `DUE` or `OVERDUE`.

**Alternate flows**
- **A1 — Overdue Task:** `current_odometer > next_due_odometer` → Status marked as `OVERDUE` (red badge on dashboard).

**Edge cases & error handling**
- [ ] FCM delivery failure → Retried up to 3 times; notification remains visible in-app notification center.

**Postconditions**
- Notifications queued and status flags updated.

**Data & API touchpoints**
- Entities touched: `maintenance_schedules`, `vehicles`, `notifications`
- Endpoint(s): Background task / `GET /api/v1/notifications`

**Acceptance criteria (testable)**
- WHEN a vehicle's odometer reaches within 500 km of `next_due_odometer` THE SYSTEM SHALL flag the schedule as `DUE` and dispatch a notification.

**Estimate:** M  
**Depends on:** UC-035, UC-072  

---

### UC-037: Digital Multi-Point Inspection Checklists

**Linked story:** FS-MNT-004  
**Actor(s):** Driver / Mechanic  
**Trigger:** Driver initiates digital inspection on SCR-MNT-003.  

**Preconditions**
- [ ] Driver assigned to vehicle.

**Main flow**
1. Driver opens inspection checklist form (tires, lights, brakes, fluid levels, wipers).
2. Driver marks each item (`PASS`, `FAIL`, `ATTENTION_NEEDED`) and adds notes/photos for failed items.
3. Driver submits inspection.
4. App posts payload to `POST /api/v1/maintenance/inspections` with checklist stored as JSONB schema.
5. If any item is marked `FAIL`, backend automatically creates an pending maintenance issue ticket.
6. API returns Inspection Log DTO.

**Alternate flows**
- **A1 — Custom Template (Pro Tier):** Pro users load organization-customized JSON checklist templates. Standard users use default 10-point checklist.

**Edge cases & error handling**
- [ ] Unfinished checklist submitted → Client enforces all mandatory items answered before POST.

**Postconditions**
- Digital inspection recorded; issues auto-created for failed items.

**Data & API touchpoints**
- Entities touched: `maintenance_inspections`, `maintenance_logs`, `vehicles`
- Endpoint(s): `POST /api/v1/maintenance/inspections`

**Acceptance criteria (testable)**
- WHEN an inspection item is marked `FAIL` THE SYSTEM SHALL automatically create a pending maintenance issue ticket for that vehicle.

**Estimate:** L  
**Depends on:** UC-034  

---

### UC-038: View Maintenance History & Service Log Directory

**Linked story:** FS-MNT-005  
**Actor(s):** User  
**Trigger:** User opens Maintenance tab (SCR-MNT-001).  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. App queries `GET /api/v1/maintenance?vehicle_id={id}&status={status}&page=1`.
2. Backend returns paginated list of maintenance logs and upcoming schedules.
3. User filters by service type or date range.
4. App displays service timeline with total spent aggregate header.

**Alternate flows**
- **A1 — Export Maintenance History:** Pro user taps Export → Downloads PDF service report (UC-110).

**Edge cases & error handling**
- [ ] Empty state → App displays "No maintenance records logged yet. Tap + to add first record."

**Postconditions**
- Maintenance history list rendered.

**Data & API touchpoints**
- Entities touched: `maintenance_logs`, `vehicles`
- Endpoint(s): `GET /api/v1/maintenance`

**Acceptance criteria (testable)**
- WHEN maintenance history is queried THE SYSTEM SHALL return paginated logs ordered by `service_date DESC`.

**Estimate:** S  
**Depends on:** UC-034  

---

### UC-039: Attach & View Maintenance Receipts & Work Orders

**Linked story:** FS-MNT-006  
**Actor(s):** User  
**Trigger:** User uploads or views receipt file on a maintenance log item.  

**Preconditions**
- [ ] Maintenance log exists.

**Main flow**
1. User taps "Attach Receipt" and selects image/PDF file.
2. App sends file to `POST /api/v1/maintenance/{log_id}/attachments` (multipart).
3. Backend uploads file to cloud storage bucket and appends file URL to `receipt_attachments` JSON array in `maintenance_logs`.
4. API returns updated log DTO.

**Alternate flows**
- **A1 — View Attachment:** User taps thumbnail → App opens secure presigned S3/CDN image URL.

**Edge cases & error handling**
- [ ] Exceeds 10MB limit → Returns `HTTP 413 Payload Too Large`.

**Postconditions**
- Attachment linked to log.

**Data & API touchpoints**
- Entities touched: `maintenance_logs`
- Endpoint(s): `POST /api/v1/maintenance/{log_id}/attachments`

**Acceptance criteria (testable)**
- WHEN a receipt attachment is uploaded THE SYSTEM SHALL store the file and append the URL to the `receipt_attachments` JSON array.

**Estimate:** S  
**Depends on:** UC-034  

---

### UC-040: Maintenance Expense Categorization & Aggregation

**Linked story:** FS-MNT-007  
**Actor(s):** Fleet Manager / Accountant  
**Trigger:** Maintenance task saved with cost details.  

**Preconditions**
- [ ] Maintenance log created.

**Main flow**
1. System automatically creates a mirror entry in `expenses` table with `category = "MAINTENANCE"` and `reference_id = maintenance_log_id`.
2. System updates organization-level monthly maintenance expenditure aggregates.
3. System updates vehicle total cost accumulator.

**Alternate flows**
- **A1 — Cost Updated:** Modifying maintenance log cost updates linked `expenses` record in single transaction.

**Edge cases & error handling**
- [ ] Deleting maintenance log → Cascades soft-delete to linked expense entry.

**Postconditions**
- Financial expense ledger synchronized with maintenance log.

**Data & API touchpoints**
- Entities touched: `maintenance_logs`, `expenses`
- Endpoint(s): Internal transaction / `GET /api/v1/expenses`

**Acceptance criteria (testable)**
- WHEN a maintenance log with cost > 0 is created THE SYSTEM SHALL automatically create a corresponding `expenses` record linked by `reference_id`.

**Estimate:** M  
**Depends on:** UC-034, UC-058  

---

### UC-041: Vendor & Service Center Directory Management

**Linked story:** FS-MNT-008  
**Actor(s):** Fleet Manager  
**Trigger:** Manager adds or manages preferred mechanics/vendors on SCR-MNT-005.  

**Preconditions**
- [ ] Manager permissions.

**Main flow**
1. Manager enters vendor name, contact person, phone, address, and specialty (e.g. "City Tires & Alignment").
2. App sends payload to `POST /api/v1/vendors`.
3. Backend creates `vendors` record for organization.
4. Vendor appears as autocomplete selection when logging maintenance tasks.

**Alternate flows**
- **A1 — Delete Vendor:** Soft-deletes vendor without breaking historical maintenance logs.

**Edge cases & error handling**
- [ ] Duplicate Vendor Name → API returns warning but allows saving.

**Postconditions**
- Vendor record available for task association.

**Data & API touchpoints**
- Entities touched: `vendors`, `organizations`
- Endpoint(s): `POST /api/v1/vendors`, `GET /api/v1/vendors`

**Acceptance criteria (testable)**
- WHEN a vendor is saved THE SYSTEM SHALL make it available for auto-completion in the service provider field of maintenance logs.

**Estimate:** S  
**Depends on:** UC-034  

---

### UC-042: Custom Maintenance Checklist Template Builder (Pro)

**Linked story:** FS-MNT-009  
**Actor(s):** Pro Tier Fleet Manager  
**Trigger:** Manager creates custom inspection template on SCR-MNT-006.  

**Preconditions**
- [ ] Active Pro/Enterprise subscription.

**Main flow**
1. Manager defines custom checklist sections (e.g. Heavy Equipment Pre-Trip Inspection) and item definitions.
2. App sends payload to `POST /api/v1/maintenance/templates`.
3. Backend validates schema and saves to `maintenance_templates` table.
4. Drivers in organization can select custom template when performing inspections.

**Alternate flows**
- **A1 — Free Tier Access Attempt:** Blocked by Quota Wall (UC-022).

**Edge cases & error handling**
- [ ] Invalid JSON structural schema → Returns `HTTP 422`.

**Postconditions**
- Custom inspection template saved.

**Data & API touchpoints**
- Entities touched: `maintenance_templates`, `organizations`
- Endpoint(s): `POST /api/v1/maintenance/templates`

**Acceptance criteria (testable)**
- WHEN a Free-tier user attempts to create a custom maintenance template THE SYSTEM SHALL reject the request with `HTTP 402 Payment Required`.

**Estimate:** M  
**Depends on:** UC-037, UC-080  

---

### UC-043: Bulk Maintenance Task Scheduling

**Linked story:** FS-MNT-010  
**Actor(s):** Fleet Manager  
**Trigger:** Manager selects multiple vehicles and clicks "Schedule Fleet Service".  

**Preconditions**
- [ ] > 1 vehicle selected.

**Main flow**
1. Manager selects 5 vehicles, service type ("Winter Tire Change"), and target completion date.
2. App calls `POST /api/v1/maintenance/schedules/bulk`.
3. Backend creates individual maintenance schedule entries for all selected vehicles in a single transaction.
4. API returns list of created schedule DTOs.

**Alternate flows**
- **A1 — Partial Failure:** Transaction rolls back entirely if any vehicle ID is invalid.

**Edge cases & error handling**
- [ ] Empty vehicle list → API returns `HTTP 400 Bad Request`.

**Postconditions**
- Service schedules created across selected fleet vehicles.

**Data & API touchpoints**
- Entities touched: `maintenance_schedules`, `vehicles`
- Endpoint(s): `POST /api/v1/maintenance/schedules/bulk`

**Acceptance criteria (testable)**
- WHEN bulk scheduling is submitted THE SYSTEM SHALL create all schedule records within a single database transaction.

**Estimate:** M  
**Depends on:** UC-035  

---

### UC-044: Part & Inventory Tracking Linkage

**Linked story:** FS-MNT-011  
**Actor(s):** Fleet Manager / Mechanic  
**Trigger:** User attaches part SKU and unit cost to maintenance log.  

**Preconditions**
- [ ] Maintenance log being created/edited.

**Main flow**
1. User adds part item (e.g. "Oil Filter - Part #12345", Quantity: 1, Unit Price: $15.00).
2. App appends item to `parts_used` JSON array payload.
3. Backend calculates total parts cost and validates log total matches parts sum + labor cost.
4. Backend saves log.

**Alternate flows**
- **A1 — No Parts Used:** `parts_used` array left empty.

**Edge cases & error handling**
- [ ] Part quantity <= 0 → Client validation blocks entry.

**Postconditions**
- Parts breakdown recorded on maintenance log.

**Data & API touchpoints**
- Entities touched: `maintenance_logs`
- Endpoint(s): `POST /api/v1/maintenance`

**Acceptance criteria (testable)**
- WHEN parts are attached to a maintenance log THE SYSTEM SHALL store the itemized breakdown in the `parts_used` JSONB field.

**Estimate:** S  
**Depends on:** UC-034  

---

### UC-045: Service Reminder Snooze & Dismissal

**Linked story:** FS-MNT-012  
**Actor(s):** Fleet Manager / Driver  
**Trigger:** User taps "Snooze 7 Days" or "Dismiss" on a maintenance alert notification.  

**Preconditions**
- [ ] Active maintenance due alert exists.

**Main flow**
1. User selects "Snooze 7 Days" on alert card.
2. App calls `POST /api/v1/maintenance/schedules/{schedule_id}/snooze` with `{ snooze_days: 7 }`.
3. Backend updates `snoozed_until = CURRENT_DATE + 7 DAYS`.
4. Evaluator cron suppresses notifications for this schedule until snoozed date expires.

**Alternate flows**
- **A1 — Dismiss Alert:** User taps Dismiss → Alert hidden from notification tray but schedule remains `DUE` on vehicle detail screen.

**Edge cases & error handling**
- [ ] Snoozing an already completed schedule → API returns `HTTP 400 Bad Request`.

**Postconditions**
- Alert notification suppressed until snooze expiration.

**Data & API touchpoints**
- Entities touched: `maintenance_schedules`, `notifications`
- Endpoint(s): `POST /api/v1/maintenance/schedules/{schedule_id}/snooze`

**Acceptance criteria (testable)**
- WHEN a reminder is snoozed for N days THE SYSTEM SHALL update `snoozed_until` and suppress FCM alerts for that duration.

**Estimate:** S  
**Depends on:** UC-036  

---

## 5. EP-FUEL — Fuel Logging

### UC-046: Log Fuel Fill-Up Entry

**Linked story:** FS-FUEL-001  
**Actor(s):** Driver / Consumer  
**Trigger:** User submits fuel log form on SCR-FUEL-002.  

**Preconditions**
- [ ] Vehicle selected.

**Main flow**
1. User enters odometer reading, fuel quantity (liters/gallons), total cost, fuel type, fill date, and `is_full_tank` boolean flag.
2. User optionally snaps receipt photo.
3. Client generates local UUID v4 `fuel_log_id`.
4. App calls `POST /api/v1/fuel`.
5. Backend creates `fuel_logs` record.
6. Backend computes fuel economy (km/L) if previous log had `is_full_tank = true` (UC-047).
7. Backend updates `vehicles.current_odometer` if mileage > current.
8. API returns Fuel Log DTO with calculated efficiency score.

**Alternate flows**
- **A1 — Ad-Rewarded Vehicle:** If vehicle is ad-rewarded (Free tier), Flutter requires rewarded ad completion and signature token prior to submission (UC-122).

**Edge cases & error handling**
- [ ] Odometer entry lower than previous fuel log → API rejects with `HTTP 400 Bad Request`.

**Postconditions**
- Fuel log saved; vehicle odometer updated; efficiency calculated.

**Data & API touchpoints**
- Entities touched: `fuel_logs`, `vehicles`, `expenses`
- Endpoint(s): `POST /api/v1/fuel`

**Acceptance criteria (testable)**
- WHEN a fuel log entry is saved THE SYSTEM SHALL automatically create a linked expense record under category `FUEL`.

**Estimate:** M  
**Depends on:** UC-026, UC-122  

---

### UC-047: Calculate Fuel Efficiency & Distance Delta

**Linked story:** FS-FUEL-002  
**Actor(s):** System  
**Trigger:** New fuel log with `is_full_tank = true` saved.  

**Preconditions**
- [ ] Previous fuel log with `is_full_tank = true` exists for same vehicle.

**Main flow**
1. System queries previous full-tank log: `prev_odometer`.
2. System computes distance delta: `distance = current_odometer - prev_odometer`.
3. System computes fuel efficiency: `efficiency_kml = distance / current_liters`.
4. System updates `fuel_logs.calculated_efficiency = efficiency_kml` and `fuel_logs.distance_traveled = distance`.
5. If efficiency is 30% lower than vehicle baseline average, system flags entry for review (potential fuel leak/theft alert).

**Alternate flows**
- **A1 — Partial Fill-up:** `is_full_tank = false` → System skips efficiency calculation for current entry and waits for next full fill-up.

**Edge cases & error handling**
- [ ] `distance <= 0` → Set `calculated_efficiency = NULL`.

**Postconditions**
- Fuel efficiency calculated and stored.

**Data & API touchpoints**
- Entities touched: `fuel_logs`
- Endpoint(s): Internal calculation / `GET /api/v1/fuel`

**Acceptance criteria (testable)**
- WHEN two consecutive full-tank fuel logs are created THE SYSTEM SHALL calculate `distance / liters` and store the result in `calculated_efficiency`.

**Estimate:** M  
**Depends on:** UC-046  

---

### UC-048: View Fuel History & Efficiency Trends

**Linked story:** FS-FUEL-003  
**Actor(s):** User  
**Trigger:** User opens Fuel tab (SCR-FUEL-001).  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. App queries `GET /api/v1/fuel?vehicle_id={id}&page=1`.
2. Backend returns paginated list of fuel logs and efficiency trend metrics.
3. Flutter client renders fuel consumption chart (km/L over time, cost per month).
4. User taps log card to view detail or receipt image.

**Alternate flows**
- **A1 — All Fleet Aggregate:** Manager views aggregated fuel consumption across all fleet vehicles.

**Edge cases & error handling**
- [ ] No fuel records → Display empty state graphic.

**Postconditions**
- Fuel log list and trend charts rendered.

**Data & API touchpoints**
- Entities touched: `fuel_logs`, `vehicles`
- Endpoint(s): `GET /api/v1/fuel`

**Acceptance criteria (testable)**
- WHEN fuel history is fetched THE SYSTEM SHALL return entries ordered by `fill_date DESC` alongside fleet aggregate average efficiency.

**Estimate:** S  
**Depends on:** UC-046  

---

### UC-049: Fuel Receipt OCR Auto-Fill (Pro)

**Linked story:** FS-FUEL-004  
**Actor(s):** Pro Tier User  
**Trigger:** User taps "Scan Receipt" on fuel entry form.  

**Preconditions**
- [ ] Camera permission granted. Pro tier account.

**Main flow**
1. User captures photo of fuel station receipt.
2. App sends image to `POST /api/v1/fuel/ocr-scan` (multipart).
3. Backend processes image using OCR engine (Cloud Vision / Tesseract).
4. Backend extracts `total_cost`, `liters`, `date`, and `fuel_station_name`.
5. API returns extracted fields JSON.
6. App auto-fills form fields for user review and confirmation.

**Alternate flows**
- **A1 — Low OCR Confidence:** Extracted fields highlighted in yellow on form for user verification.

**Edge cases & error handling**
- [ ] Unreadable image → API returns `HTTP 422` ("Could not extract receipt data. Please enter manually.").

**Postconditions**
- Form auto-filled from scanned receipt data.

**Data & API touchpoints**
- Entities touched: `fuel_logs`
- Endpoint(s): `POST /api/v1/fuel/ocr-scan`

**Acceptance criteria (testable)**
- WHEN a receipt image is submitted to OCR THE SYSTEM SHALL return extracted cost, volume, and date fields with confidence scores.

**Estimate:** L  
**Depends on:** UC-046, UC-080  

---

### UC-050: Detect Fuel Anomaly & Theft Alerts

**Linked story:** FS-FUEL-005  
**Actor(s):** System / Fleet Manager  
**Trigger:** New fuel log saved with abnormal parameters.  

**Preconditions**
- [ ] Vehicle fuel tank capacity defined in specs.

**Main flow**
1. System checks: Is `logged_liters > vehicle_specs.fuel_tank_capacity`?
2. System checks: Is `calculated_efficiency < baseline_efficiency * 0.70`?
3. System checks: Did vehicle location mismatch gas station GPS location by > 5km? (If GPS attached).
4. If any rule triggers, system flags log with `anomaly_detected = true` and logs anomaly reason.
5. System sends FCM alert to Fleet Manager: `"Fuel Anomaly Detected for Vehicle [Plate]: Volume exceeds tank capacity."`

**Alternate flows**
- **A1 — False Alarm Resolution:** Manager opens alert and taps "Mark Verified" → Clears anomaly flag.

**Edge cases & error handling**
- [ ] Vehicle tank capacity undefined → Mismatch check skipped.

**Postconditions**
- Anomaly flag set and alert dispatched.

**Data & API touchpoints**
- Entities touched: `fuel_logs`, `vehicles`, `notifications`
- Endpoint(s): `POST /api/v1/fuel`, `GET /api/v1/fuel/anomalies`

**Acceptance criteria (testable)**
- WHEN logged fuel volume exceeds tank capacity THE SYSTEM SHALL flag `anomaly_detected = true` and notify the organization admin.

**Estimate:** M  
**Depends on:** UC-046, UC-072  

---

### UC-051: Soft Delete & Edit Fuel Log Entry

**Linked story:** FS-FUEL-006  
**Actor(s):** Driver / Manager  
**Trigger:** User edits or deletes a fuel entry.  

**Preconditions**
- [ ] User created entry or has admin role.

**Main flow**
1. User taps "Delete Log" on SCR-FUEL-003.
2. App sends `DELETE /api/v1/fuel/{fuel_log_id}`.
3. Backend sets `deleted_at = NOW()` on `fuel_logs` record and linked expense record.
4. Backend triggers re-calculation of subsequent fuel log efficiency scores.
5. API returns `HTTP 200 OK`.

**Alternate flows**
- **A1 — Edit Entry:** `PATCH /api/v1/fuel/{fuel_log_id}` updates cost/liters and re-evaluates efficiency.

**Edge cases & error handling**
- [ ] Deleting non-existent log → Returns `HTTP 404`.

**Postconditions**
- Fuel log soft-deleted and subsequent efficiency chain recalculated.

**Data & API touchpoints**
- Entities touched: `fuel_logs`, `expenses`, `audit_logs`
- Endpoint(s): `DELETE /api/v1/fuel/{fuel_log_id}`, `PATCH /api/v1/fuel/{fuel_log_id}`

**Acceptance criteria (testable)**
- WHEN a fuel log is deleted THE SYSTEM SHALL soft-delete the entry and recalculate efficiency metrics for adjacent logs.

**Estimate:** S  
**Depends on:** UC-046  

---

## 6. EP-TRIP — Trip Logging

### UC-052: Start & Stop GPS Trip Tracking

**Linked story:** FS-TRIP-001  
**Actor(s):** Driver  
**Trigger:** Driver taps "Start Trip" button on SCR-TRIP-002.  

**Preconditions**
- [ ] Location permission granted (`ALWAYS` or `WHILE_IN_USE`).

**Main flow**
1. Driver selects vehicle and trip purpose (`BUSINESS`, `PERSONAL`).
2. Driver taps "Start Trip". App records starting GPS coordinate, timestamp, and starting odometer.
3. Background Flutter location service tracks polyline GPS points every 10 seconds.
4. Driver reaches destination and taps "Stop Trip".
5. App calculates total GPS distance and requests end odometer.
6. Client posts trip payload to `POST /api/v1/trips`.
7. Backend creates `trips` record and updates vehicle odometer.

**Alternate flows**
- **A1 — Manual Trip Logging:** Driver manually enters start location, end location, start odometer, and end odometer without live GPS tracking (UC-053).

**Edge cases & error handling**
- [ ] Location permission revoked mid-trip → App prompts for manual end odometer entry.

**Postconditions**
- GPS trip record saved; vehicle odometer updated.

**Data & API touchpoints**
- Entities touched: `trips`, `vehicles`
- Endpoint(s): `POST /api/v1/trips`

**Acceptance criteria (testable)**
- WHEN a GPS trip is stopped THE SYSTEM SHALL save the polyline JSON data, calculate total distance, and record the trip.

**Estimate:** L  
**Depends on:** UC-026  

---

### UC-053: Manual Trip Entry Recording

**Linked story:** FS-TRIP-002  
**Actor(s):** Driver / Manager  
**Trigger:** User submits manual trip log form on SCR-TRIP-003.  

**Preconditions**
- [ ] Vehicle active.

**Main flow**
1. User enters start date/time, end date/time, origin name, destination name, start odometer, end odometer, category (`BUSINESS`/`PERSONAL`), and notes.
2. Client generates local UUID v4 `trip_id`.
3. App calls `POST /api/v1/trips`.
4. Backend verifies `end_odometer > start_odometer`.
5. Backend computes `distance = end_odometer - start_odometer`.
6. Backend creates `trips` record with `is_manual = true`.
7. API returns Trip DTO.

**Alternate flows**
- **A1 — Ad-Rewarded Vehicle Log:** If vehicle is ad-rewarded (Free tier), Flutter requires ad playback completion signature prior to submission (UC-122).

**Edge cases & error handling**
- [ ] `end_odometer <= start_odometer` → API returns `HTTP 422 Unprocessable Entity`.

**Postconditions**
- Manual trip log stored.

**Data & API touchpoints**
- Entities touched: `trips`, `vehicles`
- Endpoint(s): `POST /api/v1/trips`

**Acceptance criteria (testable)**
- WHEN a manual trip is submitted THE SYSTEM SHALL verify `end_odometer > start_odometer` and store the computed distance.

**Estimate:** S  
**Depends on:** UC-052  

---

### UC-054: Classify Business vs Personal Trips & Tax Deduction Calculation

**Linked story:** FS-TRIP-003  
**Actor(s):** Driver / Fleet Manager  
**Trigger:** User toggles trip category or updates tax deduction rate.  

**Preconditions**
- [ ] Trip log exists.

**Main flow**
1. User opens unclassified trip card.
2. User swipes right for `BUSINESS` or left for `PERSONAL`.
3. App updates trip via `PATCH /api/v1/trips/{trip_id}` with `{ category: "BUSINESS" }`.
4. Backend computes estimated tax deduction: `tax_deduction = distance * org_tax_rate_per_km` (e.g. $0.65/km).
5. API returns updated Trip DTO.

**Alternate flows**
- **A1 — Bulk Classification:** User selects 10 trips and clicks "Mark as Business" → `PATCH /api/v1/trips/bulk-classify`.

**Edge cases & error handling**
- [ ] Invalid category code → API returns `HTTP 400 Bad Request`.

**Postconditions**
- Trip classified; tax deduction metric attached.

**Data & API touchpoints**
- Entities touched: `trips`, `organizations`
- Endpoint(s): `PATCH /api/v1/trips/{trip_id}`, `PATCH /api/v1/trips/bulk-classify`

**Acceptance criteria (testable)**
- WHEN a trip is classified as `BUSINESS` THE SYSTEM SHALL calculate `distance * tax_rate_per_km` and store the tax deduction value.

**Estimate:** S  
**Depends on:** UC-052  

---

### UC-055: View Trip Directory & Route Map

**Linked story:** FS-TRIP-004  
**Actor(s):** User  
**Trigger:** User navigates to Trips tab (SCR-TRIP-001).  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. App queries `GET /api/v1/trips?vehicle_id={id}&category={cat}&page=1`.
2. Backend returns paginated list of trip logs.
3. User selects a trip item.
4. App renders map detail view with GPS polyline overlay (for automated GPS trips) or straight route line between origin/destination (for manual trips).

**Alternate flows**
- **A1 — Filter by Driver:** Fleet Manager filters trips by specific driver ID.

**Edge cases & error handling**
- [ ] Missing polyline data → Map displays pin markers at origin and destination only.

**Postconditions**
- Trip list and map visualizer rendered.

**Data & API touchpoints**
- Entities touched: `trips`, `vehicles`, `users`
- Endpoint(s): `GET /api/v1/trips`

**Acceptance criteria (testable)**
- WHEN trip history is fetched THE SYSTEM SHALL return paginated logs containing polyline coordinates for GPS tracked trips.

**Estimate:** M  
**Depends on:** UC-052  

---

### UC-056: Export Trip Log Reports for Tax Compliance (Pro)

**Linked story:** FS-TRIP-005  
**Actor(s):** Pro Tier User / Accountant  
**Trigger:** User taps "Export Tax Log" on Trips screen.  

**Preconditions**
- [ ] Active Pro subscription.

**Main flow**
1. User selects date range (e.g. Tax Year 2025) and format (`PDF` or `CSV`).
2. App calls `POST /api/v1/trips/export` with `{ start_date, end_date, format }`.
3. Backend generates tax-compliant log report containing vehicle info, total business km, total personal km, itemized trip table, and total tax deduction.
4. API returns download URL / streams PDF binary.

**Alternate flows**
- **A1 — Free Tier Access Attempt:** Blocked by Quota Wall (UC-022).

**Edge cases & error handling**
- [ ] No trips in date range → Returns `HTTP 400` ("No trip records found for specified date range").

**Postconditions**
- Compliant tax report generated and delivered.

**Data & API touchpoints**
- Entities touched: `trips`, `vehicles`, `organizations`
- Endpoint(s): `POST /api/v1/trips/export`

**Acceptance criteria (testable)**
- WHEN a Pro user requests a trip export THE SYSTEM SHALL generate a PDF/CSV report summarizing total business distance and tax deductions.

**Estimate:** M  
**Depends on:** UC-054, UC-080  

---

### UC-057: Soft Delete & Edit Trip Log Entry

**Linked story:** FS-TRIP-006  
**Actor(s):** Driver / Manager  
**Trigger:** User edits or deletes a trip record.  

**Preconditions**
- [ ] User created entry or has admin permissions.

**Main flow**
1. User taps "Delete Trip" on trip detail card.
2. App calls `DELETE /api/v1/trips/{trip_id}`.
3. Backend sets `deleted_at = NOW()` on `trips` row.
4. API returns `HTTP 200 OK`.

**Alternate flows**
- **A1 — Edit Notes/Category:** `PATCH /api/v1/trips/{trip_id}` updates notes or classification.

**Edge cases & error handling**
- [ ] Deleting non-existent trip → Returns `HTTP 404`.

**Postconditions**
- Trip soft-deleted.

**Data & API touchpoints**
- Entities touched: `trips`, `audit_logs`
- Endpoint(s): `DELETE /api/v1/trips/{trip_id}`

**Acceptance criteria (testable)**
- WHEN a trip is deleted THE SYSTEM SHALL set `deleted_at = NOW()` and exclude the trip from business mileage totals.

**Estimate:** S  
**Depends on:** UC-052  

---

## 7. EP-EXP — Expense Recording

### UC-058: Log General Fleet Expense

**Linked story:** FS-EXP-001  
**Actor(s):** Driver / Fleet Manager  
**Trigger:** User submits expense form on SCR-EXP-002.  

**Preconditions**
- [ ] Vehicle selected.

**Main flow**
1. User selects vehicle, expense category (`TOLL`, `PARKING`, `INSURANCE`, `PERMIT`, `WASH`, `MISC`), amount, date, payment method, vendor name, and notes.
2. User attaches photo of receipt.
3. Client generates local UUID v4 `expense_id`.
4. App calls `POST /api/v1/expenses`.
5. Backend creates `expenses` record with `organization_id` and `sharding_key`.
6. API returns Expense DTO.

**Alternate flows**
- **A1 — Ad-Rewarded Vehicle Log:** If vehicle is ad-rewarded (Free tier), Flutter requires ad playback completion signature prior to submission (UC-122).

**Edge cases & error handling**
- [ ] Amount <= 0 → Client/API validation rejects with `HTTP 422`.

**Postconditions**
- Expense record created.

**Data & API touchpoints**
- Entities touched: `expenses`, `vehicles`, `organizations`
- Endpoint(s): `POST /api/v1/expenses`

**Acceptance criteria (testable)**
- WHEN an expense entry is saved THE SYSTEM SHALL store the expense record with its category, amount, and linked vehicle ID.

**Estimate:** S  
**Depends on:** UC-026  

---

### UC-059: Categorize Expenses & Recurring Bills Setup

**Linked story:** FS-EXP-002  
**Actor(s):** Fleet Manager  
**Trigger:** Manager configures recurring expense (e.g. Monthly Vehicle Insurance $150).  

**Preconditions**
- [ ] Manager permissions.

**Main flow**
1. Manager enters title, category, amount, vehicle, frequency (`MONTHLY`, `ANNUALLY`), and start date on SCR-EXP-004.
2. App calls `POST /api/v1/expenses/recurring`.
3. Backend creates `recurring_expenses` record.
4. Background cron job automatically generates matching expense log entries on due dates.

**Alternate flows**
- **A1 — Stop Recurring Expense:** Manager toggles `is_active = false` → Stops future automatic expense log generation.

**Edge cases & error handling**
- [ ] Invalid frequency code → API returns `HTTP 400 Bad Request`.

**Postconditions**
- Recurring expense schedule active.

**Data & API touchpoints**
- Entities touched: `recurring_expenses`, `expenses`
- Endpoint(s): `POST /api/v1/expenses/recurring`

**Acceptance criteria (testable)**
- WHEN a recurring expense is active THE SYSTEM SHALL auto-generate an `expenses` record on each recurring billing date.

**Estimate:** M  
**Depends on:** UC-058  

---

### UC-060: Attach & Preview Expense Receipts

**Linked story:** FS-EXP-003  
**Actor(s):** User  
**Trigger:** User uploads receipt image during or after expense logging.  

**Preconditions**
- [ ] Expense record exists.

**Main flow**
1. User attaches receipt image (JPEG/PNG/PDF).
2. App sends file to `POST /api/v1/expenses/{expense_id}/attachments` (multipart).
3. Backend uploads file to object store and stores URL in `receipt_url` field of `expenses`.
4. API returns updated Expense DTO with public/presigned thumbnail URL.

**Alternate flows**
- **A1 — Delete Attachment:** User removes file → Backend removes object from cloud storage and sets `receipt_url = NULL`.

**Edge cases & error handling**
- [ ] Exceeds 10MB → Returns `HTTP 413 Payload Too Large`.

**Postconditions**
- Receipt file linked to expense.

**Data & API touchpoints**
- Entities touched: `expenses`
- Endpoint(s): `POST /api/v1/expenses/{expense_id}/attachments`

**Acceptance criteria (testable)**
- WHEN a receipt file is uploaded THE SYSTEM SHALL store the file and update `receipt_url` on the expense record.

**Estimate:** S  
**Depends on:** UC-058  

---

### UC-061: View Expense Ledger & Filter Directory

**Linked story:** FS-EXP-004  
**Actor(s):** User / Accountant  
**Trigger:** User opens Expenses tab (SCR-EXP-001).  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. App queries `GET /api/v1/expenses?category={cat}&vehicle_id={id}&start_date={s}&end_date={e}&page=1`.
2. Backend returns paginated expense list along with category summary totals.
3. App displays expense table with category color badges and receipt icon indicators.

**Alternate flows**
- **A1 — Filter by Payment Method:** User filters by cash, corporate credit card, or driver reimbursement.

**Edge cases & error handling**
- [ ] Date range invalid (start > end) → API returns `HTTP 400 Bad Request`.

**Postconditions**
- Expense directory rendered.

**Data & API touchpoints**
- Entities touched: `expenses`, `vehicles`
- Endpoint(s): `GET /api/v1/expenses`

**Acceptance criteria (testable)**
- WHEN expenses are queried with date filters THE SYSTEM SHALL return paginated records and category sum totals for that range.

**Estimate:** S  
**Depends on:** UC-058  

---

### UC-062: Driver Expense Reimbursement Workflow

**Linked story:** FS-EXP-005  
**Actor(s):** Driver / Fleet Manager  
**Trigger:** Driver submits out-of-pocket expense for manager reimbursement.  

**Preconditions**
- [ ] Driver logged expense with `is_reimbursable = true`.

**Main flow**
1. Driver logs expense and checks "Requires Reimbursement".
2. Expense is created with status `REIMBURSEMENT_PENDING`.
3. Fleet Manager opens Reimbursement Dashboard (SCR-EXP-005).
4. Manager reviews receipt and clicks "Approve & Mark Paid".
5. App calls `POST /api/v1/expenses/{expense_id}/reimburse`.
6. Backend updates expense status to `REIMBURSED` and records `reimbursed_at` timestamp.
7. Push notification sent to driver: `"Reimbursement of $45.00 Approved."`

**Alternate flows**
- **A1 — Reject Reimbursement:** Manager clicks "Reject" with reason note → Status updated to `REIMBURSEMENT_REJECTED`.

**Edge cases & error handling**
- [ ] Driver attempts to approve own reimbursement → API blocks with `HTTP 403 Forbidden`.

**Postconditions**
- Expense reimbursement lifecycle updated.

**Data & API touchpoints**
- Entities touched: `expenses`, `users`, `notifications`
- Endpoint(s): `POST /api/v1/expenses/{expense_id}/reimburse`

**Acceptance criteria (testable)**
- WHEN a manager approves a reimbursement THE SYSTEM SHALL update status to `REIMBURSED` and notify the requesting driver.

**Estimate:** M  
**Depends on:** UC-058, UC-072  

---

### UC-063: Soft Delete & Edit Expense Entry

**Linked story:** FS-EXP-006  
**Actor(s):** User  
**Trigger:** User edits or deletes an expense.  

**Preconditions**
- [ ] User permissions verified.

**Main flow**
1. User taps "Delete Expense" on expense detail view.
2. App sends `DELETE /api/v1/expenses/{expense_id}`.
3. Backend sets `deleted_at = NOW()` on target `expenses` row.
4. API returns `HTTP 200 OK`.

**Alternate flows**
- **A1 — Edit Expense:** `PATCH /api/v1/expenses/{expense_id}` updates category, amount, or notes.

**Edge cases & error handling**
- [ ] Deleting auto-generated maintenance expense → System prompts warning that source maintenance log remains.

**Postconditions**
- Expense soft-deleted.

**Data & API touchpoints**
- Entities touched: `expenses`, `audit_logs`
- Endpoint(s): `DELETE /api/v1/expenses/{expense_id}`

**Acceptance criteria (testable)**
- WHEN an expense is deleted THE SYSTEM SHALL set `deleted_at = NOW()` and exclude it from financial totals.

**Estimate:** S  
**Depends on:** UC-058  

---

## 8. EP-DASH — Dashboards

### UC-064: Overview Fleet Dashboard KPI Metrics Render

**Linked story:** FS-DASH-001  
**Actor(s):** User (Consumer / Fleet Manager)  
**Trigger:** User opens app home tab (SCR-DASH-001).  

**Preconditions**
- [ ] User authenticated with active organization context.

**Main flow**
1. App calls `GET /api/v1/dashboard/summary`.
2. Backend queries active tenant data and computes KPI metrics:
   - Total Active Vehicles & Drivers
   - Monthly Total Expenditure (Fuel + Maintenance + Expenses)
   - Upcoming & Overdue Maintenance Count
   - Fleet Average Fuel Efficiency (km/L)
3. API returns Dashboard Summary DTO.
4. Flutter client renders metric cards with month-over-month trend indicators.

**Alternate flows**
- **A1 — Consumer View:** Personal organization hides multi-driver metrics and focuses on single/multi-vehicle cost cards.

**Edge cases & error handling**
- [ ] Tenant has 0 vehicles → Renders onboarding setup cards ("Add your first vehicle to unlock insights").

**Postconditions**
- High-level KPI metrics displayed.

**Data & API touchpoints**
- Entities touched: `vehicles`, `drivers`, `fuel_logs`, `maintenance_logs`, `expenses`
- Endpoint(s): `GET /api/v1/dashboard/summary`

**Acceptance criteria (testable)**
- WHEN the dashboard summary API is called THE SYSTEM SHALL return aggregated active vehicle counts, total monthly costs, and overdue maintenance counts in under 300ms.

**Estimate:** M  
**Depends on:** UC-015, UC-026  

---

### UC-065: Cost Breakdown Chart (Fuel vs Maintenance vs Expenses)

**Linked story:** FS-DASH-002  
**Actor(s):** User  
**Trigger:** User views Cost Analytics card on Dashboard.  

**Preconditions**
- [ ] Dashboard active.

**Main flow**
1. App queries `GET /api/v1/dashboard/cost-breakdown?timeframe=6m`.
2. Backend aggregates monthly totals grouped by category (`FUEL`, `MAINTENANCE`, `OTHER_EXPENSES`) for past 6 months.
3. API returns TimeSeries Chart DTO.
4. Flutter client renders interactive stacked bar/donut chart.

**Alternate flows**
- **A1 — Filter by Vehicle:** User selects specific vehicle from dropdown → Chart filters to single vehicle breakdown.

**Edge cases & error handling**
- [ ] No data for timeframe → Returns empty array with zeroes for months.

**Postconditions**
- Financial cost chart rendered.

**Data & API touchpoints**
- Entities touched: `fuel_logs`, `maintenance_logs`, `expenses`
- Endpoint(s): `GET /api/v1/dashboard/cost-breakdown`

**Acceptance criteria (testable)**
- WHEN cost breakdown is requested THE SYSTEM SHALL group costs by month and category for the specified timeframe.

**Estimate:** M  
**Depends on:** UC-064  

---

### UC-066: Fuel Efficiency Leaderboard & Trends

**Linked story:** FS-DASH-003  
**Actor(s):** Fleet Manager  
**Trigger:** Manager taps "Efficiency Leaderboard" card.  

**Preconditions**
- [ ] > 1 vehicle with fuel logs.

**Main flow**
1. App calls `GET /api/v1/dashboard/fuel-leaderboard`.
2. Backend ranks fleet vehicles by calculated fuel efficiency (km/L) over last 30 days.
3. API returns ranked vehicle list DTO with efficiency figures.
4. Client displays ranked list (Top Performers green, Lowest Efficiency orange/red).

**Alternate flows**
- **A1 — Single Vehicle Tenant:** Card displays single vehicle efficiency compared to standard manufacturer baseline.

**Edge cases & error handling**
- [ ] Insufficient fuel logs → Displays message "Need at least 2 full tank logs to rank vehicles."

**Postconditions**
- Efficiency leaderboard rendered.

**Data & API touchpoints**
- Entities touched: `vehicles`, `fuel_logs`
- Endpoint(s): `GET /api/v1/dashboard/fuel-leaderboard`

**Acceptance criteria (testable)**
- WHEN fuel leaderboard is requested THE SYSTEM SHALL return vehicles sorted by `calculated_efficiency DESC`.

**Estimate:** S  
**Depends on:** UC-047, UC-064  

---

### UC-067: Maintenance Due & Alert Summary Widget

**Linked story:** FS-DASH-004  
**Actor(s):** User  
**Trigger:** User checks Maintenance Widget on Dashboard.  

**Preconditions**
- [ ] Dashboard active.

**Main flow**
1. App queries `GET /api/v1/dashboard/maintenance-alerts`.
2. Backend fetches all `DUE` and `OVERDUE` schedules and expiring vehicle documents for current organization.
3. API returns Alert List DTO ordered by severity (`OVERDUE` first).
4. Client renders quick-action list (tapping item opens resolution modal).

**Alternate flows**
- **A1 — Zero Alerts:** Displays green checkmark graphic ("All fleet maintenance is up to date").

**Edge cases & error handling**
- [ ] Offline status → Reads cached alerts from Hive.

**Postconditions**
- Maintenance alerts displayed.

**Data & API touchpoints**
- Entities touched: `maintenance_schedules`, `vehicle_documents`
- Endpoint(s): `GET /api/v1/dashboard/maintenance-alerts`

**Acceptance criteria (testable)**
- WHEN maintenance alerts are fetched THE SYSTEM SHALL prioritize `OVERDUE` items ahead of `DUE` items in the response list.

**Estimate:** S  
**Depends on:** UC-036, UC-064  

---

### UC-068: Recent Activity Feed Widget

**Linked story:** FS-DASH-005  
**Actor(s):** User  
**Trigger:** User scrolls to Activity Feed section.  

**Preconditions**
- [ ] Dashboard active.

**Main flow**
1. App queries `GET /api/v1/dashboard/activity?limit=10`.
2. Backend fetches combined recent entries from `fuel_logs`, `maintenance_logs`, `trips`, and `expenses` ordered by timestamp.
3. API returns unified Activity Feed DTO.
4. Client renders chronological activity stream with actor names and action icons.

**Alternate flows**
- **A1 — Filter by My Activity:** Driver views only own logged activities.

**Edge cases & error handling**
- [ ] Empty feed → Displays "No recent activity."

**Postconditions**
- Activity stream displayed.

**Data & API touchpoints**
- Entities touched: `fuel_logs`, `maintenance_logs`, `trips`, `expenses`, `users`
- Endpoint(s): `GET /api/v1/dashboard/activity`

**Acceptance criteria (testable)**
- WHEN activity feed is requested THE SYSTEM SHALL combine recent logs across fuel, maintenance, trips, and expenses in descending chronological order.

**Estimate:** M  
**Depends on:** UC-064  

---

### UC-069: Driver Performance Overview Card

**Linked story:** FS-DASH-006  
**Actor(s):** Fleet Manager  
**Trigger:** Manager views Driver Score summary card on Dashboard.  

**Preconditions**
- [ ] Driver scoring module active (EP-DRV).

**Main flow**
1. App calls `GET /api/v1/dashboard/driver-scores`.
2. Backend computes organization average driver score and returns top/bottom drivers.
3. API returns Driver Performance DTO.
4. Client renders score gauge and driver ranking cards.

**Alternate flows**
- **A1 — Free Tier User:** Card displays locked state with "Upgrade to Pro for Driver Scoring" (UC-080).

**Edge cases & error handling**
- [ ] 0 drivers in organization → Card hidden.

**Postconditions**
- Driver performance card rendered.

**Data & API touchpoints**
- Entities touched: `driver_scores`, `users`
- Endpoint(s): `GET /api/v1/dashboard/driver-scores`

**Acceptance criteria (testable)**
- WHEN a Free tier organization views driver scores THE SYSTEM SHALL return `HTTP 402` or locked state metadata.

**Estimate:** S  
**Depends on:** UC-103  

---

### UC-070: Customizable Dashboard Layout & Widget Toggle

**Linked story:** FS-DASH-007  
**Actor(s):** User  
**Trigger:** User taps "Customize Dashboard" in settings.  

**Preconditions**
- [ ] User on dashboard screen.

**Main flow**
1. User toggles visibility or re-orders widgets (Cost Chart, Maintenance Alerts, Leaderboard, Recent Activity).
2. App saves layout preferences to local storage / `users.preferences` JSON field via `PATCH /api/v1/users/me/preferences`.
3. App re-renders dashboard grid according to saved configuration.

**Alternate flows**
- **A1 — Reset Layout:** Tapping "Reset to Default" restores standard layout arrangement.

**Edge cases & error handling**
- [ ] Preferences write fails → Falls back to local storage preference copy.

**Postconditions**
- User dashboard layout preference persisted.

**Data & API touchpoints**
- Entities touched: `users`
- Endpoint(s): `PATCH /api/v1/users/me/preferences`

**Acceptance criteria (testable)**
- WHEN layout preferences are updated THE SYSTEM SHALL persist the JSON configuration in `users.preferences`.

**Estimate:** S  
**Depends on:** UC-064  

---

### UC-071: Multi-Vehicle Fleet Comparison Matrix

**Linked story:** FS-DASH-008  
**Actor(s):** Fleet Manager  
**Trigger:** Manager opens "Fleet Comparison" on Dashboard analytics.  

**Preconditions**
- [ ] Organization has >= 2 active vehicles.

**Main flow**
1. App calls `GET /api/v1/dashboard/fleet-comparison?metric=total_cost`.
2. Backend returns side-by-side comparative table of all vehicles (Total Cost, Fuel Efficiency, Maintenance Downtime, Distance Traveled).
3. API returns Matrix DTO.
4. Client renders comparative table grid with sorting columns.

**Alternate flows**
- **A1 — Export Matrix:** Manager exports comparison matrix as CSV/PDF (UC-110).

**Edge cases & error handling**
- [ ] 1 vehicle fleet → Displays message "Add more vehicles to compare fleet performance."

**Postconditions**
- Fleet comparison matrix rendered.

**Data & API touchpoints**
- Entities touched: `vehicles`, `fuel_logs`, `maintenance_logs`, `expenses`
- Endpoint(s): `GET /api/v1/dashboard/fleet-comparison`

**Acceptance criteria (testable)**
- WHEN fleet comparison is requested THE SYSTEM SHALL calculate comparative metrics across all active vehicles in the tenant.

**Estimate:** M  
**Depends on:** UC-064  

---

## 9. EP-NOTIF — Notifications

### UC-072: Register FCM Device Push Token

**Linked story:** FS-NOTIF-001  
**Actor(s):** Client App / User  
**Trigger:** User logs in or launches app on mobile device.  

**Preconditions**
- [ ] Firebase Cloud Messaging (FCM) initialized on Flutter client.

**Main flow**
1. Flutter client obtains FCM Device Token from Firebase SDK.
2. App sends token to `POST /api/v1/notifications/devices` with `{ token: "fcm_token_str", device_type: "ANDROID" }`.
3. Backend checks if token exists for `user_id`. If not, inserts record into `user_devices`.
4. API returns `HTTP 200 OK`.

**Alternate flows**
- **A1 — Token Renewal:** Firebase issues new token → App updates existing record for device.

**Edge cases & error handling**
- [ ] Notification permission denied by user OS → FCM token registration skipped silently.

**Postconditions**
- FCM token stored for targeted push notifications.

**Data & API touchpoints**
- Entities touched: `user_devices`, `users`
- Endpoint(s): `POST /api/v1/notifications/devices`

**Acceptance criteria (testable)**
- WHEN an FCM token is registered THE SYSTEM SHALL insert or update the token record in `user_devices` for the authenticated user.

**Estimate:** S  
**Depends on:** UC-004  

---

### UC-073: In-App Notification Center Directory & Unread Counter

**Linked story:** FS-NOTIF-002  
**Actor(s):** User  
**Trigger:** User taps bell icon in header (SCR-NOTIF-001).  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. App queries `GET /api/v1/notifications?unread_only=false&page=1`.
2. Backend fetches notifications for user and active organization.
3. Backend calculates total unread count (`SELECT COUNT(*) WHERE is_read = false`).
4. API returns Notification List DTO with `unread_count`.
5. Client displays badge counter on bell icon and renders notification list.

**Alternate flows**
- **A1 — Mark All as Read:** User taps "Mark All Read" → `POST /api/v1/notifications/mark-all-read`.

**Edge cases & error handling**
- [ ] No notifications → Displays empty inbox screen.

**Postconditions**
- Notification inbox rendered.

**Data & API touchpoints**
- Entities touched: `notifications`
- Endpoint(s): `GET /api/v1/notifications`, `POST /api/v1/notifications/mark-all-read`

**Acceptance criteria (testable)**
- WHEN fetching notifications THE SYSTEM SHALL return the list alongside the accurate count of unread items.

**Estimate:** S  
**Depends on:** UC-072  

---

### UC-074: Mark Notification as Read / Deep Link Routing

**Linked story:** FS-NOTIF-003  
**Actor(s):** User  
**Trigger:** User taps an individual notification item.  

**Preconditions**
- [ ] Notification item exists in inbox.

**Main flow**
1. App calls `PATCH /api/v1/notifications/{notification_id}/read`.
2. Backend sets `is_read = true` and `read_at = NOW()`.
3. App decrements unread counter badge.
4. App handles `action_url` deep link (e.g. opens target Vehicle, Maintenance Log, or Invitation screen).

**Alternate flows**
- **A1 — Push Notification Click:** Clicking push notification from OS tray triggers same deep link router and marks notification read.

**Edge cases & error handling**
- [ ] Notification belongs to another user → Returns `HTTP 403 Forbidden`.

**Postconditions**
- Notification status set to read; user navigated to target screen.

**Data & API touchpoints**
- Entities touched: `notifications`
- Endpoint(s): `PATCH /api/v1/notifications/{notification_id}/read`

**Acceptance criteria (testable)**
- WHEN a notification is tapped THE SYSTEM SHALL mark `is_read = true` and return the deep link target payload.

**Estimate:** S  
**Depends on:** UC-073  

---

### UC-075: Configure Notification Channel Preferences

**Linked story:** FS-NOTIF-004  
**Actor(s):** User  
**Trigger:** User toggles notification switches on SCR-NOTIF-002.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. User toggles push/email preferences for specific event types (Maintenance Reminders, Document Expirations, Quota Alerts, System News).
2. App sends payload to `PATCH /api/v1/users/me/notification-preferences`.
3. Backend updates `notification_preferences` JSONB column on `users` table.
4. API returns updated preferences DTO.

**Alternate flows**
- **A1 — Master Mute Toggle:** Toggling "Disable All Push Notifications" sets master flag.

**Edge cases & error handling**
- [ ] Invalid JSON structure → Returns `HTTP 422`.

**Postconditions**
- User notification rules persisted.

**Data & API touchpoints**
- Entities touched: `users`
- Endpoint(s): `PATCH /api/v1/users/me/notification-preferences`

**Acceptance criteria (testable)**
- WHEN notification preferences are updated THE SYSTEM SHALL persist the JSON configuration and respect the settings during alert dispatch.

**Estimate:** S  
**Depends on:** UC-072  

---

### UC-076: Scheduled Vehicle Document Expiration Alerts

**Linked story:** FS-NOTIF-005  
**Actor(s):** System Cron / Worker  
**Trigger:** Nightly document expiration check cron job executes.  

**Preconditions**
- [ ] Active vehicle documents with expiration dates exist.

**Main flow**
1. Cron worker queries `vehicle_documents` where `expiration_date` is in 30 days, 7 days, or 1 day.
2. Worker checks user notification preferences for organization managers.
3. Worker creates notification records and dispatches FCM push / email alerts: `"Document Expiring: Insurance for Vehicle [Plate] expires in 7 days."`

**Alternate flows**
- **A1 — Expired Document:** Document date < today → Alert sent with `SEVERITY = HIGH` ("Document EXPIRED").

**Edge cases & error handling**
- [ ] Duplicate alerts prevented by checking `last_alert_sent_at` on document row.

**Postconditions**
- Document expiration notifications delivered.

**Data & API touchpoints**
- Entities touched: `vehicle_documents`, `notifications`, `user_devices`
- Endpoint(s): Background job

**Acceptance criteria (testable)**
- WHEN a vehicle document is 7 days from expiring THE SYSTEM SHALL queue a push notification to all organization admins.

**Estimate:** M  
**Depends on:** UC-031, UC-072  

---

### UC-077: Security & Login Alert Notifications

**Linked story:** FS-NOTIF-006  
**Actor(s):** System  
**Trigger:** Login detected from new IP / device or password reset requested.  

**Preconditions**
- [ ] Security event occurs.

**Main flow**
1. Auth module triggers security alert event.
2. Notification service immediately dispatches high-priority email and FCM push notification to user: `"New Login Detected from Chrome / Windows (IP: 192.168.1.1)"`.
3. Notification recorded in user security activity log.

**Alternate flows**
- **A1 — Recognized Device:** Known FCM device token skips new device security alert.

**Edge cases & error handling**
- [ ] Email delivery failure -> Retried automatically via email worker queue.

**Postconditions**
- Security alert dispatched.

**Data & API touchpoints**
- Entities touched: `notifications`, `audit_logs`
- Endpoint(s): Internal event bus

**Acceptance criteria (testable)**
- WHEN a login occurs from an unrecognized device THE SYSTEM SHALL immediately send a security alert email to the registered address.

**Estimate:** S  
**Depends on:** UC-004, UC-072  

---

### UC-078: Broadcast System Announcement Messages

**Linked story:** FS-NOTIF-007  
**Actor(s):** System Admin  
**Trigger:** System admin dispatches platform-wide announcement.  

**Preconditions**
- [ ] Super-admin privileges.

**Main flow**
1. Admin enters title, message body, target audience (`ALL`, `FREE_TIER`, `PRO_TIER`), and optional action link.
2. Admin submits via `POST /api/v1/admin/announcements`.
3. Backend creates system notification records for all targeted user accounts.
4. FCM background worker dispatches push notifications.

**Alternate flows**
- **A1 — In-App Banner:** Announcement also flags in-app top banner for 48 hours.

**Edge cases & error handling**
- [ ] Blank message body → Returns `HTTP 422`.

**Postconditions**
- Announcement delivered to target users.

**Data & API touchpoints**
- Entities touched: `notifications`, `users`
- Endpoint(s): `POST /api/v1/admin/announcements`

**Acceptance criteria (testable)**
- WHEN a system announcement is broadcast THE SYSTEM SHALL insert notification rows for all active users matching the target tier.

**Estimate:** M  
**Depends on:** UC-072  

---

### UC-079: Clean Up Expired & Stale Notifications

**Linked story:** FS-NOTIF-008  
**Actor(s):** System Cron  
**Trigger:** Weekly database maintenance cron runs.  

**Preconditions**
- [ ] Database operational.

**Main flow**
1. Worker executes cleanup query: `DELETE FROM notifications WHERE created_at < NOW() - INTERVAL '90 days' AND is_read = true`.
2. Worker logs total purged notification count.

**Alternate flows**
- **A1 — Keep Unread High-Priority:** Unread security alerts retained up to 180 days.

**Edge cases & error handling**
- [ ] Transaction lock timeout -> Retried during low-traffic window (03:00 UTC).

**Postconditions**
- Old read notifications purged.

**Data & API touchpoints**
- Entities touched: `notifications`
- Endpoint(s): Background maintenance job

**Acceptance criteria (testable)**
- WHEN the notification cleanup cron executes THE SYSTEM SHALL hard-delete read notification records older than 90 days.

**Estimate:** S  
**Depends on:** UC-073  

---

## 10. EP-PAY — Payments & Subscriptions

### UC-080: Initiate Pro Subscription Checkout (Stripe & Safepay)

**Linked story:** FS-PAY-001  
**Actor(s):** Fleet Owner  
**Trigger:** Owner selects Pro Tier plan and payment gateway on SCR-PAY-002.  

**Preconditions**
- [ ] Actor is organization owner.

**Main flow**
1. Owner selects billing cycle (`MONTHLY`, `ANNUALLY`) and payment provider (`STRIPE` for international credit cards, `SAFEPAY` for Pakistan local cards/wallets).
2. App posts request to `POST /api/v1/payments/checkout-session` with `{ organization_id, gateway: "STRIPE" | "SAFEPAY", billing_cycle }`.
3. Backend creates pending `subscriptions` record and calls selected payment gateway API to create checkout session.
4. API returns checkout session URL / token payload.
5. Mobile app opens WebView / Stripe SDK checkout sheet.

**Alternate flows**
- **A1 — Safepay Gateway Selection:** Backend invokes Safepay API to generate Checkout Tracker URL for PKR transactions.

**Edge cases & error handling**
- [ ] Gateway API Timeout → Backend returns `HTTP 503 Service Unavailable` ("Payment gateway temporarily unreachable. Please try again.").

**Postconditions**
- Checkout session initialized; pending subscription record created.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `organizations`
- Endpoint(s): `POST /api/v1/payments/checkout-session`

**Acceptance criteria (testable)**
- WHEN checkout initiation is requested THE SYSTEM SHALL create a pending `subscriptions` row and return a valid gateway checkout URL.

**Estimate:** L  
**Depends on:** UC-014, UC-121  

---

### UC-081: Stripe Payment Webhook Processing & Entitlement Activation

**Linked story:** FS-PAY-002  
**Actor(s):** Stripe Payment Gateway / System  
**Trigger:** Stripe posts webhook event (`checkout.session.completed`, `invoice.payment_succeeded`) to backend.  

**Preconditions**
- [ ] Webhook endpoint configured on FastAPI backend.

**Main flow**
1. Stripe sends HTTP POST to `POST /api/v1/payments/webhooks/stripe`.
2. Backend verifies Stripe signature header using webhook signing secret.
3. Backend extracts event type, customer ID, subscription ID, and `organization_id` metadata.
4. Backend executes dual gateway reconciliation logic (UC-121):
   - Updates `subscriptions` table: `status = "ACTIVE"`, `gateway = "STRIPE"`, `current_period_end = event.period_end`.
   - Stores raw Stripe event JSON inside `gateway_payload`.
   - Upgrades `organizations.tier = "pro"`, `max_vehicles = 25`, `max_drivers = 15`.
5. Backend logs event in `audit_logs` and sends confirmation email to owner.

**Alternate flows**
- **A1 — Renewal Success:** `invoice.payment_succeeded` extends `current_period_end` date without re-upgrading tier.

**Edge cases & error handling**
- [ ] Invalid Signature → Backend rejects with `HTTP 400 Bad Request` and ignores payload.

**Postconditions**
- Subscription marked active; organization entitlements upgraded to Pro tier.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/payments/webhooks/stripe`

**Acceptance criteria (testable)**
- WHEN a valid `checkout.session.completed` Stripe webhook is received THE SYSTEM SHALL set subscription `status = "ACTIVE"` and update organization tier to `"pro"` in a single transaction.

**Estimate:** L  
**Depends on:** UC-080, UC-121  

---

### UC-082: Safepay Payment Webhook Processing & Entitlement Activation

**Linked story:** FS-PAY-003  
**Actor(s):** Safepay Payment Gateway / System  
**Trigger:** Safepay posts webhook notification (`payment.completed`) to backend.  

**Preconditions**
- [ ] Safepay webhook route configured.

**Main flow**
1. Safepay sends HTTP POST to `POST /api/v1/payments/webhooks/safepay`.
2. Backend verifies Safepay HMAC signature header.
3. Backend extracts tracker ID, payment status (`PAID`), and `organization_id` from metadata.
4. Backend executes dual gateway reconciliation logic (UC-121):
   - Updates `subscriptions` table: `status = "ACTIVE"`, `gateway = "SAFEPAY"`, `current_period_end = NOW() + 30 DAYS`.
   - Preserves raw payload inside `gateway_payload` JSON.
   - Upgrades `organizations.tier = "pro"`, `max_vehicles = 25`, `max_drivers = 15`.
5. API returns `HTTP 200 OK` to Safepay server.

**Alternate flows**
- **A1 — Payment Failed:** Safepay sends `payment.failed` → Subscription status set to `PAST_DUE`; notification sent to user.

**Edge cases & error handling**
- [ ] Signature Mismatch → Returns `HTTP 401 Unauthorized`.

**Postconditions**
- Subscription activated via Safepay; entitlements upgraded.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/payments/webhooks/safepay`

**Acceptance criteria (testable)**
- WHEN a valid Safepay webhook with status `PAID` is received THE SYSTEM SHALL normalize subscription status to `"ACTIVE"` and populate `gateway_payload`.

**Estimate:** L  
**Depends on:** UC-080, UC-121  

---

### UC-083: Handle Subscription Payment Failure & Past Due Grace Period

**Linked story:** FS-PAY-004  
**Actor(s):** Payment Gateway Webhook / System  
**Trigger:** Webhook notifies failed recurring payment (`invoice.payment_failed`).  

**Preconditions**
- [ ] Active subscription exists.

**Main flow**
1. Gateway posts payment failure webhook event.
2. Backend updates `subscriptions.status = "PAST_DUE"`.
3. Backend sets 7-day grace period expiration date (`grace_period_ends_at = NOW() + 7 DAYS`).
4. Organization retains Pro access during grace period.
5. System sends urgent email & FCM push notification to owner: `"Payment Failed for Pro Subscription. Please update payment method to avoid service downgrade."`

**Alternate flows**
- **A1 — Payment Resolved in Grace Period:** User updates card -> Gateway retries and succeeds -> Status restored to `ACTIVE`.

**Edge cases & error handling**
- [ ] Grace Period Expires without payment -> Downgrade protocol executed (UC-085).

**Postconditions**
- Subscription marked PAST_DUE; 7-day grace period timer active.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `organizations`, `notifications`
- Endpoint(s): Webhook endpoints

**Acceptance criteria (testable)**
- WHEN payment fails THE SYSTEM SHALL set subscription status to `PAST_DUE` and grant a 7-day grace period before entitlement revocation.

**Estimate:** M  
**Depends on:** UC-081, UC-082  

---

### UC-084: Cancel Pro Subscription & Downgrade Scheduled Execution

**Linked story:** FS-PAY-005  
**Actor(s):** Fleet Owner  
**Trigger:** Owner selects "Cancel Subscription" on Subscription Settings screen.  

**Preconditions**
- [ ] Active Pro subscription.

**Main flow**
1. Owner submits cancellation feedback modal.
2. App sends `POST /api/v1/payments/cancel-subscription`.
3. Backend calls gateway API (Stripe/Safepay) to cancel subscription at period end (`cancel_at_period_end = true`).
4. Backend updates `subscriptions.cancel_at_period_end = true`.
5. Pro benefits remain active until `current_period_end` date.

**Alternate flows**
- **A1 — Immediate Cancellation:** Admin requests immediate cancellation → Subscription status set to `CANCELED` immediately.

**Edge cases & error handling**
- [ ] Subscription already canceled → Returns `HTTP 400 Bad Request`.

**Postconditions**
- Subscription marked for cancellation at period end.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `audit_logs`
- Endpoint(s): `POST /api/v1/payments/cancel-subscription`

**Acceptance criteria (testable)**
- WHEN a subscription cancellation is requested THE SYSTEM SHALL set `cancel_at_period_end = true` while retaining Pro access until `current_period_end`.

**Estimate:** M  
**Depends on:** UC-080  

---

### UC-085: Pro-to-Free Subscription Downgrade & Bonus Slot Preservation Protocol

**Linked story:** FS-PAY-006  
**Actor(s):** System Cron / Worker  
**Trigger:** `current_period_end` reached for canceled subscription OR grace period expires on `PAST_DUE` subscription.  

**Preconditions**
- [ ] Subscription `current_period_end <= NOW()` AND `cancel_at_period_end == true`.

**Main flow**
1. Cron worker queries subscriptions due for entitlement revocation.
2. Worker updates `subscriptions.status = "CANCELED"`.
3. Worker updates `organizations.tier = "free"`.
4. Worker executes Ad-Rewarded Quota Lifecycle rule (UC-120):
   - Computes new vehicle quota: `max_vehicles = 3 (base) + ad_bonus_vehicles (0 to 2)`.
   - Computes new driver quota: `max_drivers = 3 (base) + ad_bonus_drivers (0 to 2)`.
   - Already-earned bonus slots are preserved! (e.g. If org earned 2 bonus slots, `max_vehicles` becomes 5, not 3).
5. If active vehicle count > new `max_vehicles` (e.g. Org has 10 vehicles), existing vehicles remain in DB but user cannot add NEW vehicles until count drops below quota. Excess vehicles are flagged `READ_ONLY`.
6. Email sent to owner notifying completed downgrade.

**Alternate flows**
- **A1 — Re-Subscription:** User re-subscribes to Pro → Removes `READ_ONLY` restrictions on excess vehicles immediately.

**Edge cases & error handling**
- [ ] Database lock during batch downgrade → Retried cleanly per organization.

**Postconditions**
- Organization tier set to Free; quota updated with preserved ad-bonus slots.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `organizations`, `vehicles`, `audit_logs`
- Endpoint(s): Background downgrade task

**Acceptance criteria (testable)**
- WHEN a Pro organization with 2 ad-rewarded bonus slots downgrades to Free THE SYSTEM SHALL set `max_vehicles = 5` (3 base + 2 bonus) and preserve existing vehicles.

**Estimate:** L  
**Depends on:** UC-084, UC-120  

---

### UC-086: Quota Wall Modal Display & Upgrade Triggers

**Linked story:** FS-PAY-007  
**Actor(s):** User  
**Trigger:** User attempts an action blocked by Free Tier limits (adding 4th base vehicle/driver, requesting PDF export, setting custom checklist).  

**Preconditions**
- [ ] Free Tier organization. Action exceeds tier entitlement.

**Main flow**
1. User clicks restricted feature.
2. App intercepts action and opens Quota Wall Dialog (SCR-PAY-001).
3. Quota Wall displays feature comparison table (Free vs Pro) and dynamic call-to-action:
   - If vehicle limit reached and `ad_bonus_vehicles < 2`: Shows "Watch Ads for +1 Bonus Vehicle" AND "Upgrade to Pro".
   - If vehicle limit reached and `ad_bonus_vehicles == 2`: Shows "Upgrade to Pro for up to 25 Vehicles".
4. User selects "Upgrade to Pro" -> Directs to Payment Checkout (UC-080).

**Alternate flows**
- **A1 — User Chooses Ad Bonus:** User taps "Watch Ads" -> Initiates Rewarded Video Ad Flow (UC-120).

**Edge cases & error handling**
- [ ] User closes dialog -> Returned to previous screen without state mutation.

**Postconditions**
- Quota Wall presented without breaking application navigation.

**Data & API touchpoints**
- Entities touched: `organizations`
- Endpoint(s): Client UI trigger

**Acceptance criteria (testable)**
- WHEN a Free user at vehicle quota attempts creation THE SYSTEM SHALL display the Quota Wall dialog offering Pro upgrade and ad-rewarded options if available.

**Estimate:** S  
**Depends on:** UC-022, UC-080  

---

### UC-087: View Invoice History & Payment Receipts

**Linked story:** FS-PAY-008  
**Actor(s):** Owner / Accountant  
**Trigger:** User opens Billing History tab in Settings.  

**Preconditions**
- [ ] User authenticated as organization owner/admin.

**Main flow**
1. App queries `GET /api/v1/payments/invoices`.
2. Backend fetches invoice history from Stripe API or Safepay transactions table for organization.
3. API returns list of Invoice DTOs (date, amount, status, PDF download link).
4. User taps "Download PDF" next to an invoice item.
5. App opens invoice PDF link in browser/viewer.

**Alternate flows**
- **A1 — Free Tier User:** Displays "No billing history available on Free Tier."

**Edge cases & error handling**
- [ ] Gateway API error fetching invoices → Backend returns cached local subscription invoice log records.

**Postconditions**
- Invoice list displayed and downloadable.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `organizations`
- Endpoint(s): `GET /api/v1/payments/invoices`

**Acceptance criteria (testable)**
- WHEN invoice history is requested THE SYSTEM SHALL return past billing transactions with direct PDF download URLs.

**Estimate:** S  
**Depends on:** UC-081, UC-082  

---

### UC-088: Update Payment Method (Credit Card / Wallet)

**Linked story:** FS-PAY-009  
**Actor(s):** Fleet Owner  
**Trigger:** Owner clicks "Update Payment Method" on Billing screen.  

**Preconditions**
- [ ] Active Pro subscription.

**Main flow**
1. Owner taps "Update Payment Method".
2. App calls `POST /api/v1/payments/customer-portal`.
3. Backend creates gateway customer portal session link (Stripe Customer Portal / Safepay Management).
4. API returns Portal URL.
5. Mobile app opens WebView / external browser to complete card update.
6. Gateway updates payment method on file and redirects back to Veltrics app.

**Alternate flows**
- **A1 — Direct Card Update:** Stripe Elements embedded form updates payment method directly in-app.

**Edge cases & error handling**
- [ ] Customer portal creation fails -> API returns `HTTP 500` error message.

**Postconditions**
- Gateway payment method updated.

**Data & API touchpoints**
- Entities touched: `subscriptions`
- Endpoint(s): `POST /api/v1/payments/customer-portal`

**Acceptance criteria (testable)**
- WHEN payment method update is requested THE SYSTEM SHALL generate a secure Customer Portal session URL.

**Estimate:** M  
**Depends on:** UC-080  

---

### UC-089: Enterprise Sales Inquiry & Custom Quota Provisioning

**Linked story:** FS-PAY-010  
**Actor(s):** Enterprise Prospect / Admin  
**Trigger:** User submits "Contact Sales" form for > 25 vehicles.  

**Preconditions**
- [ ] User on Enterprise plan card.

**Main flow**
1. User enters fleet size (e.g. 150 vehicles), company name, phone number, and requirements.
2. App calls `POST /api/v1/payments/enterprise-inquiry`.
3. Backend creates lead record in CRM table / dispatches email to Veltrics sales team.
4. Veltrics Super-Admin can manually set `tier = "enterprise"`, `max_vehicles = 500`, `max_drivers = 500` on organization via `PATCH /api/v1/admin/organizations/{org_id}/quota`.

**Alternate flows**
- **A1 — Automated Confirmation Email:** Prospect receives automated acknowledgment email.

**Edge cases & error handling**
- [ ] Invalid phone format → Client validation blocks submission.

**Postconditions**
- Enterprise inquiry logged; manual quota override capability enabled.

**Data & API touchpoints**
- Entities touched: `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/payments/enterprise-inquiry`, `PATCH /api/v1/admin/organizations/{org_id}/quota`

**Acceptance criteria (testable)**
- WHEN an enterprise inquiry is submitted THE SYSTEM SHALL log the lead and notify the sales team.

**Estimate:** S  
**Depends on:** UC-014  

---

## 11. EP-SYNC — Offline Sync

### UC-090: Detect Network State & Offline Queue Transition

**Linked story:** FS-SYNC-001  
**Actor(s):** Flutter Mobile Client  
**Trigger:** Network connectivity drops or restores.  

**Preconditions**
- [ ] Connectivity monitoring plugin (`connectivity_plus`) active.

**Main flow**
1. Connectivity listener detects transition from `wifi/cellular` to `none`.
2. Client toggles internal network state flag `isOffline = true`.
3. App updates top bar status indicator: `"Offline Mode — Changes will sync when reconnected"`.
4. All subsequent entity creation/update mutations are routed to local Hive boxes (`hive_fuel_queue`, `hive_maintenance_queue`, `hive_trip_queue`, `hive_expense_queue`).

**Alternate flows**
- **A1 — Reconnection Event:** Connectivity restored to `wifi/cellular` -> System triggers automatic background batch sync (UC-091, UC-119).

**Edge cases & error handling**
- [ ] Flapping connection (rapid on/off) → Debounce timer of 3 seconds delays sync trigger until network is stable.

**Postconditions**
- Client operating state updated seamlessly.

**Data & API touchpoints**
- Entities touched: Local Hive Boxes
- Endpoint(s): Client side network listener

**Acceptance criteria (testable)**
- WHEN network connectivity is lost THE SYSTEM SHALL switch mutation storage to local Hive boxes without throwing unhandled network exceptions.

**Estimate:** S  
**Depends on:** UC-024, UC-034  

---

### UC-091: Local Mutation Enqueueing & Client-Generated UUID Allocation

**Linked story:** FS-SYNC-002  
**Actor(s):** Driver / Consumer (Offline)  
**Trigger:** User performs create/update action while offline.  

**Preconditions**
- [ ] Client offline (`isOffline = true`).

**Main flow**
1. User logs a fuel entry while offline.
2. Flutter client generates UUID v4 for `fuel_log_id`.
3. App writes entity payload to local Hive database box.
4. App appends sync operation envelope to `hive_sync_meta` queue: `{ op_id: UUID, entity_type: "fuel_log", action: "CREATE", payload: JSON, client_timestamp: ISO8601, sync_status: "PENDING" }`.
5. UI updates instantly with new entry marked with a "Pending Sync 🕒" clock icon.

**Alternate flows**
- **A1 — Offline Update:** Editing an un-synced entity updates local Hive payload in place.

**Edge cases & error handling**
- [ ] Disk storage full on mobile device → App displays alert "Local storage full. Free space to save offline logs."

**Postconditions**
- Local entity saved; sync envelope queued.

**Data & API touchpoints**
- Entities touched: Local Hive boxes (`hive_sync_meta`)
- Endpoint(s): Client local storage

**Acceptance criteria (testable)**
- WHEN an entity is created offline THE SYSTEM SHALL generate a client-side UUID v4 and append the operation envelope to `hive_sync_meta`.

**Estimate:** S  
**Depends on:** UC-090  

---

### UC-092: Automatic Background Sync Execution on Reconnection

**Linked story:** FS-SYNC-003  
**Actor(s):** Mobile Sync Engine / System  
**Trigger:** Network connectivity restored AND `hive_sync_meta` contains pending items.  

**Preconditions**
- [ ] Network restored. Pending sync envelope count > 0.

**Main flow**
1. Connectivity listener detects stable connection.
2. Sync engine reads all pending items from `hive_sync_meta` ordered by `client_timestamp ASC`.
3. Sync engine constructs batch request payload (UC-119).
4. App posts batch to `POST /api/v1/sync/batch`.
5. Upon receiving `HTTP 200` response, sync engine marks queue items as `SYNCED` and clears them from `hive_sync_meta`.
6. App removes "Pending Sync" clock icons from UI elements.

**Alternate flows**
- **A1 — Sync Errors Encountered:** Backend returns partial failures → Client updates item sync status to `CONFLICT` or `FAILED` (UC-094).

**Edge cases & error handling**
- [ ] Server timeout mid-batch → Client retains queue and retries exponential backoff (15s, 30s, 60s).

**Postconditions**
- Offline queue processed and cleared.

**Data & API touchpoints**
- Entities touched: Local Hive boxes, `hive_sync_meta`
- Endpoint(s): `POST /api/v1/sync/batch`

**Acceptance criteria (testable)**
- WHEN connectivity is restored THE SYSTEM SHALL automatically send all pending sync envelopes to `POST /api/v1/sync/batch` in a single request.

**Estimate:** M  
**Depends on:** UC-091, UC-119  

---

### UC-093: Manual "Sync Now" User Trigger

**Linked story:** FS-SYNC-004  
**Actor(s):** User  
**Trigger:** User taps "Sync Now" button on Settings or Sync Status bar.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. User taps "Sync Now".
2. UI displays spinning sync indicator.
3. App forces immediate execution of background sync protocol (UC-092, UC-119).
4. Upon completion, UI displays success toast: `"Sync Complete — 4 items updated."`

**Alternate flows**
- **A1 — No Connection:** Displays toast `"No internet connection available."`

**Edge cases & error handling**
- [ ] Sync already in progress → Prevents duplicate trigger.

**Postconditions**
- Manual sync executed.

**Data & API touchpoints**
- Entities touched: `hive_sync_meta`
- Endpoint(s): `POST /api/v1/sync/batch`

**Acceptance criteria (testable)**
- WHEN "Sync Now" is tapped THE SYSTEM SHALL force an immediate synchronization attempt and update the status UI.

**Estimate:** S  
**Depends on:** UC-092  

---

### UC-094: Sync Conflict Resolution Protocol (Server-Wins Baseline)

**Linked story:** FS-SYNC-005  
**Actor(s):** Sync Engine / Server  
**Trigger:** Client attempts to update an entity modified on server while offline.  

**Preconditions**
- [ ] Entity modified both locally and on server.

**Main flow**
1. Backend processes entity update envelope during `POST /api/v1/sync/batch`.
2. Backend compares entity `updated_at` timestamp in DB vs payload `base_updated_at`.
3. If DB `updated_at > base_updated_at`, server detects conflict.
4. Server applies **Server-Wins baseline policy**:
   - Rejects client edit.
   - Returns latest server entity state in batch response `conflicts` array.
5. Client sync engine receives conflict payload, overwrites local Hive record with server entity, and notifies user: `"Vehicle record updated from server."`

**Alternate flows**
- **A1 — Last-Write-Wins Override:** For independent fields (e.g. notes string), server merges non-conflicting fields.

**Edge cases & error handling**
- [ ] Client entity deleted on server → Server returns `ENTITY_DELETED`; client soft-deletes local Hive copy.

**Postconditions**
- Conflict resolved according to deterministic rules; data consistency guaranteed.

**Data & API touchpoints**
- Entities touched: All domain entities, `hive_sync_meta`
- Endpoint(s): `POST /api/v1/sync/batch`

**Acceptance criteria (testable)**
- WHEN a sync conflict occurs THE SYSTEM SHALL enforce Server-Wins policy and return the server's current entity state in the response.

**Estimate:** L  
**Depends on:** UC-119  

---

### UC-095: View Sync Status & Queue Health Inspector

**Linked story:** FS-SYNC-006  
**Actor(s):** User / Support  
**Trigger:** User taps "Sync Status" in Settings menu.  

**Preconditions**
- [ ] App running.

**Main flow**
1. App displays Sync Inspector screen (SCR-SET-004).
2. Screen lists:
   - Last Successful Sync Timestamp
   - Pending Queue Count (Fuel, Maintenance, Trips, Expenses)
   - Failed / Conflict Items List
3. User can tap a failed item to view details, retry sync, or discard local edit.

**Alternate flows**
- **A1 — Discard Local Edit:** User clicks "Discard" → Item removed from local queue; re-downloads server state.

**Edge cases & error handling**
- [ ] Empty queue → Displays "All data in sync with cloud."

**Postconditions**
- Sync queue health inspected.

**Data & API touchpoints**
- Entities touched: `hive_sync_meta`
- Endpoint(s): Local inspection

**Acceptance criteria (testable)**
- WHEN the sync inspector is opened THE SYSTEM SHALL list all pending and failed queue envelopes with their error messages.

**Estimate:** S  
**Depends on:** UC-091  

---

### UC-096: Delta Sync Payload Fetching (Incremental Catch-up)

**Linked story:** FS-SYNC-007  
**Actor(s):** Mobile Sync Engine  
**Trigger:** App launches or resumes after extended offline period.  

**Preconditions**
- [ ] `last_sync_timestamp` stored locally.

**Main flow**
1. App sends request `GET /api/v1/sync/delta?since={last_sync_timestamp}`.
2. Backend queries all entities (`vehicles`, `drivers`, `fuel_logs`, `maintenance_logs`, `expenses`, `trips`) where `updated_at > since` AND `organization_id = tenant_id`.
3. Backend returns Delta Sync DTO containing arrays of created/updated items and soft-deleted IDs.
4. Client sync engine updates local Hive database boxes in a single local transaction.
5. Client updates `last_sync_timestamp = NOW()`.

**Alternate flows**
- **A1 — First Launch / Full Sync:** `since` is null → Backend returns full initial snapshot payload.

**Edge cases & error handling**
- [ ] `since` > 90 days ago → Backend requests client execute full re-sync.

**Postconditions**
- Client database synchronized with server changes.

**Data & API touchpoints**
- Entities touched: All domain entities
- Endpoint(s): `GET /api/v1/sync/delta`

**Acceptance criteria (testable)**
- WHEN delta sync is called with timestamp T THE SYSTEM SHALL return only entities created or modified since T.

**Estimate:** M  
**Depends on:** UC-092  

---

### UC-097: Handle Offline Media & Image Upload Queue

**Linked story:** FS-SYNC-008  
**Actor(s):** Mobile Client  
**Trigger:** User attaches receipt image while offline.  

**Preconditions**
- [ ] Client offline.

**Main flow**
1. App saves captured receipt image file to local device storage folder.
2. App stores relative local file path in local Hive log item.
3. When network reconnects, sync engine uploads entity JSON first (UC-119).
4. Upon receiving server entity ID, sync engine uploads pending binary receipt files to multipart attachment endpoints.
5. App updates local entity with CDN URL and deletes local temporary image file.

**Alternate flows**
- **A1 — Image Upload Fails:** Binary file retained on local disk for next retry cycle.

**Edge cases & error handling**
- [ ] Image file missing/corrupted → Log entry saved without receipt; error flagged in inspector.

**Postconditions**
- Media files uploaded and linked post-reconnection.

**Data & API touchpoints**
- Entities touched: Local storage, `fuel_logs`, `maintenance_logs`, `expenses`
- Endpoint(s): `POST /api/v1/fuel/{id}/attachments`, etc.

**Acceptance criteria (testable)**
- WHEN media is attached offline THE SYSTEM SHALL queue the file on local disk and upload it after entity creation completes on server.

**Estimate:** M  
**Depends on:** UC-091, UC-097  

---

## 12. EP-AD — Advertising (Free Tier)

### UC-098: Display Banner & Native In-Feed Ads (Free Tier Only)

**Linked story:** FS-AD-001  
**Actor(s):** Free Tier User  
**Trigger:** User views Dashboard, Vehicle Directory, or Settings screens.  

**Preconditions**
- [ ] Free Tier organization (`organizations.tier == "free"`).

**Main flow**
1. Google Mobile Ads SDK / AdMob initializes on app startup.
2. App checks user subscription tier.
3. If Free Tier, app renders inline banner ad widgets at bottom of screen and native card ads inside vehicle/log lists.
4. If user upgrades to Pro Tier (`tier == "pro"`), all ad widgets are unmounted immediately.

**Alternate flows**
- **A1 — No-Ad Zones:** Ad widgets are strictly excluded on data-entry screens SCR-FUEL-001, SCR-MNT-002, SCR-TRIP-001, SCR-EXP-001 (SDS-005).

**Edge cases & error handling**
- [ ] Ad load failure -> Widget collapses gracefully (0px height) without leaving blank gap.

**Postconditions**
- Ad placement rendered per tier rules and design system guidelines.

**Data & API touchpoints**
- Entities touched: `organizations`
- Endpoint(s): Google AdMob SDK / Client rendering

**Acceptance criteria (testable)**
- WHEN a user belongs to a Pro organization THE SYSTEM SHALL destroy and suppress all banner and native ad widgets.

**Estimate:** S  
**Depends on:** UC-014  

---

### UC-099: Rewarded Video Ad Execution for Bonus Slots

**Linked story:** FS-AD-002  
**Actor(s):** Free Tier User  
**Trigger:** User taps "Watch Ads for +1 Bonus Slot" on Quota Wall.  

**Preconditions**
- [ ] Organization `tier == "free"`. `ad_bonus_vehicles < 2` OR `ad_bonus_drivers < 2`.

**Main flow**
1. App verifies Google AdMob rewarded video ad is pre-loaded.
2. App presents Rewarded Video Ad modal.
3. User watches 3 consecutive video ads (back-to-back, no skip allowed).
4. Upon completing all 3 ads, Google AdMob SDK triggers completion callback with cryptographic signature payload.
5. Flutter client submits token to `POST /api/v1/ads/verify-reward` with `{ slot_type: "VEHICLE" | "DRIVER", reward_token }`.
6. Backend validates token signature and executes Ad-Rewarded Quota Lifecycle Engine (UC-120).
7. Backend increments `ad_bonus_vehicles` or `ad_bonus_drivers` on `organizations` table.
8. Backend updates `max_vehicles` (e.g. 3 -> 4) and returns updated Organization DTO.
9. App unlocks slot and displays success celebration dialog.

**Alternate flows**
- **A1 — Abandoned Playback:** User closes ad on 2nd video -> Reward NOT granted; user progress reset to 0/3.

**Edge cases & error handling**
- [ ] Ad network unavailable -> Displays "Ads unavailable right now. Try again in a few minutes or upgrade to Pro."

**Postconditions**
- Permanent bonus slot unlocked on organization.

**Data & API touchpoints**
- Entities touched: `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/ads/verify-reward`

**Acceptance criteria (testable)**
- WHEN 3 rewarded ads are completed and verified THE SYSTEM SHALL increment the organization's bonus slot count and `max_vehicles` by 1 in a single transaction.

**Estimate:** L  
**Depends on:** UC-022, UC-120  

---

### UC-100: Ad-Gate Action Verification (Per-Action Ads on Bonus Vehicles)

**Linked story:** FS-AD-003  
**Actor(s):** Free Tier User  
**Trigger:** User attempts an action (log fuel, log maintenance, log trip) involving an ad-rewarded vehicle or driver.  

**Preconditions**
- [ ] Target vehicle has `is_ad_rewarded == true`.

**Main flow**
1. User taps "Save Fuel Log" on an ad-rewarded vehicle.
2. Flutter client opens Ad-Gate Modal: *"This vehicle was unlocked via ads. Watch 1 video ad to save your log."*
3. User watches 1 rewarded video ad.
4. AdMob SDK returns completion signature token.
5. Flutter includes `X-Ad-Reward-Token` header in the target API request (`POST /api/v1/fuel`).
6. FastAPI backend middleware validates signature token using Ad-Gate Enforcement Protocol (UC-122).
7. Upon successful validation, route executes and saves log.

**Alternate flows**
- **A1 — Pro User Action:** Ad-Gate check bypassed entirely for Pro organizations.

**Edge cases & error handling**
- [ ] Missing / Invalid Ad Token -> API rejects request with `HTTP 402 Payment Required` (`"AD_REWARD_REQUIRED"`).

**Postconditions**
- Mutation completed following verified ad playback.

**Data & API touchpoints**
- Entities touched: `organizations`, `vehicles`
- Endpoint(s): `POST /api/v1/fuel`, `POST /api/v1/maintenance`, `POST /api/v1/trips`

**Acceptance criteria (testable)**
- WHEN a mutation is requested on an ad-rewarded vehicle without a valid `X-Ad-Reward-Token` header THE SYSTEM SHALL reject the request with `HTTP 402`.

**Estimate:** M  
**Depends on:** UC-099, UC-122  

---

### UC-101: Visual Badge Tagging for Ad-Rewarded Entities

**Linked story:** FS-AD-004  
**Actor(s):** User  
**Trigger:** User views vehicle cards or driver lists.  

**Preconditions**
- [ ] Ad-rewarded vehicles or drivers exist in fleet.

**Main flow**
1. App fetches vehicle/driver directory.
2. For items with `is_ad_rewarded == true`, Flutter client attaches a distinct amber "🎬 Ad" badge on the UI card (SDS-004).
3. Tooltip on badge explains: *"Unlocked via rewarded ads. Requires 1 video ad per action."*

**Alternate flows**
- **A1 — Pro Upgrade:** When org upgrades to Pro, `is_ad_rewarded` flags are cleared and badges vanish.

**Edge cases & error handling**
- [ ] Standard vehicles -> Badge is hidden.

**Postconditions**
- Visual indicator rendered.

**Data & API touchpoints**
- Entities touched: `vehicles`, `users`
- Endpoint(s): Client UI rendering

**Acceptance criteria (testable)**
- WHEN an entity has `is_ad_rewarded = true` THE SYSTEM SHALL render the "🎬 Ad" visual badge badge on its UI list element.

**Estimate:** S  
**Depends on:** UC-099  

---

### UC-102: Ad-Free Experience Enforcement on Pro Upgrade

**Linked story:** FS-AD-005  
**Actor(s):** System  
**Trigger:** Organization upgrades from Free to Pro Tier.  

**Preconditions**
- [ ] Subscription webhook activates Pro status.

**Main flow**
1. Subscription webhook updates `organizations.tier = "pro"`.
2. Backend clears `is_ad_rewarded = false` on all vehicles and drivers belonging to the organization.
3. Mobile app re-fetches organization session payload and sets local `adFree = true`.
4. All ad widgets, ad-gate dialogs, and rewarded video prompts are completely disabled across the application.

**Alternate flows**
- **A1 — Revert on Downgrade:** If Pro subscription expires, ad widgets re-enable (UC-085).

**Edge cases & error handling**
- [ ] Active ad dialog open during upgrade -> Dialog auto-closes with "Pro activated - Ad skipped!".

**Postconditions**
- 100% ad-free experience enforced.

**Data & API touchpoints**
- Entities touched: `organizations`, `vehicles`, `users`
- Endpoint(s): `POST /api/v1/payments/webhooks/*`

**Acceptance criteria (testable)**
- WHEN an organization is upgraded to Pro THE SYSTEM SHALL set `is_ad_rewarded = false` on all tenant entities and suppress all ad network calls.

**Estimate:** S  
**Depends on:** UC-081, UC-099  

---

## 13. EP-DRV — Driver Scoring

### UC-103: Calculate Driver Safety & Behavior Score

**Linked story:** FS-DRV-001  
**Actor(s):** System Cron / Worker  
**Trigger:** Nightly driver scoring aggregation job executes.  

**Preconditions**
- [ ] Driver has logged trips/maintenance. Pro Tier organization.

**Main flow**
1. Worker queries driver activity for past 30 days:
   - On-time maintenance compliance rate (40% weight).
   - Fuel efficiency vs vehicle average (30% weight).
   - Harsh braking / speeding events recorded during GPS trips (30% weight).
2. System computes composite driver score from 0 to 100.
3. System writes result to `driver_scores` table (`driver_id`, `score`, `safety_grade` A/B/C/D/F, `evaluated_at`).

**Alternate flows**
- **A1 — Insufficient Data:** Driver with < 3 trips receives score `NULL` with status `"PENDING_DATA"`.

**Edge cases & error handling**
- [ ] Free Tier organization -> Cron skips driver score calculation for tenant.

**Postconditions**
- Driver safety score computed and stored.

**Data & API touchpoints**
- Entities touched: `driver_scores`, `users`, `trips`, `maintenance_logs`
- Endpoint(s): Background scoring worker / `GET /api/v1/drivers/{id}/score`

**Acceptance criteria (testable)**
- WHEN the nightly scoring job runs THE SYSTEM SHALL calculate a composite 0-100 score for all active drivers in Pro organizations.

**Estimate:** L  
**Depends on:** UC-034, UC-047, UC-052, UC-080  

---

### UC-104: View Driver Score Leaderboard & Detail Cards

**Linked story:** FS-DRV-002  
**Actor(s):** Fleet Manager  
**Trigger:** Manager opens Driver Performance tab (SCR-DRV-001).  

**Preconditions**
- [ ] Pro tier active.

**Main flow**
1. App queries `GET /api/v1/drivers/scores`.
2. Backend returns list of organization drivers sorted by safety score.
3. App displays driver leaderboard with letter grade badges (Grade A green, Grade F red).
4. Manager clicks a driver to view score factor breakdown (Maintenance compliance 95%, Fuel efficiency 82%, Safety 88%).

**Alternate flows**
- **A1 — Driver Self-View:** Drivers can view own score card on mobile app but cannot see peer scores.

**Edge cases & error handling**
- [ ] Free Tier -> Display Quota Wall teaser card.

**Postconditions**
- Driver safety score leaderboard rendered.

**Data & API touchpoints**
- Entities touched: `driver_scores`, `users`
- Endpoint(s): `GET /api/v1/drivers/scores`

**Acceptance criteria (testable)**
- WHEN driver scores are fetched THE SYSTEM SHALL return drivers ordered by composite score descending alongside factor breakdowns.

**Estimate:** M  
**Depends on:** UC-103  

---

### UC-105: Driver Safety Event Logging (Harsh Braking / Speeding)

**Linked story:** FS-DRV-003  
**Actor(s):** Mobile Client / GPS Engine  
**Trigger:** Accelerometer / GPS detects sudden deceleration (> 12 km/h/s) or speed exceeding limit by > 20 km/h.  

**Preconditions**
- [ ] Active GPS trip tracking session running (UC-052).

**Main flow**
1. Flutter location background service detects safety event.
2. Client logs event in local trip telemetry buffer `{ event_type: "HARSH_BRAKING", timestamp, lat, lng, g_force }`.
3. Upon trip completion, telemetry array submitted with trip log payload.
4. Backend stores safety events in `trip_events` table.
5. Events reduce driver safety score during nightly calculation (UC-103).

**Alternate flows**
- **A1 — Low Confidence Detection:** Events with < 0.8 GPS accuracy score are discarded.

**Edge cases & error handling**
- [ ] Device dropped inside cab -> Sensor noise filter ignores single-axis spikes < 100ms.

**Postconditions**
- Safety event logged and attached to trip record.

**Data & API touchpoints**
- Entities touched: `trips`, `trip_events`
- Endpoint(s): `POST /api/v1/trips`

**Acceptance criteria (testable)**
- WHEN a harsh braking event occurs during a trip THE SYSTEM SHALL store the event telemetry in `trip_events`.

**Estimate:** M  
**Depends on:** UC-052  

---

### UC-106: Export Driver Safety & Performance Certificates

**Linked story:** FS-DRV-004  
**Actor(s):** Fleet Manager / Driver  
**Trigger:** User taps "Export Safety Certificate" on Driver Profile.  

**Preconditions**
- [ ] Driver has Grade A/B score over 90 days.

**Main flow**
1. User taps "Export Certificate".
2. App calls `POST /api/v1/drivers/{driver_id}/certificate`.
3. Backend generates branded PDF safety certificate detailing driver name, fleet name, evaluation period, and score.
4. API returns download link / streams PDF binary.

**Alternate flows**
- **A1 — Grade Below B:** Action disabled with message "Driver must maintain Grade B or higher to issue safety certificate."

**Edge cases & error handling**
- [ ] Insufficient evaluation period -> Returns `HTTP 400 Bad Request`.

**Postconditions**
- PDF certificate generated.

**Data & API touchpoints**
- Entities touched: `driver_scores`, `users`, `organizations`
- Endpoint(s): `POST /api/v1/drivers/{driver_id}/certificate`

**Acceptance criteria (testable)**
- WHEN a qualifying driver requests a certificate THE SYSTEM SHALL generate a branded PDF document summarizing their safety metrics.

**Estimate:** S  
**Depends on:** UC-103, UC-110  

---

## 14. EP-THEME — Dark Mode & Theming

### UC-107: Toggle App Theme (Light / Dark / System Default)

**Linked story:** FS-THEME-001  
**Actor(s):** User  
**Trigger:** User selects Theme option in Appearance Settings.  

**Preconditions**
- [ ] App running.

**Main flow**
1. User selects `LIGHT`, `DARK`, or `SYSTEM` on SCR-SET-002.
2. App stores choice in local preferences / `users.preferences` JSON field.
3. Flutter `ThemeMode` updates dynamically without restarting application.
4. UI transitions smoothly between Slate Teal / Light (#FFFFFF) and Deep Charcoal Dark Mode (#121212) design tokens (SDS-003, `05b-flutter-theme.dart`).

**Alternate flows**
- **A1 — System Theme Sync:** `SYSTEM` option listens to OS dark mode status and updates automatically.

**Edge cases & error handling**
- [ ] Preference write fails -> Client updates runtime theme state regardless.

**Postconditions**
- App theme applied and persisted.

**Data & API touchpoints**
- Entities touched: `users`
- Endpoint(s): Client UI / `PATCH /api/v1/users/me/preferences`

**Acceptance criteria (testable)**
- WHEN dark mode is selected THE SYSTEM SHALL apply Deep Charcoal (#121212) background tokens without requiring app restart.

**Estimate:** S  
**Depends on:** UC-004  

---

### UC-108: Dynamic Palette Accent Color Selection

**Linked story:** FS-THEME-002  
**Actor(s):** User  
**Trigger:** User selects brand accent palette in settings.  

**Preconditions**
- [ ] App running.

**Main flow**
1. User selects from candidate palettes (Slate Teal, Amber Gold, Forest Green) defined in SDS-001.
2. Flutter client updates primary seed color token.
3. Buttons, active tabs, floating action buttons, and chart accents re-render with selected brand color.

**Alternate flows**
- **A1 — Reset Accent:** Restores default Slate Teal (`#0F766E`).

**Edge cases & error handling**
- [ ] Contrast compliance failure -> App enforces minimum 4.5:1 WCAG contrast against background.

**Postconditions**
- Brand accent color updated.

**Data & API touchpoints**
- Entities touched: Client theme state
- Endpoint(s): Client side rendering

**Acceptance criteria (testable)**
- WHEN a candidate palette is selected THE SYSTEM SHALL re-color primary UI components while maintaining WCAG AA contrast compliance.

**Estimate:** S  
**Depends on:** UC-107  

---

### UC-109: High-Contrast Accessibility Mode

**Linked story:** FS-THEME-003  
**Actor(s):** User  
**Trigger:** User toggles "High Contrast Mode" in Accessibility Settings.  

**Preconditions**
- [ ] App running.

**Main flow**
1. User enables High Contrast toggle.
2. App updates theme parameters to use pure black (#000000) / pure white (#FFFFFF) borders, bold 700 font weights, and high-visibility focus indicators.
3. Form fields and table rows adjust padding and border widths for max legibility.

**Alternate flows**
- **A1 — Font Size Scaling:** Respects OS text scaling settings up to 200%.

**Edge cases & error handling**
- [ ] Layout overflow on 200% font scale -> Scrollviews wrap content gracefully.

**Postconditions**
- High-contrast accessibility rules active.

**Data & API touchpoints**
- Entities touched: Client UI state
- Endpoint(s): Client side rendering

**Acceptance criteria (testable)**
- WHEN high contrast mode is enabled THE SYSTEM SHALL enforce pure black/white element borders and 700 font weight on labels.

**Estimate:** S  
**Depends on:** UC-107  

---

## 15. EP-EXPORT — Data Export (Pro)

### UC-110: Export Comprehensive Fleet Data (PDF & CSV)

**Linked story:** FS-EXPORT-001  
**Actor(s):** Pro Tier User / Accountant  
**Trigger:** User clicks "Export Data" on SCR-SET-005.  

**Preconditions**
- [ ] Pro or Enterprise subscription.

**Main flow**
1. User selects export domain (`ALL`, `VEHICLES`, `FUEL`, `MAINTENANCE`, `EXPENSES`, `TRIPS`), date range, and format (`CSV` or `PDF`).
2. App calls `POST /api/v1/exports` with filter JSON payload.
3. Backend queues background job to query records, format table rows, and generate document.
4. API returns Job ID.
5. Upon completion, system sends notification with secure download link (1-hour TTL).

**Alternate flows**
- **A1 — Free Tier Access Attempt:** Request blocked by Quota Wall (UC-022, UC-086).

**Edge cases & error handling**
- [ ] Large Export (> 50,000 rows) -> Asynchronous email delivery triggered when file is ready.

**Postconditions**
- Export file generated and delivered.

**Data & API touchpoints**
- Entities touched: All domain entities
- Endpoint(s): `POST /api/v1/exports`, `GET /api/v1/exports/{job_id}`

**Acceptance criteria (testable)**
- WHEN a Pro user requests a CSV export THE SYSTEM SHALL generate a formatted CSV file containing all matching domain records.

**Estimate:** M  
**Depends on:** UC-080  

---

### UC-111: Automated Scheduled Email Reports (Weekly / Monthly)

**Linked story:** FS-EXPORT-002  
**Actor(s):** Fleet Manager  
**Trigger:** Manager configures recurring email report schedule.  

**Preconditions**
- [ ] Pro tier active.

**Main flow**
1. Manager selects report frequency (`WEEKLY_MONDAY`, `MONTHLY_FIRST`), recipient emails, and attached format (PDF executive summary).
2. App calls `POST /api/v1/reports/schedules`.
3. Background worker executes on schedule, compiles fleet performance summary, generates PDF attachment, and sends emails.

**Alternate flows**
- **A1 — Unsubscribe Link:** Recipient clicks unsubscribe in email footer -> Disables automated email delivery.

**Edge cases & error handling**
- [ ] Organization downgraded to Free -> Scheduled report jobs paused automatically.

**Postconditions**
- Recurring report schedule configured.

**Data & API touchpoints**
- Entities touched: `report_schedules`, `organizations`
- Endpoint(s): `POST /api/v1/reports/schedules`

**Acceptance criteria (testable)**
- WHEN a recurring report schedule is active THE SYSTEM SHALL auto-generate and email the PDF executive summary on the scheduled interval.

**Estimate:** M  
**Depends on:** UC-110  

---

### UC-112: Export Audit Log Records for Compliance

**Linked story:** FS-EXPORT-003  
**Actor(s):** Organization Owner / Auditor  
**Trigger:** Owner requests audit trail download in Security Settings.  

**Preconditions**
- [ ] Actor is owner. Pro/Enterprise tier.

**Main flow**
1. Owner selects date range for audit logs.
2. App calls `POST /api/v1/exports/audit-logs`.
3. Backend extracts immutable rows from `audit_logs` table for organization.
4. Backend packages rows into encrypted CSV file.
5. API returns download URL.

**Alternate flows**
- **A1 — Non-Owner Access Attempt:** Returns `HTTP 403 Forbidden`.

**Edge cases & error handling**
- [ ] Date range > 1 year -> Requires splitting query into smaller windows.

**Postconditions**
- Audit trail exported.

**Data & API touchpoints**
- Entities touched: `audit_logs`
- Endpoint(s): `POST /api/v1/exports/audit-logs`

**Acceptance criteria (testable)**
- WHEN an owner requests audit logs THE SYSTEM SHALL generate a CSV export containing all matching `audit_logs` entries for that tenant.

**Estimate:** S  
**Depends on:** UC-012, UC-110  

---

## 16. EP-SET — Settings & Account

### UC-113: Manage Profile & Security Settings

**Linked story:** FS-SET-001  
**Actor(s):** User  
**Trigger:** User updates account settings on SCR-SET-001.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. User changes name, phone number, or updates password.
2. App posts updates to `PATCH /api/v1/users/me`.
3. Backend validates input and updates `users` record.
4. System dispatches confirmation email for security sensitive changes (password, email).

**Alternate flows**
- **A1 — Change Email Address:** Sends verification link to new email before updating primary `email` field.

**Edge cases & error handling**
- [ ] Invalid phone format -> Returns `HTTP 422`.

**Postconditions**
- User profile updated.

**Data & API touchpoints**
- Entities touched: `users`, `audit_logs`
- Endpoint(s): `PATCH /api/v1/users/me`

**Acceptance criteria (testable)**
- WHEN password or email is changed THE SYSTEM SHALL send a confirmation notification to the user's registered address.

**Estimate:** S  
**Depends on:** UC-004  

---

### UC-114: Unit Measurement System Configuration (Metric vs Imperial)

**Linked story:** FS-SET-002  
**Actor(s):** User  
**Trigger:** User toggles unit measurement system in Settings.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. User selects `METRIC` (km, liters) or `IMPERIAL` (miles, gallons).
2. App sends update to `PATCH /api/v1/users/me/preferences` with `{ units: "IMPERIAL" }`.
3. Backend stores preference JSON in `users` record.
4. Mobile UI updates dynamically: converts displayed odometer readings, distance values, and efficiency figures (km/L vs MPG) across all screens.

**Alternate flows**
- **A1 — Database Storage Standard:** Database ALWAYS stores values in metric baseline (kilometers, liters); conversion occurs exclusively at UI boundary.

**Edge cases & error handling**
- [ ] Unsupported unit system -> Returns `HTTP 400 Bad Request`.

**Postconditions**
- Unit preference persisted; UI unit conversions applied.

**Data & API touchpoints**
- Entities touched: `users`
- Endpoint(s): `PATCH /api/v1/users/me/preferences`

**Acceptance criteria (testable)**
- WHEN Imperial units are selected THE SYSTEM SHALL store values in metric in the database and convert to miles/gallons on client display.

**Estimate:** S  
**Depends on:** UC-107  

---

### UC-115: Manage App Language & Localization Preferences

**Linked story:** FS-SET-003  
**Actor(s):** User  
**Trigger:** User selects language dropdown on Settings screen.  

**Preconditions**
- [ ] App running.

**Main flow**
1. User selects language (English `en`, Urdu `ur`, Arabic `ar`).
2. App updates Flutter `Locale`.
3. Flutter client re-renders UI strings using ARB translation files.
4. If RTL language selected (Urdu, Arabic), UI layout direction mirrors to Right-To-Left automatically.

**Alternate flows**
- **A1 — Persist Preference:** Saves selected locale code to `users.preferences` JSON.

**Edge cases & error handling**
- [ ] Missing translation string -> Falls back to English (`en`) string default.

**Postconditions**
- Language and RTL direction applied.

**Data & API touchpoints**
- Entities touched: `users`
- Endpoint(s): Client UI rendering / `PATCH /api/v1/users/me/preferences`

**Acceptance criteria (testable)**
- WHEN an RTL language like Urdu is selected THE SYSTEM SHALL mirror the app layout direction to Right-to-Left.

**Estimate:** M  
**Depends on:** UC-107  

---

### UC-116: Data Storage Management & Cache Clearing

**Linked story:** FS-SET-004  
**Actor(s):** User  
**Trigger:** User taps "Clear Cached Data" in Storage Settings.  

**Preconditions**
- [ ] App running.

**Main flow**
1. App displays current storage usage breakdown (Cached Images, Off-line Sync Logs, Local DB size).
2. User taps "Clear Cache".
3. App purges temporary image files and cached network responses.
4. Local Hive boxes containing un-synced offline pending logs are EXCLUDED from purge!
5. App displays success toast: `"Cleared 45 MB of temporary cache."`

**Alternate flows**
- **A1 — Force Reset:** Tapping "Reset App Data" clears all data and logs out user (requires confirmation).

**Edge cases & error handling**
- [ ] Purge attempt during active sync -> Delayed until sync completes.

**Postconditions**
- Temporary cache purged without losing un-synced offline records.

**Data & API touchpoints**
- Entities touched: Local device disk
- Endpoint(s): Client storage API

**Acceptance criteria (testable)**
- WHEN cache clearing is executed THE SYSTEM SHALL purge image caches while strictly preserving un-synced entries in `hive_sync_meta`.

**Estimate:** S  
**Depends on:** UC-091  

---

### UC-117: View App Licenses, Terms of Service & Legal Policies

**Linked story:** FS-SET-005  
**Actor(s):** User  
**Trigger:** User taps "Terms of Service" or "Privacy Policy" link.  

**Preconditions**
- [ ] App running.

**Main flow**
1. User selects legal item on SCR-SET-006.
2. App opens in-app markdown viewer / WebView rendering current Terms of Service, Privacy Policy, and Open Source Licenses.
3. Screen displays document version and last updated date.

**Alternate flows**
- **A1 — Offline View:** Reads bundled local assets if offline.

**Edge cases & error handling**
- [ ] Content load failure -> Renders fallback bundled asset.

**Postconditions**
- Legal document rendered.

**Data & API touchpoints**
- Entities touched: Static app assets / CDN
- Endpoint(s): Client UI rendering

**Acceptance criteria (testable)**
- WHEN a legal policy is selected THE SYSTEM SHALL display the complete text along with its version and last updated date.

**Estimate:** S  
**Depends on:** UC-107  

---

### UC-118: Send Feedback & Contact Support Ticket Submission

**Linked story:** FS-SET-006  
**Actor(s):** User  
**Trigger:** User submits form on SCR-SET-007.  

**Preconditions**
- [ ] User authenticated.

**Main flow**
1. User selects category (`BUG`, `FEATURE_REQUEST`, `BILLING`, `OTHER`), enters description, and attaches screenshot.
2. App calls `POST /api/v1/support/tickets`.
3. Backend attaches user profile ID, device specs, OS version, and app version to ticket payload.
4. Backend creates support ticket in database / dispatches to Zendesk/HelpDesk webhook.
5. API returns Ticket ID DTO.
6. User receives confirmation toast and email notification.

**Alternate flows**
- **A1 — Anonymous Feedback:** User submits without logging in from login screen.

**Edge cases & error handling**
- [ ] Empty description -> Client validation blocks submission.

**Postconditions**
- Support ticket created.

**Data & API touchpoints**
- Entities touched: `support_tickets`, `users`
- Endpoint(s): `POST /api/v1/support/tickets`

**Acceptance criteria (testable)**
- WHEN a support ticket is submitted THE SYSTEM SHALL store the ticket alongside automatically attached device and app version metadata.

**Estimate:** S  
**Depends on:** UC-004  

---

## 17. Core Technical Infrastructure Tickets (Dedicated)

### UC-119: Offline Sync Batch Transaction Engine

**Linked story:** Core Infrastructure / EP-SYNC (FS-SYNC-001..008)  
**Actor(s):** Mobile Client / Backend API Transaction Manager  
**Trigger:** Client sends pending offline operation queue via `POST /api/v1/sync/batch`.  

**Preconditions**
- [ ] Offline operation envelope array provided. Valid Access JWT header present.

**Main flow**
1. Mobile app collects pending envelopes from `hive_sync_meta`.
2. Mobile app sorts operations into strict topological entity dependency order:
   `organizations` → `users` → `vehicles` → `drivers` → `fuel_logs` / `maintenance_logs` / `trips` / `expenses`.
3. Mobile app POSTs sorted array to `POST /api/v1/sync/batch`.
4. FastAPI backend opens a single database transaction (`async with session.begin():`).
5. Backend iterates through envelopes in exact array order:
   - For `CREATE` with client-generated UUID: Checks if primary key already exists. If not, inserts record.
   - For `UPDATE`: Checks entity `updated_at` against envelope `base_updated_at`. If match, executes update. If conflict, applies Server-Wins baseline (UC-094).
   - For `DELETE`: Sets `deleted_at = NOW()`.
6. If all operations process cleanly, backend commits transaction and writes audit log.
7. Backend returns `HTTP 200 OK` with status per envelope `{ op_id, status: "SUCCESS" | "CONFLICT", server_entity }`.
8. Mobile app updates local Hive boxes and clears processed envelopes from `hive_sync_meta`.

**Alternate flows**
- **A1 — Foreign Key Dependency Violation:** If client array order is invalid or an upstream parent entity failed validation, database transaction rolls back entirely, and backend returns `HTTP 400 Bad Request` specifying failing operation ID.

**Edge cases & error handling**
- [ ] DB constraint violation on 4th of 10 items -> Entire transaction rolls back; no partial DB corruption. Response identifies failing item index.

**Postconditions**
- Offline batch committed in atomic single transaction; foreign key constraints preserved.

**Data & API touchpoints**
- Entities touched: All domain entities (`organizations`, `users`, `vehicles`, `drivers`, `fuel_logs`, `maintenance_logs`, `trips`, `expenses`, `audit_logs`)
- Endpoint(s): `POST /api/v1/sync/batch`

**Acceptance criteria (testable)**
- WHEN a sync batch request is processed THE SYSTEM SHALL execute all entity mutations inside a single database transaction in strict topological order (`organizations → users → vehicles → drivers → logs`).
- WHEN any single operation in a batch fails constraint validation THE SYSTEM SHALL roll back all mutations in the batch and return `HTTP 400`.

**Estimate:** L  
**Depends on:** UC-014, UC-024, UC-034, UC-046, UC-052, UC-058, UC-092  

---

### UC-120: Ad-Rewarded Quota Lifecycle Engine

**Linked story:** Core Infrastructure / EP-AD (FS-AD-001..005) & EP-PAY (FS-PAY-007)  
**Actor(s):** Backend Entitlement Engine / Ad Verification Handler  
**Trigger:** User completes rewarded ads or changes subscription tier.  

**Preconditions**
- [ ] Organization exists.

**Main flow**
1. Upon verified completion of 3 rewarded ads (UC-099), backend receives `POST /api/v1/ads/verify-reward`.
2. Backend validates reward token signature.
3. Backend checks current organization counts: `ad_bonus_vehicles` and `ad_bonus_drivers`.
4. If `ad_bonus_vehicles < 2` for vehicle reward request:
   - Backend increments `organizations.ad_bonus_vehicles += 1`.
   - Backend updates `organizations.max_vehicles = 3 (base) + ad_bonus_vehicles`.
   - Bonus slot is permanently attached to `organization` entity.
5. If user later downgrades from Pro to Free Tier (UC-085):
   - Entitlement engine checks `ad_bonus_vehicles` and `ad_bonus_drivers`.
   - Engine sets Free quota to `max_vehicles = 3 + ad_bonus_vehicles` (up to 5 maximum) and `max_drivers = 3 + ad_bonus_drivers` (up to 5 maximum).
   - Earned bonus slots are preserved across downgrades!
6. Backend commits transaction and returns updated Organization DTO.

**Alternate flows**
- **A1 — Maximum Bonus Cap Reached:** If `ad_bonus_vehicles == 2` and user attempts another reward ad, API rejects with `HTTP 400 Bad Request` (`"MAX_BONUS_SLOTS_REACHED"`).

**Edge cases & error handling**
- [ ] Forged ad reward token -> API rejects with `HTTP 401 Unauthorized`.

**Postconditions**
- Bonus slot permanently bound to organization; quota cap updated.

**Data & API touchpoints**
- Entities touched: `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/ads/verify-reward`

**Acceptance criteria (testable)**
- WHEN 3 rewarded ads are completed THE SYSTEM SHALL increment `ad_bonus_vehicles` on the `organizations` table and increase `max_vehicles` by 1.
- WHEN a Pro organization with 2 bonus slots downgrades to Free THE SYSTEM SHALL cap max vehicles at 5 (3 base + 2 bonus) rather than resetting to 3.

**Estimate:** L  
**Depends on:** UC-014, UC-022, UC-085, UC-099  

---

### UC-121: Dual Payment Gateway Webhook Reconciliation Engine

**Linked story:** Core Infrastructure / EP-PAY (FS-PAY-001..010)  
**Actor(s):** Webhook Middleware / Stripe & Safepay Integration Services  
**Trigger:** Webhook event received from Stripe (`POST /api/v1/payments/webhooks/stripe`) or Safepay (`POST /api/v1/payments/webhooks/safepay`).  

**Preconditions**
- [ ] Webhook signature verified.

**Main flow**
1. Webhook endpoint receives HTTP POST from Stripe or Safepay.
2. Middleware verifies provider cryptographic signature (Stripe Webhook Secret / Safepay HMAC Key).
3. Payload handler extracts unified fields:
   - Provider Name (`"STRIPE"` or `"SAFEPAY"`)
   - Provider Subscription / Transaction ID
   - Internal `organization_id`
   - Normalized Event Type (`PAYMENT_SUCCESS`, `PAYMENT_FAILED`, `SUBSCRIPTION_CANCELED`)
4. Handler updates normalized `subscriptions` table:
   - Sets `status` to normalized state (`"ACTIVE"`, `"PAST_DUE"`, `"CANCELED"`).
   - Sets `current_period_end` timestamp.
   - Stores raw original event JSON inside `gateway_payload` JSONB column.
5. If status transition is `ACTIVE`, handler updates `organizations.tier = "pro"` and sets Pro quotas (`max_vehicles = 25`, `max_drivers = 15`).
6. Handler logs event in `audit_logs`.
7. Endpoint returns `HTTP 200 OK` to payment gateway.

**Alternate flows**
- **A1 — Duplicate Webhook Event:** Handler checks provider event ID in `audit_logs`. If already processed, returns `HTTP 200 OK` immediately without re-mutating state (idempotency enforcement).

**Edge cases & error handling**
- [ ] Unrecognized event type -> Logged in audit trail and returned `HTTP 200 OK` to prevent gateway retry loops.

**Postconditions**
- Subscription state normalized; raw gateway event saved in JSONB; entitlements updated.

**Data & API touchpoints**
- Entities touched: `subscriptions`, `organizations`, `audit_logs`
- Endpoint(s): `POST /api/v1/payments/webhooks/stripe`, `POST /api/v1/payments/webhooks/safepay`

**Acceptance criteria (testable)**
- WHEN a valid webhook is received from either Stripe or Safepay THE SYSTEM SHALL normalize subscription status to `ACTIVE`/`PAST_DUE`/`CANCELED` and store the raw payload in `gateway_payload`.
- WHEN a duplicate webhook event ID is received THE SYSTEM SHALL process it idempotently and return `HTTP 200` without repeating mutations.

**Estimate:** L  
**Depends on:** UC-080, UC-081, UC-082  

---

### UC-122: Ad-Gate Signature Enforcement Protocol

**Linked story:** Core Infrastructure / EP-AD (FS-AD-003) & EP-VEH (FS-VEH-001)  
**Actor(s):** Flutter Mobile Client / FastAPI Ad-Gate Middleware  
**Trigger:** Client submits mutation request (fuel log, trip log, maintenance log) for an ad-rewarded vehicle.  

**Preconditions**
- [ ] Request target entity has `is_ad_rewarded == true`. User organization is on Free Tier.

**Main flow**
1. User completes required rewarded video ad on mobile device.
2. AdMob SDK issues signed completion payload signed with secret key.
3. Mobile app constructs JSON header or request field `X-Ad-Reward-Token`.
4. Mobile app submits mutation request (e.g. `POST /api/v1/fuel`).
5. FastAPI middleware intercepts request:
   - Checks if target vehicle has `is_ad_rewarded == true` AND `organizations.tier == "free"`.
   - If false (Pro user or standard vehicle), middleware passes request immediately.
   - If true (Ad-rewarded vehicle on Free tier), middleware extracts `X-Ad-Reward-Token`.
   - Middleware validates cryptographic signature of token and checks token timestamp (must be < 5 minutes old and not previously consumed).
6. Upon successful validation, token is marked consumed in Redis/DB cache, and request continues to route handler.

**Alternate flows**
- **A1 — Invalid / Expired Token:** Middleware aborts request processing immediately and returns `HTTP 402 Payment Required` with detail `{"code": "AD_REWARD_REQUIRED", "message": "Ad completion token invalid or expired."}`.

**Edge cases & error handling**
- [ ] Replayed token (attempting to use same ad completion token twice) -> Middleware rejects with `HTTP 402` ("Ad token already consumed").

**Postconditions**
- State mutation authorized strictly following verified rewarded ad playback.

**Data & API touchpoints**
- Entities touched: `organizations`, `vehicles`, `fuel_logs`, `maintenance_logs`, `trips`
- Endpoint(s): `POST /api/v1/fuel`, `POST /api/v1/maintenance`, `POST /api/v1/trips`, `POST /api/v1/expenses`

**Acceptance criteria (testable)**
- WHEN a mutation is requested on an ad-rewarded vehicle without a valid `X-Ad-Reward-Token` THE SYSTEM SHALL return `HTTP 402 Payment Required`.
- WHEN an ad token older than 5 minutes or previously consumed is submitted THE SYSTEM SHALL reject the request with `HTTP 402`.

**Estimate:** M  
**Depends on:** UC-099, UC-100  

---

## Summary Matrix of Implementation Tickets

| Category / Epic | Ticket Range | Ticket Count | Focus / Key Deliverable |
|:---|:---|:---|:---|
| **EP-AUTH** | UC-001 – UC-013 | 13 | Multi-provider Auth (Google, Facebook, Email, Phone OTP), Session JWTs, GDPR |
| **EP-ORG** | UC-014 – UC-023 | 10 | Multi-Tenancy, Team Roles, Invitations, Quotas, Soft Delete |
| **EP-VEH** | UC-024 – UC-033 | 10 | Vehicle Registry, Drivers, Odometer Tracking, Documents, Analytics |
| **EP-MNT** | UC-034 – UC-045 | 12 | Maintenance Logs, Recurring Schedules, Inspection Checklists, Vendors, Snooze |
| **EP-FUEL** | UC-046 – UC-051 | 6 | Fuel Logging, Efficiency Calculations, OCR Receipts, Theft Alerts |
| **EP-TRIP** | UC-052 – UC-057 | 6 | GPS & Manual Trips, Business Classification, Tax Deductions, Exports |
| **EP-EXP** | UC-058 – UC-063 | 6 | Expense Records, Recurring Bills, Reimbursement Workflow, Receipts |
| **EP-DASH** | UC-064 – UC-071 | 8 | Dashboards, Cost Charts, Alert Widgets, Leaderboards, Customization |
| **EP-NOTIF** | UC-072 – UC-079 | 8 | FCM Push Tokens, Notification Inbox, Expiration Alerts, Security Alerts |
| **EP-PAY** | UC-080 – UC-089 | 10 | Stripe & Safepay Checkout, Subscriptions, Quota Wall, Enterprise Sales |
| **EP-SYNC** | UC-090 – UC-097 | 8 | Offline Queueing, Client UUIDs, Incremental Delta Sync, Conflict Resolution |
| **EP-AD** | UC-098 – UC-102 | 5 | AdMob Banners, Rewarded Video Ads, Bonus Slots, Ad-Free Pro Enforcement |
| **EP-DRV** | UC-103 – UC-106 | 4 | Safety Score Calculation, Leaderboard, Telemetry Events, Certificates |
| **EP-THEME** | UC-107 – UC-109 | 3 | Slate Teal / Charcoal Dark Mode, Palette Accents, High Contrast |
| **EP-EXPORT**| UC-110 – UC-112 | 3 | PDF/CSV Data Exports, Scheduled Email Reports, Compliance Logs |
| **EP-SET** | UC-113 – UC-118 | 6 | Profile Settings, Metric/Imperial Conversion, Locales (Urdu/RTL), Support |
| **CORE INFRA**| UC-119 – UC-122 | 4 | Sync Batch Transaction, Ad Bonus Lifecycle, Dual Webhook Engine, Ad-Gate Protocol |
| **TOTAL** | **UC-001 – UC-122** | **122** | **100% Implementation-Ready Backlog** |
