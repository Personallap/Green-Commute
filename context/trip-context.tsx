"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { api } from "@/lib/api";
import { AxiosError } from "axios";
import { useAuth } from "@/context/auth-context";

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
  duration?: string;
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
  saveTrip: (route: RouteOption) => Promise<boolean>;
  fetchTripHistory: () => Promise<void>;
  isLoadingHistory: boolean;
  currentSearchOrigin: string;
  currentSearchDestination: string;
}

const TripContext = createContext<TripContextType | undefined>(undefined);

export function TripProvider({ children }: { children: React.ReactNode }) {
  const [searchResults, setSearchResults] = useState<RouteOption[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [tripHistory, setTripHistory] = useState<Trip[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [currentSearchOrigin, setCurrentSearchOrigin] = useState("");
  const [currentSearchDestination, setCurrentSearchDestination] = useState("");
  const { refreshUser } = useAuth();

  // Fetch trip history on mount if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      fetchTripHistory();
    }
  }, []);

  const searchRoutes = async (from: string, to: string) => {
    setIsSearching(true);
    setSearchResults([]);

    // Store current search locations
    setCurrentSearchOrigin(from);
    setCurrentSearchDestination(to);

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

  const fetchTripHistory = async () => {
    setIsLoadingHistory(true);
    try {
      const userStr = localStorage.getItem("user_id");
      if (!userStr) {
        // Try to get user ID from auth/me endpoint
        const meResponse = await api.get("/auth/me");
        const userId = meResponse.data.user.id;
        localStorage.setItem("user_id", userId.toString());

        const response = await api.get(`/trips/${userId}`);
        const trips = response.data.trips.map(
          (trip: {
            id: number;
            origin: string;
            destination: string;
            created_at: string;
            distance_km: number;
            co2_saved: number;
            cost: number;
            mode?: string;
            duration_minutes: number;
          }) => ({
            id: trip.id.toString(),
            from: trip.origin,
            to: trip.destination,
            date: new Date(trip.created_at).toLocaleDateString(),
            distance: `${trip.distance_km} km`,
            co2Saved: trip.co2_saved,
            moneySaved: trip.cost,
            mode: trip.mode || "bus",
            duration: `${Math.round(trip.duration_minutes)} min`,
          })
        );
        setTripHistory(trips);
      } else {
        const userId = parseInt(userStr);
        const response = await api.get(`/trips/${userId}`);
        const trips = response.data.trips.map(
          (trip: {
            id: number;
            origin: string;
            destination: string;
            created_at: string;
            distance_km: number;
            co2_saved: number;
            cost: number;
            mode?: string;
            duration_minutes: number;
          }) => ({
            id: trip.id.toString(),
            from: trip.origin,
            to: trip.destination,
            date: new Date(trip.created_at).toLocaleDateString(),
            distance: `${trip.distance_km} km`,
            co2Saved: trip.co2_saved,
            moneySaved: trip.cost,
            mode: trip.mode || "bus",
            duration: `${Math.round(trip.duration_minutes)} min`,
          })
        );
        setTripHistory(trips);
      }
    } catch (error: unknown) {
      const axiosError = error as AxiosError;
      console.error("Failed to fetch trip history:", axiosError);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const saveTrip = async (route: RouteOption): Promise<boolean> => {
    try {
      const userStr = localStorage.getItem("user_id");
      let userId: number | null = null;

      if (userStr) {
        userId = parseInt(userStr);
      } else {
        try {
          const meResponse = await api.get("/auth/me");
          userId = meResponse.data.user.id;
          if (userId !== null) {
            localStorage.setItem("user_id", userId.toString());
          }
        } catch {
          console.log("User not authenticated, saving trip without user_id");
        }
      }

      const distanceKm = parseFloat(route.distance.replace(" km", ""));
      const durationMinutes = parseFloat(route.duration.replace(" min", ""));

      // Calculate car CO2 for comparison (120g per km)
      const carCo2 = distanceKm * 120;
      const co2Saved = carCo2 - route.co2;

      const tripData = {
        user_id: userId ?? undefined,
        origin: currentSearchOrigin,
        destination: currentSearchDestination,
        distance_km: distanceKm,
        duration_minutes: durationMinutes,
        cost: route.cost,
        transfers: route.switches,
        co2_saved: co2Saved,
        transit_co2: route.co2,
        car_co2: carCo2,
        mode: route.mode,
      };

      const response = await api.post("/trips", tripData);

      if (response.status === 201) {
        // Add to local state
        const newTrip: Trip = {
          id: response.data.trip.id.toString(),
          from: currentSearchOrigin,
          to: currentSearchDestination,
          date: new Date().toLocaleDateString(),
          distance: route.distance,
          co2Saved: co2Saved,
          moneySaved: route.cost,
          mode: route.mode,
          duration: route.duration,
        };
        addTrip(newTrip);

        // Refresh trip history to get updated data
        await fetchTripHistory();

        // Refresh user data to update dashboard CO2 stats
        await refreshUser();

        return true;
      }
      return false;
    } catch (error: unknown) {
      const axiosError = error as AxiosError;
      console.error("Failed to save trip:", axiosError);
      return false;
    }
  };

  return (
    <TripContext.Provider
      value={{
        searchResults,
        isSearching,
        searchRoutes,
        tripHistory,
        addTrip,
        saveTrip,
        fetchTripHistory,
        isLoadingHistory,
        currentSearchOrigin,
        currentSearchDestination,
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
