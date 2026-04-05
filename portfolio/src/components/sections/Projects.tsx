import { ExternalLink } from "lucide-react"
import { GithubIcon } from "@/components/icons"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { projects } from "@/lib/data"
import { cn } from "@/lib/utils"

const tagColors: Record<string, string> = {
  Python: "bg-blue-500/10 text-blue-600 dark:text-blue-400",
  DuckDB: "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400",
  dbt: "bg-orange-500/10 text-orange-600 dark:text-orange-400",
  "Evidence.dev": "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
  "GitHub Actions": "bg-purple-500/10 text-purple-600 dark:text-purple-400",
}

export function Projects() {
  return (
    <section
      id="projects"
      className="bg-muted/30 py-20 sm:py-28"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6">

        <div className="grid gap-6 lg:grid-cols-2">
          {projects.map((project) => (
            <article
              key={project.id}
              className={cn(
                "flex flex-col gap-5 rounded-xl border border-border/60 bg-card p-6 sm:p-8",
                "hover:border-border transition-all duration-300",
                "hover:shadow-lg dark:hover:shadow-none dark:hover:bg-card/80",
              )}
            >
              {/* Header */}
              <div className="flex flex-col gap-2">
                <h3 className="text-xl font-semibold tracking-tight">
                  {project.title}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {project.description}
                </p>
              </div>

              {/* Tags */}
              <div className="flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <span
                    key={tag}
                    className={cn(
                      "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                      tagColors[tag] ?? "bg-muted text-muted-foreground",
                    )}
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                {project.stats.map((stat) => (
                  <div
                    key={stat.label}
                    className="flex flex-col gap-0.5 rounded-lg bg-muted/60 p-3"
                  >
                    <span className="text-lg font-bold">{stat.value}</span>
                    <span className="text-[10px] text-muted-foreground leading-tight">
                      {stat.label}
                    </span>
                  </div>
                ))}
              </div>

              {/* Actions */}
              <div className="flex flex-wrap gap-3 pt-1">
                <Button variant="outline" size="sm" asChild>
                  <a
                    href={project.githubUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2"
                  >
                    <GithubIcon className="h-3.5 w-3.5" />
                    View Code
                  </a>
                </Button>
                {project.liveUrl && (
                  <Button size="sm" asChild>
                    <a
                      href={project.liveUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2"
                    >
                      <ExternalLink className="h-3.5 w-3.5" />
                      Live Dashboard
                    </a>
                  </Button>
                )}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
