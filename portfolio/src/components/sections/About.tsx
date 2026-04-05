import { cn } from "@/lib/utils"
import { profile, projects } from "@/lib/data"

const stats = [
  { label: "Cities tracked", value: "8" },
  { label: "Days of weather data", value: "365" },
  { label: "dbt models", value: "5" },
  { label: "CI runs", value: "Daily" },
]

export function About() {
  return (
    <section
      id="about"
      className="mx-auto max-w-6xl px-4 py-20 sm:px-6 sm:py-28"
    >
      <div className="grid gap-12 lg:grid-cols-2 lg:gap-20 lg:items-center">
        {/* Bio */}
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <span className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
              About
            </span>
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Building reliable data foundations
            </h2>
          </div>
          <div className="flex flex-col gap-4 text-muted-foreground leading-relaxed">
            <p>
              I&apos;m an analytics engineer with a focus on building data
              pipelines that are reproducible, tested, and easy to understand.
              My work spans the full ELT stack — extraction, warehousing,
              transformation with dbt, and visualisation.
            </p>
            <p>
              This portfolio showcases end-to-end projects that demonstrate
              real data engineering patterns: layered dbt models, automated CI,
              and dashboards that stakeholders can actually trust.
            </p>
          </div>
          <a
            href={profile.repoUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex w-fit items-center gap-1 text-sm font-medium underline underline-offset-4 hover:text-muted-foreground transition-colors"
          >
            Browse the monorepo →
          </a>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 gap-4">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className={cn(
                "flex flex-col gap-1 rounded-xl border border-border/60 bg-card p-6",
                "hover:border-border transition-colors",
              )}
            >
              <span className="text-3xl font-bold tracking-tight">
                {stat.value}
              </span>
              <span className="text-sm text-muted-foreground">{stat.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
