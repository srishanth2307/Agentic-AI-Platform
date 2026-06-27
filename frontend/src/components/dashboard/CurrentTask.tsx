import { Clock, Target } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { currentTask } from "@/data/mockDashboard";
import { formatRelativeTime } from "@/lib/utils";

export function CurrentTask() {
  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">Current Task</CardTitle>
          <Badge variant="secondary" className="font-mono text-[10px]">
            {currentTask.runId}
          </Badge>
        </div>
        <CardDescription>Active goal being processed by agents</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-3 rounded-lg bg-accent/60 p-4">
          <Target className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
          <p className="text-sm leading-relaxed">{currentTask.goal}</p>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-lg border bg-muted/30 p-3">
            <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Started
            </p>
            <p className="mt-1 flex items-center gap-1.5 text-sm font-medium">
              <Clock className="h-3.5 w-3.5 text-muted-foreground" />
              {formatRelativeTime(currentTask.startedAt)}
            </p>
          </div>
          <div className="rounded-lg border bg-muted/30 p-3">
            <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              ETA
            </p>
            <p className="mt-1 text-sm font-medium">~2 min remaining</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
