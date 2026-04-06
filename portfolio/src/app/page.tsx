import { Nav } from "@/components/sections/Nav"
import { Hero } from "@/components/sections/Hero"
import { Projects } from "@/components/sections/Projects"
import { SideProjects } from "@/components/sections/SideProjects"
import { Contact } from "@/components/sections/Contact"
import { Footer } from "@/components/sections/Footer"

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Projects />
        <SideProjects />
        <Contact />
      </main>
      <Footer />
    </>
  )
}
