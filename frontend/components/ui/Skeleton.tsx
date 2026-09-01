import React from "react";
import { clsx } from "clsx";

export const Skeleton: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, ...props }) => (
  <div className={clsx("animate-pulse bg-slate-800/80 rounded-xl", className)} {...props} />
);

export const CardSkeleton: React.FC = () => (
  <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
    <div className="flex items-center space-x-3">
      <Skeleton className="w-10 h-10 rounded-xl" />
      <div className="space-y-2 flex-1">
        <Skeleton className="h-4 w-1/3" />
        <Skeleton className="h-3 w-1/2" />
      </div>
    </div>
    <Skeleton className="h-20 w-full" />
    <div className="flex justify-between">
      <Skeleton className="h-4 w-20" />
      <Skeleton className="h-4 w-16" />
    </div>
  </div>
);
