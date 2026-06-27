import { ArrowUpRight, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { RecommendationData } from "@/types/api";
import { cn } from "@/lib/utils";

const priorityStyles: Record<string, string> = {
  high: "bg-rose-50 text-rose-700 border-rose-200",
  medium: "bg-amber-50 text-amber-700 border-amber-200",
  low: "bg-slate-50 text-slate-600 border-slate-200",
};

interface RecommendationPanelProps {
  recommendation: RecommendationData | null;
}

export function RecommendationPanel({ recommendation }: RecommendationPanelProps) {
  if (!recommendation) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="h-4 w-4 text-primary" />
            Recommendations
          </CardTitle>
          <CardDescription>AI-generated next-best action after pipeline completes</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="py-8 text-center text-sm text-muted-foreground">
            No data available
          </p>
        </CardContent>
      </Card>
    );
  }

  const priority = recommendation.priority ?? "medium";
  const confidence = recommendation.confidence_score ?? 0;

  return (
    <Card className="h-full border-primary/20 bg-gradient-to-br from-card to-accent/20">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between gap-2">
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="h-4 w-4 text-primary" />
            Recommendations
          </CardTitle>
          <div className="flex gap-2">
            <Badge variant="outline" className="tabular-nums">
              {Math.round(confidence * 100)}% confidence
            </Badge>
            <Badge variant="outline" className={cn("capitalize", priorityStyles[priority])}>
              {priority} priority
            </Badge>
          </div>
        </div>
        <CardDescription>Explainable summary from the Recommendation Agent</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {recommendation.summary && (
          <p className="text-sm leading-relaxed">{recommendation.summary}</p>
        )}

        {recommendation.business_reasoning && (
          <div className="rounded-lg border bg-card/80 p-3">
            <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Business reasoning
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {recommendation.business_reasoning}
            </p>
          </div>
        )}

        <div className="rounded-lg border bg-card p-3 shadow-sm">
          <p className="text-sm font-medium capitalize">
            {(recommendation.recommended_action ?? "").replace(/_/g, " ")}
          </p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            {recommendation.target_contact} · {recommendation.target_title}
          </p>
          {recommendation.draft_subject && (
            <p className="mt-2 rounded-md bg-muted/50 px-3 py-2 text-sm font-medium">
              &ldquo;{recommendation.draft_subject}&rdquo;
            </p>
          )}
        </div>

        {recommendation.talking_points && recommendation.talking_points.length > 0 && (
          <ul className="space-y-2">
            {recommendation.talking_points.map((point) => (
              <li key={point} className="flex items-start gap-2 text-sm text-muted-foreground">
                <ArrowUpRight className="mt-0.5 h-3.5 w-3.5 shrink-0 text-primary" />
                {point}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
