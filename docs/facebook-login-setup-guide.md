# Admin Guide: Facebook Login Setup (Meta Developer Console & Firebase Integration)

> **Purpose:** Step-by-step guide for developers/admins to register Meta App credentials, link Firebase Authentication, and configure native mobile client settings for Facebook Sign-In in Veltrics.

---

## Overview of Credentials & Touchpoints

```
  +-----------------------+              +-----------------------+
  | Meta Developer Console|              |    Firebase Console   |
  | (developers.facebook) |              |  (Authentication)     |
  +-----------+-----------+              +-----------+-----------+
              |                                      |
              | App ID & Secret                      | Enable Facebook Provider
              v                                      v
  +--------------------------------------------------------------+
  |                 Veltrics Client App & Backend                 |
  +--------------------------------------------------------------+
```

---

## Step 1: Meta Developer Portal Setup

1. Go to [Meta for Developers Portal](https://developers.facebook.com/) and log in.
2. Click **My Apps** → **Create App**.
3. Select **Authenticate and request data from users with Facebook Login** (or **Consumer** app type).
4. Enter App Display Name (e.g., `Veltrics Fleet Management`) and App Contact Email.
5. Click **Create App**.

---

## Step 2: Configure Facebook Login Product

1. Under the App Dashboard, locate **Facebook Login** and click **Set Up**.
2. Select **Web** (or Android/iOS).
3. In the left navigation sidebar, go to **Facebook Login → Settings**.
4. Under **Client OAuth Settings**:
   - Enable **Client OAuth Login**: `YES`
   - Enable **Web OAuth Login**: `YES`
   - Set **Valid OAuth Redirect URIs**:
     ```text
     https://<YOUR-FIREBASE-PROJECT-ID>.firebaseapp.com/__/auth/handler
     ```
     *(Replace `<YOUR-FIREBASE-PROJECT-ID>` with your Firebase project ID, e.g. `veltrics-dev` or `veltrics-prod`)*.
5. Save changes.

---

## Step 3: Retrieve App ID & App Secret

1. In the left sidebar, navigate to **App Settings → Basic**.
2. Copy the following credentials:
   - **App ID** (e.g., `1234567890123456`)
   - **App Secret** (Click *Show* to reveal, e.g., `a1b2c3d4e5f6...`)
3. Add Privacy Policy URL and Terms of Service URL if moving to production mode.

---

## Step 4: Configure Firebase Authentication

1. Open [Firebase Console](https://console.firebase.google.com/).
2. Select your Veltrics Firebase project (`veltrics-dev`, `veltrics-staging`, or `veltrics-prod`).
3. In the left menu, go to **Build → Authentication → Sign-in method**.
4. Click **Add new provider** → Select **Facebook**.
5. Toggle **Enable**.
6. Enter credentials copied from Meta Developer Portal:
   - **App ID:** Paste Facebook App ID
   - **App Secret:** Paste Facebook App Secret
7. Copy the OAuth Redirect URI provided by Firebase and verify it matches Step 2.4.
8. Click **Save**.

---

## Step 5: Native Android Configuration (`src/frontend/android`)

1. Open `src/frontend/android/app/src/main/res/values/strings.xml` (create if missing):
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <resources>
       <string name="app_name">Veltrics</string>
       <string name="facebook_app_id">YOUR_FACEBOOK_APP_ID</string>
       <string name="fb_login_protocol_scheme">fbYOUR_FACEBOOK_APP_ID</string>
       <string name="facebook_client_token">YOUR_FACEBOOK_CLIENT_TOKEN</string>
   </resources>
   ```
2. Open `src/frontend/android/app/src/main/AndroidManifest.xml`:
   - Inside `<application>` tag, add:
     ```xml
     <meta-data android:name="com.facebook.sdk.ApplicationId" android:value="@string/facebook_app_id"/>
     <meta-data android:name="com.facebook.sdk.ClientToken" android:value="@string/facebook_client_token"/>

     <activity android:name="com.facebook.FacebookActivity"
         android:configChanges="keyboard|keyboardHidden|screenLayout|screenSize|orientation"
         android:label="@string/app_name" />
     <activity
         android:name="com.facebook.CustomTabActivity"
         android:exported="true">
         <intent-filter>
             <action android:name="android.intent.action.VIEW" />
             <category android:name="android.intent.category.DEFAULT" />
             <category android:name="android.intent.category.BROWSABLE" />
             <data android:scheme="@string/fb_login_protocol_scheme" />
         </intent-filter>
     </activity>
     ```

---

## Step 6: Native iOS Configuration (`src/frontend/ios`)

1. Open `src/frontend/ios/Runner/Info.plist` and add the following keys:
   ```xml
   <key>CFBundleURLTypes</key>
   <array>
     <dict>
       <key>CFBundleURLSchemes</key>
       <array>
         <string>fbYOUR_FACEBOOK_APP_ID</string>
       </array>
     </dict>
   </array>
   <key>FacebookAppID</key>
   <string>YOUR_FACEBOOK_APP_ID</string>
   <key>FacebookClientToken</key>
   <string>YOUR_FACEBOOK_CLIENT_TOKEN</string>
   <key>FacebookDisplayName</key>
   <string>Veltrics</string>
   <key>LSApplicationQueriesSchemes</key>
   <array>
     <string>fbapi</string>
     <string>fb-messenger-share-api</string>
   </array>
   ```

---

## Verification & Testing

- **Development Testing:** In Meta App Dashboard, add developer/tester Facebook accounts under **Roles → Roles → Add Testers** to test before submitting for Meta App Review.
- **Production Mode:** Switch mode from *Development* to *Live* in top navigation bar of Meta Developer Portal after adding Privacy Policy URL.
