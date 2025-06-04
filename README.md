# Fullstack Face Recognition AI with AWS

## Features
- 🔍 Live face recognition from camera
- ☁️ Uploads image results to AWS S3
- 🗃️ Logs data in PostgreSQL (AWS RDS)
- 🌐 React frontend to view stream
- 🐳 Dockerized deployment on AWS EC2 Free Tier

## Setup

### 1. Backend
- Set environment variables:
  - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`, `S3_BUCKET`
- Run with Docker:
```bash
docker-compose up --build
```

### 2. Frontend
```bash
cd frontend
npm install
npm start
```

## Deployment on AWS EC2 (Free Tier)
1. Launch EC2 instance
2. Install Docker, Git, Node
3. Clone this repo
4. Set env variables
5. Run `docker-compose up --build`

## Notes
- You need an AWS S3 bucket and AWS RDS PostgreSQL instance.
- IAM role with proper permissions required for EC2 to access S3.