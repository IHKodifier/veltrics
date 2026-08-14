# AuditLog

> God node · 93 connections · [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\audit_log.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/audit_log.py#L5)

## Call Trace Diagram

```mermaid
sequenceDiagram
    participant P0 as AuditLog
    participant P1 as AuthService
    participant P2 as Organization
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
    participant P32 as PaymentService
    participant P33 as UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    participant P34 as UC-024: Register New Vehicle with organization quota validation & duplicate VIN
    participant P35 as UC-025: List Organization Vehicles directory with status, search, fuel type, and
    participant P36 as UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur
    participant P37 as UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    participant P38 as UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow
    participant P39 as UC-007: Fetch current user profile details.
    participant P40 as UC-007: Update current user profile (full name, phone, city, job role, avatar).
    participant P41 as UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessio
    participant P42 as UC-007: Multi-tenant authorization boundary verification endpoint.
    participant P43 as UC-011: Account Deletion (GDPR Right to be Forgotten).     Soft-deletes user re
    participant P44 as UC-013: Active Session Management & Device Tracking     Returns list of active
    participant P45 as UC-013: Revoke Specific Device Session     Revokes the specified refresh token
    participant P46 as UC-013 Alternate Flow A1: Revoke All Other Sessions     Revokes all active sess
    participant P47 as create_test_user_and_org()
    participant P48 as UC-053: Get Trip Summary & Tax Deduction Metrics.
    participant P49 as UC-052: Start GPS Trip Tracking session.
    participant P50 as UC-052: Stop active GPS Trip Tracking session and calculate distance.
    participant P51 as UC-052 / UC-053: Create trip entry (Manual or completed GPS trip).
    participant P52 as UC-053: View Trip History.
    participant P53 as UC-054: Edit Trip Entry & Classification.
    participant P54 as UC-055: Soft Delete Trip Entry.
    participant P55 as UC-056: Quick-Log Trip from Dashboard.
    participant P56 as UC-057: View Distance & Mileage Summary Analytics.
    participant P57 as register_or_login()
    participant P58 as create_test_user_and_org()
    participant P59 as UC-014: Provision commercial or custom organization.
    participant P60 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P61 as Retrieve organizations list.
    participant P62 as UC-015: Switch active organization context for user.
    participant P63 as UC-015: Get active organization for user.
    participant P64 as Retrieve organization details by ID.
    participant P65 as UC-016: Invite Team Member to Organization.     Generates a secure 64-character
    participant P66 as UC-016: List pending organization invitations.
    participant P67 as UC-019: Inspect / validate organization invitation token details.     Returns HT
    participant P68 as UC-019: Accept Organization Invitation for existing authenticated user.
    participant P69 as UC-020: Redeem Org Invitation Code for new user during signup/onboard.
    participant P70 as AdService
    participant P71 as UC-058: Log General Fleet Expense.
    participant P72 as UC-059: Expense Category & Cost Summary Metrics.
    participant P73 as UC-059: View Expense History.
    participant P74 as UC-060: Edit Expense Entry.
    participant P75 as UC-061: Soft Delete Expense Entry.
    participant P76 as UC-062: Quick-Log Expense from Dashboard.
    participant P77 as UC-048: View Fuel Efficiency Trends & Aggregate Metrics.
    participant P78 as UC-050: Detect Fuel Anomaly & Theft Alerts - Fetch anomaly logs.
    participant P79 as UC-050 (A1): Manager clears fuel anomaly flag.
    participant P80 as UC-049: Fuel Receipt OCR Auto-Fill (Pro).
    participant P81 as UC-046: Log Fuel Fill-Up Entry.     Automatically updates vehicle current odome
    participant P82 as UC-047 / UC-048: View Fuel Log History with optional pagination.
    participant P83 as UC-051: Edit Fuel Log Entry.     Updates entry, syncs linked ExpenseLog, and re
    participant P84 as UC-051: Soft Delete Fuel Log Entry.     Soft-deletes entry and linked ExpenseLo
    participant P85 as Test 1: Verify all 7 core data models instantiate clean database tables.
    participant P86 as Test 2: Verify database seeding populates master vehicle catalogue idempotently.
    participant P87 as Test 3: Verify POST /api/v1/admin/seed endpoint.
    participant P88 as setup_database()
    participant P89 as setup_database()
    participant P90 as setup_database()
    participant P91 as setup_database()
    participant P92 as UC-086 & UC-087: Vehicle and Driver Quota Wall Enforcement
    participant P93 as UC-100 & UC-120: Verify Rewarded Ad Completion & Increment Bonus Quota
    participant P94 as UC-122: Ad-Gate Signature Forgery & Token Replay Prevention
    participant P95 as UC-101: Render Ad-Free Experience & Unlimited Quota for Pro Subscribers
    participant P96 as UC-067: Verify Fleet Manager Web Dashboard KPI Aggregation.
    participant P97 as UC-068: Verify Fleet Cost Ranking Table & Heatmap endpoint.
    participant P98 as UC-069: Verify Fleet Vehicle Availability Widget endpoint.
    participant P99 as UC-071: Verify customizing & saving dashboard widget layout preferences.
    participant P100 as UC-103 & UC-104: Verify driver safety score calculation & performance detail end
    participant P101 as UC-105: Verify idle driver and expiring license anomaly detection.
    participant P102 as UC-106: Verify safety certificate generation with digital signature hash.
    participant P103 as UC-070: Verify fleet driver safety leaderboard widget endpoint.
    participant P104 as UC-110: Verify Exporting Maintenance History to PDF.
    participant P105 as UC-111: Verify Exporting Fuel & Expense Logs to CSV.
    participant P106 as UC-112: Verify Generating & Emailing Monthly Fleet Summary PDF.
    participant P107 as UC-076: Verify Notification Inbox Retrieval and Marking Read.
    participant P108 as UC-077: Verify Notification Preferences & Channel Configuration.
    participant P109 as UC-078: Verify Billing & Payment Alert Notification Trigger.
    participant P110 as UC-079: Verify Purging Stale FCM Push Notification Tokens (>90 days).
    participant P111 as UC-039: Verify adding custom maintenance service item.
    participant P112 as UC-040: Verify updating an existing service record.
    participant P113 as UC-041: Verify soft deleting a service record.
    participant P114 as UC-042: Verify searching & filtering service history.
    participant P115 as UC-043: Verify maintenance vendor creation and directory endpoint.
    participant P116 as UC-044: Verify vehicle pre-trip/post-trip safety inspection checklist.
    participant P117 as UC-045: Verify snoozing maintenance alert by days and kilometers.
    participant P118 as complete_profile()
    participant P119 as login()
    participant P120 as test_uc118_schema_instantiation()
    participant P121 as UC-087 & UC-018: Register Driver with organization driver quota enforcement.
    participant P122 as UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,
    participant P123 as UC-064: Requests for Org 2 return only Org 2's metrics.
    participant P124 as UC-064: Empty organization returns 0 stats so client can render onboarding card.
    participant P125 as UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missin
    participant P126 as UC-081 & UC-121: Safepay Webhook Processing & Entitlement Activation
    participant P127 as UC-082 & UC-121: Handle Payment Checkout Failure & Grace Period
    participant P128 as UC-083: View Subscription Status & Billing History
    participant P129 as UC-084: Cancel Active Subscription
    participant P130 as UC-085 & UC-120: Pro-to-Free Downgrade & Bonus Slot Preservation Protocol
    participant P131 as UC-121: Safepay Webhook Idempotency & Unrecognized Event Logging
    participant P132 as refresh_token()
    participant P133 as setup_db()
    participant P134 as dashboard_setup()
    participant P135 as test_data()
    participant P136 as AC 1: GIVEN an authenticated user     WHEN DELETE /api/v1/users/me is invoked
    participant P137 as AC 2: GIVEN a user who is the sole owner of an active non-personal organization
    participant P138 as AC 3: GIVEN a soft-deleted user account     WHEN attempting to authenticate, ac
    participant P139 as AC 1: System creates immutable AuditLog entry upon user registration.
    participant P140 as AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadat
    participant P141 as A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None.
    participant P142 as AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS
    participant P143 as AC 4: System records USER_LOGOUT audit entry upon session termination.
    participant P144 as Edge Case: Audit log DB write exception is handled safely and does not block use
    participant P145 as UC-046: Test successful fuel log creation & vehicle current odometer update.
    participant P146 as UC-046 Acceptance Criterion: WHEN a fuel log entry is saved     THE SYSTEM SHAL
    participant P147 as UC-046 Edge Case: Odometer entry lower than vehicle's current odometer -> API re
    participant P148 as UC-046 & UC-047: Verify calculated km/L efficiency on 2nd full tank fill-up.
    participant P149 as UC-047: Test retrieving fuel log history via GET /api/v1/fuel.     Should retur
    participant P150 as UC-047 Acceptance Criterion: WHEN two consecutive full-tank fuel logs are create
    participant P151 as UC-047 Alternate Flow A1: Partial fill-up (is_full_tank = False) skips efficienc
    participant P152 as UC-047 Main Flow 5: If efficiency is 30% lower than vehicle baseline average,
    participant P153 as UC-051 Alternate Flow A1: PATCH /api/v1/fuel/{id} updates entry & recalculates e
    participant P154 as UC-051 Main Flow: DELETE /api/v1/fuel/{id} soft-deletes log & linked expense and
    participant P155 as UC-051 Edge Case: Deleting or patching non-existent log returns HTTP 404.
    participant P156 as UC-034: GET /api/v1/maintenance/schedules should auto-populate schedule template
    participant P157 as UC-034: POST /api/v1/maintenance logs record, updates odometer, and resets sched
    participant P158 as UC-034: POST /api/v1/maintenance rejects negative cost with HTTP 422.
    participant P159 as UC-034: Tenant cross-access rejected.
    participant P160 as UC-036: POST /api/v1/maintenance logs service record and updates linked schedule
    participant P161 as UC-036: Odometer reading > current_odometer_km updates vehicle current_odometer_
    participant P162 as UC-036: Omitting maintenance_schedule_id matches schedule item by task name subs
    participant P163 as UC-036: Rejects negative cost, negative odometer, whitespace service_type, or in
    participant P164 as UC-036: Enforces X-Organization-ID header presence and cross-tenant access prote
    participant P165 as UC-037: GET /api/v1/maintenance/records retrieves service records sorted by serv
    participant P166 as UC-037: Pagination limit and offset parameters operate correctly.
    participant P167 as UC-037: Returns 404 when vehicle_id does not exist in active organization.
    participant P168 as UC-037: Header requirements and cross-tenant boundaries are strictly enforced.
    participant P169 as Test 1: Verify GET /api/v1/vehicles/types?q=Toyota returns seeded Toyota models.
    participant P170 as Test 2: Verify POST /api/v1/vehicles registers new vehicle with tenant organizat
    participant P171 as Test 3: Verify duplicate VIN within same organization returns HTTP 409 Conflict.
    participant P172 as Test 4: Verify exceeding max_vehicles quota (max=2 for sample_org) returns HTTP
    participant P173 as Test 5: Verify custom make/model is dynamically indexed into VehicleType catalog
    participant P174 as ensure_organization()
    participant P175 as test_uc011_sole_owner_blocking()
    participant P176 as test_setup()
    participant P177 as UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency a
    participant P178 as UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per veh
    participant P179 as UC-035: POST /api/v1/maintenance/schedules creates custom schedule with default
    participant P180 as UC-035: POST /api/v1/maintenance/schedules uses provided last_performed_km and l
    participant P181 as UC-035: Rejects zero/negative intervals or empty task names with 422.
    participant P182 as UC-035: PATCH /api/v1/maintenance/schedules/{id} updates parameters and recalcul
    participant P183 as UC-035: DELETE /api/v1/maintenance/schedules/{id} soft-deletes schedule task.
    participant P184 as UC-035: Header validation and tenant cross-access isolation.
    participant P185 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with empty schedule_ids a
    participant P186 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with specific schedule_id
    participant P187 as UC-038: Returns 404 when vehicle_id is not found in active organization.
    participant P188 as UC-038: Returns 404 when one or more schedule_ids do not belong to the vehicle.
    participant P189 as UC-038: Headers and cross-tenant boundaries are strictly enforced.
    participant P190 as UC-016: Owner can create organization invitation, generating a secure 64-char to
    participant P191 as UC-016: Inviting with invalid or blank email yields HTTP 422 Unprocessable Entit
    participant P192 as UC-016: Inviting with unsupported role string yields HTTP 422 Unprocessable Enti
    participant P193 as UC-016: Re-inviting same email updates existing invitation token and TTL without
    participant P194 as UC-016: Non-owner caller attempting to send invitation yields HTTP 403 Forbidden
    participant P195 as UC-016: Owner can list all pending invitations for organization.
    participant P196 as UC-016: Listing invitations for non-existent org yields HTTP 404 Not Found.
    participant P197 as Test 1: Verify PATCH /api/v1/vehicles/{vehicle_id} successfully updates vehicle
    participant P198 as Test 2: Verify updating vehicle under wrong organization_id returns HTTP 403 For
    participant P199 as Test 3: Verify updating non-existent vehicle returns HTTP 404 Not Found.
    participant P200 as Test 4: Verify manual odometer update with discrepancy > 500 km generates an Aud
    participant P201 as Test 5: Verify non-dictionary custom_specs payload returns HTTP 422 Unprocessabl
    participant P202 as create_organization()
    participant P203 as auto_create_personal_organization()
    participant P204 as setup_db()
    participant P205 as test_setup()
    participant P206 as test_setup()
    participant P207 as test_setup()
    participant P208 as AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr
    participant P209 as AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL
    participant P210 as AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store \"facebook\" insid
    participant P211 as Alternate Flow A1: Account Linking     If email matches existing account with d
    participant P212 as Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Requ
    participant P213 as AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT
    participant P214 as Alternate Flow A1: Account Linking     If user signed up via Google, submitting
    participant P215 as Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu
    participant P216 as Edge Case: Missing email or missing password for email auth provider returns HTT
    participant P217 as AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200
    participant P218 as Edge Case: Incorrect password returns HTTP 401 Unauthorized.
    participant P219 as Edge Case: Unregistered email returns HTTP 401 Unauthorized.
    participant P220 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P221 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P222 as AC 1: WHEN an existing Google user signs in,     THE SYSTEM SHALL return HTTP 2
    participant P223 as AC 2: WHEN an existing Facebook user signs in,     THE SYSTEM SHALL return HTTP
    participant P224 as AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,
    participant P225 as AC 4 (Account Linking Flow A1): WHEN an existing user registered via email
    participant P226 as Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized.
    participant P227 as Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized.
    participant P228 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P229 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P230 as AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u
    participant P231 as AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P
    participant P232 as AC 3: GIVEN a profile update request with invalid display name length (< 2 chars
    participant P233 as AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro
    participant P234 as UC-014: POST /api/v1/organizations creates commercial organization and sets owne
    participant P235 as UC-014: POST /api/v1/organizations/personal auto-creates personal organization f
    participant P236 as UC-014: Blank or whitespace organization name rejected with HTTP 422.
    participant P237 as UC-014: GET /api/v1/organizations?user_id={id} returns list of user organization
    participant P238 as UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found.
    participant P239 as UC-015: POST /api/v1/organizations/switch switches active context for valid user
    participant P240 as UC-015: Switch attempt to organization owned by another user yields HTTP 403 For
    participant P241 as UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found.
    participant P242 as UC-015: GET /api/v1/organizations/active returns current primary organization fo
    participant P243 as UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 N
    participant P244 as Test 1: Verify GET /api/v1/vehicles?status=MAINTENANCE returns only vehicles in
    participant P245 as Test 2: Verify search query matches license plate, make, or model.
    participant P246 as Test 3: Verify filtering by province (e.g. Sindh).
    participant P247 as Test 1: Verify GET /api/v1/vehicles/{vehicle_id} returns detailed vehicle metada
    participant P248 as Test 2: Verify non-existent vehicle ID returns HTTP 404 Not Found.
    participant P249 as Test 3: Verify requesting another tenant's vehicle returns HTTP 403 Forbidden.
    participant P250 as Test 4: Verify PATCH /api/v1/vehicles/{vehicle_id}/status updates vehicle status
    participant P251 as setup_db()
    participant P252 as setup_db()
    participant P253 as setup_db()
    participant P254 as test_setup()
    participant P255 as test_setup()
    participant P256 as test_setup()
    participant P257 as test_setup()
    participant P258 as test_setup()
    participant P259 as test_setup()
    participant P260 as setup_db()
    participant P261 as test_setup()
    participant P262 as test_setup()
    participant P263 as setup_db()
    participant P264 as setup_db()
    participant P265 as test_data()
    participant P266 as setup_db()
    participant P267 as setup_db()
    participant P268 as setup_db()
    participant P269 as setup_db()
    participant P270 as sample_fleet()
    participant P271 as test_setup()
    participant P272 as test_setup()
    participant P273 as sample_org()
    participant P274 as User
    participant P275 as UserOrganization
    participant P276 as AuthSessionDTO
    participant P277 as SessionRevokeResponse
    participant P278 as UC-004: User Password Authentication & Session Initiation     Authenticates reg
    participant P279 as UC-006: Forgot Password Request     Issues a password reset JWT token with 5-mi
    participant P280 as UC-006: Password Reset Execution     Verifies reset token, validates password p
    participant P281 as UC-009: Session Refresh & Access Token Renewal     Validates active refresh tok
    participant P282 as UC-010: User Sign Out & Token Revocation     Revokes the provided refresh token
    participant P283 as UserDTO
    participant P284 as OrganizationDTO
    participant P285 as UserSessionDTO
    participant P286 as AuditService
    participant P287 as ForgotPasswordResponse
    participant P288 as ResetPasswordResponse
    participant P289 as RefreshTokenResponse
    participant P290 as LogoutResponse
    participant P291 as UserSession
    participant P292 as RegisterRequest
    participant P293 as LoginRequest
    participant P294 as ForgotPasswordRequest
    participant P295 as ResetPasswordRequest
    participant P296 as RefreshTokenRequest
    participant P297 as LogoutRequest
    participant P298 as log_event()
    participant P299 as execute_sync_batch()
    participant P300 as accept_organization_invitation()
    participant P301 as redeem_organization_invitation_code()
    participant P302 as reconcile_safepay_webhook()
    participant P303 as create_organization_invitation()
    participant P304 as submit_enterprise_inquiry()
    participant P305 as update_organization_profile()
    participant P306 as remove_organization_member()
    participant P307 as cancel_organization_invitation()
    participant P308 as verify_and_claim_ad_reward()
    participant P309 as AC 1: GIVEN an authenticated user session with a valid refresh token     WHEN s
    participant P310 as AC 2: GIVEN a revoked refresh token     WHEN submitted to POST /api/v1/auth/ref
    participant P311 as AC 3: GIVEN a malformed or invalid refresh token     WHEN submitted to POST /ap
    participant P312 as AC 4: GIVEN a refresh token that has already been revoked     WHEN logout is ca
    participant P313 as soft_delete_organization()
    participant P314 as update_vehicle()
    participant P315 as delete_vehicle()
    participant P316 as update_vehicle_odometer()
    participant P317 as restore_deleted_vehicle()
    participant P318 as assign_primary_driver()
    participant P319 as unassign_primary_driver()
    participant P320 as cancel_subscription()
    participant P321 as execute_downgrade_protocol()
    participant P322 as UC-012: Audit Log Recording for Authentication Events.         Extracts event m
    P0->>+ P1: uses
    P1-->>- P0: return
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
    P2->>+ P46: uses
    P46-->>- P2: return
    P2->>+ P47: calls
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
    P2->>+ P57: calls
    P57-->>- P2: return
    P2->>+ P58: calls
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
    P2->>+ P86: uses
    P86-->>- P2: return
    P2->>+ P87: uses
    P87-->>- P2: return
    P2->>+ P88: calls
    P88-->>- P2: return
    P2->>+ P89: calls
    P89-->>- P2: return
    P2->>+ P90: calls
    P90-->>- P2: return
    P2->>+ P91: calls
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
    P2->>+ P118: calls
    P118-->>- P2: return
    P2->>+ P119: calls
    P119-->>- P2: return
    P2->>+ P120: calls
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
    P2->>+ P132: calls
    P132-->>- P2: return
    P2->>+ P133: calls
    P133-->>- P2: return
    P2->>+ P134: calls
    P134-->>- P2: return
    P2->>+ P135: calls
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
    P2->>+ P151: uses
    P151-->>- P2: return
    P2->>+ P152: uses
    P152-->>- P2: return
    P2->>+ P153: uses
    P153-->>- P2: return
    P2->>+ P154: uses
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
    P2->>+ P168: uses
    P168-->>- P2: return
    P2->>+ P169: uses
    P169-->>- P2: return
    P2->>+ P170: uses
    P170-->>- P2: return
    P2->>+ P171: uses
    P171-->>- P2: return
    P2->>+ P172: uses
    P172-->>- P2: return
    P2->>+ P173: uses
    P173-->>- P2: return
    P2->>+ P174: calls
    P174-->>- P2: return
    P2->>+ P175: calls
    P175-->>- P2: return
    P2->>+ P176: calls
    P176-->>- P2: return
    P2->>+ P177: uses
    P177-->>- P2: return
    P2->>+ P178: uses
    P178-->>- P2: return
    P2->>+ P179: uses
    P179-->>- P2: return
    P2->>+ P180: uses
    P180-->>- P2: return
    P2->>+ P181: uses
    P181-->>- P2: return
    P2->>+ P182: uses
    P182-->>- P2: return
    P2->>+ P183: uses
    P183-->>- P2: return
    P2->>+ P184: uses
    P184-->>- P2: return
    P2->>+ P185: uses
    P185-->>- P2: return
    P2->>+ P186: uses
    P186-->>- P2: return
    P2->>+ P187: uses
    P187-->>- P2: return
    P2->>+ P188: uses
    P188-->>- P2: return
    P2->>+ P189: uses
    P189-->>- P2: return
    P2->>+ P190: uses
    P190-->>- P2: return
    P2->>+ P191: uses
    P191-->>- P2: return
    P2->>+ P192: uses
    P192-->>- P2: return
    P2->>+ P193: uses
    P193-->>- P2: return
    P2->>+ P194: uses
    P194-->>- P2: return
    P2->>+ P195: uses
    P195-->>- P2: return
    P2->>+ P196: uses
    P196-->>- P2: return
    P2->>+ P197: uses
    P197-->>- P2: return
    P2->>+ P198: uses
    P198-->>- P2: return
    P2->>+ P199: uses
    P199-->>- P2: return
    P2->>+ P200: uses
    P200-->>- P2: return
    P2->>+ P201: uses
    P201-->>- P2: return
    P2->>+ P202: calls
    P202-->>- P2: return
    P2->>+ P203: calls
    P203-->>- P2: return
    P2->>+ P204: calls
    P204-->>- P2: return
    P2->>+ P205: calls
    P205-->>- P2: return
    P2->>+ P206: calls
    P206-->>- P2: return
    P2->>+ P207: calls
    P207-->>- P2: return
    P2->>+ P208: uses
    P208-->>- P2: return
    P2->>+ P209: uses
    P209-->>- P2: return
    P2->>+ P210: uses
    P210-->>- P2: return
    P2->>+ P211: uses
    P211-->>- P2: return
    P2->>+ P212: uses
    P212-->>- P2: return
    P2->>+ P213: uses
    P213-->>- P2: return
    P2->>+ P214: uses
    P214-->>- P2: return
    P2->>+ P215: uses
    P215-->>- P2: return
    P2->>+ P216: uses
    P216-->>- P2: return
    P2->>+ P217: uses
    P217-->>- P2: return
    P2->>+ P218: uses
    P218-->>- P2: return
    P2->>+ P219: uses
    P219-->>- P2: return
    P2->>+ P220: uses
    P220-->>- P2: return
    P2->>+ P221: uses
    P221-->>- P2: return
    P2->>+ P222: uses
    P222-->>- P2: return
    P2->>+ P223: uses
    P223-->>- P2: return
    P2->>+ P224: uses
    P224-->>- P2: return
    P2->>+ P225: uses
    P225-->>- P2: return
    P2->>+ P226: uses
    P226-->>- P2: return
    P2->>+ P227: uses
    P227-->>- P2: return
    P2->>+ P228: uses
    P228-->>- P2: return
    P2->>+ P229: uses
    P229-->>- P2: return
    P2->>+ P230: uses
    P230-->>- P2: return
    P2->>+ P231: uses
    P231-->>- P2: return
    P2->>+ P232: uses
    P232-->>- P2: return
    P2->>+ P233: uses
    P233-->>- P2: return
    P2->>+ P234: uses
    P234-->>- P2: return
    P2->>+ P235: uses
    P235-->>- P2: return
    P2->>+ P236: uses
    P236-->>- P2: return
    P2->>+ P237: uses
    P237-->>- P2: return
    P2->>+ P238: uses
    P238-->>- P2: return
    P2->>+ P239: uses
    P239-->>- P2: return
    P2->>+ P240: uses
    P240-->>- P2: return
    P2->>+ P241: uses
    P241-->>- P2: return
    P2->>+ P242: uses
    P242-->>- P2: return
    P2->>+ P243: uses
    P243-->>- P2: return
    P2->>+ P244: uses
    P244-->>- P2: return
    P2->>+ P245: uses
    P245-->>- P2: return
    P2->>+ P246: uses
    P246-->>- P2: return
    P2->>+ P247: uses
    P247-->>- P2: return
    P2->>+ P248: uses
    P248-->>- P2: return
    P2->>+ P249: uses
    P249-->>- P2: return
    P2->>+ P250: uses
    P250-->>- P2: return
    P2->>+ P251: calls
    P251-->>- P2: return
    P2->>+ P252: calls
    P252-->>- P2: return
    P2->>+ P253: calls
    P253-->>- P2: return
    P2->>+ P254: calls
    P254-->>- P2: return
    P2->>+ P255: calls
    P255-->>- P2: return
    P2->>+ P256: calls
    P256-->>- P2: return
    P2->>+ P257: calls
    P257-->>- P2: return
    P2->>+ P258: calls
    P258-->>- P2: return
    P2->>+ P259: calls
    P259-->>- P2: return
    P2->>+ P260: calls
    P260-->>- P2: return
    P2->>+ P261: calls
    P261-->>- P2: return
    P2->>+ P262: calls
    P262-->>- P2: return
    P2->>+ P263: calls
    P263-->>- P2: return
    P2->>+ P264: calls
    P264-->>- P2: return
    P2->>+ P265: calls
    P265-->>- P2: return
    P2->>+ P266: calls
    P266-->>- P2: return
    P2->>+ P267: calls
    P267-->>- P2: return
    P2->>+ P268: calls
    P268-->>- P2: return
    P2->>+ P269: calls
    P269-->>- P2: return
    P2->>+ P270: calls
    P270-->>- P2: return
    P2->>+ P271: calls
    P271-->>- P2: return
    P2->>+ P272: calls
    P272-->>- P2: return
    P2->>+ P273: calls
    P273-->>- P2: return
    P1->>+ P274: uses
    P274-->>- P1: return
    P1->>+ P0: uses
    P0-->>- P1: return
    P1->>+ P275: uses
    P275-->>- P1: return
    P1->>+ P276: uses
    P276-->>- P1: return
    P1->>+ P277: uses
    P277-->>- P1: return
    P1->>+ P278: uses
    P278-->>- P1: return
    P1->>+ P279: uses
    P279-->>- P1: return
    P1->>+ P280: uses
    P280-->>- P1: return
    P1->>+ P281: uses
    P281-->>- P1: return
    P1->>+ P282: uses
    P282-->>- P1: return
    P1->>+ P283: uses
    P283-->>- P1: return
    P1->>+ P284: uses
    P284-->>- P1: return
    P1->>+ P285: uses
    P285-->>- P1: return
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
    P1->>+ P286: uses
    P286-->>- P1: return
    P1->>+ P287: uses
    P287-->>- P1: return
    P1->>+ P288: uses
    P288-->>- P1: return
    P1->>+ P289: uses
    P289-->>- P1: return
    P1->>+ P290: uses
    P290-->>- P1: return
    P1->>+ P291: uses
    P291-->>- P1: return
    P1->>+ P292: uses
    P292-->>- P1: return
    P1->>+ P293: uses
    P293-->>- P1: return
    P1->>+ P294: uses
    P294-->>- P1: return
    P1->>+ P295: uses
    P295-->>- P1: return
    P1->>+ P296: uses
    P296-->>- P1: return
    P1->>+ P297: uses
    P297-->>- P1: return
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
    P0->>+ P298: calls
    P298-->>- P0: return
    P0->>+ P286: uses
    P286-->>- P0: return
    P0->>+ P67: uses
    P67-->>- P0: return
    P0->>+ P68: uses
    P68-->>- P0: return
    P0->>+ P69: uses
    P69-->>- P0: return
    P0->>+ P70: uses
    P70-->>- P0: return
    P0->>+ P299: calls
    P299-->>- P0: return
    P0->>+ P92: uses
    P92-->>- P0: return
    P0->>+ P93: uses
    P93-->>- P0: return
    P0->>+ P94: uses
    P94-->>- P0: return
    P0->>+ P95: uses
    P95-->>- P0: return
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
    P0->>+ P300: calls
    P300-->>- P0: return
    P0->>+ P301: calls
    P301-->>- P0: return
    P0->>+ P302: calls
    P302-->>- P0: return
    P0->>+ P136: uses
    P136-->>- P0: return
    P0->>+ P137: uses
    P137-->>- P0: return
    P0->>+ P138: uses
    P138-->>- P0: return
    P0->>+ P139: uses
    P139-->>- P0: return
    P0->>+ P140: uses
    P140-->>- P0: return
    P0->>+ P141: uses
    P141-->>- P0: return
    P0->>+ P142: uses
    P142-->>- P0: return
    P0->>+ P143: uses
    P143-->>- P0: return
    P0->>+ P144: uses
    P144-->>- P0: return
    P0->>+ P303: calls
    P303-->>- P0: return
    P0->>+ P304: calls
    P304-->>- P0: return
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
    P0->>+ P305: calls
    P305-->>- P0: return
    P0->>+ P306: calls
    P306-->>- P0: return
    P0->>+ P307: calls
    P307-->>- P0: return
    P0->>+ P308: calls
    P308-->>- P0: return
    P0->>+ P309: uses
    P309-->>- P0: return
    P0->>+ P310: uses
    P310-->>- P0: return
    P0->>+ P311: uses
    P311-->>- P0: return
    P0->>+ P312: uses
    P312-->>- P0: return
    P0->>+ P313: calls
    P313-->>- P0: return
    P0->>+ P314: calls
    P314-->>- P0: return
    P0->>+ P315: calls
    P315-->>- P0: return
    P0->>+ P316: calls
    P316-->>- P0: return
    P0->>+ P317: calls
    P317-->>- P0: return
    P0->>+ P318: calls
    P318-->>- P0: return
    P0->>+ P319: calls
    P319-->>- P0: return
    P0->>+ P320: calls
    P320-->>- P0: return
    P0->>+ P321: calls
    P321-->>- P0: return
    P0->>+ P322: uses
    P322-->>- P0: return
```

## Connections by Relation

### calls
- [[log_event()]] `INFERRED`
- [[execute_sync_batch()]] `INFERRED`
- [[accept_organization_invitation()]] `INFERRED`
- [[redeem_organization_invitation_code()]] `INFERRED`
- [[reconcile_safepay_webhook()]] `INFERRED`
- [[create_organization_invitation()]] `INFERRED`
- [[submit_enterprise_inquiry()]] `INFERRED`
- [[update_organization_profile()]] `INFERRED`
- [[remove_organization_member()]] `INFERRED`
- [[cancel_organization_invitation()]] `INFERRED`
- [[verify_and_claim_ad_reward()]] `INFERRED`
- [[soft_delete_organization()]] `INFERRED`
- [[update_vehicle()]] `INFERRED`
- [[delete_vehicle()]] `INFERRED`
- [[update_vehicle_odometer()]] `INFERRED`
- [[restore_deleted_vehicle()]] `INFERRED`
- [[assign_primary_driver()]] `INFERRED`
- [[unassign_primary_driver()]] `INFERRED`
- [[cancel_subscription()]] `INFERRED`
- [[execute_downgrade_protocol()]] `INFERRED`

### contains
- [[audit_log.py]] `EXTRACTED`

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