# Mobile Apps (Android & iOS)

## Option A: Expo (React Native)

1. Install Node.js (LTS) and Expo CLI:
   - `npm install -g expo-cli`
2. Create app:
   - `npx create-expo-app loan-manager-mobile`
3. Configure API base in `.env`:
   - `API_BASE=https://globe-swift.org/api`
4. Build:
   - Android: `expo build:android`
   - iOS: `expo build:ios` (via EAS)

## Option B: Capacitor (wrap web)

1. Create Capacitor app:
   - `npm create @capacitor/app`
2. Point `webDir` to frontend build (`frontend/.next` or a static build)
3. Add platforms:
   - `npx cap add android`
   - `npx cap add ios`
4. Open native IDEs and build:
   - Android Studio (APK/AAB)
   - Xcode (IPA)
