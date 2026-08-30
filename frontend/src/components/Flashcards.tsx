import React from 'react';
import { CreditCard } from 'lucide-react';
export default function Flashcards() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><CreditCard /> Flashcards</h1>
      <p className="text-muted-foreground mt-2 mb-6">Spaced repetition with SM-2 algorithm.</p>
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-card border border-border rounded-lg p-6">
          <h2 className="font-semibold text-lg mb-2">Deck Stats</h2>
          <div className="text-sm space-y-1 text-muted-foreground">
            <p>Cards reviewed: 42</p>
            <p>Due today: 7</p>
            <p>Retention: 87%</p>
          </div>
        </div>
        <div className="md:col-span-2 bg-card border border-border rounded-lg p-6">
          <h2 className="font-semibold text-lg mb-2">Next Card</h2>
          <div className="p-6 bg-secondary/30 rounded-lg border border-border/30 mt-3 text-center min-h-[8rem] flex flex-col justify-center">
            <p className="text-lg font-medium">What is a vector space?</p>
            <button className="mt-4 text-sm text-primary hover:underline">Show Answer</button>
          </div>
          <div className="flex gap-3 mt-4">
            <button className="px-3 py-1 text-sm bg-red-50 text-red-600 rounded">Again</button>
            <button className="px-3 py-1 text-sm bg-amber-50 text-amber-600 rounded">Hard</button>
            <button className="px-3 py-1 text-sm bg-emerald-50 text-emerald-600 rounded">Good</button>
            <button className="px-3 py-1 text-sm bg-blue-50 text-blue-600 rounded">Easy</button>
          </div>
        </div>
      </div>
    </div>
  );
}
