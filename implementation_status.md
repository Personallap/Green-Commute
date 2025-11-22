# GreenCommute Implementation Status

## Overview

The GreenCommute project is a full-stack application designed to help users find eco-friendly commuting routes and track their CO2 savings. It consists of a Next.js frontend and a Flask backend.

## Frontend Implementation

**Tech Stack:** Next.js 16, React 19, Tailwind CSS 4

**Current Status:**

- **Initialization:** The project has been initialized with `create-next-app`.
- **Structure:** Standard Next.js App Router structure (`app/` directory).
- **Pages:** Only the default landing page (`app/page.tsx`) is currently present.
- **Styling:** Tailwind CSS is configured (`globals.css`).
- **Missing:** No custom components, pages, or API integration have been implemented on the frontend yet.

## Backend Implementation

**Tech Stack:** Python, Flask, SQLAlchemy, SQLite (implied)

**Current Status:**
The backend is more advanced, with a structured API and core logic for route planning and user management.

### API Endpoints

The following endpoints are implemented in `backend/app/routes/routes.py`:

#### General

- `GET /api/health`: Checks if the API is running.

#### Users

- `POST /api/users`: Creates a new user account.
- `GET /api/users/<user_id>`: Retrieves user details.

#### Routes & Transit

- `POST /api/routes/search`: Core feature. Searches for optimal routes between an origin and destination.
  - **Logic:** Uses a graph-based approach (Dijkstra's algorithm) to find paths.
  - **Optimization:** Supports optimizing by **Time**, **Cost**, and **CO2 Emissions**.
  - **Fallback:** Generates sample routes if no direct transit path is found.
- `GET /api/stops`: Retrieves all available transit stops.
- `GET /api/transit/stops`: (Duplicate/Alias) Retrieves all transit stops.
- `GET /api/transit/lines`: Retrieves all transit lines.

#### Trips & Tracking

- `POST /api/trips`: Saves a completed trip for a user.
- `GET /api/trips/<user_id>`: Retrieves a user's trip history.
- `GET /api/trips/stats/<user_id>`: Calculates and returns user statistics:
  - Total trips
  - Total distance traveled
  - Total CO2 saved
  - Total cost
  - Average CO2 saved per trip

#### CO2 Calculator

- `POST /api/co2/compare`: Compares CO2 emissions for a given distance between a specific transit mode and driving.

### Data Models

- **User:** Stores username, email, and total CO2 saved.
- **Trip:** Records details of individual trips (origin, destination, mode, CO2 saved, cost, etc.).
- **Transit Models:** `TransitStop`, `TransitLine`, `StopConnection` (implied from usage) support the routing graph.

## Summary

The backend logic for GreenCommute is largely in place, supporting the core value proposition of eco-friendly route finding and tracking. The frontend is currently a blank slate and needs to be built out to consume these APIs and present the UI to the user.
