"use client";

import React, { useState } from "react";
import { useTrip, RouteOption } from "@/context/trip-context";
import { Leaf, ArrowRight, ChevronDown, ChevronUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

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
  const [isExpanded, setIsExpanded] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const { saveTrip } = useTrip();

  // Calculate car CO2 for comparison
  const distanceKm = parseFloat(route.distance.replace(" km", ""));
  const carCo2 = distanceKm * 120;
  const co2Saved = carCo2 - route.co2;

  const handleSelectRoute = async () => {
    setIsSaving(true);
    try {
      const success = await saveTrip(route);

      if (success) {
        alert(
          "Trip saved successfully! Check your dashboard to see it in your history."
        );
      } else {
        alert("Failed to save trip. Please try again.");
      }
    } catch (error) {
      console.error("Error saving trip:", error);
      alert("Failed to save trip. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`rounded-xl border transition-all ${
        isBest
          ? "bg-green-50 border-green-200 ring-1 ring-green-500"
          : "bg-white border-gray-100"
      }`}
    >
      <div
        className="p-4 cursor-pointer hover:shadow-md transition-shadow"
        onClick={() => setIsExpanded(!isExpanded)}
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
          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="font-bold text-gray-900">
                ${(route.cost ?? 0).toFixed(2)}
              </div>
              <div className="text-xs text-gray-500">{route.duration}</div>
            </div>
            <button
              className="text-gray-400 hover:text-gray-600 transition-colors"
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(!isExpanded);
              }}
            >
              {isExpanded ? (
                <ChevronUp className="h-5 w-5" />
              ) : (
                <ChevronDown className="h-5 w-5" />
              )}
            </button>
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
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 border-t border-gray-100 pt-4 space-y-4">
              {/* Route Steps */}
              <div>
                <h5 className="font-semibold text-gray-900 mb-2 text-sm">
                  Route Steps:
                </h5>
                <ol className="space-y-2">
                  {route.steps.map((step, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex gap-2">
                      <span className="text-green-600 font-semibold">
                        {idx + 1}.
                      </span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ol>
              </div>

              {/* Details Grid */}
              <div className="grid grid-cols-2 gap-3 bg-gray-50 p-3 rounded-lg">
                <div>
                  <p className="text-xs text-gray-500">Total Distance</p>
                  <p className="font-semibold text-gray-900">
                    {route.distance}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Switches</p>
                  <p className="font-semibold text-gray-900">
                    {route.switches}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">CO₂ Saved vs Car</p>
                  <p className="font-semibold text-green-600">
                    {co2Saved.toFixed(0)}g
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Duration</p>
                  <p className="font-semibold text-gray-900">
                    {route.duration}
                  </p>
                </div>
              </div>

              {/* Select Button */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleSelectRoute();
                }}
                disabled={isSaving}
                className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                {isSaving ? "Saving..." : "Select This Route"}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
