export const defaultBusinessConfig = {
  icp: {
    industries: ["B2B SaaS", "DevTools"],
    min_employees: 50,
    max_employees: 500,
    regions: ["North America", "Europe"],
    keywords: ["sales automation", "outbound", "pipeline"],
  },
  personas: [
    {
      title: "VP Sales",
      seniority: "executive",
      department: "Sales",
      pain_points: ["pipeline velocity", "rep productivity"],
    },
    {
      title: "Head of Revenue",
      seniority: "executive",
      department: "Revenue",
      pain_points: ["forecast accuracy", "GTM alignment"],
    },
  ],
  qualification_rules: {
    min_fit_score: 0.7,
    required_signals: ["hiring", "funding"],
    disqualifiers: ["bankruptcy", "direct competitor"],
  },
};

export const defaultGoal =
  "Discover B2B SaaS companies matching our ICP and recommend outreach strategy";
