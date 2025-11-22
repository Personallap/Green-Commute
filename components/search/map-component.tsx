"use client";

import React, { useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useTrip } from "@/context/trip-context";

// Fix for default marker icon in Leaflet with Next.js
const iconUrl = "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png";
const iconRetinaUrl =
  "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png";
const shadowUrl =
  "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png";

const customIcon = new L.Icon({
  iconUrl,
  iconRetinaUrl,
  shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

function MapUpdater({ center }: { center: [number, number] }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo(center, 13);
  }, [center, map]);
  return null;
}

export function MapComponent() {
  const { searchResults } = useTrip();
  const defaultCenter: [number, number] = [51.505, -0.09]; // London default

  // Mock coordinates for demo
  const startPos: [number, number] = [51.505, -0.09];
  const endPos: [number, number] = [51.515, -0.1];

  return (
    <MapContainer
      center={defaultCenter}
      zoom={13}
      style={{ height: "100%", width: "100%", minHeight: "500px" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={startPos} icon={customIcon}>
        <Popup>Start</Popup>
      </Marker>

      <Marker position={endPos} icon={customIcon}>
        <Popup>End</Popup>
      </Marker>

      {searchResults.length > 0 && (
        <Polyline
          positions={[startPos, endPos]}
          color="green"
          weight={4}
          opacity={0.7}
        />
      )}

      <MapUpdater center={startPos} />
    </MapContainer>
  );
}
