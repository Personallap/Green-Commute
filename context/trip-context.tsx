"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { api } from "@/lib/api";
import { AxiosError } from "axios";

export interface RouteOption {
  id: string;
  mode: "bus" | "train" | "car" | "bike" | "walk";
  duration: string; // e.g., "45 min"
  distance: string; // e.g., "12 km"
  cost: number;
  co2: number; // in grams
  switches: number;
  steps: string[];
}

export interface Trip {
  id: string;
  from: string;
  to: string;
  date: string;
  distance: string;
  co2Saved: number;
  moneySaved: number;
  mode: string;
}

interface RouteSegment {
  mode: string;
  line?: string;
  line_number?: string;
  from_stop: string;
  to_stop: string;
  distance_km: number;
  duration_minutes: number;
  cost: number;
  co2: number;
}

interface BackendRoute {
  segments: RouteSegment[];
  total_duration_minutes: number;
  total_distance_km: number;
  total_cost: number;
  total_co2: number;
  transfers: number;
}

interface TripContextType {
  searchResults: RouteOption[];
  isSearching: boolean;
  searchRoutes: (from: string, to: string) => Promise<void>;
  tripHistory: Trip[];
  addTrip: (trip: Trip) => void;
}

const TripContext = createContext<TripContextType | undefined>(undefined);

export function TripProvider({ children }: { children: React.ReactNode }) {
  const [searchResults, setSearchResults] = useState<RouteOption[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [tripHistory, setTripHistory] = useState<Trip[]>([]);

  // Load history from local storage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem("trip_history");
    if (savedHistory) {
      try {
        // Use a timeout to avoid synchronous state update warning during mount
        setTimeout(() => {
          setTripHistory(JSON.parse(savedHistory));
        }, 0);
      } catch (e) {
        console.error("Failed to parse trip history", e);
      }
    }
  }, []);

  // Save history to local storage whenever it changes
  useEffect(() => {
    localStorage.setItem("trip_history", JSON.stringify(tripHistory));
  }, [tripHistory]);

  const searchRoutes = async (from: string, to: string) => {
    setIsSearching(true);
    setSearchResults([]);

    try {
      const response = await api.post("/routes/search", {
        origin: from,
        destination: to,
      });

      const routes = response.data.routes.map(
        (route: BackendRoute, index: number) => {
          // Determine primary mode from segments or default to bus
          const primaryMode =
            route.segments.length > 0 ? route.segments[0].mode : "bus";

          // Format steps from segments
          const steps = route.segments.map((segment: RouteSegment) => {
            return `${
              segment.mode === "walk" ? "Walk" : "Take " + segment.mode
            } (${segment.line || segment.line_number || "Direct"}) from ${
              segment.from_stop
            } to ${segment.to_stop}`;
          });

          return {
            id: `route-${index}-${Date.now()}`,
            mode: primaryMode as "bus" | "train" | "car" | "bike" | "walk",
            duration: `${Math.round(route.total_duration_minutes)} min`,
            distance: `${route.total_distance_km} km`,
            cost: route.total_cost,
            co2: route.total_co2,
            switches: route.transfers,
            steps: steps,
          };
        }
      );

      console.log("API Response:", response.data);
      console.log("Mapped Routes:", routes);
      setSearchResults(routes);
    } catch (error: unknown) {
      const axiosError = error as AxiosError;
      console.error("Failed to search routes:", axiosError);
      if (axiosError.response) {
        console.error("Error Response Data:", axiosError.response.data);
        console.error("Error Status:", axiosError.response.status);
      }
      // Optionally handle error state here, e.g., show a toast
    } finally {
      setIsSearching(false);
    }
  };

  const addTrip = (trip: Trip) => {
    setTripHistory((prev) => [trip, ...prev]);
  };

  return (
    <TripContext.Provider
      value={{
        searchResults,
        isSearching,
        searchRoutes,
        tripHistory,
        addTrip,
      }}
    >
      {children}
    </TripContext.Provider>
  );
}

export function useTrip() {
  const context = useContext(TripContext);
  if (context === undefined) {
    throw new Error("useTrip must be used within a TripProvider");
  }
  return context;
}
