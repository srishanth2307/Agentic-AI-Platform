import {
  Bot,
  Building2,
  ChevronRight,
  LayoutDashboard,
  MemoryStick,
  Play,
  Settings,
  Sparkles,
  Users,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { navItems } from "@/data/mockDashboard";

const iconMap: Record<string, React.ElementType> = {
  Dashboard: LayoutDashboard,
  Runs: Play,
  Companies: Building2,
  Agents: Bot,
  Memory: MemoryStick,
  Settings: Settings,
};

export function Sidebar() {
  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col bg-sidebar text-sidebar-foreground">
      <div className="flex h-16 items-center gap-2.5 border-b border-sidebar-border px-5">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sidebar-accent">
          <Sparkles className="h-4 w-4 text-white" />
        </div>
        <div>
          <p className="text-sm font-semibold tracking-tight text-white">
            ProspectPilot
          </p>
          <p className="text-[11px] text-sidebar-muted">Agentic AI Platform</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-4">
        {navItems.map((item) => {
          const Icon = iconMap[item.label] ?? LayoutDashboard;
          return (
            <a
              key={item.label}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                item.active
                  ? "bg-sidebar-accent/20 text-white"
                  : "text-sidebar-muted hover:bg-white/5 hover:text-sidebar-foreground",
              )}
            >
              <Icon className="h-4 w-4 shrink-0" />
              {item.label}
              {item.active && (
                <ChevronRight className="ml-auto h-4 w-4 opacity-60" />
              )}
            </a>
          );
        })}
      </nav>

      <div className="border-t border-sidebar-border p-4">
        <div className="rounded-lg bg-white/5 p-3">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-full bg-sidebar-accent/30">
              <Users className="h-3.5 w-3.5 text-sidebar-accent" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-xs font-medium text-white">
                XL Ventures
              </p>
              <p className="text-[11px] text-sidebar-muted">Pro plan</p>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-[11px] text-sidebar-muted">
            <Zap className="h-3 w-3 text-amber-400" />
            <span>847 agent runs this month</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
