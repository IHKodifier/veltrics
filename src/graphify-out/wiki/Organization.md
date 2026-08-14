# Organization

> God node · 233 connections · [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\organization.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/organization.py#L8)

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
    participant P46 as register_or_login()
    participant P47 as UC-014: Provision commercial or custom organization.
    participant P48 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P49 as Retrieve organizations list.
    participant P50 as UC-015: Switch active organization context for user.
    participant P51 as UC-015: Get active organization for user.
    participant P52 as Retrieve organization details by ID.
    participant P53 as UC-016: Invite Team Member to Organization.     Generates a secure 64-character
    participant P54 as UC-016: List pending organization invitations.
    participant P55 as UC-019: Inspect / validate organization invitation token details.     Returns HT
    participant P56 as UC-019: Accept Organization Invitation for existing authenticated user.
    participant P57 as UC-020: Redeem Org Invitation Code for new user during signup/onboard.
    participant P58 as Test 1: Verify all 7 core data models instantiate clean database tables.
    participant P59 as Test 2: Verify database seeding populates master vehicle catalogue idempotently.
    participant P60 as Test 3: Verify POST /api/v1/admin/seed endpoint.
    participant P61 as test_data()
    participant P62 as AC 1: GIVEN an authenticated user     WHEN DELETE /api/v1/users/me is invoked
    participant P63 as AC 2: GIVEN a user who is the sole owner of an active non-personal organization
    participant P64 as AC 3: GIVEN a soft-deleted user account     WHEN attempting to authenticate, ac
    participant P65 as AC 1: System creates immutable AuditLog entry upon user registration.
    participant P66 as AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadat
    participant P67 as A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None.
    participant P68 as AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS
    participant P69 as AC 4: System records USER_LOGOUT audit entry upon session termination.
    participant P70 as Edge Case: Audit log DB write exception is handled safely and does not block use
    participant P71 as Test 1: Verify GET /api/v1/vehicles/types?q=Toyota returns seeded Toyota models.
    participant P72 as Test 2: Verify POST /api/v1/vehicles registers new vehicle with tenant organizat
    participant P73 as Test 3: Verify duplicate VIN within same organization returns HTTP 409 Conflict.
    participant P74 as Test 4: Verify exceeding max_vehicles quota (max=2 for sample_org) returns HTTP
    participant P75 as Test 5: Verify custom make/model is dynamically indexed into VehicleType catalog
    participant P76 as ensure_organization()
    participant P77 as test_uc011_sole_owner_blocking()
    participant P78 as test_setup()
    participant P79 as UC-016: Owner can create organization invitation, generating a secure 64-char to
    participant P80 as UC-016: Inviting with invalid or blank email yields HTTP 422 Unprocessable Entit
    participant P81 as UC-016: Inviting with unsupported role string yields HTTP 422 Unprocessable Enti
    participant P82 as UC-016: Re-inviting same email updates existing invitation token and TTL without
    participant P83 as UC-016: Non-owner caller attempting to send invitation yields HTTP 403 Forbidden
    participant P84 as UC-016: Owner can list all pending invitations for organization.
    participant P85 as UC-016: Listing invitations for non-existent org yields HTTP 404 Not Found.
    participant P86 as setup_db()
    participant P87 as AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr
    participant P88 as AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL
    participant P89 as AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store \"facebook\" insid
    participant P90 as Alternate Flow A1: Account Linking     If email matches existing account with d
    participant P91 as Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Requ
    participant P92 as AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT
    participant P93 as Alternate Flow A1: Account Linking     If user signed up via Google, submitting
    participant P94 as Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu
    participant P95 as Edge Case: Missing email or missing password for email auth provider returns HTT
    participant P96 as AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200
    participant P97 as Edge Case: Incorrect password returns HTTP 401 Unauthorized.
    participant P98 as Edge Case: Unregistered email returns HTTP 401 Unauthorized.
    participant P99 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P100 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P101 as AC 1: WHEN an existing Google user signs in,     THE SYSTEM SHALL return HTTP 2
    participant P102 as AC 2: WHEN an existing Facebook user signs in,     THE SYSTEM SHALL return HTTP
    participant P103 as AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,
    participant P104 as AC 4 (Account Linking Flow A1): WHEN an existing user registered via email
    participant P105 as Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized.
    participant P106 as Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized.
    participant P107 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P108 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P109 as AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u
    participant P110 as AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P
    participant P111 as AC 3: GIVEN a profile update request with invalid display name length (< 2 chars
    participant P112 as AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro
    participant P113 as AC 1: GIVEN an authenticated user session with a valid refresh token     WHEN s
    participant P114 as AC 2: GIVEN a revoked refresh token     WHEN submitted to POST /api/v1/auth/ref
    participant P115 as AC 3: GIVEN a malformed or invalid refresh token     WHEN submitted to POST /ap
    participant P116 as AC 4: GIVEN a refresh token that has already been revoked     WHEN logout is ca
    participant P117 as AC 1: WHEN GET /api/v1/users/me/sessions is called THE SYSTEM SHALL return activ
    participant P118 as AC 2: User can revoke a specific session.
    participant P119 as Acceptance Criterion: WHEN a session is revoked via API THE SYSTEM SHALL block a
    participant P120 as A1: User can revoke all other active sessions.
    participant P121 as UC-014: POST /api/v1/organizations creates commercial organization and sets owne
    participant P122 as UC-014: POST /api/v1/organizations/personal auto-creates personal organization f
    participant P123 as UC-014: Blank or whitespace organization name rejected with HTTP 422.
    participant P124 as UC-014: GET /api/v1/organizations?user_id={id} returns list of user organization
    participant P125 as UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found.
    participant P126 as UC-015: POST /api/v1/organizations/switch switches active context for valid user
    participant P127 as UC-015: Switch attempt to organization owned by another user yields HTTP 403 For
    participant P128 as UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found.
    participant P129 as UC-015: GET /api/v1/organizations/active returns current primary organization fo
    participant P130 as UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 N
    participant P131 as setup_db()
    participant P132 as test_setup()
    participant P133 as test_setup()
    participant P134 as test_data()
    participant P135 as AC 1: WHEN a registered user requests a password reset link/token for their emai
    participant P136 as AC 2: WHEN a reset request is submitted for a non-existent email     THE SYSTEM
    participant P137 as AC 3: WHEN a user submits a valid reset token and strong new password     THE S
    participant P138 as AC 4: WHEN an invalid token or token of wrong type (e.g. access token) is submit
    participant P139 as AC 5: WHEN a new password does not satisfy password policy (min 8 chars, 1 upper
    participant P140 as AC 1: GIVEN an authenticated registered user     WHEN they request GET /api/v1/
    participant P141 as AC 2: GIVEN an authenticated user updating their profile details     WHEN they
    participant P142 as AC 3: GIVEN a profile update request with invalid full name length (< 2 characte
    participant P143 as AC 4: GIVEN an unauthenticated request to profile endpoints without user identit
    participant P144 as AC 1: GIVEN a valid active refresh token     WHEN submitted to POST /api/v1/aut
    participant P145 as AC 2: GIVEN an invalid, expired, or non-refresh token (e.g. access or reset toke
    participant P146 as AC 3: GIVEN a refresh token for a disabled or soft-deleted user account     WHE
    participant P147 as AC 4: GIVEN a newly issued access token from POST /api/v1/auth/refresh     WHEN
    participant P148 as test_setup()
    participant P149 as AuditLog
    participant P150 as UserOrganization
    participant P151 as AuthSessionDTO
    participant P152 as SessionRevokeResponse
    participant P153 as UC-004: User Password Authentication & Session Initiation     Authenticates reg
    participant P154 as UC-006: Forgot Password Request     Issues a password reset JWT token with 5-mi
    participant P155 as UC-006: Password Reset Execution     Verifies reset token, validates password p
    participant P156 as UC-009: Session Refresh & Access Token Renewal     Validates active refresh tok
    participant P157 as UC-010: User Sign Out & Token Revocation     Revokes the provided refresh token
    participant P158 as UserDTO
    participant P159 as OrganizationDTO
    participant P160 as UserSessionDTO
    participant P161 as AuditService
    participant P162 as ForgotPasswordResponse
    participant P163 as ResetPasswordResponse
    participant P164 as RefreshTokenResponse
    participant P165 as LogoutResponse
    participant P166 as UserSession
    participant P167 as RegisterRequest
    participant P168 as LoginRequest
    participant P169 as ForgotPasswordRequest
    participant P170 as ResetPasswordRequest
    participant P171 as RefreshTokenRequest
    participant P172 as LogoutRequest
    participant P173 as UC-053: Get Trip Summary & Tax Deduction Metrics.
    participant P174 as UC-052: Start GPS Trip Tracking session.
    participant P175 as UC-052: Stop active GPS Trip Tracking session and calculate distance.
    participant P176 as UC-052 / UC-053: Create trip entry (Manual or completed GPS trip).
    participant P177 as UC-053: View Trip History.
    participant P178 as UC-054: Edit Trip Entry & Classification.
    participant P179 as UC-055: Soft Delete Trip Entry.
    participant P180 as UC-056: Quick-Log Trip from Dashboard.
    participant P181 as UC-057: View Distance & Mileage Summary Analytics.
    participant P182 as UC-058: Log General Fleet Expense.
    participant P183 as UC-059: Expense Category & Cost Summary Metrics.
    participant P184 as UC-059: View Expense History.
    participant P185 as UC-060: Edit Expense Entry.
    participant P186 as UC-061: Soft Delete Expense Entry.
    participant P187 as UC-062: Quick-Log Expense from Dashboard.
    participant P188 as UC-048: View Fuel Efficiency Trends & Aggregate Metrics.
    participant P189 as UC-050: Detect Fuel Anomaly & Theft Alerts - Fetch anomaly logs.
    participant P190 as UC-050 (A1): Manager clears fuel anomaly flag.
    participant P191 as UC-049: Fuel Receipt OCR Auto-Fill (Pro).
    participant P192 as UC-046: Log Fuel Fill-Up Entry.     Automatically updates vehicle current odome
    participant P193 as UC-047 / UC-048: View Fuel Log History with optional pagination.
    participant P194 as UC-051: Edit Fuel Log Entry.     Updates entry, syncs linked ExpenseLog, and re
    participant P195 as UC-051: Soft Delete Fuel Log Entry.     Soft-deletes entry and linked ExpenseLo
    participant P196 as complete_profile()
    participant P197 as login()
    participant P198 as test_uc118_schema_instantiation()
    participant P199 as UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,
    participant P200 as UC-064: Requests for Org 2 return only Org 2's metrics.
    participant P201 as UC-064: Empty organization returns 0 stats so client can render onboarding card.
    participant P202 as UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missin
    participant P203 as refresh_token()
    participant P204 as setup_db()
    participant P205 as dashboard_setup()
    participant P206 as UC-046: Test successful fuel log creation & vehicle current odometer update.
    participant P207 as UC-046 Acceptance Criterion: WHEN a fuel log entry is saved     THE SYSTEM SHAL
    participant P208 as UC-046 Edge Case: Odometer entry lower than vehicle's current odometer -> API re
    participant P209 as UC-046 & UC-047: Verify calculated km/L efficiency on 2nd full tank fill-up.
    participant P210 as UC-047: Test retrieving fuel log history via GET /api/v1/fuel.     Should retur
    participant P211 as UC-047 Acceptance Criterion: WHEN two consecutive full-tank fuel logs are create
    participant P212 as UC-047 Alternate Flow A1: Partial fill-up (is_full_tank = False) skips efficienc
    participant P213 as UC-047 Main Flow 5: If efficiency is 30% lower than vehicle baseline average,
    participant P214 as UC-051 Alternate Flow A1: PATCH /api/v1/fuel/{id} updates entry & recalculates e
    participant P215 as UC-051 Main Flow: DELETE /api/v1/fuel/{id} soft-deletes log & linked expense and
    participant P216 as UC-051 Edge Case: Deleting or patching non-existent log returns HTTP 404.
    participant P217 as UC-034: GET /api/v1/maintenance/schedules should auto-populate schedule template
    participant P218 as UC-034: POST /api/v1/maintenance logs record, updates odometer, and resets sched
    participant P219 as UC-034: POST /api/v1/maintenance rejects negative cost with HTTP 422.
    participant P220 as UC-034: Tenant cross-access rejected.
    participant P221 as UC-036: POST /api/v1/maintenance logs service record and updates linked schedule
    participant P222 as UC-036: Odometer reading > current_odometer_km updates vehicle current_odometer_
    participant P223 as UC-036: Omitting maintenance_schedule_id matches schedule item by task name subs
    participant P224 as UC-036: Rejects negative cost, negative odometer, whitespace service_type, or in
    participant P225 as UC-036: Enforces X-Organization-ID header presence and cross-tenant access prote
    participant P226 as UC-037: GET /api/v1/maintenance/records retrieves service records sorted by serv
    participant P227 as UC-037: Pagination limit and offset parameters operate correctly.
    participant P228 as UC-037: Returns 404 when vehicle_id does not exist in active organization.
    participant P229 as UC-037: Header requirements and cross-tenant boundaries are strictly enforced.
    participant P230 as UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency a
    participant P231 as UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per veh
    participant P232 as UC-035: POST /api/v1/maintenance/schedules creates custom schedule with default
    participant P233 as UC-035: POST /api/v1/maintenance/schedules uses provided last_performed_km and l
    participant P234 as UC-035: Rejects zero/negative intervals or empty task names with 422.
    participant P235 as UC-035: PATCH /api/v1/maintenance/schedules/{id} updates parameters and recalcul
    participant P236 as UC-035: DELETE /api/v1/maintenance/schedules/{id} soft-deletes schedule task.
    participant P237 as UC-035: Header validation and tenant cross-access isolation.
    participant P238 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with empty schedule_ids a
    participant P239 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with specific schedule_id
    participant P240 as UC-038: Returns 404 when vehicle_id is not found in active organization.
    participant P241 as UC-038: Returns 404 when one or more schedule_ids do not belong to the vehicle.
    participant P242 as UC-038: Headers and cross-tenant boundaries are strictly enforced.
    participant P243 as Test 1: Verify PATCH /api/v1/vehicles/{vehicle_id} successfully updates vehicle
    participant P244 as Test 2: Verify updating vehicle under wrong organization_id returns HTTP 403 For
    participant P245 as Test 3: Verify updating non-existent vehicle returns HTTP 404 Not Found.
    participant P246 as Test 4: Verify manual odometer update with discrepancy > 500 km generates an Aud
    participant P247 as Test 5: Verify non-dictionary custom_specs payload returns HTTP 422 Unprocessabl
    participant P248 as create_organization()
    participant P249 as auto_create_personal_organization()
    participant P250 as test_setup()
    participant P251 as test_setup()
    participant P252 as test_setup()
    participant P253 as Test 1: Verify GET /api/v1/vehicles?status=MAINTENANCE returns only vehicles in
    participant P254 as Test 2: Verify search query matches license plate, make, or model.
    participant P255 as Test 3: Verify filtering by province (e.g. Sindh).
    participant P256 as Test 1: Verify GET /api/v1/vehicles/{vehicle_id} returns detailed vehicle metada
    participant P257 as Test 2: Verify non-existent vehicle ID returns HTTP 404 Not Found.
    participant P258 as Test 3: Verify requesting another tenant's vehicle returns HTTP 403 Forbidden.
    participant P259 as Test 4: Verify PATCH /api/v1/vehicles/{vehicle_id}/status updates vehicle status
    participant P260 as setup_db()
    participant P261 as setup_db()
    participant P262 as setup_db()
    participant P263 as test_setup()
    participant P264 as test_setup()
    participant P265 as test_setup()
    participant P266 as test_setup()
    participant P267 as test_setup()
    participant P268 as test_setup()
    participant P269 as setup_db()
    participant P270 as setup_db()
    participant P271 as setup_db()
    participant P272 as setup_db()
    participant P273 as setup_db()
    participant P274 as setup_db()
    participant P275 as sample_fleet()
    participant P276 as test_setup()
    participant P277 as test_setup()
    participant P278 as sample_org()
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
    P2->>+ P47: uses
    P47-->>- P2: return
    P2->>+ P48: uses
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
    P2->>+ P61: calls
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
    P2->>+ P76: calls
    P76-->>- P2: return
    P2->>+ P77: calls
    P77-->>- P2: return
    P2->>+ P78: calls
    P78-->>- P2: return
    P2->>+ P79: uses
    P79-->>- P2: return
    P2->>+ P80: uses
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
    P2->>+ P86: calls
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
    P2->>+ P95: uses
    P95-->>- P2: return
    P2->>+ P96: uses
    P96-->>- P2: return
    P2->>+ P97: uses
    P97-->>- P2: return
    P2->>+ P98: uses
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
    P2->>+ P106: uses
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
    P2->>+ P131: calls
    P131-->>- P2: return
    P2->>+ P132: calls
    P132-->>- P2: return
    P2->>+ P133: calls
    P133-->>- P2: return
    P2->>+ P134: calls
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
    P2->>+ P148: calls
    P148-->>- P2: return
    P1->>+ P149: uses
    P149-->>- P1: return
    P1->>+ P150: uses
    P150-->>- P1: return
    P1->>+ P151: uses
    P151-->>- P1: return
    P1->>+ P152: uses
    P152-->>- P1: return
    P1->>+ P153: uses
    P153-->>- P1: return
    P1->>+ P154: uses
    P154-->>- P1: return
    P1->>+ P155: uses
    P155-->>- P1: return
    P1->>+ P156: uses
    P156-->>- P1: return
    P1->>+ P157: uses
    P157-->>- P1: return
    P1->>+ P158: uses
    P158-->>- P1: return
    P1->>+ P159: uses
    P159-->>- P1: return
    P1->>+ P160: uses
    P160-->>- P1: return
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
    P1->>+ P161: uses
    P161-->>- P1: return
    P1->>+ P162: uses
    P162-->>- P1: return
    P1->>+ P163: uses
    P163-->>- P1: return
    P1->>+ P164: uses
    P164-->>- P1: return
    P1->>+ P165: uses
    P165-->>- P1: return
    P1->>+ P166: uses
    P166-->>- P1: return
    P1->>+ P167: uses
    P167-->>- P1: return
    P1->>+ P168: uses
    P168-->>- P1: return
    P1->>+ P169: uses
    P169-->>- P1: return
    P1->>+ P170: uses
    P170-->>- P1: return
    P1->>+ P171: uses
    P171-->>- P1: return
    P1->>+ P172: uses
    P172-->>- P1: return
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
    P0->>+ P173: uses
    P173-->>- P0: return
    P0->>+ P174: uses
    P174-->>- P0: return
    P0->>+ P175: uses
    P175-->>- P0: return
    P0->>+ P176: uses
    P176-->>- P0: return
    P0->>+ P177: uses
    P177-->>- P0: return
    P0->>+ P178: uses
    P178-->>- P0: return
    P0->>+ P179: uses
    P179-->>- P0: return
    P0->>+ P180: uses
    P180-->>- P0: return
    P0->>+ P181: uses
    P181-->>- P0: return
    P0->>+ P46: calls
    P46-->>- P0: return
    P0->>+ P47: uses
    P47-->>- P0: return
    P0->>+ P48: uses
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
    P0->>+ P182: uses
    P182-->>- P0: return
    P0->>+ P183: uses
    P183-->>- P0: return
    P0->>+ P184: uses
    P184-->>- P0: return
    P0->>+ P185: uses
    P185-->>- P0: return
    P0->>+ P186: uses
    P186-->>- P0: return
    P0->>+ P187: uses
    P187-->>- P0: return
    P0->>+ P188: uses
    P188-->>- P0: return
    P0->>+ P189: uses
    P189-->>- P0: return
    P0->>+ P190: uses
    P190-->>- P0: return
    P0->>+ P191: uses
    P191-->>- P0: return
    P0->>+ P192: uses
    P192-->>- P0: return
    P0->>+ P193: uses
    P193-->>- P0: return
    P0->>+ P194: uses
    P194-->>- P0: return
    P0->>+ P195: uses
    P195-->>- P0: return
    P0->>+ P58: uses
    P58-->>- P0: return
    P0->>+ P59: uses
    P59-->>- P0: return
    P0->>+ P60: uses
    P60-->>- P0: return
    P0->>+ P196: calls
    P196-->>- P0: return
    P0->>+ P197: calls
    P197-->>- P0: return
    P0->>+ P198: calls
    P198-->>- P0: return
    P0->>+ P199: uses
    P199-->>- P0: return
    P0->>+ P200: uses
    P200-->>- P0: return
    P0->>+ P201: uses
    P201-->>- P0: return
    P0->>+ P202: uses
    P202-->>- P0: return
    P0->>+ P203: calls
    P203-->>- P0: return
    P0->>+ P204: calls
    P204-->>- P0: return
    P0->>+ P205: calls
    P205-->>- P0: return
    P0->>+ P61: calls
    P61-->>- P0: return
    P0->>+ P62: uses
    P62-->>- P0: return
    P0->>+ P63: uses
    P63-->>- P0: return
    P0->>+ P64: uses
    P64-->>- P0: return
    P0->>+ P65: uses
    P65-->>- P0: return
    P0->>+ P66: uses
    P66-->>- P0: return
    P0->>+ P67: uses
    P67-->>- P0: return
    P0->>+ P68: uses
    P68-->>- P0: return
    P0->>+ P69: uses
    P69-->>- P0: return
    P0->>+ P70: uses
    P70-->>- P0: return
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
    P0->>+ P218: uses
    P218-->>- P0: return
    P0->>+ P219: uses
    P219-->>- P0: return
    P0->>+ P220: uses
    P220-->>- P0: return
    P0->>+ P221: uses
    P221-->>- P0: return
    P0->>+ P222: uses
    P222-->>- P0: return
    P0->>+ P223: uses
    P223-->>- P0: return
    P0->>+ P224: uses
    P224-->>- P0: return
    P0->>+ P225: uses
    P225-->>- P0: return
    P0->>+ P226: uses
    P226-->>- P0: return
    P0->>+ P227: uses
    P227-->>- P0: return
    P0->>+ P228: uses
    P228-->>- P0: return
    P0->>+ P229: uses
    P229-->>- P0: return
    P0->>+ P71: uses
    P71-->>- P0: return
    P0->>+ P72: uses
    P72-->>- P0: return
    P0->>+ P73: uses
    P73-->>- P0: return
    P0->>+ P74: uses
    P74-->>- P0: return
    P0->>+ P75: uses
    P75-->>- P0: return
    P0->>+ P76: calls
    P76-->>- P0: return
    P0->>+ P77: calls
    P77-->>- P0: return
    P0->>+ P78: calls
    P78-->>- P0: return
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
    P0->>+ P79: uses
    P79-->>- P0: return
    P0->>+ P80: uses
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
    P0->>+ P248: calls
    P248-->>- P0: return
    P0->>+ P249: calls
    P249-->>- P0: return
    P0->>+ P86: calls
    P86-->>- P0: return
    P0->>+ P250: calls
    P250-->>- P0: return
    P0->>+ P251: calls
    P251-->>- P0: return
    P0->>+ P252: calls
    P252-->>- P0: return
    P0->>+ P87: uses
    P87-->>- P0: return
    P0->>+ P88: uses
    P88-->>- P0: return
    P0->>+ P89: uses
    P89-->>- P0: return
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
    P0->>+ P95: uses
    P95-->>- P0: return
    P0->>+ P96: uses
    P96-->>- P0: return
    P0->>+ P97: uses
    P97-->>- P0: return
    P0->>+ P98: uses
    P98-->>- P0: return
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
    P0->>+ P106: uses
    P106-->>- P0: return
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
    P0->>+ P260: calls
    P260-->>- P0: return
    P0->>+ P261: calls
    P261-->>- P0: return
    P0->>+ P262: calls
    P262-->>- P0: return
    P0->>+ P263: calls
    P263-->>- P0: return
    P0->>+ P264: calls
    P264-->>- P0: return
    P0->>+ P265: calls
    P265-->>- P0: return
    P0->>+ P266: calls
    P266-->>- P0: return
    P0->>+ P267: calls
    P267-->>- P0: return
    P0->>+ P268: calls
    P268-->>- P0: return
    P0->>+ P131: calls
    P131-->>- P0: return
    P0->>+ P132: calls
    P132-->>- P0: return
    P0->>+ P133: calls
    P133-->>- P0: return
    P0->>+ P269: calls
    P269-->>- P0: return
    P0->>+ P270: calls
    P270-->>- P0: return
    P0->>+ P134: calls
    P134-->>- P0: return
    P0->>+ P271: calls
    P271-->>- P0: return
    P0->>+ P272: calls
    P272-->>- P0: return
    P0->>+ P273: calls
    P273-->>- P0: return
    P0->>+ P274: calls
    P274-->>- P0: return
    P0->>+ P275: calls
    P275-->>- P0: return
    P0->>+ P276: calls
    P276-->>- P0: return
    P0->>+ P277: calls
    P277-->>- P0: return
    P0->>+ P278: calls
    P278-->>- P0: return
```

## Connections by Relation

### calls
- [[register_or_login()]] `INFERRED`
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
- [[setup_db()]] `INFERRED`
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