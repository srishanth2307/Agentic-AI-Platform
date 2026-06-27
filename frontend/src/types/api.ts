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

export interface ICP {
  industries: string[];
  min_employees: number;
  max_employees: number;
  regions: string[];
  keywords: string[];
}

export interface Persona {
  title: string;
  seniority: string;
  department: string;
  pain_points: string[];
}

export interface QualificationRules {
  min_fit_score: number;
  required_signals: string[];
  disqualifiers: string[];
}

export interface BusinessConfiguration {
  icp: ICP;
  personas: Persona[];
  qualification_rules: QualificationRules;
}

export interface RunRequest {
  goal: string;
  run_id?: string | null;
  business_config?: BusinessConfiguration;
}

export interface AgentResult {
  agent: string;
  status: string;
  data: Record<string, unknown>;
}

export interface PlanStep {
  step_id: string;
  order: number;
  agent: string;
  description: string;
}

export interface Plan {
  plan_id: string;
  task: { goal: string; run_id?: string | null };
  steps: PlanStep[];
  created_at: string;
}

export interface RunResponse {
  run_id: string;
  plan_id: string;
  status: string;
  plan: Plan;
  results: AgentResult[];
  memory: Record<string, unknown>;
}

export type RunPhase =
  | "idle"
  | "running"
  | "completed"
  | "awaiting_approval"
  | "approved"
  | "rejected"
  | "error";

export interface PlannerState {
  status: "executing" | "planning" | "completed" | "idle";
  planId: string;
  runId: string;
  totalSteps: number;
  completedSteps: number;
  currentAgent: string;
  mode: "fixed_pipeline" | "llm";
}

export interface CompanyRow {
  id: string;
  name: string;
  domain: string;
  industry: string;
  employees: number;
  fitScore: number;
  status: "qualified" | "researching" | "contacted" | "new";
  isValid?: boolean;
}

export interface ContactRecord {
  name: string;
  title: string;
  email?: string;
  linkedin_url?: string;
  phone?: string;
  department?: string;
  enrichment_source?: string;
  company_name?: string;
}

export interface RecommendationData {
  summary?: string;
  confidence_score?: number;
  business_reasoning?: string;
  recommended_action?: string;
  priority?: string;
  target_contact?: string;
  target_title?: string;
  talking_points?: string[];
  draft_subject?: string;
}

export type StreamEventName =
  | "planner_started"
  | "planner_completed"
  | "discovery_started"
  | "discovery_completed"
  | "validation_started"
  | "validation_completed"
  | "contact_started"
  | "contact_completed"
  | "recommendation_started"
  | "recommendation_completed"
  | "memory_updated"
  | "run_completed"
  | "run_failed";

export interface StreamEvent {
  event: StreamEventName;
  timestamp?: string;
  run_id?: string;
  agent?: string;
  status?: string;
  progress?: number;
  memory?: Record<string, unknown>;
  output?: unknown;
  response?: RunResponse;
  error?: string;
}

export const AGENT_PIPELINE = [
  { id: "planner", agent: "planner", label: "Planner Agent" },
  { id: "discovery", agent: "discovery", label: "Discovery Agent" },
  { id: "validation", agent: "validation", label: "Validation Agent" },
  { id: "contact", agent: "contact", label: "Contact Agent" },
  { id: "recommendation", agent: "recommendation", label: "Recommendation Agent" },
] as const;

export function createInitialSteps(): AgentStep[] {
  return AGENT_PIPELINE.map((s) => ({
    id: s.id,
    agent: s.agent,
    label: s.label,
    status: "pending" as AgentStatus,
  }));
}
