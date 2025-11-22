"use client";

import React from "react";
import { Card } from "@/components/ui/auth-components";
import { Leaf, DollarSign, Calendar } from "lucide-react";

// Mock data for history
const historyData = [
  {
    id: 1,
    from: "Central Station",
    to: "City Park",
    date: "2023-10-25",
    distance: "12 km",
    co2Saved: 120,
    moneySaved: 2.5,
    mode: "Bus",
  },
  {
    id: 2,
    from: "Home",
    to: "Office",
    date: "2023-10-24",
    distance: "8 km",
    co2Saved: 80,
    moneySaved: 1.5,
    mode: "Bike",
  },
  {
    id: 3,
    from: "Library",
    to: "Gym",
    date: "2023-10-23",
    distance: "5 km",
    co2Saved: 50,
    moneySaved: 0.0,
    mode: "Walk",
  },
];

export function TripHistory() {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Trips</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Route
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Mode
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Savings
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {historyData.map((trip) => (
              <tr key={trip.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {trip.from} → {trip.to}
                  </div>
                  <div className="text-sm text-gray-500">{trip.distance}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center text-sm text-gray-500">
                    <Calendar className="h-4 w-4 mr-1" />
                    {trip.date}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    {trip.mode}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <div className="flex flex-col gap-1">
                    <span className="flex items-center text-green-600">
                      <Leaf className="h-3 w-3 mr-1" />
                      {trip.co2Saved}g CO₂
                    </span>
                    <span className="flex items-center text-blue-600">
                      <DollarSign className="h-3 w-3 mr-1" />${trip.moneySaved}
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
