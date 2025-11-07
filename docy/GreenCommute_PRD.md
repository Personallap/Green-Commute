
# GreenCommute – Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** 2025-10-05  
**Author:** Aditya Raj  

---

## 1. Executive Summary

**GreenCommute** is a web-based platform that empowers urban commuters to make climate-conscious travel decisions by finding optimized public transit routes. The system analyzes user input (origin/destination) to calculate and compare multiple travel routes based on time, cost, number of transfers, and carbon footprint — offering the most eco-friendly route available.

GreenCommute’s purpose is not just route optimization but behavior change. By visualizing carbon emissions saved through public transit vs private vehicles, it nudges users toward sustainable commuting.

---

## 2. Problem and User Pain Points

### 🔍 Problem
- Private vehicles contribute significantly to urban pollution, yet many people avoid public transit due to perceived inconvenience.
- Lack of transparent environmental impact data makes commuters unaware of how beneficial public transit could be.

### 😣 User Pain Points
- No easy way to compare multiple public transit routes based on time and carbon footprint.
- Users lack motivation to prefer public transportation owing to insufficient environmental incentive or awareness.
- Transport apps only optimize for time, not sustainability.

---

## 3. Goals and Success Metrics

| Goal | Success Metric |
|------|----------------|
| Encourage public transit usage | 20% repeat users in 3 months |
| Provide carbon footprint insights | 90% route searches show CO₂ savings data |
| Simplify eco-friendly route selection | 80% of users accept recommended route |
| Grow platform engagement | 500 daily active users (DAU) within 6 months |

---

## 4. Target Audience and Personas

### 🎯 Target Audience
- Urban commuters (students, employees, eco-conscious users)
- Cities with active public transit networks
- Climate-tech startups and educational institutions

### 👤 Personas

| Name | Profile | Key Need |
|------|---------|----------|
| Rahul (Student) | Takes college bus/metro daily | Find shortest and cheapest route |
| Shreya (Tech Employee) | Commutes daily via bus/metro | Compare carbon impact of public vs ride-sharing |
| Karan (Eco-Conscious Blogger) | Wants to reduce personal carbon emissions | Track CO₂ savings and promote green choices |

---

## 5. Key Features

### ✨ MVP Features
- 🧭 Route Optimization: Based on time, emissions, transfers, and cost
- 🔄 CO₂ Comparison Tool: Public transport vs private vehicle emissions
- 📊 Visual Dashboard: Graphs showing trip data and savings
- 💾 Trip History: Saved searches and CO₂ stats per user
- 🖥️ Responsive UI: Works on desktop and mobile browsers

### 🚀 Future Roadmap
- 🚌 Real-time transit API integration (e.g., Google Transit, MapMyIndia)
- 🔐 User Authentication for personalized dashboards
- 🎮 Gamification: Rewards for CO₂ saved
- 📱 Mobile App (React Native)

---

## 6. User Flow / Journey Map

1. User opens app
2. Inputs origin and destination
3. System fetches routes and calculates:
   - Time
   - Cost
   - Transfers
   - CO₂ footprint
4. User views ranked route options + emission comparison chart
5. Optionally saves the route to their profile
6. Dashboard shows total CO₂ saved over time

---

## 7. Technical Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js, Tailwind CSS |
| Backend | Python (FastAPI or Flask) |
| Database | SQLite (MVP), Firebase (Auth/Realtime for v2) |
| Visualization | Chart.js / Recharts (Frontend), Matplotlib (Backend) |
| Algorithm | Dijkstra or A* for route optimization |
| Hosting | Vercel (Frontend), Render / Heroku (Backend) |

---

## 8. Design Principles & Accessibility

- 🌱 Sustainable theme using green/earthy colors
- 🎨 Simple UI with visual cues for eco-friendly decisions
- ♿ WCAG AA accessibility standards: high contrast, ALT tags, keyboard navigation
- 📱 Mobile-first responsive design

---

## 9. Monetization Strategy

- Freemium model: Basic route analysis free, advanced stats for paid users
- API access package for government/corporate use
- Sponsored green initiatives (earn by featuring eco-friendly brands)
- Carbon offset affiliates (earn per purchase of verified offset)

---

## 10. Risks, Dependencies, and Assumptions

| Risk/Dependency | Mitigation/Assumption |
|-----------------|------------------------|
| Transit API access required for real-time data | Use static data in MVP, upgrade later |
| User adoption slow due to niche target | Target urban hubs & college campuses first |
| Relies on external vehicle CO₂ standards | Use publicly available emissions estimates |
| Technical complexity of algorithm | Implement MVP with Dijkstra, scale later |

---

## 11. Appendix

- System Diagram
- Route Scoring Formula (TBD)
- CO₂ Calculation Models

---

**End of Document**
