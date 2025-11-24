"use client";

import React, { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { Card } from "@/components/ui/auth-components";
import { useTrip } from "@/context/trip-context";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8B5CF6"];

export function StatsCharts() {
  const { tripHistory, isLoadingHistory } = useTrip();

  // Generate bar chart data from trip history
  const barData = useMemo(() => {
    return tripHistory
      .slice(0, 5)
      .reverse()
      .map((trip, idx) => ({
        name: `Trip ${tripHistory.length - idx}`,
        co2: trip.co2Saved,
        money: trip.moneySaved,
      }));
  }, [tripHistory]);

  // Generate pie chart data from trip modes
  const pieData = useMemo(() => {
    const modeCounts: Record<string, number> = {};

    tripHistory.forEach((trip) => {
      const mode = trip.mode || "unknown";
      modeCounts[mode] = (modeCounts[mode] || 0) + 1;
    });

    return Object.entries(modeCounts).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value,
    }));
  }, [tripHistory]);

  if (isLoadingHistory) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card className="p-6">
          <div className="flex items-center justify-center h-[300px]">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600" />
          </div>
        </Card>
        <Card className="p-6">
          <div className="flex items-center justify-center h-[300px]">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600" />
          </div>
        </Card>
      </div>
    );
  }

  if (tripHistory.length === 0) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Savings Analysis
          </h3>
          <div className="flex items-center justify-center h-[300px]">
            <p className="text-gray-500">No trip data available yet</p>
          </div>
        </Card>
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Transport Modes
          </h3>
          <div className="flex items-center justify-center h-[300px]">
            <p className="text-gray-500">No trip data available yet</p>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Savings Analysis
        </h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={barData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="co2" name="CO2 Saved (g)" fill="#16a34a" />
              <Bar dataKey="money" name="Money Saved ($)" fill="#2563eb" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Transport Modes
        </h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name} ${((percent || 0) * 100).toFixed(0)}%`
                }
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
}
