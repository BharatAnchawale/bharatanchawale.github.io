| Component          | Technology                                     |
| ------------------ | ---------------------------------------------- |
| Frontend           | Next.js (React) + TailwindCSS                  |
| Backend            | **FastAPI** (Python)                           |
| Auth               | Firebase Auth / Auth0 / Clerk                  |
| Object Storage     | **Amazon S3** (with SSE)                       |
| Video Conversion   | FFmpeg in Cloud Function / container           |
| Database (Logging) | **Firebase Firestore** or **MongoDB Atlas**    |
| Hosting (Frontend) | **Vercel** (with GitHub integration)           |
| Hosting (Backend)  | **Render** / **Fly.io** / **Google Cloud Run** |
| CI/CD              | GitHub Actions                                 |
| Secret Management  | GitHub Actions + Render secrets                |


1. User Authentication
Use Firebase Auth or Clerk.dev for OAuth/email login

JWT tokens sent to backend for secure communication

2. Frontend (Next.js)
Pages:

/login – Auth login/signup

/upload – File selection + optional client encryption

/convert – Resolution + format selection

/history – Logs for past conversions

/download/:fileId – Download page

3. Backend (FastAPI - Python)
API Endpoints:

| Endpoint         | Method | Description                      |
| ---------------- | ------ | -------------------------------- |
| `/upload`        | POST   | Accepts encrypted video upload   |
| `/convert`       | POST   | Triggers FFmpeg conversion       |
| `/download/{id}` | GET    | Serves encrypted video securely  |
| `/logs`          | GET    | Admin logs (with access control) |

4. Encryption Strategy
Server-Side:
Encrypt videos using AES-256 before storing in S3

Store encryption keys per video, encrypted with app master key

Optional Client-Side:
Use WebCrypto API to encrypt before upload

Share decryption key via secure key exchange (out of scope unless needed)

5. Video Conversion (FFmpeg)
FFmpeg runs in:

a Cloud Run container (preferred for scaling), or

Render service, with mounted volume or S3 integration

Use Python subprocess or ffmpeg-python wrapper

6. Object Storage (S3)
Store uploaded and converted files

Use S3 Server-Side Encryption (SSE) + signed URLs

Files auto-expire after X days using lifecycle policies

7. Logging System
Log every action:

Upload

Conversion

Download

Errors

Use Firebase Firestore or MongoDB Atlas for cloud-managed logging.

GitHub Repository Structure
secure-video-converter/
├── frontend/             # Next.js App
│   ├── pages/
│   ├── components/
│   └── services/         # API + Auth helpers
├── backend/              # FastAPI App
│   ├── main.py
│   ├── routes/
│   ├── services/         # ffmpeg, encryption, s3
│   └── models/           # pydantic schemas
├── .github/workflows/    # CI/CD
├── docker/
│   ├── ffmpeg.Dockerfile
│   └── fastapi.Dockerfile
├── README.md
└── .env.example

Deployment Plan
| Component | Platform     | How                               |
| --------- | ------------ | --------------------------------- |
| Frontend  | Vercel       | GitHub → Vercel auto-deploy       |
| Backend   | Render / GCP | Docker-based deployment (FastAPI) |
| S3        | AWS          | Secure bucket + signed URLs       |
| Logs      | Firestore    | Firebase Firestore setup          |
| CI/CD     | GitHub       | With GitHub Actions on push       |


Phase 1: Setup
 GitHub repo init

 Bootstrap frontend (Next.js) and backend (FastAPI)

 Add Firebase Auth integration

Phase 2: File Upload & Encryption
 Frontend upload page

 Encrypt file before sending (client or server-side)

 Upload to backend → save to S3

Phase 3: FFmpeg Conversion
 Backend triggers FFmpeg with user-selected resolution

 Upload converted file to S3

 Store mapping in DB

Phase 4: Download Flow
 Generate pre-signed S3 URL

 Download + optional decrypt on client

Phase 5: Logging & Admin Tools
 Record logs to Firestore

 Build a /history or /admin page


