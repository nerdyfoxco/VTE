# VTE Security Controls Map (OWASP/MASVS)
**Status**: DRAFT

## 1. OWASP ASVS (Web)
| ID | Requirement | VTE Implementation |
|----|-------------|--------------------|
| 2.1.1 | Verify all authentication controls are enforced on the server side. | Implemented in `spine` middleware (FastAPI Dependencies). |
| 3.1.1 | Verify Session Tokens are signed and secure. | OIDC Tokens validated via JWKS. |
| 5.3.3 | Verify output encoding (XSS prevention). | React/Next.js Auto-Escaping + strict CSP. |
| 8.1.1 | Verify data protection in transit. | TLS 1.3 enforced (Deny-All Egress Policy). |

## 2. OWASP MASVS (Mobile)
| ID | Requirement | VTE Implementation |
|----|-------------|--------------------|
| MSTG-AUTH-1 | Enforce Authentication on Server. | Mobile App sends Bearer Token to Spine. |
| MSTG-STORAGE-1 | Secure Storage of Secrets. | Device KeyStore/Keychain usage mandated. |
| MSTG-CRYPTO-1 | Cryptographic Agility. | LibSodium/BouncyCastle wrapper usage. |
