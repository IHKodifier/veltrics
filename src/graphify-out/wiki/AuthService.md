# AuthService

> God node · 35 connections · [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\services\auth_service.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/services/auth_service.py#L57)

## Call Trace Diagram

```mermaid
sequenceDiagram
    participant P0 as AuthService
    participant P1 as Organization
    participant P2 as UC-014: Provision commercial or custom organization.
    participant P3 as User
    participant P4 as Vehicle
    participant P5 as MaintenanceSchedule
    participant P6 as AuditLog
    participant P7 as ServiceRecord
    participant P8 as Driver
    participant P9 as UserOrganization
    participant P10 as OrganizationInvitation
    participant P11 as FuelLog
    participant P12 as ExpenseLog
    participant P13 as OrganizationInvitationResponse
    participant P14 as SwitchOrganizationResponse
    participant P15 as OrganizationCreate
    participant P16 as PersonalOrganizationCreate
    participant P17 as OrganizationResponse
    participant P18 as SwitchOrganizationRequest
    participant P19 as OrganizationInvitationCreate
    participant P20 as Trip
    participant P21 as OrganizationUpdate
    participant P22 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P23 as Retrieve organizations list.
    participant P24 as UC-015: Switch active organization context for user.
    participant P25 as UC-015: Get active organization for user.
    participant P26 as Retrieve organization details by ID.
    participant P27 as UC-017: Edit Organization Profile Details.     Enforces ISO 4217 currency valida
    participant P28 as UC-018: Invite Driver / Manager via Email or Phone.     Generates a secure 64-ch
    participant P29 as UC-018: List pending organization invitations.
    participant P30 as UC-021: Remove Member from Organization.     Prevents owner removal. Unassigns u
    participant P31 as UC-022: Cancel Pending Member Invitation.
    participant P32 as UC-023: Soft Delete Organization & Child Entities.     Rejects personal org dele
    participant P33 as UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    participant P34 as UC-024: Register New Vehicle with organization quota validation & duplicate VIN
    participant P35 as UC-025: List Organization Vehicles directory with status, search, fuel type, and
    participant P36 as UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur
    participant P37 as UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    participant P38 as UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow
    participant P39 as UC-028: Soft Delete Vehicle & Write Audit Log.     Frees up 1 vehicle slot in a
    participant P40 as UC-029: Log Manual Odometer Update.     Enforces lower-reading guard unless is_
    participant P41 as UC-030: Upload & Manage Vehicle Documents (Registration / Insurance / Permit).
    participant P42 as UC-030: List Vehicle Documents.
    participant P43 as UC-031: Recover Soft-Deleted Vehicle.     Enforces active organization quota li
    participant P44 as UC-032: Assign Primary Driver to Vehicle.     Enforces tenant isolation on assi
    participant P45 as UC-033: Unassign Primary Driver from Vehicle.
    participant P46 as UC-011: Account Deletion (GDPR Right to be Forgotten)         Soft-deletes user
    participant P47 as Helper to convert SQLAlchemy model instance to dict.
    participant P48 as UC-119: Offline Sync Batch Transaction Engine.     Processes operation envelopes
    participant P49 as UC-096: Delta Sync Payload Fetching (Incremental Catch-up).     Returns active e
    participant P50 as UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    participant P51 as UC-024: Register New Vehicle with organization quota validation & duplicate VIN
    participant P52 as UC-025: List Organization Vehicles directory with status, search, fuel type, and
    participant P53 as UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur
    participant P54 as UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    participant P55 as UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow
    participant P56 as UC-007: Fetch current user profile details.
    participant P57 as UC-007: Update current user profile (full name, phone, city, job role, avatar).
    participant P58 as UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessio
    participant P59 as UC-007: Multi-tenant authorization boundary verification endpoint.
    participant P60 as UC-011: Account Deletion (GDPR Right to be Forgotten).     Soft-deletes user re
    participant P61 as UC-013: Active Session Management & Device Tracking     Returns list of active
    participant P62 as UC-013: Revoke Specific Device Session     Revokes the specified refresh token
    participant P63 as UC-013 Alternate Flow A1: Revoke All Other Sessions     Revokes all active sess
    participant P64 as UC-053: Get Trip Summary & Tax Deduction Metrics.
    participant P65 as UC-052: Start GPS Trip Tracking session.
    participant P66 as UC-052: Stop active GPS Trip Tracking session and calculate distance.
    participant P67 as UC-052 / UC-053: Create trip entry (Manual or completed GPS trip).
    participant P68 as UC-053: View Trip History.
    participant P69 as UC-054: Edit Trip Entry & Classification.
    participant P70 as UC-055: Soft Delete Trip Entry.
    participant P71 as UC-056: Quick-Log Trip from Dashboard.
    participant P72 as UC-057: View Distance & Mileage Summary Analytics.
    participant P73 as register_or_login()
    participant P74 as UC-014: Provision commercial or custom organization.
    participant P75 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P76 as Retrieve organizations list.
    participant P77 as UC-015: Switch active organization context for user.
    participant P78 as UC-015: Get active organization for user.
    participant P79 as Retrieve organization details by ID.
    participant P80 as UC-016: Invite Team Member to Organization.     Generates a secure 64-character
    participant P81 as UC-016: List pending organization invitations.
    participant P82 as UC-019: Inspect / validate organization invitation token details.     Returns HT
    participant P83 as UC-019: Accept Organization Invitation for existing authenticated user.
    participant P84 as UC-020: Redeem Org Invitation Code for new user during signup/onboard.
    participant P85 as UC-058: Log General Fleet Expense.
    participant P86 as UC-059: Expense Category & Cost Summary Metrics.
    participant P87 as UC-059: View Expense History.
    participant P88 as UC-060: Edit Expense Entry.
    participant P89 as UC-061: Soft Delete Expense Entry.
    participant P90 as UC-062: Quick-Log Expense from Dashboard.
    participant P91 as UC-048: View Fuel Efficiency Trends & Aggregate Metrics.
    participant P92 as UC-050: Detect Fuel Anomaly & Theft Alerts - Fetch anomaly logs.
    participant P93 as UC-050 (A1): Manager clears fuel anomaly flag.
    participant P94 as UC-049: Fuel Receipt OCR Auto-Fill (Pro).
    participant P95 as UC-046: Log Fuel Fill-Up Entry.     Automatically updates vehicle current odome
    participant P96 as UC-047 / UC-048: View Fuel Log History with optional pagination.
    participant P97 as UC-051: Edit Fuel Log Entry.     Updates entry, syncs linked ExpenseLog, and re
    participant P98 as UC-051: Soft Delete Fuel Log Entry.     Soft-deletes entry and linked ExpenseLo
    participant P99 as Test 1: Verify all 7 core data models instantiate clean database tables.
    participant P100 as Test 2: Verify database seeding populates master vehicle catalogue idempotently.
    participant P101 as Test 3: Verify POST /api/v1/admin/seed endpoint.
    participant P102 as complete_profile()
    participant P103 as login()
    participant P104 as test_uc118_schema_instantiation()
    participant P105 as UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,
    participant P106 as UC-064: Requests for Org 2 return only Org 2's metrics.
    participant P107 as UC-064: Empty organization returns 0 stats so client can render onboarding card.
    participant P108 as UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missin
    participant P109 as refresh_token()
    participant P110 as setup_db()
    participant P111 as dashboard_setup()
    participant P112 as test_data()
    participant P113 as AC 1: GIVEN an authenticated user     WHEN DELETE /api/v1/users/me is invoked
    participant P114 as AC 2: GIVEN a user who is the sole owner of an active non-personal organization
    participant P115 as AC 3: GIVEN a soft-deleted user account     WHEN attempting to authenticate, ac
    participant P116 as AC 1: System creates immutable AuditLog entry upon user registration.
    participant P117 as AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadat
    participant P118 as A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None.
    participant P119 as AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS
    participant P120 as AC 4: System records USER_LOGOUT audit entry upon session termination.
    participant P121 as Edge Case: Audit log DB write exception is handled safely and does not block use
    participant P122 as UC-046: Test successful fuel log creation & vehicle current odometer update.
    participant P123 as UC-046 Acceptance Criterion: WHEN a fuel log entry is saved     THE SYSTEM SHAL
    participant P124 as UC-046 Edge Case: Odometer entry lower than vehicle's current odometer -> API re
    participant P125 as UC-046 & UC-047: Verify calculated km/L efficiency on 2nd full tank fill-up.
    participant P126 as UC-047: Test retrieving fuel log history via GET /api/v1/fuel.     Should retur
    participant P127 as UC-047 Acceptance Criterion: WHEN two consecutive full-tank fuel logs are create
    participant P128 as UC-047 Alternate Flow A1: Partial fill-up (is_full_tank = False) skips efficienc
    participant P129 as UC-047 Main Flow 5: If efficiency is 30% lower than vehicle baseline average,
    participant P130 as UC-051 Alternate Flow A1: PATCH /api/v1/fuel/{id} updates entry & recalculates e
    participant P131 as UC-051 Main Flow: DELETE /api/v1/fuel/{id} soft-deletes log & linked expense and
    participant P132 as UC-051 Edge Case: Deleting or patching non-existent log returns HTTP 404.
    participant P133 as UC-034: GET /api/v1/maintenance/schedules should auto-populate schedule template
    participant P134 as UC-034: POST /api/v1/maintenance logs record, updates odometer, and resets sched
    participant P135 as UC-034: POST /api/v1/maintenance rejects negative cost with HTTP 422.
    participant P136 as UC-034: Tenant cross-access rejected.
    participant P137 as UC-036: POST /api/v1/maintenance logs service record and updates linked schedule
    participant P138 as UC-036: Odometer reading > current_odometer_km updates vehicle current_odometer_
    participant P139 as UC-036: Omitting maintenance_schedule_id matches schedule item by task name subs
    participant P140 as UC-036: Rejects negative cost, negative odometer, whitespace service_type, or in
    participant P141 as UC-036: Enforces X-Organization-ID header presence and cross-tenant access prote
    participant P142 as UC-037: GET /api/v1/maintenance/records retrieves service records sorted by serv
    participant P143 as UC-037: Pagination limit and offset parameters operate correctly.
    participant P144 as UC-037: Returns 404 when vehicle_id does not exist in active organization.
    participant P145 as UC-037: Header requirements and cross-tenant boundaries are strictly enforced.
    participant P146 as Test 1: Verify GET /api/v1/vehicles/types?q=Toyota returns seeded Toyota models.
    participant P147 as Test 2: Verify POST /api/v1/vehicles registers new vehicle with tenant organizat
    participant P148 as Test 3: Verify duplicate VIN within same organization returns HTTP 409 Conflict.
    participant P149 as Test 4: Verify exceeding max_vehicles quota (max=2 for sample_org) returns HTTP
    participant P150 as Test 5: Verify custom make/model is dynamically indexed into VehicleType catalog
    participant P151 as ensure_organization()
    participant P152 as test_uc011_sole_owner_blocking()
    participant P153 as test_setup()
    participant P154 as UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency a
    participant P155 as UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per veh
    participant P156 as UC-035: POST /api/v1/maintenance/schedules creates custom schedule with default
    participant P157 as UC-035: POST /api/v1/maintenance/schedules uses provided last_performed_km and l
    participant P158 as UC-035: Rejects zero/negative intervals or empty task names with 422.
    participant P159 as UC-035: PATCH /api/v1/maintenance/schedules/{id} updates parameters and recalcul
    participant P160 as UC-035: DELETE /api/v1/maintenance/schedules/{id} soft-deletes schedule task.
    participant P161 as UC-035: Header validation and tenant cross-access isolation.
    participant P162 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with empty schedule_ids a
    participant P163 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with specific schedule_id
    participant P164 as UC-038: Returns 404 when vehicle_id is not found in active organization.
    participant P165 as UC-038: Returns 404 when one or more schedule_ids do not belong to the vehicle.
    participant P166 as UC-038: Headers and cross-tenant boundaries are strictly enforced.
    participant P167 as UC-016: Owner can create organization invitation, generating a secure 64-char to
    participant P168 as UC-016: Inviting with invalid or blank email yields HTTP 422 Unprocessable Entit
    participant P169 as UC-016: Inviting with unsupported role string yields HTTP 422 Unprocessable Enti
    participant P170 as UC-016: Re-inviting same email updates existing invitation token and TTL without
    participant P171 as UC-016: Non-owner caller attempting to send invitation yields HTTP 403 Forbidden
    participant P172 as UC-016: Owner can list all pending invitations for organization.
    participant P173 as UC-016: Listing invitations for non-existent org yields HTTP 404 Not Found.
    participant P174 as Test 1: Verify PATCH /api/v1/vehicles/{vehicle_id} successfully updates vehicle
    participant P175 as Test 2: Verify updating vehicle under wrong organization_id returns HTTP 403 For
    participant P176 as Test 3: Verify updating non-existent vehicle returns HTTP 404 Not Found.
    participant P177 as Test 4: Verify manual odometer update with discrepancy > 500 km generates an Aud
    participant P178 as Test 5: Verify non-dictionary custom_specs payload returns HTTP 422 Unprocessabl
    participant P179 as create_organization()
    participant P180 as auto_create_personal_organization()
    participant P181 as setup_db()
    participant P182 as test_setup()
    participant P183 as test_setup()
    participant P184 as test_setup()
    participant P185 as AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr
    participant P186 as AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL
    participant P187 as AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store \"facebook\" insid
    participant P188 as Alternate Flow A1: Account Linking     If email matches existing account with d
    participant P189 as Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Requ
    participant P190 as AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT
    participant P191 as Alternate Flow A1: Account Linking     If user signed up via Google, submitting
    participant P192 as Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu
    participant P193 as Edge Case: Missing email or missing password for email auth provider returns HTT
    participant P194 as AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200
    participant P195 as Edge Case: Incorrect password returns HTTP 401 Unauthorized.
    participant P196 as Edge Case: Unregistered email returns HTTP 401 Unauthorized.
    participant P197 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P198 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P199 as AC 1: WHEN an existing Google user signs in,     THE SYSTEM SHALL return HTTP 2
    participant P200 as AC 2: WHEN an existing Facebook user signs in,     THE SYSTEM SHALL return HTTP
    participant P201 as AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,
    participant P202 as AC 4 (Account Linking Flow A1): WHEN an existing user registered via email
    participant P203 as Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized.
    participant P204 as Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized.
    participant P205 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P206 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P207 as AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u
    participant P208 as AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P
    participant P209 as AC 3: GIVEN a profile update request with invalid display name length (< 2 chars
    participant P210 as AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro
    participant P211 as UC-014: POST /api/v1/organizations creates commercial organization and sets owne
    participant P212 as UC-014: POST /api/v1/organizations/personal auto-creates personal organization f
    participant P213 as UC-014: Blank or whitespace organization name rejected with HTTP 422.
    participant P214 as UC-014: GET /api/v1/organizations?user_id={id} returns list of user organization
    participant P215 as UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found.
    participant P216 as UC-015: POST /api/v1/organizations/switch switches active context for valid user
    participant P217 as UC-015: Switch attempt to organization owned by another user yields HTTP 403 For
    participant P218 as UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found.
    participant P219 as UC-015: GET /api/v1/organizations/active returns current primary organization fo
    participant P220 as UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 N
    participant P221 as Test 1: Verify GET /api/v1/vehicles?status=MAINTENANCE returns only vehicles in
    participant P222 as Test 2: Verify search query matches license plate, make, or model.
    participant P223 as Test 3: Verify filtering by province (e.g. Sindh).
    participant P224 as Test 1: Verify GET /api/v1/vehicles/{vehicle_id} returns detailed vehicle metada
    participant P225 as Test 2: Verify non-existent vehicle ID returns HTTP 404 Not Found.
    participant P226 as Test 3: Verify requesting another tenant's vehicle returns HTTP 403 Forbidden.
    participant P227 as Test 4: Verify PATCH /api/v1/vehicles/{vehicle_id}/status updates vehicle status
    participant P228 as setup_db()
    participant P229 as setup_db()
    participant P230 as setup_db()
    participant P231 as test_setup()
    participant P232 as test_setup()
    participant P233 as test_setup()
    participant P234 as test_setup()
    participant P235 as test_setup()
    participant P236 as test_setup()
    participant P237 as setup_db()
    participant P238 as test_setup()
    participant P239 as test_setup()
    participant P240 as setup_db()
    participant P241 as setup_db()
    participant P242 as test_data()
    participant P243 as setup_db()
    participant P244 as setup_db()
    participant P245 as setup_db()
    participant P246 as setup_db()
    participant P247 as sample_fleet()
    participant P248 as test_setup()
    participant P249 as test_setup()
    participant P250 as sample_org()
    participant P251 as AuthSessionDTO
    participant P252 as SessionRevokeResponse
    participant P253 as UC-004: User Password Authentication & Session Initiation     Authenticates reg
    participant P254 as UC-006: Forgot Password Request     Issues a password reset JWT token with 5-mi
    participant P255 as UC-006: Password Reset Execution     Verifies reset token, validates password p
    participant P256 as UC-009: Session Refresh & Access Token Renewal     Validates active refresh tok
    participant P257 as UC-010: User Sign Out & Token Revocation     Revokes the provided refresh token
    participant P258 as UserDTO
    participant P259 as OrganizationDTO
    participant P260 as UserSessionDTO
    participant P261 as AuditService
    participant P262 as ForgotPasswordResponse
    participant P263 as ResetPasswordResponse
    participant P264 as RefreshTokenResponse
    participant P265 as LogoutResponse
    participant P266 as UserSession
    participant P267 as RegisterRequest
    participant P268 as LoginRequest
    participant P269 as ForgotPasswordRequest
    participant P270 as ResetPasswordRequest
    participant P271 as RefreshTokenRequest
    participant P272 as LogoutRequest
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
    P1->>+ P22: uses
    P22-->>- P1: return
    P1->>+ P23: uses
    P23-->>- P1: return
    P1->>+ P24: uses
    P24-->>- P1: return
    P1->>+ P25: uses
    P25-->>- P1: return
    P1->>+ P26: uses
    P26-->>- P1: return
    P1->>+ P27: uses
    P27-->>- P1: return
    P1->>+ P28: uses
    P28-->>- P1: return
    P1->>+ P29: uses
    P29-->>- P1: return
    P1->>+ P30: uses
    P30-->>- P1: return
    P1->>+ P31: uses
    P31-->>- P1: return
    P1->>+ P32: uses
    P32-->>- P1: return
    P1->>+ P33: uses
    P33-->>- P1: return
    P1->>+ P34: uses
    P34-->>- P1: return
    P1->>+ P35: uses
    P35-->>- P1: return
    P1->>+ P36: uses
    P36-->>- P1: return
    P1->>+ P37: uses
    P37-->>- P1: return
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
    P1->>+ P46: uses
    P46-->>- P1: return
    P1->>+ P47: uses
    P47-->>- P1: return
    P1->>+ P48: uses
    P48-->>- P1: return
    P1->>+ P49: uses
    P49-->>- P1: return
    P1->>+ P50: uses
    P50-->>- P1: return
    P1->>+ P51: uses
    P51-->>- P1: return
    P1->>+ P52: uses
    P52-->>- P1: return
    P1->>+ P53: uses
    P53-->>- P1: return
    P1->>+ P54: uses
    P54-->>- P1: return
    P1->>+ P55: uses
    P55-->>- P1: return
    P1->>+ P56: uses
    P56-->>- P1: return
    P1->>+ P57: uses
    P57-->>- P1: return
    P1->>+ P58: uses
    P58-->>- P1: return
    P1->>+ P59: uses
    P59-->>- P1: return
    P1->>+ P60: uses
    P60-->>- P1: return
    P1->>+ P61: uses
    P61-->>- P1: return
    P1->>+ P62: uses
    P62-->>- P1: return
    P1->>+ P63: uses
    P63-->>- P1: return
    P1->>+ P64: uses
    P64-->>- P1: return
    P1->>+ P65: uses
    P65-->>- P1: return
    P1->>+ P66: uses
    P66-->>- P1: return
    P1->>+ P67: uses
    P67-->>- P1: return
    P1->>+ P68: uses
    P68-->>- P1: return
    P1->>+ P69: uses
    P69-->>- P1: return
    P1->>+ P70: uses
    P70-->>- P1: return
    P1->>+ P71: uses
    P71-->>- P1: return
    P1->>+ P72: uses
    P72-->>- P1: return
    P1->>+ P73: calls
    P73-->>- P1: return
    P1->>+ P74: uses
    P74-->>- P1: return
    P1->>+ P75: uses
    P75-->>- P1: return
    P1->>+ P76: uses
    P76-->>- P1: return
    P1->>+ P77: uses
    P77-->>- P1: return
    P1->>+ P78: uses
    P78-->>- P1: return
    P1->>+ P79: uses
    P79-->>- P1: return
    P1->>+ P80: uses
    P80-->>- P1: return
    P1->>+ P81: uses
    P81-->>- P1: return
    P1->>+ P82: uses
    P82-->>- P1: return
    P1->>+ P83: uses
    P83-->>- P1: return
    P1->>+ P84: uses
    P84-->>- P1: return
    P1->>+ P85: uses
    P85-->>- P1: return
    P1->>+ P86: uses
    P86-->>- P1: return
    P1->>+ P87: uses
    P87-->>- P1: return
    P1->>+ P88: uses
    P88-->>- P1: return
    P1->>+ P89: uses
    P89-->>- P1: return
    P1->>+ P90: uses
    P90-->>- P1: return
    P1->>+ P91: uses
    P91-->>- P1: return
    P1->>+ P92: uses
    P92-->>- P1: return
    P1->>+ P93: uses
    P93-->>- P1: return
    P1->>+ P94: uses
    P94-->>- P1: return
    P1->>+ P95: uses
    P95-->>- P1: return
    P1->>+ P96: uses
    P96-->>- P1: return
    P1->>+ P97: uses
    P97-->>- P1: return
    P1->>+ P98: uses
    P98-->>- P1: return
    P1->>+ P99: uses
    P99-->>- P1: return
    P1->>+ P100: uses
    P100-->>- P1: return
    P1->>+ P101: uses
    P101-->>- P1: return
    P1->>+ P102: calls
    P102-->>- P1: return
    P1->>+ P103: calls
    P103-->>- P1: return
    P1->>+ P104: calls
    P104-->>- P1: return
    P1->>+ P105: uses
    P105-->>- P1: return
    P1->>+ P106: uses
    P106-->>- P1: return
    P1->>+ P107: uses
    P107-->>- P1: return
    P1->>+ P108: uses
    P108-->>- P1: return
    P1->>+ P109: calls
    P109-->>- P1: return
    P1->>+ P110: calls
    P110-->>- P1: return
    P1->>+ P111: calls
    P111-->>- P1: return
    P1->>+ P112: calls
    P112-->>- P1: return
    P1->>+ P113: uses
    P113-->>- P1: return
    P1->>+ P114: uses
    P114-->>- P1: return
    P1->>+ P115: uses
    P115-->>- P1: return
    P1->>+ P116: uses
    P116-->>- P1: return
    P1->>+ P117: uses
    P117-->>- P1: return
    P1->>+ P118: uses
    P118-->>- P1: return
    P1->>+ P119: uses
    P119-->>- P1: return
    P1->>+ P120: uses
    P120-->>- P1: return
    P1->>+ P121: uses
    P121-->>- P1: return
    P1->>+ P122: uses
    P122-->>- P1: return
    P1->>+ P123: uses
    P123-->>- P1: return
    P1->>+ P124: uses
    P124-->>- P1: return
    P1->>+ P125: uses
    P125-->>- P1: return
    P1->>+ P126: uses
    P126-->>- P1: return
    P1->>+ P127: uses
    P127-->>- P1: return
    P1->>+ P128: uses
    P128-->>- P1: return
    P1->>+ P129: uses
    P129-->>- P1: return
    P1->>+ P130: uses
    P130-->>- P1: return
    P1->>+ P131: uses
    P131-->>- P1: return
    P1->>+ P132: uses
    P132-->>- P1: return
    P1->>+ P133: uses
    P133-->>- P1: return
    P1->>+ P134: uses
    P134-->>- P1: return
    P1->>+ P135: uses
    P135-->>- P1: return
    P1->>+ P136: uses
    P136-->>- P1: return
    P1->>+ P137: uses
    P137-->>- P1: return
    P1->>+ P138: uses
    P138-->>- P1: return
    P1->>+ P139: uses
    P139-->>- P1: return
    P1->>+ P140: uses
    P140-->>- P1: return
    P1->>+ P141: uses
    P141-->>- P1: return
    P1->>+ P142: uses
    P142-->>- P1: return
    P1->>+ P143: uses
    P143-->>- P1: return
    P1->>+ P144: uses
    P144-->>- P1: return
    P1->>+ P145: uses
    P145-->>- P1: return
    P1->>+ P146: uses
    P146-->>- P1: return
    P1->>+ P147: uses
    P147-->>- P1: return
    P1->>+ P148: uses
    P148-->>- P1: return
    P1->>+ P149: uses
    P149-->>- P1: return
    P1->>+ P150: uses
    P150-->>- P1: return
    P1->>+ P151: calls
    P151-->>- P1: return
    P1->>+ P152: calls
    P152-->>- P1: return
    P1->>+ P153: calls
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
    P1->>+ P179: calls
    P179-->>- P1: return
    P1->>+ P180: calls
    P180-->>- P1: return
    P1->>+ P181: calls
    P181-->>- P1: return
    P1->>+ P182: calls
    P182-->>- P1: return
    P1->>+ P183: calls
    P183-->>- P1: return
    P1->>+ P184: calls
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
    P1->>+ P193: uses
    P193-->>- P1: return
    P1->>+ P194: uses
    P194-->>- P1: return
    P1->>+ P195: uses
    P195-->>- P1: return
    P1->>+ P196: uses
    P196-->>- P1: return
    P1->>+ P197: uses
    P197-->>- P1: return
    P1->>+ P198: uses
    P198-->>- P1: return
    P1->>+ P199: uses
    P199-->>- P1: return
    P1->>+ P200: uses
    P200-->>- P1: return
    P1->>+ P201: uses
    P201-->>- P1: return
    P1->>+ P202: uses
    P202-->>- P1: return
    P1->>+ P203: uses
    P203-->>- P1: return
    P1->>+ P204: uses
    P204-->>- P1: return
    P1->>+ P205: uses
    P205-->>- P1: return
    P1->>+ P206: uses
    P206-->>- P1: return
    P1->>+ P207: uses
    P207-->>- P1: return
    P1->>+ P208: uses
    P208-->>- P1: return
    P1->>+ P209: uses
    P209-->>- P1: return
    P1->>+ P210: uses
    P210-->>- P1: return
    P1->>+ P211: uses
    P211-->>- P1: return
    P1->>+ P212: uses
    P212-->>- P1: return
    P1->>+ P213: uses
    P213-->>- P1: return
    P1->>+ P214: uses
    P214-->>- P1: return
    P1->>+ P215: uses
    P215-->>- P1: return
    P1->>+ P216: uses
    P216-->>- P1: return
    P1->>+ P217: uses
    P217-->>- P1: return
    P1->>+ P218: uses
    P218-->>- P1: return
    P1->>+ P219: uses
    P219-->>- P1: return
    P1->>+ P220: uses
    P220-->>- P1: return
    P1->>+ P221: uses
    P221-->>- P1: return
    P1->>+ P222: uses
    P222-->>- P1: return
    P1->>+ P223: uses
    P223-->>- P1: return
    P1->>+ P224: uses
    P224-->>- P1: return
    P1->>+ P225: uses
    P225-->>- P1: return
    P1->>+ P226: uses
    P226-->>- P1: return
    P1->>+ P227: uses
    P227-->>- P1: return
    P1->>+ P228: calls
    P228-->>- P1: return
    P1->>+ P229: calls
    P229-->>- P1: return
    P1->>+ P230: calls
    P230-->>- P1: return
    P1->>+ P231: calls
    P231-->>- P1: return
    P1->>+ P232: calls
    P232-->>- P1: return
    P1->>+ P233: calls
    P233-->>- P1: return
    P1->>+ P234: calls
    P234-->>- P1: return
    P1->>+ P235: calls
    P235-->>- P1: return
    P1->>+ P236: calls
    P236-->>- P1: return
    P1->>+ P237: calls
    P237-->>- P1: return
    P1->>+ P238: calls
    P238-->>- P1: return
    P1->>+ P239: calls
    P239-->>- P1: return
    P1->>+ P240: calls
    P240-->>- P1: return
    P1->>+ P241: calls
    P241-->>- P1: return
    P1->>+ P242: calls
    P242-->>- P1: return
    P1->>+ P243: calls
    P243-->>- P1: return
    P1->>+ P244: calls
    P244-->>- P1: return
    P1->>+ P245: calls
    P245-->>- P1: return
    P1->>+ P246: calls
    P246-->>- P1: return
    P1->>+ P247: calls
    P247-->>- P1: return
    P1->>+ P248: calls
    P248-->>- P1: return
    P1->>+ P249: calls
    P249-->>- P1: return
    P1->>+ P250: calls
    P250-->>- P1: return
    P0->>+ P3: uses
    P3-->>- P0: return
    P0->>+ P6: uses
    P6-->>- P0: return
    P0->>+ P9: uses
    P9-->>- P0: return
    P0->>+ P251: uses
    P251-->>- P0: return
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
    P0->>+ P56: uses
    P56-->>- P0: return
    P0->>+ P57: uses
    P57-->>- P0: return
    P0->>+ P58: uses
    P58-->>- P0: return
    P0->>+ P59: uses
    P59-->>- P0: return
    P0->>+ P60: uses
    P60-->>- P0: return
    P0->>+ P61: uses
    P61-->>- P0: return
    P0->>+ P62: uses
    P62-->>- P0: return
    P0->>+ P63: uses
    P63-->>- P0: return
    P0->>+ P261: uses
    P261-->>- P0: return
    P0->>+ P262: uses
    P262-->>- P0: return
    P0->>+ P263: uses
    P263-->>- P0: return
    P0->>+ P264: uses
    P264-->>- P0: return
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
    P0->>+ P270: uses
    P270-->>- P0: return
    P0->>+ P271: uses
    P271-->>- P0: return
    P0->>+ P272: uses
    P272-->>- P0: return
```

## Connections by Relation

### contains
- [[auth_service.py]] `EXTRACTED`

### uses
- [[Organization]] `INFERRED`
- [[User]] `INFERRED`
- [[AuditLog]] `INFERRED`
- [[UserOrganization]] `INFERRED`
- [[AuthSessionDTO]] `INFERRED`
- [[SessionRevokeResponse]] `INFERRED`
- [[UC-004: User Password Authentication & Session Initiation     Authenticates reg]] `INFERRED`
- [[UC-006: Forgot Password Request     Issues a password reset JWT token with 5-mi]] `INFERRED`
- [[UC-006: Password Reset Execution     Verifies reset token, validates password p]] `INFERRED`
- [[UC-009: Session Refresh & Access Token Renewal     Validates active refresh tok]] `INFERRED`
- [[UC-010: User Sign Out & Token Revocation     Revokes the provided refresh token]] `INFERRED`
- [[UserDTO]] `INFERRED`
- [[OrganizationDTO]] `INFERRED`
- [[UserSessionDTO]] `INFERRED`
- [[UC-007: Fetch current user profile details.]] `INFERRED`
- [[UC-007: Update current user profile (full name, phone, city, job role, avatar).]] `INFERRED`
- [[UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessio]] `INFERRED`
- [[UC-007: Multi-tenant authorization boundary verification endpoint.]] `INFERRED`
- [[UC-011: Account Deletion (GDPR Right to be Forgotten).     Soft-deletes user re]] `INFERRED`
- [[UC-013: Active Session Management & Device Tracking     Returns list of active]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*