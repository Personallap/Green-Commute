import React from "react";
import { Quote } from "lucide-react";

interface QuoteCardProps {
  quote: string;
  author: string;
}

export function QuoteCard({ quote, author }: QuoteCardProps) {
  return (
    <figure className="flex flex-col gap-4 p-8 rounded-2xl bg-white/10 backdrop-blur-sm border border-white/10">
      <Quote className="h-8 w-8 text-green-300 opacity-50" />
      <blockquote className="text-xl font-medium leading-relaxed text-white">
        &quot;{quote}&quot;
      </blockquote>
      <figcaption className="text-green-200 font-medium">— {author}</figcaption>
    </figure>
  );
}
