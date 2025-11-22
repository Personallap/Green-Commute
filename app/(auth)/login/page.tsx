"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/auth-context";
import { api } from "@/lib/api";
import { Button, Input, Card } from "@/components/ui/auth-components";
import { Leaf } from "lucide-react";
import axios from "axios";

export default function LoginPage() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const response = await api.post("/auth/login", formData);
      const { access_token, refresh_token, user } = response.data;
      login(access_token, refresh_token, user);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        setError(
          err.response?.data?.error ||
            "Login failed. Please check your credentials."
        );
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md p-8 space-y-8">
        <div className="flex flex-col items-center text-center">
          <div className="h-12 w-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
            <Leaf className="h-6 w-6 text-green-600" />
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            Welcome back
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Sign in to your GreenCommute account
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Input
              label="Username or Email"
              type="text"
              required
              value={formData.username}
              onChange={(e) =>
                setFormData({ ...formData, username: e.target.value })
              }
              placeholder="Enter your username"
            />

            <Input
              label="Password"
              type="password"
              required
              value={formData.password}
              onChange={(e) =>
                setFormData({ ...formData, password: e.target.value })
              }
              placeholder="••••••••"
            />
          </div>

          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
              {error}
            </div>
          )}

          <Button type="submit" isLoading={isLoading}>
            Sign in
          </Button>

          <div className="text-center text-sm">
            <span className="text-gray-500">Don&apos;t have an account? </span>
            <Link
              href="/register"
              className="font-medium text-green-600 hover:text-green-500"
            >
              Sign up
            </Link>
          </div>
        </form>
      </Card>
    </div>
  );
}
