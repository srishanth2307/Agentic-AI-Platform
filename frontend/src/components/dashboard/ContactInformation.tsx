import { Linkedin, Mail, Phone, User } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { ContactRecord } from "@/types/api";

interface ContactInformationProps {
  contacts: ContactRecord[];
}

export function ContactInformation({ contacts }: ContactInformationProps) {
  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-base">Contact Information</CardTitle>
        <CardDescription>Enriched decision-makers from the Contact Agent</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[320px] pr-3">
          {contacts.length === 0 ? (
            <p className="py-8 text-center text-sm text-muted-foreground">
              No data available
            </p>
          ) : (
            <div className="space-y-3">
              {contacts.map((contact, i) => (
                <div
                  key={`${contact.email}-${i}`}
                  className="rounded-lg border bg-card p-4 shadow-sm"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10">
                        <User className="h-4 w-4 text-primary" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">{contact.name}</p>
                        <p className="text-xs text-muted-foreground">
                          {contact.title}
                          {contact.company_name ? ` · ${contact.company_name}` : ""}
                        </p>
                      </div>
                    </div>
                    <Badge
                      variant={contact.enrichment_source === "mock" ? "outline" : "success"}
                      className="text-[10px] capitalize"
                    >
                      {contact.enrichment_source ?? "unknown"}
                    </Badge>
                  </div>
                  <div className="mt-3 space-y-1.5 text-xs text-muted-foreground">
                    {contact.email && (
                      <p className="flex items-center gap-2">
                        <Mail className="h-3.5 w-3.5" />
                        {contact.email}
                      </p>
                    )}
                    {contact.linkedin_url && (
                      <a
                        href={contact.linkedin_url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-2 hover:text-primary"
                      >
                        <Linkedin className="h-3.5 w-3.5" />
                        LinkedIn profile
                      </a>
                    )}
                    {contact.phone ? (
                      <p className="flex items-center gap-2">
                        <Phone className="h-3.5 w-3.5" />
                        {contact.phone}
                      </p>
                    ) : (
                      <p className="flex items-center gap-2 opacity-50">
                        <Phone className="h-3.5 w-3.5" />
                        Phone not available
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
