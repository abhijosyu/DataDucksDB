# Spring 2026 CS 3200 Project - Dining Ducks
**Team Members**: Abhirham Josyula, Pranay Pentyala, Seongwon Yang, Jaylen Zeng, Huizhi (Sara) Zou

## Overview
Dining Ducks is a data-driven restaurant review & analytics platform which connects customers, staff, and businesses through structured feedback. The platform allows customers to make better dining decisions while employees share transparent workplace insights to help restaurants gain actionable analytics to improve performance.

## Features and User Roles
- **Administrator**
  - Manages the platform
  - Handles reviews and restaurant listings

- **Reviewer (Customers / Critics)**
  - Submits restaurant reviews
  - Rates categories such as:
    - Customer Service
    - Food Quality
    - Price Value

- **Employee**
  - Provides behind-the-scenes reviews
  - Rates categories such as:
    - Pay
    - Management
    - Work-Life Balance
  - Shares insights about workplace conditions

- **Company (Restaurant Owners / Managers)**
  - Views analytics dashboard
  - Tracks performance across locations
  - Identifies trends and improvement areas

## Tech Stack
- Frontend: Streamlit
- Backnend: Flask
- Database: MySQL
- Containerization: Docker

## Project Structure
- `./app`              - streamlit frontend
- `./api`              - Flask API (Blueprints & routes)
- `./database-files/`  - SQL schema + mock data
- docker-compose.yml   - Container setup
- README.md

## How to Run the Project
1. Clone the Repository
```bash
git clone https://github.com/abhijosyu/DataDucksDB.git
cd <repo-name>
```
2. Create `.env` file
3. Run Docker Containers
```bash
docker compose up -d
```
4. Access the App
- Streamlit UI: http://localhost:8501
- API server: http://localhost:4000

## REST API Overview
- The API is organized using Flask Blueprints by role or resources.
Examples:
  - `GET/reviews` --> fetch reviews
  - `POST/reviews` --> create review
  - `PUT/reviews/{id}` --> update review
  - `DELETE/reviews/{id}` --> fetch review


## Database
- Includes mock data
- Tables include:
  - User
  - Compnay
  - CustomerReview
  - Rating
  - RestaurantLocation

