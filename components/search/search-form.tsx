"use client";

import React, { useState } from "react";
import { Button, Input } from "@/components/ui/auth-components";
import { useTrip } from "@/context/trip-context";
import { Search, MapPin } from "lucide-react";

export function SearchForm() {
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const { searchRoutes, isSearching } = useTrip();

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!from.trim() || !to.trim()) return;
    await searchRoutes(from, to);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <Search className="h-5 w-5 text-green-600" />
        Find Routes
      </h2>
      <form onSubmit={handleSearch} className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">From</label>
          <div className="relative">
            <MapPin className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <Input
              value={from}
              onChange={(e) => setFrom(e.target.value)}
              placeholder="Origin (e.g. Central Station)"
              className="pl-10"
              required
            />
          </div>
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">To</label>
          <div className="relative">
            <MapPin className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <Input
              value={to}
              onChange={(e) => setTo(e.target.value)}
              placeholder="Destination (e.g. City Park)"
              className="pl-10"
              required
            />
          </div>
        </div>
        <Button type="submit" disabled={isSearching} className="w-full">
          {isSearching ? "Searching..." : "Search Routes"}
        </Button>
      </form>
    </div>
  );
}
