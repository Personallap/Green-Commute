"use client";

import React, { useEffect } from "react";
import { useAuth } from "@/context/auth-context";
import { useRouter } from "next/navigation";
import { Button, Card } from "@/components/ui/auth-components";
import { Leaf, LogOut, User } from "lucide-react";
import { StatsCharts } from "@/components/dashboard/stats-charts";
import { TripHistory } from "@/components/dashboard/trip-history";

export default function DashboardPage() {
  const { user, logout, isLoading, isAuthenticated } = useAuth();
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

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Leaf className="h-8 w-8 text-green-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">
                GreenCommute
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-700">
                <User className="h-4 w-4" />
                <span>{user.username}</span>
              </div>
              <Button variant="outline" onClick={logout} className="w-auto">
                <LogOut className="h-4 w-4 mr-2 text-black" />
                Sign out
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">
            {/* Welcome Card */}
            <Card className="p-6 col-span-full">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Welcome back, {user.username}! 👋
                  </h2>
                  <p className="text-gray-600">
                    You&apos;ve saved{" "}
                    <span className="font-bold text-green-600">
                      {user.total_co2_saved}g
                    </span>{" "}
                    of CO2 so far. Keep it up!
                  </p>
                </div>
                <Button onClick={() => router.push("/search")}>
                  Plan New Trip
                </Button>
              </div>
            </Card>

            {/* Quick Stats */}
            <Card className="p-6">
              <h3 className="font-semibold text-gray-900 mb-2">
                Total CO2 Saved
              </h3>
              <div className="text-3xl font-bold text-green-600">
                {user.total_co2_saved}g
              </div>
              <p className="text-sm text-gray-500 mt-1">Lifetime savings</p>
            </Card>

            <Card className="p-6">
              <h3 className="font-semibold text-gray-900 mb-2">
                Account Status
              </h3>
              <div className="flex items-center space-x-2">
                <div className="h-3 w-3 bg-green-500 rounded-full" />
                <span className="text-gray-900">Active</span>
              </div>
              <p className="text-sm text-gray-500 mt-1">
                Member since{" "}
                {new Date(
                  user.created_at || new Date().toISOString()
                ).toLocaleDateString()}
              </p>
            </Card>

            <Card className="p-6">
              <h3 className="font-semibold text-gray-900 mb-2">Next Goal</h3>
              <div className="text-3xl font-bold text-blue-600">500g</div>
              <p className="text-sm text-gray-500 mt-1">
                Reach 500g CO2 savings
              </p>
            </Card>
          </div>

          <StatsCharts />
          <TripHistory />
        </div>
      </main>
    </div>
  );
}
