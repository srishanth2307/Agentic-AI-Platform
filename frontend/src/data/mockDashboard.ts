export type AgentStatus = "completed" | "running" | "pending" | "failed";

export interface AgentStep {
  id: string;
  agent: string;
  label: string;
  status: AgentStatus;
  startedAt?: string;
  completedAt?: string;
  durationMs?: number;
}

export interface MemoryEntry {
  key: string;
  value: unknown;
  updatedAt: string;
}

export interface Company {
  id: string;
  name: string;
  domain: string;
  industry: string;
  employees: number;
  fitScore: number;
  status: "qualified" | "researching" | "contacted" | "new";
  lastActivity: string;
}

export interface Recommendation {
  action: string;
  priority: "high" | "medium" | "low";
  targetContact: string;
  targetTitle: string;
  talkingPoints: string[];
  draftSubject: string;
}

export interface PlannerState {
  status: "executing" | "planning" | "completed" | "idle";
  planId: string;
  runId: string;
  totalSteps: number;
  completedSteps: number;
  currentAgent: string;
  mode: "fixed_pipeline" | "llm";
}

export interface CurrentTask {
  goal: string;
  runId: string;
  startedAt: string;
  estimatedCompletion: string;
}

export const currentTask: CurrentTask = {
  goal: "Research Acme Corp, validate ICP fit, and draft outreach for VP Sales",
  runId: "run-a3f9c2e1",
  startedAt: "2026-06-26T14:32:00Z",
  estimatedCompletion: "2026-06-26T14:36:00Z",
};

export const plannerStatus: PlannerState = {
  status: "executing",
  planId: "plan-8b4d2f10",
  runId: "run-a3f9c2e1",
  totalSteps: 4,
  completedSteps: 2,
  currentAgent: "Contact Agent",
  mode: "fixed_pipeline",
};

export const agentTimeline: AgentStep[] = [
  {
    id: "step-1",
    agent: "discovery",
    label: "Discovery Agent",
    status: "completed",
    startedAt: "2026-06-26T14:32:04Z",
    completedAt: "2026-06-26T14:32:05Z",
    durationMs: 1020,
  },
  {
    id: "step-2",
    agent: "validation",
    label: "Validation Agent",
    status: "completed",
    startedAt: "2026-06-26T14:32:05Z",
    completedAt: "2026-06-26T14:32:06Z",
    durationMs: 980,
  },
  {
    id: "step-3",
    agent: "contact",
    label: "Contact Agent",
    status: "running",
    startedAt: "2026-06-26T14:32:06Z",
  },
  {
    id: "step-4",
    agent: "recommendation",
    label: "Recommendation Agent",
    status: "pending",
  },
];

export const memoryEntries: MemoryEntry[] = [
  {
    key: "goal",
    value: "Research Acme Corp, validate ICP fit, and draft outreach for VP Sales",
    updatedAt: "2026-06-26T14:32:00Z",
  },
  {
    key: "plan_id",
    value: "plan-8b4d2f10",
    updatedAt: "2026-06-26T14:32:01Z",
  },
  {
    key: "discovery",
    value: {
      company_name: "Acme Corp",
      domain: "acme.example",
      industry: "B2B SaaS",
      employee_count: 250,
      signals: ["Series B funding", "Hiring VP Sales"],
    },
    updatedAt: "2026-06-26T14:32:05Z",
  },
  {
    key: "validation",
    value: {
      is_valid: true,
      fit_score: 0.82,
      checks_passed: ["domain_resolves", "icp_industry_match", "minimum_headcount"],
    },
    updatedAt: "2026-06-26T14:32:06Z",
  },
];

export const companies: Company[] = [
  {
    id: "co-1",
    name: "Acme Corp",
    domain: "acme.example",
    industry: "B2B SaaS",
    employees: 250,
    fitScore: 0.82,
    status: "researching",
    lastActivity: "2026-06-26T14:32:06Z",
  },
  {
    id: "co-2",
    name: "NovaStack",
    domain: "novastack.io",
    industry: "DevTools",
    employees: 120,
    fitScore: 0.91,
    status: "qualified",
    lastActivity: "2026-06-26T13:15:00Z",
  },
  {
    id: "co-3",
    name: "BrightLedger",
    domain: "brightledger.com",
    industry: "FinTech",
    employees: 480,
    fitScore: 0.74,
    status: "contacted",
    lastActivity: "2026-06-25T09:40:00Z",
  },
  {
    id: "co-4",
    name: "PulseHR",
    domain: "pulsehr.co",
    industry: "HR Tech",
    employees: 85,
    fitScore: 0.68,
    status: "new",
    lastActivity: "2026-06-26T10:00:00Z",
  },
  {
    id: "co-5",
    name: "CloudNest",
    domain: "cloudnest.dev",
    industry: "Infrastructure",
    employees: 310,
    fitScore: 0.79,
    status: "qualified",
    lastActivity: "2026-06-24T16:22:00Z",
  },
];

export const recommendation: Recommendation = {
  action: "send_intro_email",
  priority: "high",
  targetContact: "Jane Doe",
  targetTitle: "VP Sales",
  talkingPoints: [
    "Reference recent Series B and sales team expansion",
    "Align with their B2B SaaS outbound motion",
    "Offer a 15-minute discovery call on pipeline tooling",
  ],
  draftSubject: "Quick idea for scaling Acme's outbound",
};

export const navItems = [
  { label: "Dashboard", href: "#", active: true },
  { label: "Runs", href: "#", active: false },
  { label: "Companies", href: "#", active: false },
  { label: "Agents", href: "#", active: false },
  { label: "Memory", href: "#", active: false },
  { label: "Settings", href: "#", active: false },
];
