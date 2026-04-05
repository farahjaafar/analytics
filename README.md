# Analytics

A monorepo housing analytics engineering projects — each project demonstrates a different aspect of the modern data stack, from ingestion and transformation to visualisation and CI/CD.

---

## What This Repo Is

This is a personal analytics portfolio. Every project lives in its own subdirectory and is fully self-contained: it has its own dependencies, environment configuration, orchestration script, and detailed README. This top-level README serves as the index — for depth on any project, follow the link to its own documentation.

---

## Projects

| Project | Description | Stack | Status |
|---------|-------------|-------|--------|
| [weather-analytics-pipeline](./weather-analytics-pipeline/README.md) | End-to-end ELT pipeline ingesting global weather data, transforming it with dbt, and visualising it with an Evidence.dev dashboard | Python · DuckDB · dbt · Evidence.dev | Active |
| [portfolio](./portfolio/) | Personal portfolio website showcasing analytics engineering projects | Next.js · Tailwind · shadcn/ui · 21st.dev | Active |

---

## Repository Structure

```
analytics/
├── .github/
│   └── workflows/
│       ├── ci.yml                     # GitHub Actions — weather pipeline CI
│       └── portfolio-deploy.yml       # GitHub Actions — portfolio build check
├── weather-analytics-pipeline/        # Project 1: Weather ELT pipeline
│   ├── extract/                       # Python extraction scripts
│   ├── dbt_project/                   # dbt transformation layer
│   ├── evidence_dashboard/            # Evidence.dev dashboard
│   ├── data/                          # Local DuckDB warehouse
│   ├── run_pipeline.sh                # End-to-end pipeline runner
│   ├── requirements.txt               # Python dependencies
│   └── README.md                      # Full project documentation
├── portfolio/                         # Project 2: Personal portfolio website
│   ├── src/                           # Next.js App Router source
│   ├── public/                        # Static assets
│   ├── vercel.json                    # Vercel deployment config
│   └── package.json
└── README.md                          # You are here
```

---

## CI/CD

Continuous integration is handled by GitHub Actions. The workflow at [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs each project's pipeline end-to-end on every push and pull request to `main`, on a daily schedule, and on manual trigger. Each project's README documents the specific steps run for that project.

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/farahjaafar/analytics.git
cd analytics

# Navigate to the project you want to run
cd weather-analytics-pipeline

# Follow the setup instructions in the project's README
```
