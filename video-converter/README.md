# Secure 4K UHD Video Converter

A cloud-native web application that allows users to securely upload, convert, and download 4K UHD video files at custom resolutions. Built with Python, FastAPI, Next.js, FFmpeg, and AWS S3 — with encryption, user authentication, and activity logging.

---

## Features

- 🔐 **Google Authentication** via Firebase Auth
- 📤 **Secure Upload** of 4K UHD video files
- 🎛️ **Video Conversion** to 1080p, 720p, 480p using FFmpeg
- 🛡️ **AES-256 Encryption** of videos before storage
- ☁️ **Encrypted Cloud Storage** in AWS S3
- 📜 **Activity Logging** in Firestore or MongoDB Atlas
- 📥 **Secure Download** via signed, time-limited URLs
- ⚙️ **Cloud Hosted**: Firebase Hosting (frontend) + Render/GCR (backend)
- 🧩 **Simple Frontend** built with HTML, Tailwind CSS, jQuery

---

## Tech Stack

| Layer                  | Technology / Tool                                     | Purpose                                            |
| ---------------------- | ----------------------------------------------------- | -------------------------------------------------- |
| **Frontend**           | **HTML + Tailwind CSS**                               | UI layout & styling                                |
|                        | **jQuery**                                            | Ajax-based API communication                       |
|                        | **Firebase JS SDK**                                   | Client-side authentication (Google login)          |
|                        | **Hosted on Firebase Hosting / S3**                   | Static hosting of the frontend                     |
| **Backend**            | **FastAPI (Python)**                                  | Handles uploads, conversion, auth token validation |
|                        | **FFmpeg (Python subprocess)**                        | Video resolution conversion                        |
|                        | **PyCryptodome / Cryptography**                       | AES-256 encryption at rest                         |
| **Authentication**     | **Firebase Authentication**                           | Secure login using Google                          |
| **Storage**            | **Amazon S3 (encrypted buckets)**                     | Secure cloud storage for videos                    |
| **Database**           | **Firestore** or **MongoDB Atlas**                    | Activity logging (uploads, conversions, downloads) |
| **Video Processing**   | **FFmpeg**                                            | Downscaling videos (e.g. 4K to 1080p, 720p)        |
| **Hosting (Frontend)** | **Firebase Hosting**, **AWS S3**, or **Netlify**      | For static files                                   |
| **Hosting (Backend)**  | **Render**, **Google Cloud Run**, or **EC2 + Docker** | For FastAPI service                                |
| **CI/CD**              | **GitHub Actions**                                    | Auto-deploy frontend/backend, run tests            |


---

## Project Structure

secure-video-converter/
├── frontend/ # Static frontend
│ ├── index.html
│ ├── app.js # jQuery + Firebase auth + upload
│ ├── firebase-config.js # Firebase SDK config
│ └── style.css # Tailwind custom styles (optional)
├── backend/ # FastAPI service
│ ├── main.py # Upload API, FFmpeg, encryption
│ └── utils/ # Video and encryption logic
├── docker/ # Dockerfiles for backend
├── .github/workflows/ # CI/CD pipeline config
├── .env.example # Environment variable template
└── README.md # Project documentation

