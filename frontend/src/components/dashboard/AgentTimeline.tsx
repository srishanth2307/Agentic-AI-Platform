import {
  CheckCircle2,
  Circle,
  Loader2,
  XCircle,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { AgentStep, AgentStatus } from "@/types/api";
import { cn } from "@/lib/utils";

const statusConfig: Record<
  AgentStatus,
  { icon: React.ElementType; badge: "success" | "default" | "muted" | "destructive"; label: string }
> = {
  completed: { icon: CheckCircle2, badge: "success", label: "Completed" },
  running: { icon: Loader2, badge: "default", label: "Running" },
  pending: { icon: Circle, badge: "muted", label: "Pending" },
  failed: { icon: XCircle, badge: "destructive", label: "Failed" },
};

interface AgentTimelineProps {
  steps: AgentStep[];
}

export function AgentTimeline({ steps }: AgentTimelineProps) {
  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-base">Agent Execution Timeline</CardTitle>
        <CardDescription>Live sequential trace from LangGraph</CardDescription>
      </CardHeader>
      <CardContent>
        {steps.every((s) => s.status === "pending") ? (
          <p className="py-8 text-center text-sm text-muted-foreground">
            No data available
          </p>
        ) : (
          <ol className="relative space-y-0">
            {steps.map((step, index) => {
              const config = statusConfig[step.status];
              const Icon = config.icon;
              const isLast = index === steps.length - 1;

              return (
                <li key={step.id} className="relative flex gap-4 pb-6 last:pb-0">
                  {!isLast && (
                    <span
                      className={cn(
                        "absolute left-[11px] top-7 h-[calc(100%-12px)] w-px",
                        step.status === "completed" ? "bg-emerald-200" : "bg-border",
                      )}
                    />
                  )}
                  <div
                    className={cn(
                      "relative z-10 flex h-6 w-6 shrink-0 items-center justify-center rounded-full ring-4 ring-card",
                      step.status === "completed" && "bg-emerald-50",
                      step.status === "running" && "bg-accent",
                      step.status === "pending" && "bg-muted",
                      step.status === "failed" && "bg-red-50",
                    )}
                  >
                    <Icon
                      className={cn(
                        "h-3.5 w-3.5",
                        step.status === "completed" && "text-emerald-600",
                        step.status === "running" && "animate-spin text-primary",
                        step.status === "pending" && "text-muted-foreground",
                        step.status === "failed" && "text-destructive",
                      )}
                    />
                  </div>
                  <div className="min-w-0 flex-1 pt-0.5">
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-sm font-medium">{step.label}</p>
                      <Badge variant={config.badge}>{config.label}</Badge>
                    </div>
                    <p className="mt-0.5 text-xs capitalize text-muted-foreground">
                      {step.agent} agent
                    </p>
                    {step.durationMs != null && (
                      <p className="mt-1 text-xs text-muted-foreground">
                        {step.durationMs}ms
                      </p>
                    )}
                  </div>
                </li>
              );
            })}
          </ol>
        )}
      </CardContent>
    </Card>
  );
}
