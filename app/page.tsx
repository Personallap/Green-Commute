"use client";

import React from "react";
import Link from "next/link";
import { Button, Card } from "@/components/ui/auth-components";
import { FeatureCard } from "@/components/landing/feature-card";
import { Step } from "@/components/landing/step";
import { QuoteCard } from "@/components/landing/quote-card";
import { Leaf, Map, BarChart3, ArrowRight, CheckCircle2 } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-white text-gray-900 font-sans">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 w-full border-b border-gray-100 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100 text-green-600">
              <Leaf className="h-5 w-5" />
            </div>
            <span className="text-xl font-bold tracking-tight text-gray-900">
              GreenCommute
            </span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="secondary" className="hidden sm:flex">
                Sign In
              </Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden pt-16 pb-24 sm:pt-24 sm:pb-32">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center animate-fade-in">
            <div className="mx-auto max-w-3xl">
              <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-6xl mb-6">
                Travel Smarter, <br className="hidden sm:block" />
                <span className="text-green-600">Breathe Easier</span>
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-600 mb-10">
                Analyze your transit routes based on carbon footprint, cost, and
                efficiency. Make informed decisions for a sustainable future.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link href="/register" className="w-full sm:w-auto">
                  <Button className="h-12 px-8 text-base w-full sm:w-auto">
                    Start Analyzing <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Link href="/login" className="w-full sm:w-auto">
                  <Button
                    variant="outline"
                    className="h-12 px-8 text-base w-full sm:w-auto"
                  >
                    Log In
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-24 sm:py-32 bg-gray-50">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center mb-16">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Why Choose GreenCommute?
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                We provide the tools you need to make eco-friendly travel
                choices without compromising on convenience.
              </p>
            </div>
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <FeatureCard
                icon={<Leaf className="h-6 w-6 text-green-600" />}
                title="Carbon Footprint"
                description="Track your CO2 emissions for every trip and see how much you save by choosing greener options."
              />
              <FeatureCard
                icon={<BarChart3 className="h-6 w-6 text-blue-600" />}
                title="Cost Analysis"
                description="Compare ticket prices and fuel costs to find the most budget-friendly route for your commute."
              />
              <FeatureCard
                icon={<Map className="h-6 w-6 text-purple-600" />}
                title="Route Switching"
                description="Seamlessly switch between bus, train, bike, and car routes to find the perfect balance."
              />
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-24 sm:py-32 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center mb-16">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                How It Works
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Start your sustainable journey in three simple steps.
              </p>
            </div>
            <div className="grid grid-cols-1 gap-12 md:grid-cols-3">
              <Step
                number="1"
                title="Create an Account"
                description="Sign up for free to access personalized route planning and history tracking."
              />
              <Step
                number="2"
                title="Enter Your Route"
                description="Input your origin and destination to see all available transit options."
              />
              <Step
                number="3"
                title="Compare & Go"
                description="Choose the best route based on CO2, time, and cost, and start your journey."
              />
            </div>
          </div>
        </section>

        {/* Quotes Section */}
        <section className="py-24 sm:py-32 bg-green-900 text-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
              <QuoteCard
                quote="The greatest threat to our planet is the belief that someone else will save it."
                author="Robert Swan"
              />
              <QuoteCard
                quote="We do not inherit the earth from our ancestors, we borrow it from our children."
                author="Native American Proverb"
              />
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-full bg-green-100 text-green-600">
              <Leaf className="h-4 w-4" />
            </div>
            <span className="text-lg font-semibold text-gray-900">
              GreenCommute
            </span>
          </div>
          <p className="text-sm text-gray-500">
            &copy; {new Date().getFullYear()} GreenCommute. All rights reserved.
          </p>
          <div className="flex gap-6">
            <a href="#" className="text-sm text-gray-500 hover:text-gray-900">
              Privacy
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-900">
              Terms
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-900">
              Contact
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
