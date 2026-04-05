export const profile = {
  name: "Farah Jaafar",
  title: "Analytics Engineer",
  tagline:
    "I build data pipelines that transform raw signals into insights — from API to warehouse to dashboard.",
  github: "https://github.com/farahjaafar",
  repoUrl: "https://github.com/farahjaafar/analytics",
  linkedin: "https://www.linkedin.com/in/farahjaafar/",
  email: "farahnjaafar@gmail.com",
  location: "Berlin, Germany", // update if needed
}

export const projects = [
  {
    id: "weather-analytics-pipeline",
    title: "Weather Analytics Pipeline",
    description:
      "End-to-end ELT pipeline ingesting global weather data for 8 cities across 6 continents. Python extracts from the Open-Meteo API into DuckDB; dbt handles 3-layer transformation (staging → intermediate → marts); Evidence.dev renders interactive dashboards. Automated daily via GitHub Actions.",
    tags: ["Python", "DuckDB", "dbt", "Evidence.dev", "GitHub Actions"],
    githubUrl:
      "https://github.com/farahjaafar/analytics/tree/main/weather-analytics-pipeline",
    liveUrl: "https://weather-dashboard-ocnd7e3fb-farahjaafars-projects.vercel.app/",
    stats: [
      { label: "Cities tracked", value: "8" },
      { label: "Days of history", value: "365" },
      { label: "dbt models", value: "5" },
      { label: "CI status", value: "Passing" },
    ],
    featured: true,
  },
]

export const skills: Record<string, string[]> = {
  "Data Engineering": [
    "Python",
    "DuckDB",
    "ELT pipeline design",
    "REST API integration",
    "Parquet / columnar storage",
  ],
  "SQL & dbt": [
    "dbt Core",
    "3-layer modeling",
    "Macros & tests",
    "dbt_utils",
    "Incremental models",
  ],
  "Analytics & BI": [
    "Evidence.dev",
    "Dashboard design",
    "KPI frameworks",
    "Data storytelling",
  ],
  "Infrastructure & CI": [
    "GitHub Actions",
    "Vercel",
    "Git",
    "Environment management",
  ],
}

export const navLinks = [
  { label: "Projects", href: "#projects" },
  { label: "Contact", href: "#contact" },
]
