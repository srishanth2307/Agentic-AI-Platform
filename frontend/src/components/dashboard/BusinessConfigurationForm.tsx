import { Play, Settings2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import type { BusinessConfiguration } from "@/types/api";

interface BusinessConfigurationFormProps {
  goal: string;
  onGoalChange: (goal: string) => void;
  config: BusinessConfiguration;
  onConfigChange: (config: BusinessConfiguration) => void;
  onRun: () => void;
  isRunning: boolean;
}

export function BusinessConfigurationForm({
  goal,
  onGoalChange,
  config,
  onConfigChange,
  onRun,
  isRunning,
}: BusinessConfigurationFormProps) {
  const updateIcp = (field: keyof BusinessConfiguration["icp"], value: string | number) => {
    onConfigChange({
      ...config,
      icp: { ...config.icp, [field]: value },
    });
  };

  const listField = (
    label: string,
    value: string[],
    onChange: (v: string[]) => void,
  ) => (
    <div>
      <label className="text-xs font-medium text-muted-foreground">{label}</label>
      <Input
        value={value.join(", ")}
        onChange={(e) =>
          onChange(
            e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
          )
        }
        placeholder="Comma-separated"
        disabled={isRunning}
        className="mt-1"
      />
    </div>
  );

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2 text-base">
              <Settings2 className="h-4 w-4 text-primary" />
              Business Configuration
            </CardTitle>
            <CardDescription>
              Define ICP, personas, and qualification rules — then run the planner
            </CardDescription>
          </div>
          <Button onClick={onRun} disabled={isRunning || !goal.trim()} size="lg">
            <Play className="h-4 w-4" />
            {isRunning ? "Running…" : "Run Pipeline"}
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-5">
        <div>
          <label className="text-xs font-medium text-muted-foreground">Goal</label>
          <Textarea
            value={goal}
            onChange={(e) => onGoalChange(e.target.value)}
            disabled={isRunning}
            className="mt-1 min-h-[72px]"
            placeholder="What should the agents accomplish?"
          />
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {listField("Industries", config.icp.industries, (v) =>
            onConfigChange({ ...config, icp: { ...config.icp, industries: v } }),
          )}
          {listField("Regions", config.icp.regions, (v) =>
            onConfigChange({ ...config, icp: { ...config.icp, regions: v } }),
          )}
          {listField("Keywords", config.icp.keywords, (v) =>
            onConfigChange({ ...config, icp: { ...config.icp, keywords: v } }),
          )}
          <div>
            <label className="text-xs font-medium text-muted-foreground">Min employees</label>
            <Input
              type="number"
              value={config.icp.min_employees}
              onChange={(e) => updateIcp("min_employees", Number(e.target.value))}
              disabled={isRunning}
              className="mt-1"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-muted-foreground">Max employees</label>
            <Input
              type="number"
              value={config.icp.max_employees}
              onChange={(e) => updateIcp("max_employees", Number(e.target.value))}
              disabled={isRunning}
              className="mt-1"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-muted-foreground">Min fit score</label>
            <Input
              type="number"
              step="0.01"
              min={0}
              max={1}
              value={config.qualification_rules.min_fit_score}
              onChange={(e) =>
                onConfigChange({
                  ...config,
                  qualification_rules: {
                    ...config.qualification_rules,
                    min_fit_score: Number(e.target.value),
                  },
                })
              }
              disabled={isRunning}
              className="mt-1"
            />
          </div>
        </div>

        <div>
          <p className="mb-2 text-xs font-medium text-muted-foreground">Target personas</p>
          <div className="flex flex-wrap gap-2">
            {config.personas.map((p) => (
              <span
                key={p.title}
                className="rounded-full border bg-muted/40 px-3 py-1 text-xs font-medium"
              >
                {p.title} · {p.department}
              </span>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
