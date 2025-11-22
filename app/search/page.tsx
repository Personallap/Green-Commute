"use client";

import React, { useEffect } from "react";
import { useAuth } from "@/context/auth-context";
import { useRouter } from "next/navigation";
import { SearchForm } from "@/components/search/search-form";
import { RouteResults } from "@/components/search/route-results";
import dynamic from "next/dynamic";

// Dynamically import MapComponent to avoid SSR issues with Leaflet
const MapComponent = dynamic(
  () =>
    import("@/components/search/map-component").then((mod) => mod.MapComponent),
  { ssr: false }
);

export default function SearchPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600" />
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900">Plan Your Trip</h1>
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm text-gray-600 hover:text-green-600 font-medium"
          >
            Go to Dashboard
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col lg:flex-row gap-6">
        {/* Left Sidebar: Search & Results */}
        <div className="w-full lg:w-1/3 flex flex-col gap-6">
          <SearchForm />
          <RouteResults />
        </div>

        {/* Right Side: Map */}
        <div className="w-full lg:w-2/3 bg-white rounded-xl shadow-sm overflow-hidden min-h-[500px] lg:min-h-0 relative">
          <MapComponent />
        </div>
      </main>
    </div>
  );
}
