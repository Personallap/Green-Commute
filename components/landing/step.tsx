import React from "react";

interface StepProps {
  number: string;
  title: string;
  description: string;
}

export function Step({ number, title, description }: StepProps) {
  return (
    <div className="flex flex-col items-center text-center">
      <div className="flex items-center justify-center w-12 h-12 rounded-full bg-green-600 text-white text-xl font-bold mb-6 shadow-lg shadow-green-600/20">
        {number}
      </div>
      <h3 className="text-xl font-semibold text-gray-900 mb-3">{title}</h3>
      <p className="text-gray-600 leading-relaxed max-w-xs">{description}</p>
    </div>
  );
}
