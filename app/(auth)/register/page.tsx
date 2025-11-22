"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/auth-context";
import { api } from "@/lib/api";
import { Button, Input, Card } from "@/components/ui/auth-components";
import { Leaf } from "lucide-react";
import axios from "axios";

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setIsLoading(true);

    try {
      const response = await api.post("/auth/register", {
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });

      const { access_token, refresh_token, user } = response.data;
      login(access_token, refresh_token, user);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        setError(
          err.response?.data?.error || "Registration failed. Please try again."
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
            Create an account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Join GreenCommute and start saving CO2 today
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Input
              label="Username"
              type="text"
              required
              value={formData.username}
              onChange={(e) =>
                setFormData({ ...formData, username: e.target.value })
              }
              placeholder="Choose a username"
            />

            <Input
              label="Email"
              type="email"
              required
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
              placeholder="name@example.com"
            />

            <Input
              label="Password"
              type="password"
              required
              value={formData.password}
              onChange={(e) =>
                setFormData({ ...formData, password: e.target.value })
              }
              placeholder="Min. 6 characters"
            />

            <Input
              label="Confirm Password"
              type="password"
              required
              value={formData.confirmPassword}
              onChange={(e) =>
                setFormData({ ...formData, confirmPassword: e.target.value })
              }
              placeholder="Confirm your password"
            />
          </div>

          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
              {error}
            </div>
          )}

          <Button type="submit" isLoading={isLoading}>
            Create Account
          </Button>

          <div className="text-center text-sm">
            <span className="text-gray-500">Already have an account? </span>
            <Link
              href="/login"
              className="font-medium text-green-600 hover:text-green-500"
            >
              Sign in
            </Link>
          </div>
        </form>
      </Card>
    </div>
  );
}
