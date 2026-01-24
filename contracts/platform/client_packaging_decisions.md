# VTE Client Packaging Decisions
**Status**: APPROVED
**Date**: 2026-01-23

## 1. Strategy: "Thin Shell, Thick Spine"
The Client Apps are minimal wrappers around the WebView (or PWA context) that bridge hardware biometrics to the API.

## 2. Platform Matrix

| Platform | Packaging Format | Distribution Channel | Signing Mechanism | Update Strategy |
|:---|:---|:---|:---|:---|
| **Windows** | MSIX | Microsoft Store (Private) | EV Code Signing (Sectigo) | Store Auto-Update |
| **MacOS** | DMG / PKG | Corporate MDM (Jamf) | Apple Developer ID | Sparkle |
| **iOS** | IPA | Apple Business Manager | Enterprise Cert | MDM Push |
| **Android** | APK | Managed Google Play | Play Signing Key | Play Auto-Update |
| **Web** | PWA (Manifest) | Browser | TLS + HSTS | Service Worker Cache |

## 3. Critical Constraints
*   **No Sideloading**: All installs must verify against the Corp Root CA or be signed by the VTE Release Key.
*   **Anti-Tamper**: Mobile apps must use RASP (Runtime Application Self-Protection) to detect root/jailbreak.
