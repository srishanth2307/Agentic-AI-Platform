import { AlertCircle } from "lucide-react";
import { AgentTimeline } from "@/components/dashboard/AgentTimeline";
import { BusinessConfigurationForm } from "@/components/dashboard/BusinessConfigurationForm";
import { CompaniesTable } from "@/components/dashboard/CompaniesTable";
import { ContactInformation } from "@/components/dashboard/ContactInformation";
import { HumanApprovalPanel } from "@/components/dashboard/HumanApprovalPanel";
import { MemoryPanel } from "@/components/dashboard/MemoryPanel";
import { PlannerStatus } from "@/components/dashboard/PlannerStatus";
import { RecommendationPanel } from "@/components/dashboard/RecommendationPanel";
import { Sidebar } from "@/components/dashboard/Sidebar";
import { useAgentRun } from "@/hooks/useAgentRun";

export function DashboardPage() {
  const run = useAgentRun();

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-16 shrink-0 items-center justify-between border-b bg-card px-6">
          <div>
            <h1 className="text-lg font-semibold tracking-tight">ProspectPilot</h1>
            <p className="text-xs text-muted-foreground">
              Agentic B2B discovery · live backend
            </p>
          </div>
          {run.plannerStatus.runId && (
            <code className="hidden rounded-lg bg-muted px-2 py-1 text-[10px] sm:block">
              {run.plannerStatus.runId}
            </code>
          )}
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mx-auto max-w-7xl space-y-6">
            <BusinessConfigurationForm
              goal={run.goal}
              onGoalChange={run.setGoal}
              config={run.businessConfig}
              onConfigChange={run.setBusinessConfig}
              onRun={run.startRun}
              isRunning={run.isRunning}
            />

            {run.error && (
              <div className="flex items-center gap-2 rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive">
                <AlertCircle className="h-4 w-4 shrink-0" />
                {run.error}
              </div>
            )}

            <PlannerStatus planner={run.plannerStatus} />

            <div className="grid gap-6 lg:grid-cols-2">
              <AgentTimeline steps={run.steps} />
              <MemoryPanel memory={run.memory} />
            </div>

            <CompaniesTable companies={run.companies} />

            <div className="grid gap-6 lg:grid-cols-2">
              <ContactInformation contacts={run.contacts} />
              <RecommendationPanel recommendation={run.recommendation} />
            </div>

            <HumanApprovalPanel
              phase={run.phase}
              recommendation={run.recommendation}
              approvalStatus={run.approvalStatus}
              onApprove={run.approve}
              onReject={run.reject}
            />
          </div>
        </main>
      </div>
    </div>
  );
}
