import { CheckCircle2, ShieldCheck, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { RecommendationData, RunPhase } from "@/types/api";
import { cn } from "@/lib/utils";

interface HumanApprovalPanelProps {
  phase: RunPhase;
  recommendation: RecommendationData | null;
  approvalStatus: "pending" | "approved" | "rejected";
  onApprove: () => void;
  onReject: () => void;
}

export function HumanApprovalPanel({
  phase,
  recommendation,
  approvalStatus,
  onApprove,
  onReject,
}: HumanApprovalPanelProps) {
  const awaiting = phase === "awaiting_approval";
  const decided = phase === "approved" || phase === "rejected";

  return (
    <Card className={cn(awaiting && "border-primary/40 ring-1 ring-primary/20")}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-base">
            <ShieldCheck className="h-4 w-4 text-primary" />
            Human Approval
          </CardTitle>
          {decided && (
            <Badge variant={phase === "approved" ? "success" : "destructive"}>
              {phase === "approved" ? "Approved" : "Rejected"}
            </Badge>
          )}
          {awaiting && <Badge variant="warning">Awaiting review</Badge>}
        </div>
        <CardDescription>
          Review the recommendation before any outbound action is taken
        </CardDescription>
      </CardHeader>
      <CardContent>
        {!recommendation || phase === "idle" || phase === "running" ? (
          <p className="py-6 text-center text-sm text-muted-foreground">
            No data available
          </p>
        ) : (
          <div className="space-y-4">
            <div className="rounded-lg bg-muted/40 p-4 text-sm">
              <p className="font-medium capitalize">
                {(recommendation.recommended_action ?? "action").replace(/_/g, " ")}
              </p>
              <p className="mt-1 text-muted-foreground">
                Target: {recommendation.target_contact} ({recommendation.target_title})
              </p>
              {recommendation.draft_subject && (
                <p className="mt-2 text-xs italic">&ldquo;{recommendation.draft_subject}&rdquo;</p>
              )}
            </div>

            {awaiting && approvalStatus === "pending" && (
              <div className="flex gap-3">
                <Button className="flex-1" onClick={onApprove}>
                  <CheckCircle2 className="h-4 w-4" />
                  Approve outreach
                </Button>
                <Button variant="outline" className="flex-1" onClick={onReject}>
                  <XCircle className="h-4 w-4" />
                  Reject
                </Button>
              </div>
            )}

            {phase === "approved" && (
              <p className="flex items-center gap-2 text-sm text-emerald-700">
                <CheckCircle2 className="h-4 w-4" />
                Outreach approved — ready to execute (HITL checkpoint saved).
              </p>
            )}

            {phase === "rejected" && (
              <p className="flex items-center gap-2 text-sm text-destructive">
                <XCircle className="h-4 w-4" />
                Recommendation rejected — no action will be taken.
              </p>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
