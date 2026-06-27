import { BrainCircuit, GitBranch } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import type { PlannerState } from "@/types/api";
import { cn } from "@/lib/utils";

const statusStyles = {
  executing: { label: "Executing", dot: "bg-primary animate-pulse", badge: "default" as const },
  planning: { label: "Planning", dot: "bg-amber-500 animate-pulse", badge: "warning" as const },
  completed: { label: "Completed", dot: "bg-emerald-500", badge: "success" as const },
  idle: { label: "Idle", dot: "bg-muted-foreground/40", badge: "muted" as const },
};

interface PlannerStatusProps {
  planner: PlannerState;
}

export function PlannerStatus({ planner }: PlannerStatusProps) {
  const config = statusStyles[planner.status];
  const progress =
    planner.totalSteps > 0
      ? Math.round((planner.completedSteps / planner.totalSteps) * 100)
      : 0;

  return (
    <Card className="border-none bg-transparent shadow-none">
      <CardContent className="flex flex-wrap items-center gap-4 p-0 lg:gap-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
            <BrainCircuit className="h-5 w-5 text-primary" />
          </div>
          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
              Planner Status
            </p>
            <div className="flex items-center gap-2">
              <span className={cn("h-2 w-2 rounded-full", config.dot)} />
              <p className="text-lg font-semibold tracking-tight">{config.label}</p>
            </div>
          </div>
        </div>

        <div className="hidden h-10 w-px bg-border sm:block" />

        <div className="min-w-[140px]">
          <p className="text-xs text-muted-foreground">Current agent</p>
          <p className="text-sm font-medium">{planner.currentAgent || "No data available"}</p>
        </div>

        <div className="min-w-[120px]">
          <p className="text-xs text-muted-foreground">Progress</p>
          <p className="text-sm font-medium">
            {planner.completedSteps} / {planner.totalSteps} steps
          </p>
        </div>

        <div className="min-w-[160px] flex-1">
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>Pipeline progress</span>
            <span className="font-medium text-foreground">{progress}%</span>
          </div>
          <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-muted">
            <div
              className="h-full rounded-full bg-primary transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <Badge variant="outline" className="gap-1 font-mono text-[10px]">
          <GitBranch className="h-3 w-3" />
          {planner.mode}
        </Badge>

        {planner.planId && (
          <Badge variant="secondary" className="font-mono text-[10px]">
            {planner.planId.slice(0, 8)}…
          </Badge>
        )}
      </CardContent>
    </Card>
  );
}
