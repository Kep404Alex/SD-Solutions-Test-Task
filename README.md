# **Weather API Service**

A FastAPI-based weather API that fetches weather data for a city, caches responses, and stores logs in DynamoDB.

---

## **What is this?**

This service provides:
- **Weather Data**: Fetch weather information from an OpenWeatherMap.
- **Caching**: Cache responses locally for 5 minutes to reduce API calls.
- **Logs**: Store weather data logs in **DynamoDB**.

---

## **How to Run It with Docker Compose**

1. **Ensure Docker and Docker Compose are Installed**:
   - [Install Docker](https://www.docker.com/)
   - [Install Docker Compose](https://docs.docker.com/compose/)

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/Kep404Alex/SD-Solutions-Test-Task.git
   cd SD-Solutions-Test-Task

3. **Start the Application**:
   ```bash
   docker-compose up --build

4. **Access the API**:
   ```bash
   Swagger UI: http://127.0.0.1:8000/docs
   ReDoc: http://127.0.0.1:8000/redoc
