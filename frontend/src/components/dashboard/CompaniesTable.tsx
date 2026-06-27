import { ExternalLink, MoreHorizontal } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { CompanyRow } from "@/types/api";
import { cn } from "@/lib/utils";

const statusVariant: Record<
  CompanyRow["status"],
  "success" | "default" | "warning" | "muted"
> = {
  qualified: "success",
  researching: "default",
  contacted: "warning",
  new: "muted",
};

function FitScoreBar({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  return (
    <div className="flex items-center gap-2">
      <div className="h-1.5 w-16 overflow-hidden rounded-full bg-muted">
        <div
          className={cn(
            "h-full rounded-full transition-all",
            score >= 0.8 ? "bg-emerald-500" : score >= 0.7 ? "bg-amber-500" : "bg-slate-400",
          )}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-xs font-medium tabular-nums">{pct}%</span>
    </div>
  );
}

interface CompaniesTableProps {
  companies: CompanyRow[];
}

export function CompaniesTable({ companies }: CompaniesTableProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-base">Companies</CardTitle>
        <CardDescription>Discovered prospects from the Discovery & Validation agents</CardDescription>
      </CardHeader>
      <CardContent className="px-0 pb-0">
        {companies.length === 0 ? (
          <p className="px-5 pb-5 text-sm text-muted-foreground">
            No data available
          </p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead>Company</TableHead>
                <TableHead>Industry</TableHead>
                <TableHead>Employees</TableHead>
                <TableHead>Fit Score</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-10" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {companies.map((company) => (
                <TableRow key={company.id}>
                  <TableCell>
                    <div>
                      <p className="font-medium">{company.name}</p>
                      {company.domain && (
                        <a
                          href={`https://${company.domain}`}
                          target="_blank"
                          rel="noreferrer"
                          className="flex items-center gap-1 text-xs text-muted-foreground hover:text-primary"
                        >
                          {company.domain}
                          <ExternalLink className="h-3 w-3" />
                        </a>
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{company.industry}</TableCell>
                  <TableCell className="tabular-nums text-muted-foreground">
                    {company.employees.toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <FitScoreBar score={company.fitScore} />
                  </TableCell>
                  <TableCell>
                    <Badge variant={statusVariant[company.status]} className="capitalize">
                      {company.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <button
                      type="button"
                      className="rounded-md p-1 text-muted-foreground hover:bg-muted"
                      aria-label="More options"
                    >
                      <MoreHorizontal className="h-4 w-4" />
                    </button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
