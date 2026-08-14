# Organization

> God node · 248 connections · [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\organization.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/organization.py#L8)

## Call Trace Diagram

```mermaid
sequenceDiagram
    participant P0 as Organization
    participant P1 as AuthService
    participant P2 as User
    participant P3 as UC-014: Provision commercial or custom organization.
    participant P4 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P5 as Retrieve organizations list.
    participant P6 as UC-015: Switch active organization context for user.
    participant P7 as UC-015: Get active organization for user.
    participant P8 as Retrieve organization details by ID.
    participant P9 as UC-017: Edit Organization Profile Details.     Enforces ISO 4217 currency valida
    participant P10 as UC-018: Invite Driver / Manager via Email or Phone.     Generates a secure 64-ch
    participant P11 as UC-018: List pending organization invitations.
    participant P12 as UC-021: Remove Member from Organization.     Prevents owner removal. Unassigns u
    participant P13 as UC-022: Cancel Pending Member Invitation.
    participant P14 as UC-023: Soft Delete Organization & Child Entities.     Rejects personal org dele
    participant P15 as UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    participant P16 as UC-024: Register New Vehicle with organization quota validation & duplicate VIN
    participant P17 as UC-025: List Organization Vehicles directory with status, search, fuel type, and
    participant P18 as UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur
    participant P19 as UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    participant P20 as UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow
    participant P21 as UC-028: Soft Delete Vehicle & Write Audit Log.     Frees up 1 vehicle slot in a
    participant P22 as UC-029: Log Manual Odometer Update.     Enforces lower-reading guard unless is_
    participant P23 as UC-030: Upload & Manage Vehicle Documents (Registration / Insurance / Permit).
    participant P24 as UC-030: List Vehicle Documents.
    participant P25 as UC-031: Recover Soft-Deleted Vehicle.     Enforces active organization quota li
    participant P26 as UC-032: Assign Primary Driver to Vehicle.     Enforces tenant isolation on assi
    participant P27 as UC-033: Unassign Primary Driver from Vehicle.
    participant P28 as UC-011: Account Deletion (GDPR Right to be Forgotten)         Soft-deletes user
    participant P29 as Helper to convert SQLAlchemy model instance to dict.
    participant P30 as UC-119: Offline Sync Batch Transaction Engine.     Processes operation envelopes
    participant P31 as UC-096: Delta Sync Payload Fetching (Incremental Catch-up).     Returns active e
    participant P32 as UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    participant P33 as UC-024: Register New Vehicle with organization quota validation & duplicate VIN
    participant P34 as UC-025: List Organization Vehicles directory with status, search, fuel type, and
    participant P35 as UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur
    participant P36 as UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    participant P37 as UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow
    participant P38 as UC-007: Fetch current user profile details.
    participant P39 as UC-007: Update current user profile (full name, phone, city, job role, avatar).
    participant P40 as UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessio
    participant P41 as UC-007: Multi-tenant authorization boundary verification endpoint.
    participant P42 as UC-011: Account Deletion (GDPR Right to be Forgotten).     Soft-deletes user re
    participant P43 as UC-013: Active Session Management & Device Tracking     Returns list of active
    participant P44 as UC-013: Revoke Specific Device Session     Revokes the specified refresh token
    participant P45 as UC-013 Alternate Flow A1: Revoke All Other Sessions     Revokes all active sess
    participant P46 as create_test_user_and_org()
    participant P47 as register_or_login()
    participant P48 as create_test_user_and_org()
    participant P49 as UC-014: Provision commercial or custom organization.
    participant P50 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P51 as Retrieve organizations list.
    participant P52 as UC-015: Switch active organization context for user.
    participant P53 as UC-015: Get active organization for user.
    participant P54 as Retrieve organization details by ID.
    participant P55 as UC-016: Invite Team Member to Organization.     Generates a secure 64-character
    participant P56 as UC-016: List pending organization invitations.
    participant P57 as UC-019: Inspect / validate organization invitation token details.     Returns HT
    participant P58 as UC-019: Accept Organization Invitation for existing authenticated user.
    participant P59 as UC-020: Redeem Org Invitation Code for new user during signup/onboard.
    participant P60 as UC-081, UC-082 & UC-121: Safepay Webhook Processing & Reconciliation Engine
    participant P61 as UC-083: View Subscription Status & Billing History
    participant P62 as UC-084: Cancel Active Subscription
    participant P63 as UC-085 & UC-120: Process Pro-to-Free Subscription Downgrades & Preserved Quotas
    participant P64 as Test 1: Verify all 7 core data models instantiate clean database tables.
    participant P65 as Test 2: Verify database seeding populates master vehicle catalogue idempotently.
    participant P66 as Test 3: Verify POST /api/v1/admin/seed endpoint.
    participant P67 as UC-100 & UC-120 & UC-122: Verify Rewarded Ad Completion Signature Token & Claim
    participant P68 as UC-089: Contact Enterprise Sales Inquiry Form (>25 Fleets).     Submits custom
    participant P69 as UC-086 & UC-087: Vehicle and Driver Quota Wall Enforcement
    participant P70 as UC-100 & UC-120: Verify Rewarded Ad Completion & Increment Bonus Quota
    participant P71 as UC-122: Ad-Gate Signature Forgery & Token Replay Prevention
    participant P72 as UC-101: Render Ad-Free Experience & Unlimited Quota for Pro Subscribers
    participant P73 as UC-087 & UC-018: Register Driver with organization driver quota enforcement.
    participant P74 as UC-081 & UC-121: Safepay Webhook Processing & Entitlement Activation
    participant P75 as UC-082 & UC-121: Handle Payment Checkout Failure & Grace Period
    participant P76 as UC-083: View Subscription Status & Billing History
    participant P77 as UC-084: Cancel Active Subscription
    participant P78 as UC-085 & UC-120: Pro-to-Free Downgrade & Bonus Slot Preservation Protocol
    participant P79 as UC-121: Safepay Webhook Idempotency & Unrecognized Event Logging
    participant P80 as test_data()
    participant P81 as AC 1: GIVEN an authenticated user     WHEN DELETE /api/v1/users/me is invoked
    participant P82 as AC 2: GIVEN a user who is the sole owner of an active non-personal organization
    participant P83 as AC 3: GIVEN a soft-deleted user account     WHEN attempting to authenticate, ac
    participant P84 as AC 1: System creates immutable AuditLog entry upon user registration.
    participant P85 as AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadat
    participant P86 as A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None.
    participant P87 as AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS
    participant P88 as AC 4: System records USER_LOGOUT audit entry upon session termination.
    participant P89 as Edge Case: Audit log DB write exception is handled safely and does not block use
    participant P90 as Test 1: Verify GET /api/v1/vehicles/types?q=Toyota returns seeded Toyota models.
    participant P91 as Test 2: Verify POST /api/v1/vehicles registers new vehicle with tenant organizat
    participant P92 as Test 3: Verify duplicate VIN within same organization returns HTTP 409 Conflict.
    participant P93 as Test 4: Verify exceeding max_vehicles quota (max=2 for sample_org) returns HTTP
    participant P94 as Test 5: Verify custom make/model is dynamically indexed into VehicleType catalog
    participant P95 as ensure_organization()
    participant P96 as test_uc011_sole_owner_blocking()
    participant P97 as test_setup()
    participant P98 as test_uc080_checkout_session_safepay()
    participant P99 as UC-016: Owner can create organization invitation, generating a secure 64-char to
    participant P100 as UC-016: Inviting with invalid or blank email yields HTTP 422 Unprocessable Entit
    participant P101 as UC-016: Inviting with unsupported role string yields HTTP 422 Unprocessable Enti
    participant P102 as UC-016: Re-inviting same email updates existing invitation token and TTL without
    participant P103 as UC-016: Non-owner caller attempting to send invitation yields HTTP 403 Forbidden
    participant P104 as UC-016: Owner can list all pending invitations for organization.
    participant P105 as UC-016: Listing invitations for non-existent org yields HTTP 404 Not Found.
    participant P106 as setup_db()
    participant P107 as AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr
    participant P108 as AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL
    participant P109 as AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store \"facebook\" insid
    participant P110 as Alternate Flow A1: Account Linking     If email matches existing account with d
    participant P111 as Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Requ
    participant P112 as AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT
    participant P113 as Alternate Flow A1: Account Linking     If user signed up via Google, submitting
    participant P114 as Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu
    participant P115 as Edge Case: Missing email or missing password for email auth provider returns HTT
    participant P116 as AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200
    participant P117 as Edge Case: Incorrect password returns HTTP 401 Unauthorized.
    participant P118 as Edge Case: Unregistered email returns HTTP 401 Unauthorized.
    participant P119 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P120 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P121 as AC 1: WHEN an existing Google user signs in,     THE SYSTEM SHALL return HTTP 2
    participant P122 as AC 2: WHEN an existing Facebook user signs in,     THE SYSTEM SHALL return HTTP
    participant P123 as AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,
    participant P124 as AC 4 (Account Linking Flow A1): WHEN an existing user registered via email
    participant P125 as Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized.
    participant P126 as Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized.
    participant P127 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P128 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P129 as AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u
    participant P130 as AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P
    participant P131 as AC 3: GIVEN a profile update request with invalid display name length (< 2 chars
    participant P132 as AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro
    participant P133 as AC 1: GIVEN an authenticated user session with a valid refresh token     WHEN s
    participant P134 as AC 2: GIVEN a revoked refresh token     WHEN submitted to POST /api/v1/auth/ref
    participant P135 as AC 3: GIVEN a malformed or invalid refresh token     WHEN submitted to POST /ap
    participant P136 as AC 4: GIVEN a refresh token that has already been revoked     WHEN logout is ca
    participant P137 as AC 1: WHEN GET /api/v1/users/me/sessions is called THE SYSTEM SHALL return activ
    participant P138 as AC 2: User can revoke a specific session.
    participant P139 as Acceptance Criterion: WHEN a session is revoked via API THE SYSTEM SHALL block a
    participant P140 as A1: User can revoke all other active sessions.
    participant P141 as UC-014: POST /api/v1/organizations creates commercial organization and sets owne
    participant P142 as UC-014: POST /api/v1/organizations/personal auto-creates personal organization f
    participant P143 as UC-014: Blank or whitespace organization name rejected with HTTP 422.
    participant P144 as UC-014: GET /api/v1/organizations?user_id={id} returns list of user organization
    participant P145 as UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found.
    participant P146 as UC-015: POST /api/v1/organizations/switch switches active context for valid user
    participant P147 as UC-015: Switch attempt to organization owned by another user yields HTTP 403 For
    participant P148 as UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found.
    participant P149 as UC-015: GET /api/v1/organizations/active returns current primary organization fo
    participant P150 as UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 N
    participant P151 as setup_db()
    participant P152 as test_setup()
    participant P153 as test_setup()
    participant P154 as test_data()
    participant P155 as AC 1: WHEN a registered user requests a password reset link/token for their emai
    participant P156 as AC 2: WHEN a reset request is submitted for a non-existent email     THE SYSTEM
    participant P157 as AC 3: WHEN a user submits a valid reset token and strong new password     THE S
    participant P158 as AC 4: WHEN an invalid token or token of wrong type (e.g. access token) is submit
    participant P159 as AC 5: WHEN a new password does not satisfy password policy (min 8 chars, 1 upper
    participant P160 as AC 1: GIVEN an authenticated registered user     WHEN they request GET /api/v1/
    participant P161 as AC 2: GIVEN an authenticated user updating their profile details     WHEN they
    participant P162 as AC 3: GIVEN a profile update request with invalid full name length (< 2 characte
    participant P163 as AC 4: GIVEN an unauthenticated request to profile endpoints without user identit
    participant P164 as AC 1: GIVEN a valid active refresh token     WHEN submitted to POST /api/v1/aut
    participant P165 as AC 2: GIVEN an invalid, expired, or non-refresh token (e.g. access or reset toke
    participant P166 as AC 3: GIVEN a refresh token for a disabled or soft-deleted user account     WHE
    participant P167 as AC 4: GIVEN a newly issued access token from POST /api/v1/auth/refresh     WHEN
    participant P168 as test_setup()
    participant P169 as AuditLog
    participant P170 as UserOrganization
    participant P171 as AuthSessionDTO
    participant P172 as SessionRevokeResponse
    participant P173 as UC-004: User Password Authentication & Session Initiation     Authenticates reg
    participant P174 as UC-006: Forgot Password Request     Issues a password reset JWT token with 5-mi
    participant P175 as UC-006: Password Reset Execution     Verifies reset token, validates password p
    participant P176 as UC-009: Session Refresh & Access Token Renewal     Validates active refresh tok
    participant P177 as UC-010: User Sign Out & Token Revocation     Revokes the provided refresh token
    participant P178 as UserDTO
    participant P179 as OrganizationDTO
    participant P180 as UserSessionDTO
    participant P181 as AuditService
    participant P182 as ForgotPasswordResponse
    participant P183 as ResetPasswordResponse
    participant P184 as RefreshTokenResponse
    participant P185 as LogoutResponse
    participant P186 as UserSession
    participant P187 as RegisterRequest
    participant P188 as LoginRequest
    participant P189 as ForgotPasswordRequest
    participant P190 as ResetPasswordRequest
    participant P191 as RefreshTokenRequest
    participant P192 as LogoutRequest
    participant P193 as PaymentService
    participant P194 as UC-053: Get Trip Summary & Tax Deduction Metrics.
    participant P195 as UC-052: Start GPS Trip Tracking session.
    participant P196 as UC-052: Stop active GPS Trip Tracking session and calculate distance.
    participant P197 as UC-052 / UC-053: Create trip entry (Manual or completed GPS trip).
    participant P198 as UC-053: View Trip History.
    participant P199 as UC-054: Edit Trip Entry & Classification.
    participant P200 as UC-055: Soft Delete Trip Entry.
    participant P201 as UC-056: Quick-Log Trip from Dashboard.
    participant P202 as UC-057: View Distance & Mileage Summary Analytics.
    participant P203 as AdService
    participant P204 as UC-058: Log General Fleet Expense.
    participant P205 as UC-059: Expense Category & Cost Summary Metrics.
    participant P206 as UC-059: View Expense History.
    participant P207 as UC-060: Edit Expense Entry.
    participant P208 as UC-061: Soft Delete Expense Entry.
    participant P209 as UC-062: Quick-Log Expense from Dashboard.
    participant P210 as UC-048: View Fuel Efficiency Trends & Aggregate Metrics.
    participant P211 as UC-050: Detect Fuel Anomaly & Theft Alerts - Fetch anomaly logs.
    participant P212 as UC-050 (A1): Manager clears fuel anomaly flag.
    participant P213 as UC-049: Fuel Receipt OCR Auto-Fill (Pro).
    participant P214 as UC-046: Log Fuel Fill-Up Entry.     Automatically updates vehicle current odome
    participant P215 as UC-047 / UC-048: View Fuel Log History with optional pagination.
    participant P216 as UC-051: Edit Fuel Log Entry.     Updates entry, syncs linked ExpenseLog, and re
    participant P217 as UC-051: Soft Delete Fuel Log Entry.     Soft-deletes entry and linked ExpenseLo
    participant P218 as complete_profile()
    participant P219 as login()
    participant P220 as test_uc118_schema_instantiation()
    participant P221 as UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,
    participant P222 as UC-064: Requests for Org 2 return only Org 2's metrics.
    participant P223 as UC-064: Empty organization returns 0 stats so client can render onboarding card.
    participant P224 as UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missin
    participant P225 as refresh_token()
    participant P226 as setup_db()
    participant P227 as dashboard_setup()
    participant P228 as UC-046: Test successful fuel log creation & vehicle current odometer update.
    participant P229 as UC-046 Acceptance Criterion: WHEN a fuel log entry is saved     THE SYSTEM SHAL
    participant P230 as UC-046 Edge Case: Odometer entry lower than vehicle's current odometer -> API re
    participant P231 as UC-046 & UC-047: Verify calculated km/L efficiency on 2nd full tank fill-up.
    participant P232 as UC-047: Test retrieving fuel log history via GET /api/v1/fuel.     Should retur
    participant P233 as UC-047 Acceptance Criterion: WHEN two consecutive full-tank fuel logs are create
    participant P234 as UC-047 Alternate Flow A1: Partial fill-up (is_full_tank = False) skips efficienc
    participant P235 as UC-047 Main Flow 5: If efficiency is 30% lower than vehicle baseline average,
    participant P236 as UC-051 Alternate Flow A1: PATCH /api/v1/fuel/{id} updates entry & recalculates e
    participant P237 as UC-051 Main Flow: DELETE /api/v1/fuel/{id} soft-deletes log & linked expense and
    participant P238 as UC-051 Edge Case: Deleting or patching non-existent log returns HTTP 404.
    participant P239 as UC-034: GET /api/v1/maintenance/schedules should auto-populate schedule template
    participant P240 as UC-034: POST /api/v1/maintenance logs record, updates odometer, and resets sched
    participant P241 as UC-034: POST /api/v1/maintenance rejects negative cost with HTTP 422.
    participant P242 as UC-034: Tenant cross-access rejected.
    participant P243 as UC-036: POST /api/v1/maintenance logs service record and updates linked schedule
    participant P244 as UC-036: Odometer reading > current_odometer_km updates vehicle current_odometer_
    participant P245 as UC-036: Omitting maintenance_schedule_id matches schedule item by task name subs
    participant P246 as UC-036: Rejects negative cost, negative odometer, whitespace service_type, or in
    participant P247 as UC-036: Enforces X-Organization-ID header presence and cross-tenant access prote
    participant P248 as UC-037: GET /api/v1/maintenance/records retrieves service records sorted by serv
    participant P249 as UC-037: Pagination limit and offset parameters operate correctly.
    participant P250 as UC-037: Returns 404 when vehicle_id does not exist in active organization.
    participant P251 as UC-037: Header requirements and cross-tenant boundaries are strictly enforced.
    participant P252 as UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency a
    participant P253 as UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per veh
    participant P254 as UC-035: POST /api/v1/maintenance/schedules creates custom schedule with default
    participant P255 as UC-035: POST /api/v1/maintenance/schedules uses provided last_performed_km and l
    participant P256 as UC-035: Rejects zero/negative intervals or empty task names with 422.
    participant P257 as UC-035: PATCH /api/v1/maintenance/schedules/{id} updates parameters and recalcul
    participant P258 as UC-035: DELETE /api/v1/maintenance/schedules/{id} soft-deletes schedule task.
    participant P259 as UC-035: Header validation and tenant cross-access isolation.
    participant P260 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with empty schedule_ids a
    participant P261 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with specific schedule_id
    participant P262 as UC-038: Returns 404 when vehicle_id is not found in active organization.
    participant P263 as UC-038: Returns 404 when one or more schedule_ids do not belong to the vehicle.
    participant P264 as UC-038: Headers and cross-tenant boundaries are strictly enforced.
    participant P265 as Test 1: Verify PATCH /api/v1/vehicles/{vehicle_id} successfully updates vehicle
    participant P266 as Test 2: Verify updating vehicle under wrong organization_id returns HTTP 403 For
    participant P267 as Test 3: Verify updating non-existent vehicle returns HTTP 404 Not Found.
    participant P268 as Test 4: Verify manual odometer update with discrepancy > 500 km generates an Aud
    participant P269 as Test 5: Verify non-dictionary custom_specs payload returns HTTP 422 Unprocessabl
    participant P270 as create_organization()
    participant P271 as auto_create_personal_organization()
    participant P272 as test_setup()
    participant P273 as test_setup()
    participant P274 as test_setup()
    participant P275 as Test 1: Verify GET /api/v1/vehicles?status=MAINTENANCE returns only vehicles in
    participant P276 as Test 2: Verify search query matches license plate, make, or model.
    participant P277 as Test 3: Verify filtering by province (e.g. Sindh).
    participant P278 as Test 1: Verify GET /api/v1/vehicles/{vehicle_id} returns detailed vehicle metada
    participant P279 as Test 2: Verify non-existent vehicle ID returns HTTP 404 Not Found.
    participant P280 as Test 3: Verify requesting another tenant's vehicle returns HTTP 403 Forbidden.
    participant P281 as Test 4: Verify PATCH /api/v1/vehicles/{vehicle_id}/status updates vehicle status
    participant P282 as setup_db()
    participant P283 as setup_db()
    participant P284 as setup_db()
    participant P285 as test_setup()
    participant P286 as test_setup()
    participant P287 as test_setup()
    participant P288 as test_setup()
    participant P289 as test_setup()
    participant P290 as test_setup()
    participant P291 as setup_db()
    participant P292 as setup_db()
    participant P293 as setup_db()
    participant P294 as setup_db()
    participant P295 as setup_db()
    participant P296 as setup_db()
    participant P297 as sample_fleet()
    participant P298 as test_setup()
    participant P299 as test_setup()
    participant P300 as sample_org()
    P0->>+ P1: uses
    P1-->>- P0: return
    P1->>+ P0: uses
    P0-->>- P1: return
    P1->>+ P2: uses
    P2-->>- P1: return
    P2->>+ P1: uses
    P1-->>- P2: return
    P2->>+ P3: uses
    P3-->>- P2: return
    P2->>+ P4: uses
    P4-->>- P2: return
    P2->>+ P5: uses
    P5-->>- P2: return
    P2->>+ P6: uses
    P6-->>- P2: return
    P2->>+ P7: uses
    P7-->>- P2: return
    P2->>+ P8: uses
    P8-->>- P2: return
    P2->>+ P9: uses
    P9-->>- P2: return
    P2->>+ P10: uses
    P10-->>- P2: return
    P2->>+ P11: uses
    P11-->>- P2: return
    P2->>+ P12: uses
    P12-->>- P2: return
    P2->>+ P13: uses
    P13-->>- P2: return
    P2->>+ P14: uses
    P14-->>- P2: return
    P2->>+ P15: uses
    P15-->>- P2: return
    P2->>+ P16: uses
    P16-->>- P2: return
    P2->>+ P17: uses
    P17-->>- P2: return
    P2->>+ P18: uses
    P18-->>- P2: return
    P2->>+ P19: uses
    P19-->>- P2: return
    P2->>+ P20: uses
    P20-->>- P2: return
    P2->>+ P21: uses
    P21-->>- P2: return
    P2->>+ P22: uses
    P22-->>- P2: return
    P2->>+ P23: uses
    P23-->>- P2: return
    P2->>+ P24: uses
    P24-->>- P2: return
    P2->>+ P25: uses
    P25-->>- P2: return
    P2->>+ P26: uses
    P26-->>- P2: return
    P2->>+ P27: uses
    P27-->>- P2: return
    P2->>+ P28: uses
    P28-->>- P2: return
    P2->>+ P29: uses
    P29-->>- P2: return
    P2->>+ P30: uses
    P30-->>- P2: return
    P2->>+ P31: uses
    P31-->>- P2: return
    P2->>+ P32: uses
    P32-->>- P2: return
    P2->>+ P33: uses
    P33-->>- P2: return
    P2->>+ P34: uses
    P34-->>- P2: return
    P2->>+ P35: uses
    P35-->>- P2: return
    P2->>+ P36: uses
    P36-->>- P2: return
    P2->>+ P37: uses
    P37-->>- P2: return
    P2->>+ P38: uses
    P38-->>- P2: return
    P2->>+ P39: uses
    P39-->>- P2: return
    P2->>+ P40: uses
    P40-->>- P2: return
    P2->>+ P41: uses
    P41-->>- P2: return
    P2->>+ P42: uses
    P42-->>- P2: return
    P2->>+ P43: uses
    P43-->>- P2: return
    P2->>+ P44: uses
    P44-->>- P2: return
    P2->>+ P45: uses
    P45-->>- P2: return
    P2->>+ P46: calls
    P46-->>- P2: return
    P2->>+ P47: calls
    P47-->>- P2: return
    P2->>+ P48: calls
    P48-->>- P2: return
    P2->>+ P49: uses
    P49-->>- P2: return
    P2->>+ P50: uses
    P50-->>- P2: return
    P2->>+ P51: uses
    P51-->>- P2: return
    P2->>+ P52: uses
    P52-->>- P2: return
    P2->>+ P53: uses
    P53-->>- P2: return
    P2->>+ P54: uses
    P54-->>- P2: return
    P2->>+ P55: uses
    P55-->>- P2: return
    P2->>+ P56: uses
    P56-->>- P2: return
    P2->>+ P57: uses
    P57-->>- P2: return
    P2->>+ P58: uses
    P58-->>- P2: return
    P2->>+ P59: uses
    P59-->>- P2: return
    P2->>+ P60: uses
    P60-->>- P2: return
    P2->>+ P61: uses
    P61-->>- P2: return
    P2->>+ P62: uses
    P62-->>- P2: return
    P2->>+ P63: uses
    P63-->>- P2: return
    P2->>+ P64: uses
    P64-->>- P2: return
    P2->>+ P65: uses
    P65-->>- P2: return
    P2->>+ P66: uses
    P66-->>- P2: return
    P2->>+ P67: uses
    P67-->>- P2: return
    P2->>+ P68: uses
    P68-->>- P2: return
    P2->>+ P69: uses
    P69-->>- P2: return
    P2->>+ P70: uses
    P70-->>- P2: return
    P2->>+ P71: uses
    P71-->>- P2: return
    P2->>+ P72: uses
    P72-->>- P2: return
    P2->>+ P73: uses
    P73-->>- P2: return
    P2->>+ P74: uses
    P74-->>- P2: return
    P2->>+ P75: uses
    P75-->>- P2: return
    P2->>+ P76: uses
    P76-->>- P2: return
    P2->>+ P77: uses
    P77-->>- P2: return
    P2->>+ P78: uses
    P78-->>- P2: return
    P2->>+ P79: uses
    P79-->>- P2: return
    P2->>+ P80: calls
    P80-->>- P2: return
    P2->>+ P81: uses
    P81-->>- P2: return
    P2->>+ P82: uses
    P82-->>- P2: return
    P2->>+ P83: uses
    P83-->>- P2: return
    P2->>+ P84: uses
    P84-->>- P2: return
    P2->>+ P85: uses
    P85-->>- P2: return
    P2->>+ P86: uses
    P86-->>- P2: return
    P2->>+ P87: uses
    P87-->>- P2: return
    P2->>+ P88: uses
    P88-->>- P2: return
    P2->>+ P89: uses
    P89-->>- P2: return
    P2->>+ P90: uses
    P90-->>- P2: return
    P2->>+ P91: uses
    P91-->>- P2: return
    P2->>+ P92: uses
    P92-->>- P2: return
    P2->>+ P93: uses
    P93-->>- P2: return
    P2->>+ P94: uses
    P94-->>- P2: return
    P2->>+ P95: calls
    P95-->>- P2: return
    P2->>+ P96: calls
    P96-->>- P2: return
    P2->>+ P97: calls
    P97-->>- P2: return
    P2->>+ P98: calls
    P98-->>- P2: return
    P2->>+ P99: uses
    P99-->>- P2: return
    P2->>+ P100: uses
    P100-->>- P2: return
    P2->>+ P101: uses
    P101-->>- P2: return
    P2->>+ P102: uses
    P102-->>- P2: return
    P2->>+ P103: uses
    P103-->>- P2: return
    P2->>+ P104: uses
    P104-->>- P2: return
    P2->>+ P105: uses
    P105-->>- P2: return
    P2->>+ P106: calls
    P106-->>- P2: return
    P2->>+ P107: uses
    P107-->>- P2: return
    P2->>+ P108: uses
    P108-->>- P2: return
    P2->>+ P109: uses
    P109-->>- P2: return
    P2->>+ P110: uses
    P110-->>- P2: return
    P2->>+ P111: uses
    P111-->>- P2: return
    P2->>+ P112: uses
    P112-->>- P2: return
    P2->>+ P113: uses
    P113-->>- P2: return
    P2->>+ P114: uses
    P114-->>- P2: return
    P2->>+ P115: uses
    P115-->>- P2: return
    P2->>+ P116: uses
    P116-->>- P2: return
    P2->>+ P117: uses
    P117-->>- P2: return
    P2->>+ P118: uses
    P118-->>- P2: return
    P2->>+ P119: uses
    P119-->>- P2: return
    P2->>+ P120: uses
    P120-->>- P2: return
    P2->>+ P121: uses
    P121-->>- P2: return
    P2->>+ P122: uses
    P122-->>- P2: return
    P2->>+ P123: uses
    P123-->>- P2: return
    P2->>+ P124: uses
    P124-->>- P2: return
    P2->>+ P125: uses
    P125-->>- P2: return
    P2->>+ P126: uses
    P126-->>- P2: return
    P2->>+ P127: uses
    P127-->>- P2: return
    P2->>+ P128: uses
    P128-->>- P2: return
    P2->>+ P129: uses
    P129-->>- P2: return
    P2->>+ P130: uses
    P130-->>- P2: return
    P2->>+ P131: uses
    P131-->>- P2: return
    P2->>+ P132: uses
    P132-->>- P2: return
    P2->>+ P133: uses
    P133-->>- P2: return
    P2->>+ P134: uses
    P134-->>- P2: return
    P2->>+ P135: uses
    P135-->>- P2: return
    P2->>+ P136: uses
    P136-->>- P2: return
    P2->>+ P137: uses
    P137-->>- P2: return
    P2->>+ P138: uses
    P138-->>- P2: return
    P2->>+ P139: uses
    P139-->>- P2: return
    P2->>+ P140: uses
    P140-->>- P2: return
    P2->>+ P141: uses
    P141-->>- P2: return
    P2->>+ P142: uses
    P142-->>- P2: return
    P2->>+ P143: uses
    P143-->>- P2: return
    P2->>+ P144: uses
    P144-->>- P2: return
    P2->>+ P145: uses
    P145-->>- P2: return
    P2->>+ P146: uses
    P146-->>- P2: return
    P2->>+ P147: uses
    P147-->>- P2: return
    P2->>+ P148: uses
    P148-->>- P2: return
    P2->>+ P149: uses
    P149-->>- P2: return
    P2->>+ P150: uses
    P150-->>- P2: return
    P2->>+ P151: calls
    P151-->>- P2: return
    P2->>+ P152: calls
    P152-->>- P2: return
    P2->>+ P153: calls
    P153-->>- P2: return
    P2->>+ P154: calls
    P154-->>- P2: return
    P2->>+ P155: uses
    P155-->>- P2: return
    P2->>+ P156: uses
    P156-->>- P2: return
    P2->>+ P157: uses
    P157-->>- P2: return
    P2->>+ P158: uses
    P158-->>- P2: return
    P2->>+ P159: uses
    P159-->>- P2: return
    P2->>+ P160: uses
    P160-->>- P2: return
    P2->>+ P161: uses
    P161-->>- P2: return
    P2->>+ P162: uses
    P162-->>- P2: return
    P2->>+ P163: uses
    P163-->>- P2: return
    P2->>+ P164: uses
    P164-->>- P2: return
    P2->>+ P165: uses
    P165-->>- P2: return
    P2->>+ P166: uses
    P166-->>- P2: return
    P2->>+ P167: uses
    P167-->>- P2: return
    P2->>+ P168: calls
    P168-->>- P2: return
    P1->>+ P169: uses
    P169-->>- P1: return
    P1->>+ P170: uses
    P170-->>- P1: return
    P1->>+ P171: uses
    P171-->>- P1: return
    P1->>+ P172: uses
    P172-->>- P1: return
    P1->>+ P173: uses
    P173-->>- P1: return
    P1->>+ P174: uses
    P174-->>- P1: return
    P1->>+ P175: uses
    P175-->>- P1: return
    P1->>+ P176: uses
    P176-->>- P1: return
    P1->>+ P177: uses
    P177-->>- P1: return
    P1->>+ P178: uses
    P178-->>- P1: return
    P1->>+ P179: uses
    P179-->>- P1: return
    P1->>+ P180: uses
    P180-->>- P1: return
    P1->>+ P38: uses
    P38-->>- P1: return
    P1->>+ P39: uses
    P39-->>- P1: return
    P1->>+ P40: uses
    P40-->>- P1: return
    P1->>+ P41: uses
    P41-->>- P1: return
    P1->>+ P42: uses
    P42-->>- P1: return
    P1->>+ P43: uses
    P43-->>- P1: return
    P1->>+ P44: uses
    P44-->>- P1: return
    P1->>+ P45: uses
    P45-->>- P1: return
    P1->>+ P181: uses
    P181-->>- P1: return
    P1->>+ P182: uses
    P182-->>- P1: return
    P1->>+ P183: uses
    P183-->>- P1: return
    P1->>+ P184: uses
    P184-->>- P1: return
    P1->>+ P185: uses
    P185-->>- P1: return
    P1->>+ P186: uses
    P186-->>- P1: return
    P1->>+ P187: uses
    P187-->>- P1: return
    P1->>+ P188: uses
    P188-->>- P1: return
    P1->>+ P189: uses
    P189-->>- P1: return
    P1->>+ P190: uses
    P190-->>- P1: return
    P1->>+ P191: uses
    P191-->>- P1: return
    P1->>+ P192: uses
    P192-->>- P1: return
    P0->>+ P3: uses
    P3-->>- P0: return
    P0->>+ P4: uses
    P4-->>- P0: return
    P0->>+ P5: uses
    P5-->>- P0: return
    P0->>+ P6: uses
    P6-->>- P0: return
    P0->>+ P7: uses
    P7-->>- P0: return
    P0->>+ P8: uses
    P8-->>- P0: return
    P0->>+ P9: uses
    P9-->>- P0: return
    P0->>+ P10: uses
    P10-->>- P0: return
    P0->>+ P11: uses
    P11-->>- P0: return
    P0->>+ P12: uses
    P12-->>- P0: return
    P0->>+ P13: uses
    P13-->>- P0: return
    P0->>+ P14: uses
    P14-->>- P0: return
    P0->>+ P15: uses
    P15-->>- P0: return
    P0->>+ P16: uses
    P16-->>- P0: return
    P0->>+ P17: uses
    P17-->>- P0: return
    P0->>+ P18: uses
    P18-->>- P0: return
    P0->>+ P19: uses
    P19-->>- P0: return
    P0->>+ P20: uses
    P20-->>- P0: return
    P0->>+ P21: uses
    P21-->>- P0: return
    P0->>+ P22: uses
    P22-->>- P0: return
    P0->>+ P23: uses
    P23-->>- P0: return
    P0->>+ P24: uses
    P24-->>- P0: return
    P0->>+ P25: uses
    P25-->>- P0: return
    P0->>+ P26: uses
    P26-->>- P0: return
    P0->>+ P27: uses
    P27-->>- P0: return
    P0->>+ P28: uses
    P28-->>- P0: return
    P0->>+ P29: uses
    P29-->>- P0: return
    P0->>+ P30: uses
    P30-->>- P0: return
    P0->>+ P31: uses
    P31-->>- P0: return
    P0->>+ P193: uses
    P193-->>- P0: return
    P0->>+ P32: uses
    P32-->>- P0: return
    P0->>+ P33: uses
    P33-->>- P0: return
    P0->>+ P34: uses
    P34-->>- P0: return
    P0->>+ P35: uses
    P35-->>- P0: return
    P0->>+ P36: uses
    P36-->>- P0: return
    P0->>+ P37: uses
    P37-->>- P0: return
    P0->>+ P38: uses
    P38-->>- P0: return
    P0->>+ P39: uses
    P39-->>- P0: return
    P0->>+ P40: uses
    P40-->>- P0: return
    P0->>+ P41: uses
    P41-->>- P0: return
    P0->>+ P42: uses
    P42-->>- P0: return
    P0->>+ P43: uses
    P43-->>- P0: return
    P0->>+ P44: uses
    P44-->>- P0: return
    P0->>+ P45: uses
    P45-->>- P0: return
    P0->>+ P46: calls
    P46-->>- P0: return
    P0->>+ P194: uses
    P194-->>- P0: return
    P0->>+ P195: uses
    P195-->>- P0: return
    P0->>+ P196: uses
    P196-->>- P0: return
    P0->>+ P197: uses
    P197-->>- P0: return
    P0->>+ P198: uses
    P198-->>- P0: return
    P0->>+ P199: uses
    P199-->>- P0: return
    P0->>+ P200: uses
    P200-->>- P0: return
    P0->>+ P201: uses
    P201-->>- P0: return
    P0->>+ P202: uses
    P202-->>- P0: return
    P0->>+ P47: calls
    P47-->>- P0: return
    P0->>+ P48: calls
    P48-->>- P0: return
    P0->>+ P49: uses
    P49-->>- P0: return
    P0->>+ P50: uses
    P50-->>- P0: return
    P0->>+ P51: uses
    P51-->>- P0: return
    P0->>+ P52: uses
    P52-->>- P0: return
    P0->>+ P53: uses
    P53-->>- P0: return
    P0->>+ P54: uses
    P54-->>- P0: return
    P0->>+ P55: uses
    P55-->>- P0: return
    P0->>+ P56: uses
    P56-->>- P0: return
    P0->>+ P57: uses
    P57-->>- P0: return
    P0->>+ P58: uses
    P58-->>- P0: return
    P0->>+ P59: uses
    P59-->>- P0: return
    P0->>+ P203: uses
    P203-->>- P0: return
    P0->>+ P204: uses
    P204-->>- P0: return
    P0->>+ P205: uses
    P205-->>- P0: return
    P0->>+ P206: uses
    P206-->>- P0: return
    P0->>+ P207: uses
    P207-->>- P0: return
    P0->>+ P208: uses
    P208-->>- P0: return
    P0->>+ P209: uses
    P209-->>- P0: return
    P0->>+ P210: uses
    P210-->>- P0: return
    P0->>+ P211: uses
    P211-->>- P0: return
    P0->>+ P212: uses
    P212-->>- P0: return
    P0->>+ P213: uses
    P213-->>- P0: return
    P0->>+ P214: uses
    P214-->>- P0: return
    P0->>+ P215: uses
    P215-->>- P0: return
    P0->>+ P216: uses
    P216-->>- P0: return
    P0->>+ P217: uses
    P217-->>- P0: return
    P0->>+ P64: uses
    P64-->>- P0: return
    P0->>+ P65: uses
    P65-->>- P0: return
    P0->>+ P66: uses
    P66-->>- P0: return
    P0->>+ P69: uses
    P69-->>- P0: return
    P0->>+ P70: uses
    P70-->>- P0: return
    P0->>+ P71: uses
    P71-->>- P0: return
    P0->>+ P72: uses
    P72-->>- P0: return
    P0->>+ P218: calls
    P218-->>- P0: return
    P0->>+ P219: calls
    P219-->>- P0: return
    P0->>+ P220: calls
    P220-->>- P0: return
    P0->>+ P73: uses
    P73-->>- P0: return
    P0->>+ P221: uses
    P221-->>- P0: return
    P0->>+ P222: uses
    P222-->>- P0: return
    P0->>+ P223: uses
    P223-->>- P0: return
    P0->>+ P224: uses
    P224-->>- P0: return
    P0->>+ P74: uses
    P74-->>- P0: return
    P0->>+ P75: uses
    P75-->>- P0: return
    P0->>+ P76: uses
    P76-->>- P0: return
    P0->>+ P77: uses
    P77-->>- P0: return
    P0->>+ P78: uses
    P78-->>- P0: return
    P0->>+ P79: uses
    P79-->>- P0: return
    P0->>+ P225: calls
    P225-->>- P0: return
    P0->>+ P226: calls
    P226-->>- P0: return
    P0->>+ P227: calls
    P227-->>- P0: return
    P0->>+ P80: calls
    P80-->>- P0: return
    P0->>+ P81: uses
    P81-->>- P0: return
    P0->>+ P82: uses
    P82-->>- P0: return
    P0->>+ P83: uses
    P83-->>- P0: return
    P0->>+ P84: uses
    P84-->>- P0: return
    P0->>+ P85: uses
    P85-->>- P0: return
    P0->>+ P86: uses
    P86-->>- P0: return
    P0->>+ P87: uses
    P87-->>- P0: return
    P0->>+ P88: uses
    P88-->>- P0: return
    P0->>+ P89: uses
    P89-->>- P0: return
    P0->>+ P228: uses
    P228-->>- P0: return
    P0->>+ P229: uses
    P229-->>- P0: return
    P0->>+ P230: uses
    P230-->>- P0: return
    P0->>+ P231: uses
    P231-->>- P0: return
    P0->>+ P232: uses
    P232-->>- P0: return
    P0->>+ P233: uses
    P233-->>- P0: return
    P0->>+ P234: uses
    P234-->>- P0: return
    P0->>+ P235: uses
    P235-->>- P0: return
    P0->>+ P236: uses
    P236-->>- P0: return
    P0->>+ P237: uses
    P237-->>- P0: return
    P0->>+ P238: uses
    P238-->>- P0: return
    P0->>+ P239: uses
    P239-->>- P0: return
    P0->>+ P240: uses
    P240-->>- P0: return
    P0->>+ P241: uses
    P241-->>- P0: return
    P0->>+ P242: uses
    P242-->>- P0: return
    P0->>+ P243: uses
    P243-->>- P0: return
    P0->>+ P244: uses
    P244-->>- P0: return
    P0->>+ P245: uses
    P245-->>- P0: return
    P0->>+ P246: uses
    P246-->>- P0: return
    P0->>+ P247: uses
    P247-->>- P0: return
    P0->>+ P248: uses
    P248-->>- P0: return
    P0->>+ P249: uses
    P249-->>- P0: return
    P0->>+ P250: uses
    P250-->>- P0: return
    P0->>+ P251: uses
    P251-->>- P0: return
    P0->>+ P90: uses
    P90-->>- P0: return
    P0->>+ P91: uses
    P91-->>- P0: return
    P0->>+ P92: uses
    P92-->>- P0: return
    P0->>+ P93: uses
    P93-->>- P0: return
    P0->>+ P94: uses
    P94-->>- P0: return
    P0->>+ P95: calls
    P95-->>- P0: return
    P0->>+ P96: calls
    P96-->>- P0: return
    P0->>+ P97: calls
    P97-->>- P0: return
    P0->>+ P252: uses
    P252-->>- P0: return
    P0->>+ P253: uses
    P253-->>- P0: return
    P0->>+ P254: uses
    P254-->>- P0: return
    P0->>+ P255: uses
    P255-->>- P0: return
    P0->>+ P256: uses
    P256-->>- P0: return
    P0->>+ P257: uses
    P257-->>- P0: return
    P0->>+ P258: uses
    P258-->>- P0: return
    P0->>+ P259: uses
    P259-->>- P0: return
    P0->>+ P260: uses
    P260-->>- P0: return
    P0->>+ P261: uses
    P261-->>- P0: return
    P0->>+ P262: uses
    P262-->>- P0: return
    P0->>+ P263: uses
    P263-->>- P0: return
    P0->>+ P264: uses
    P264-->>- P0: return
    P0->>+ P99: uses
    P99-->>- P0: return
    P0->>+ P100: uses
    P100-->>- P0: return
    P0->>+ P101: uses
    P101-->>- P0: return
    P0->>+ P102: uses
    P102-->>- P0: return
    P0->>+ P103: uses
    P103-->>- P0: return
    P0->>+ P104: uses
    P104-->>- P0: return
    P0->>+ P105: uses
    P105-->>- P0: return
    P0->>+ P265: uses
    P265-->>- P0: return
    P0->>+ P266: uses
    P266-->>- P0: return
    P0->>+ P267: uses
    P267-->>- P0: return
    P0->>+ P268: uses
    P268-->>- P0: return
    P0->>+ P269: uses
    P269-->>- P0: return
    P0->>+ P270: calls
    P270-->>- P0: return
    P0->>+ P271: calls
    P271-->>- P0: return
    P0->>+ P106: calls
    P106-->>- P0: return
    P0->>+ P272: calls
    P272-->>- P0: return
    P0->>+ P273: calls
    P273-->>- P0: return
    P0->>+ P274: calls
    P274-->>- P0: return
    P0->>+ P107: uses
    P107-->>- P0: return
    P0->>+ P108: uses
    P108-->>- P0: return
    P0->>+ P109: uses
    P109-->>- P0: return
    P0->>+ P110: uses
    P110-->>- P0: return
    P0->>+ P111: uses
    P111-->>- P0: return
    P0->>+ P112: uses
    P112-->>- P0: return
    P0->>+ P113: uses
    P113-->>- P0: return
    P0->>+ P114: uses
    P114-->>- P0: return
    P0->>+ P115: uses
    P115-->>- P0: return
    P0->>+ P116: uses
    P116-->>- P0: return
    P0->>+ P117: uses
    P117-->>- P0: return
    P0->>+ P118: uses
    P118-->>- P0: return
    P0->>+ P119: uses
    P119-->>- P0: return
    P0->>+ P120: uses
    P120-->>- P0: return
    P0->>+ P121: uses
    P121-->>- P0: return
    P0->>+ P122: uses
    P122-->>- P0: return
    P0->>+ P123: uses
    P123-->>- P0: return
    P0->>+ P124: uses
    P124-->>- P0: return
    P0->>+ P125: uses
    P125-->>- P0: return
    P0->>+ P126: uses
    P126-->>- P0: return
    P0->>+ P127: uses
    P127-->>- P0: return
    P0->>+ P128: uses
    P128-->>- P0: return
    P0->>+ P129: uses
    P129-->>- P0: return
    P0->>+ P130: uses
    P130-->>- P0: return
    P0->>+ P131: uses
    P131-->>- P0: return
    P0->>+ P132: uses
    P132-->>- P0: return
    P0->>+ P141: uses
    P141-->>- P0: return
    P0->>+ P142: uses
    P142-->>- P0: return
    P0->>+ P143: uses
    P143-->>- P0: return
    P0->>+ P144: uses
    P144-->>- P0: return
    P0->>+ P145: uses
    P145-->>- P0: return
    P0->>+ P146: uses
    P146-->>- P0: return
    P0->>+ P147: uses
    P147-->>- P0: return
    P0->>+ P148: uses
    P148-->>- P0: return
    P0->>+ P149: uses
    P149-->>- P0: return
    P0->>+ P150: uses
    P150-->>- P0: return
    P0->>+ P275: uses
    P275-->>- P0: return
    P0->>+ P276: uses
    P276-->>- P0: return
    P0->>+ P277: uses
    P277-->>- P0: return
    P0->>+ P278: uses
    P278-->>- P0: return
    P0->>+ P279: uses
    P279-->>- P0: return
    P0->>+ P280: uses
    P280-->>- P0: return
    P0->>+ P281: uses
    P281-->>- P0: return
    P0->>+ P282: calls
    P282-->>- P0: return
    P0->>+ P283: calls
    P283-->>- P0: return
    P0->>+ P284: calls
    P284-->>- P0: return
    P0->>+ P285: calls
    P285-->>- P0: return
    P0->>+ P286: calls
    P286-->>- P0: return
    P0->>+ P287: calls
    P287-->>- P0: return
    P0->>+ P288: calls
    P288-->>- P0: return
    P0->>+ P289: calls
    P289-->>- P0: return
    P0->>+ P290: calls
    P290-->>- P0: return
    P0->>+ P151: calls
    P151-->>- P0: return
    P0->>+ P152: calls
    P152-->>- P0: return
    P0->>+ P153: calls
    P153-->>- P0: return
    P0->>+ P291: calls
    P291-->>- P0: return
    P0->>+ P292: calls
    P292-->>- P0: return
    P0->>+ P154: calls
    P154-->>- P0: return
    P0->>+ P293: calls
    P293-->>- P0: return
    P0->>+ P294: calls
    P294-->>- P0: return
    P0->>+ P295: calls
    P295-->>- P0: return
    P0->>+ P296: calls
    P296-->>- P0: return
    P0->>+ P297: calls
    P297-->>- P0: return
    P0->>+ P298: calls
    P298-->>- P0: return
    P0->>+ P299: calls
    P299-->>- P0: return
    P0->>+ P300: calls
    P300-->>- P0: return
```

## Connections by Relation

### calls
- [[create_test_user_and_org()]] `INFERRED`
- [[register_or_login()]] `INFERRED`
- [[create_test_user_and_org()]] `INFERRED`
- [[complete_profile()]] `INFERRED`
- [[login()]] `INFERRED`
- [[test_uc118_schema_instantiation()]] `INFERRED`
- [[refresh_token()]] `INFERRED`
- [[setup_db()]] `INFERRED`
- [[dashboard_setup()]] `INFERRED`
- [[test_data()]] `INFERRED`
- [[ensure_organization()]] `INFERRED`
- [[test_uc011_sole_owner_blocking()]] `INFERRED`
- [[test_setup()]] `INFERRED`
- [[create_organization()]] `INFERRED`
- [[auto_create_personal_organization()]] `INFERRED`
- [[setup_db()]] `INFERRED`
- [[test_setup()]] `INFERRED`
- [[test_setup()]] `INFERRED`
- [[test_setup()]] `INFERRED`
- [[setup_db()]] `INFERRED`

### contains
- [[organization.py]] `EXTRACTED`

### inherits
- [[Base]] `EXTRACTED`

### uses
- [[AuthService]] `INFERRED`
- [[UC-014: Provision commercial or custom organization.]] `INFERRED`
- [[UC-014: Auto-provision personal organization for a user during registration or s]] `INFERRED`
- [[Retrieve organizations list.]] `INFERRED`
- [[UC-015: Switch active organization context for user.]] `INFERRED`
- [[UC-015: Get active organization for user.]] `INFERRED`
- [[Retrieve organization details by ID.]] `INFERRED`
- [[UC-017: Edit Organization Profile Details.     Enforces ISO 4217 currency valida]] `INFERRED`
- [[UC-018: Invite Driver / Manager via Email or Phone.     Generates a secure 64-ch]] `INFERRED`
- [[UC-018: List pending organization invitations.]] `INFERRED`
- [[UC-021: Remove Member from Organization.     Prevents owner removal. Unassigns u]] `INFERRED`
- [[UC-022: Cancel Pending Member Invitation.]] `INFERRED`
- [[UC-023: Soft Delete Organization & Child Entities.     Rejects personal org dele]] `INFERRED`
- [[UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.]] `INFERRED`
- [[UC-024: Register New Vehicle with organization quota validation & duplicate VIN]] `INFERRED`
- [[UC-025: List Organization Vehicles directory with status, search, fuel type, and]] `INFERRED`
- [[UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur]] `INFERRED`
- [[UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).]] `INFERRED`
- [[UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow]] `INFERRED`
- [[UC-028: Soft Delete Vehicle & Write Audit Log.     Frees up 1 vehicle slot in a]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*