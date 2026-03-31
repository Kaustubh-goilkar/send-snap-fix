# 📸 Send Snap Fix

Welcome to **Send Snap Fix**!
A web application built using **Python Flask** that allows users to submit issues (with images, comments, and location), while admins can review and manage them.

This project is fully containerized using **Docker**, so you can run it without worrying about local environment setup.

---

## 🚀 Features

* 📷 Upload images with issue reports
* 📝 Add comments and problem types
* 📍 Capture user location
* 👨‍💼 Admin panel to view and manage submissions
* 🐳 Docker-based setup for easy deployment

---

## 📋 Prerequisites

Make sure you have the following installed:

* Docker
* Docker Compose

### Install Docker

* Windows: [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)
* Mac: [https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)
* Linux: [https://docs.docker.com/desktop/install/linux-install/](https://docs.docker.com/desktop/install/linux-install/)

> Note: Docker Desktop (Windows/Mac) includes Docker Compose.
> Linux users may need to install it separately.

---

## 📂 Project Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd send-snap-fix
```

---

### 2️⃣ Build & Run the Application

Make sure Docker is running, then execute:

```bash
docker-compose up --build
```

### 🔍 What this does:

* Builds the Docker image using your `Dockerfile`
* Instantiates containers defined in `docker-compose.yml`
* Starts the Flask application

---

### 3️⃣ Access the Application

Once the server is running, open your browser and go to:

👉 [http://localhost:8000](http://localhost:8000)

---

## 🛑 Stopping the Application

To stop the running containers:

```bash
Ctrl + C
```

To completely stop and remove containers, networks:

```bash
docker-compose down
```

---

## ⚙️ Environment Variables (Optional)

If your project uses environment variables, you can create a `.env` file:

```env
FLASK_ENV=development
FLASK_APP=app.py
```

Docker Compose will automatically pick this up.

---

## 🧱 Project Structure (Example)

```
send-snap-fix/
│── app.py
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── static/
│── templates/
│── uploads/
```

---

## 🐳 Docker Overview

* **Dockerfile** → Defines the Flask app environment
* **docker-compose.yml** → Manages multi-container setup
* **Port 8000** → Exposed for accessing the app

---

## ⚠️ Common Issues

### Port already in use

Change the port in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"
```

---

### Changes not reflecting

Rebuild containers:

```bash
docker-compose up --build
```

---

### Docker not running

Make sure Docker Desktop/service is started.

---

## 📌 Future Improvements

* Authentication system
* Role-based access control
* Notifications system
* Cloud deployment (AWS / Azure / GCP)

---

## 🤝 Contributing

Feel free to fork the repository and submit pull requests.

---

## 📄 License

This project is licensed under the MIT License.

---

If you want, I can also:

* add API documentation section
* create a **professional GitHub badge header**
* or tailor this README specifically for your **Flask + React / Admin workflow** 🚀
