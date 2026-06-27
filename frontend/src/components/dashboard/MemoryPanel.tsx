import { Database } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

function formatValue(value: unknown): string {
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 2);
}

interface MemoryPanelProps {
  memory: Record<string, unknown>;
}

export function MemoryPanel({ memory }: MemoryPanelProps) {
  const entries = Object.entries(memory).filter(([k]) => k !== "run_id");

  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">Shared Memory Viewer</CardTitle>
          <Badge variant="outline" className="gap-1">
            <Database className="h-3 w-3" />
            SQLite · {entries.length} keys
          </Badge>
        </div>
        <CardDescription>Live state persisted after each agent step</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[320px] pr-3">
          {entries.length === 0 ? (
            <p className="py-8 text-center text-sm text-muted-foreground">
              No data available
            </p>
          ) : (
            <div className="space-y-3">
              {entries.map(([key, value]) => (
                <div
                  key={key}
                  className="rounded-lg border bg-muted/20 p-3 transition-colors hover:bg-muted/40"
                >
                  <code className="rounded bg-primary/10 px-1.5 py-0.5 text-xs font-semibold text-primary">
                    {key}
                  </code>
                  <pre className="mt-2 max-h-32 overflow-auto whitespace-pre-wrap break-words font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {formatValue(value)}
                  </pre>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
