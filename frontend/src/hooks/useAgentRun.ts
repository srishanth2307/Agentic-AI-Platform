import { useCallback, useRef, useState } from "react";
import { streamRun } from "@/api/runs";
import { defaultBusinessConfig, defaultGoal } from "@/lib/defaults";
import {
  AGENT_PIPELINE,
  createInitialSteps,
  type AgentStep,
  type BusinessConfiguration,
  type CompanyRow,
  type ContactRecord,
  type PlannerState,
  type RecommendationData,
  type RunPhase,
  type RunResponse,
  type StreamEvent,
} from "@/types/api";

const AGENT_LABELS: Record<string, string> = Object.fromEntries(
  AGENT_PIPELINE.map((s) => [s.agent, s.label]),
);

function deriveCompanies(memory: Record<string, unknown>): CompanyRow[] {
  const discovery = memory.discovery as Record<string, unknown> | undefined;
  const validation = memory.validation as Record<string, unknown> | undefined;
  if (!discovery) return [];

  const validations = (validation?.validations as Array<Record<string, unknown>>) ?? [];
  const scoreByName = Object.fromEntries(
    validations.map((v) => [v.validated_company ?? v.company_name, v.fit_score ?? 0]),
  );
  const validByName = Object.fromEntries(
    validations.map((v) => [v.validated_company ?? v.company_name, v.is_valid]),
  );

  const companies = (discovery.companies as Array<Record<string, unknown>>) ?? [];
  if (companies.length === 0 && discovery.company_name) {
    companies.push(discovery);
  }

  return companies.map((c, i) => ({
    id: `co-${i}`,
    name: String(c.company_name ?? "Unknown"),
    domain: String(c.domain ?? ""),
    industry: String(c.industry ?? ""),
    employees: Number(c.employee_count ?? 0),
    fitScore: Number(scoreByName[c.company_name as string] ?? validation?.fit_score ?? 0),
    status: validByName[c.company_name as string] ? "qualified" : "researching",
    isValid: Boolean(validByName[c.company_name as string]),
  }));
}

function deriveContacts(memory: Record<string, unknown>): ContactRecord[] {
  const contact = memory.contact as Record<string, unknown> | undefined;
  if (!contact) return [];

  const byCompany = (contact.enrichment_by_company as Array<Record<string, unknown>>) ?? [];
  const flat: ContactRecord[] = [];

  for (const block of byCompany) {
    const company = String(block.company_name ?? "");
    for (const c of (block.contacts as ContactRecord[]) ?? []) {
      flat.push({ ...c, company_name: company });
    }
  }

  if (flat.length === 0) {
    return ((contact.contacts as ContactRecord[]) ?? []).map((c) => ({ ...c }));
  }
  return flat;
}

function deriveRecommendation(memory: Record<string, unknown>): RecommendationData | null {
  const rec = memory.recommendation as RecommendationData | undefined;
  return rec ?? null;
}

function agentFromEvent(event: StreamEvent): string | null {
  if (event.agent && event.agent !== "system" && event.agent !== "done") {
    return event.agent;
  }
  const match = event.event.match(/^(planner|discovery|validation|contact|recommendation)_/);
  return match ? match[1] : null;
}

