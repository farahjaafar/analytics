import { ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { sideProjects } from "@/lib/data"
import { cn } from "@/lib/utils"

export function SideProjects() {
  return (
    <section id="side-projects" className="bg-muted/30 py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">

        {/* Section header */}
        <div className="mb-10 flex items-center gap-4">
          <div className="flex flex-col gap-1">
            <span className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
              Just for fun
            </span>
            <h2 className="text-2xl font-bold tracking-tight">Side Projects</h2>
          </div>
          <div className="h-px flex-1 bg-border/60" />
        </div>

        <div className="flex justify-center">
          {sideProjects.map((project) => (
            <article
              key={project.id}
              className={cn(
                "flex flex-col gap-4 rounded-xl border border-border/60 bg-card p-6",
                "hover:border-border transition-all duration-300",
                "hover:shadow-md dark:hover:bg-card/80",
                "w-full max-w-sm",
              )}
            >
              <div className="flex flex-col gap-2">
                <h3 className="text-base font-semibold tracking-tight">
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
                    className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* Actions */}
              <div className="mt-auto flex flex-wrap gap-3 pt-1">
                <Button size="sm" asChild>
                  <a
                    href={project.liveUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2"
                  >
                    <ExternalLink className="h-3.5 w-3.5" />
                    Visit Site
                  </a>
                </Button>
              </div>
            </article>
          ))}
        </div>

      </div>
    </section>
  )
}
