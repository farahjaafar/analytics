import { GithubIcon, LinkedinIcon } from "@/components/icons"
import { Button } from "@/components/ui/button"
import { profile } from "@/lib/data"

export function Contact() {
  return (
    <section
      id="contact"
      className="bg-muted/30 py-10 sm:py-14"
    >
      <div className="mx-auto max-w-2xl px-4 sm:px-6 text-center flex flex-col items-center gap-5">
        <h2 className="text-xl font-bold tracking-tight">
          Contact
        </h2>
        <div className="flex flex-wrap justify-center gap-3">
          <Button variant="outline" size="sm" asChild>
            <a
              href={profile.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2"
            >
              <LinkedinIcon className="h-4 w-4" />
              LinkedIn
            </a>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <a
              href={profile.github}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2"
            >
              <GithubIcon className="h-4 w-4" />
              GitHub
            </a>
          </Button>
        </div>
      </div>
    </section>
  )
}
