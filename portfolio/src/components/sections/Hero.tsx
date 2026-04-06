import { ArrowDown } from "lucide-react"
import { GithubIcon } from "@/components/icons"
import { Button } from "@/components/ui/button"
import { profile } from "@/lib/data"
import { cn } from "@/lib/utils"

export function Hero() {
  return (
    <section
      className={cn(
        "relative bg-muted/30 text-foreground",
        "min-h-screen px-4",
        "overflow-hidden",
      )}
    >
      <div className="mx-auto max-w-4xl flex flex-col items-center justify-center gap-8 text-center min-h-screen">
        {/* Heading */}
        <h1
          className={cn(
            "animate-appear [animation-fill-mode:both]",
            "text-5xl sm:text-6xl md:text-7xl lg:text-8xl",
            "leading-[1.1] tracking-tight",
            "text-foreground",
          )}
          style={{ fontFamily: '"Geller Headline", serif', fontWeight: 400 }}
        >
          {profile.name}
        </h1>

        {/* CTAs */}
        <div
          className={cn(
            "animate-appear [animation-fill-mode:both] [animation-delay:150ms]",
            "flex flex-wrap justify-center gap-4",
          )}
        >
          <Button size="lg" asChild>
            <a href="#projects">View Projects</a>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <a
              href={profile.repoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2"
            >
              <GithubIcon className="h-4 w-4" />
              GitHub
            </a>
          </Button>
        </div>

        {/* Scroll cue */}
        <a
          href="#about"
          className={cn(
            "animate-appear [animation-fill-mode:both] [animation-delay:300ms]",
            "flex flex-col items-center gap-1 text-xs text-muted-foreground/60 hover:text-muted-foreground transition-colors",
          )}
        >
          <ArrowDown className="h-4 w-4 animate-bounce" />
        </a>
      </div>

    </section>
  )
}