export function useAgentRun() {
  const [phase, setPhase] = useState<RunPhase>("idle");
  const [goal, setGoal] = useState(defaultGoal);
  const [businessConfig, setBusinessConfig] =
    useState<BusinessConfiguration>(defaultBusinessConfig);
  const [steps, setSteps] = useState<AgentStep[]>(createInitialSteps);
  const [memory, setMemory] = useState<Record<string, unknown>>({});
  const [runResponse, setRunResponse] = useState<RunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [approvalStatus, setApprovalStatus] = useState<"pending" | "approved" | "rejected">("pending");
  const abortRef = useRef<AbortController | null>(null);
  const stepTimers = useRef<Record<string, number>>({});

  const markAgentStarted = useCallback((agent: string) => {
    stepTimers.current[agent] = Date.now();
    setSteps((prev) =>
      prev.map((s) =>
        s.agent === agent
          ? { ...s, status: "running", startedAt: new Date().toISOString() }
          : s,
      ),
    );
  }, []);

  const markAgentCompleted = useCallback((agent: string) => {
    const started = stepTimers.current[agent];
    const durationMs = started ? Date.now() - started : undefined;
    setSteps((prev) =>
      prev.map((s) =>
        s.agent === agent
          ? {
              ...s,
              status: "completed",
              completedAt: new Date().toISOString(),
              durationMs,
            }
          : s,
      ),
    );
  }, []);

  const handleStreamEvent = useCallback(
    (event: StreamEvent) => {
      if (event.memory) setMemory(event.memory);

      const agent = agentFromEvent(event);

      if (event.event.endsWith("_started") && agent) {
        markAgentStarted(agent);
      }

      if (event.event.endsWith("_completed") && agent) {
        markAgentCompleted(agent);
      }

      if (event.event === "run_completed") {
        if (event.response) {
          setRunResponse(event.response);
          setMemory(event.response.memory);
        } else if (event.memory) {
          setMemory(event.memory);
        }
        setPhase("awaiting_approval");
        setApprovalStatus("pending");
      }

      if (event.event === "run_failed") {
        setError(event.error ?? "Run failed");
        setPhase("error");
        setSteps((prev) =>
          prev.map((s) =>
            s.status === "running" ? { ...s, status: "failed" as const } : s,
          ),
        );
      }
    },
    [markAgentStarted, markAgentCompleted],
  );

  const startRun = useCallback(async () => {
    abortRef.current?.abort();
    abortRef.current = new AbortController();

    setPhase("running");
    setError(null);
    setRunResponse(null);
    setMemory({});
    setApprovalStatus("pending");
    stepTimers.current = {};
    setSteps(createInitialSteps());

    try {
      await streamRun(
        { goal, business_config: businessConfig },
        handleStreamEvent,
        abortRef.current.signal,
      );
    } catch (err) {
      if ((err as Error).name === "AbortError") return;
      setError(err instanceof Error ? err.message : "Run failed");
      setPhase("error");
      setSteps((prev) =>
        prev.map((s) =>
          s.status === "running" ? { ...s, status: "failed" as const } : s,
        ),
      );
    }
  }, [goal, businessConfig, handleStreamEvent]);

  const approve = useCallback(() => {
    setApprovalStatus("approved");
    setPhase("approved");
  }, []);

  const reject = useCallback(() => {
    setApprovalStatus("rejected");
    setPhase("rejected");
  }, []);

  const completedCount = steps.filter((s) => s.status === "completed").length;
  const runningStep = steps.find((s) => s.status === "running");
  const progress =
  AGENT_PIPELINE.length === 0
    ? 0
    : Math.round((completedCount / AGENT_PIPELINE.length) * 100);
  const plannerStatus: PlannerState = {
    status:
      phase === "idle" || phase === "error"
        ? "idle"
        : phase === "running"
          ? "executing"
          : "completed",
    planId: runResponse?.plan_id ?? "",
    runId: runResponse?.run_id ?? String(memory.run_id ?? ""),
    totalSteps: AGENT_PIPELINE.length,
    completedSteps: completedCount,
    currentAgent: runningStep?.label ?? AGENT_LABELS[String(memory.current_agent)] ?? "",
    mode: "fixed_pipeline",
  };

  return {
    phase,
    goal,
    setGoal,
    businessConfig,
    setBusinessConfig,
    steps,
    memory,
    runResponse,
    error,
    approvalStatus,
    plannerStatus,
    progress ,
    companies: deriveCompanies(memory),
    contacts: deriveContacts(memory),
    recommendation: deriveRecommendation(memory),
    startRun,
    approve,
    reject,
    isRunning: phase === "running",
  };
}
