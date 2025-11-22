# GreenCommute Future Implementation Plan

This document outlines the roadmap for transforming the current GreenCommute prototype into a fully functional, production-ready application.

## 1. Authentication & User Management

**Goal:** Secure the application and enable personalized user experiences.

### Backend Changes

- **Technology:** JSON Web Tokens (JWT) via `flask-jwt-extended`.
- **New Endpoints:**
  - `POST /api/auth/register`: Register a new user.
  - `POST /api/auth/login`: Authenticate and return access/refresh tokens.
  - `POST /api/auth/refresh`: Refresh expired access tokens.
  - `GET /api/auth/me`: Get current user profile (protected).
- **Database Updates:**
  - Add `password_hash` column to `User` model.
  - Implement password hashing using `werkzeug.security`.

### Frontend Integration

- **Auth Context:** Create a React Context (`AuthContext`) to manage user state (user object, loading status, tokens).
- **Protected Routes:** Create a `ProtectedRoute` component to redirect unauthenticated users from private pages (e.g., Dashboard, Profile).
- **Interceptors:** Configure Axios/Fetch to automatically attach the JWT token to outgoing requests.

## 2. Frontend Development (Full Scale)

# GreenCommute Future Implementation Plan

This document outlines the roadmap for transforming the current GreenCommute prototype into a fully functional, production-ready application.

## 1. Authentication & User Management

**Goal:** Secure the application and enable personalized user experiences.

### Backend Changes

-   **Technology:** JSON Web Tokens (JWT) via `flask-jwt-extended`.
-   **New Endpoints:**
    -   `POST /api/auth/register`: Register a new user.
    -   `POST /api/auth/login`: Authenticate and return access/refresh tokens.
    -   `POST /api/auth/refresh`: Refresh expired access tokens.
    -   `GET /api/auth/me`: Get current user profile (protected).
-   **Database Updates:**
    -   Add `password_hash` column to `User` model.
    -   Implement password hashing using `werkzeug.security`.

### Frontend Integration

-   **Auth Context:** Create a React Context (`AuthContext`) to manage user state (user object, loading status, tokens).
-   **Protected Routes:** Create a `ProtectedRoute` component to redirect unauthenticated users from private pages (e.g., Dashboard, Profile).
-   **Interceptors:** Configure Axios/Fetch to automatically attach the JWT token to outgoing requests.

## 2. Frontend Development (Full Scale)

**Goal:** Build a modern, responsive, and interactive user interface.

### Architecture

-   **Framework:** Next.js 16 (App Router).
-   **Styling:** Tailwind CSS 4 with a custom design system (colors, typography).
-   **State Management:** React Context for global state (Auth, Theme), local state for forms/UI.
-   **Visualization:** `recharts` for data visualization (charts/graphs).
-   **Maps:** `react-leaflet` (with OpenStreetMap) or Google Maps API for route visualization.

### Key Pages & Features

1.  **Landing Page (`/`)**
    -   Hero section with value proposition.
    -   "How it Works" section.
    -   Call to Action (CTA) to Register/Login.
2.  **Authentication Pages**
    -   `/login`: User login form.
    -   `/register`: New user registration.
3.  **Dashboard (`/dashboard`)**
    -   **Route Search:** Interactive form to enter Origin/Destination.
    -   **Map View:** Visual representation of routes (integration with Google Maps or Leaflet).
    -   **Results List:** Display calculated routes with comparison (Time vs. Cost vs. CO2).
4.  **Trip History (`/trips`)**
    -   List of past trips.
    -   Details view for specific trips.
5.  **Statistics (`/stats`)**
    -   Visual charts (Bar/Line) showing CO2 savings over time.
    -   Gamification elements (Badges, Ranks).

### Core Components

-   `Button`, `Input`, `Card`: Reusable UI building blocks.
-   `RouteCard`: Displays route details (mode icons, duration, cost, CO2).
-   `MapComponent`: Handles map rendering and markers.
-   `Navbar` / `Sidebar`: Navigation structure.

## 3. Backend-Frontend Integration

**Goal:** Connect the UI to the backend logic.

### API Client

-   Create a centralized API client (e.g., `src/lib/api.ts`) to handle all HTTP requests.
-   Define TypeScript interfaces for all API responses (User, Trip, Route, Stop).

### Data Flow

1.  **Search Flow:**
    -   User types location -> Frontend calls `GET /api/stops` (cached) for autocomplete.
    -   User submits -> Frontend calls `POST /api/routes/search`.
    -   Backend calculates routes -> Returns JSON.
    -   Frontend renders `RouteCard` list.
2.  **Trip Saving:**
    -   User selects a route -> Frontend calls `POST /api/trips`.
    -   Backend saves trip -> Updates User stats.
    -   Frontend redirects to Trip History or shows success modal.

## 4. Testing & Quality Assurance

-   **Backend:** Add `pytest` suite for all API endpoints.
-   **Frontend:** Add `Jest` + `React Testing Library` for component testing.
-   **E2E:** Use Playwright/Cypress for critical user flows (Login -> Search -> Save Trip).

## 5. Deployment Pipeline

-   **Backend:** Dockerize the Flask app. Deploy to a cloud provider (AWS/GCP/Render).
-   **Frontend:** Deploy Next.js app to Vercel.
-   **Database:** Migrate SQLite to PostgreSQL for production.

## 6. Visualization & Maps
**Goal:** Make data understandable and actionable through visual representation.

### Data Visualization (Charts)
-   **Library:** `recharts` (Native React support, lightweight).
-   **Key Charts:**
    -   **CO2 Savings Over Time:** Line chart showing cumulative savings.
    -   **Mode Comparison:** Bar chart comparing Cost/Time/CO2 for different transit modes (Car vs. Metro vs. Bus).
    -   **Trip Distribution:** Pie chart showing usage of different transport modes.

### Map Integration
-   **Library:** `react-leaflet` (Open-source, free) or `@react-google-maps/api` (Requires API Key).
-   **Features:**
    -   **Interactive Map:** Display source and destination markers.
    -   **Route Rendering:** Draw polyline paths for calculated routes.
    -   **Stop Selection:** Clickable transit stops on the map.
    -   **Real-time Tracking:** (Future scope) Show live vehicle positions.

## 7. Deployment Pipeline
-   **Backend:** Dockerize the Flask app. Deploy to a cloud provider (AWS/GCP/Render).
-   **Frontend:** Deploy Next.js app to Vercel.
-   **Database:** Migrate SQLite to PostgreSQL for production.
