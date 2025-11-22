"use client";

import React from "react";
import { useTrip, RouteOption } from "@/context/trip-context";
import { Leaf, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

export function RouteResults() {
  const { searchResults, isSearching } = useTrip();

  if (isSearching) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-32 bg-gray-100 rounded-xl animate-pulse" />
        ))}
      </div>
    );
  }

  if (searchResults.length === 0) {
    return null;
  }

  // Find best route (lowest CO2)
  const bestRouteId = [...searchResults].sort((a, b) => a.co2 - b.co2)[0]?.id;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Available Routes</h3>
      <div className="space-y-3">
        {searchResults.map((route) => (
          <RouteCard
            key={route.id}
            route={route}
            isBest={route.id === bestRouteId}
          />
        ))}
      </div>
    </div>
  );
}

function RouteCard({ route, isBest }: { route: RouteOption; isBest: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`p-4 rounded-xl border transition-all hover:shadow-md cursor-pointer ${
        isBest
          ? "bg-green-50 border-green-200 ring-1 ring-green-500"
          : "bg-white border-gray-100"
      }`}
    >
      {isBest && (
        <div className="mb-2 inline-flex items-center px-2 py-1 rounded-full bg-green-100 text-green-700 text-xs font-medium">
          <Leaf className="h-3 w-3 mr-1" /> Best for Planet
        </div>
      )}
      <div className="flex justify-between items-start mb-3">
        <div>
          <h4 className="font-semibold text-gray-900 capitalize flex items-center gap-2">
            {route.mode}
            <span className="text-gray-400 font-normal text-sm">
              • {route.distance}
            </span>
          </h4>
        </div>
        <div className="text-right">
          <div className="font-bold text-gray-900">
            ${route.cost.toFixed(2)}
          </div>
          <div className="text-xs text-gray-500">{route.duration}</div>
        </div>
      </div>

      <div className="flex items-center justify-between text-sm text-gray-600 bg-gray-50/50 p-2 rounded-lg">
        <div className="flex items-center gap-1" title="CO2 Emissions">
          <Leaf
            className={`h-4 w-4 ${
              route.co2 < 100 ? "text-green-500" : "text-orange-500"
            }`}
          />
          <span>{route.co2}g CO₂</span>
        </div>
        <div className="flex items-center gap-1">
          <ArrowRight className="h-4 w-4 text-gray-400" />
          <span>{route.switches} switches</span>
        </div>
      </div>
    </motion.div>
  );
}
