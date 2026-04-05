import { skills } from "@/lib/data"
import { cn } from "@/lib/utils"

const categoryStyles: Record<
  string,
  { accent: string; size: string }
> = {
  "Data Engineering": {
    accent: "border-blue-500/20 bg-blue-500/5 hover:border-blue-500/40",
    size: "lg:col-span-2",
  },
  "SQL & dbt": {
    accent: "border-orange-500/20 bg-orange-500/5 hover:border-orange-500/40",
    size: "",
  },
  "Analytics & BI": {
    accent:
      "border-emerald-500/20 bg-emerald-500/5 hover:border-emerald-500/40",
    size: "",
  },
  "Infrastructure & CI": {
    accent: "border-purple-500/20 bg-purple-500/5 hover:border-purple-500/40",
    size: "",
  },
}

export function Skills() {
  return (
    <section id="skills" className="mx-auto max-w-6xl px-4 py-20 sm:px-6 sm:py-28">
      <div className="flex flex-col gap-3 mb-12">
        <span className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
          Skills
        </span>
        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
          The stack
        </h2>
      </div>

      {/* Bento grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Object.entries(skills).map(([category, items]) => {
          const style = categoryStyles[category]
          return (
            <div
              key={category}
              className={cn(
                "flex flex-col gap-4 rounded-xl border p-6 transition-colors",
                style?.accent ??
                  "border-border/60 hover:border-border bg-card",
                style?.size,
              )}
            >
              <h3 className="text-sm font-semibold tracking-tight">
                {category}
              </h3>
              <div className="flex flex-wrap gap-2">
                {items.map((item) => (
                  <span
                    key={item}
                    className="rounded-full border border-border/60 bg-background/60 px-3 py-1 text-xs text-muted-foreground"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          )
        })}

        {/* "Currently learning" tile */}
        <div className="flex flex-col gap-4 rounded-xl border border-dashed border-border/60 p-6 hover:border-border transition-colors">
          <h3 className="text-sm font-semibold tracking-tight text-muted-foreground">
            Currently exploring
          </h3>
          <div className="flex flex-wrap gap-2">
            {["Apache Airflow", "Snowflake", "dbt Cloud", "Dagster"].map(
              (item) => (
                <span
                  key={item}
                  className="rounded-full border border-dashed border-border/60 px-3 py-1 text-xs text-muted-foreground/60"
                >
                  {item}
                </span>
              ),
            )}
          </div>
        </div>
      </div>
    </section>
  )
}
