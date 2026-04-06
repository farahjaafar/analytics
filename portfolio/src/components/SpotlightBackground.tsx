"use client"

import { useState, useEffect, useRef } from "react"
import { useTheme } from "next-themes"

export function SpotlightBackground() {
  const [mouse, setMouse] = useState({ x: 0, y: 0 })
  const [isMoving, setIsMoving] = useState(false)
  const [mounted, setMounted] = useState(false)
  const moveTimeout = useRef<NodeJS.Timeout | null>(null)
  const { resolvedTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMouse({ x: e.clientX, y: e.clientY })
      setIsMoving(true)
      if (moveTimeout.current) clearTimeout(moveTimeout.current)
      moveTimeout.current = setTimeout(() => setIsMoving(false), 150)
    }
    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  if (!mounted) return null

  const isDark = resolvedTheme === "dark"

  return (
    <div
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 9999 }}
    >
      <div
        className="absolute rounded-full transition-all duration-300 ease-out"
        style={{
          left: mouse.x,
          top: mouse.y,
          width: isMoving ? "220px" : "280px",
          height: isMoving ? "220px" : "280px",
          transform: "translate(-50%, -50%)",
          background: isDark
            ? "radial-gradient(circle, rgba(255,218,61,0.5) 0%, transparent 70%)"
            : "radial-gradient(circle, rgba(245,158,11,0.2) 0%, transparent 70%)",
          mixBlendMode: isDark ? "screen" : "multiply",
        }}
      />
    </div>
  )
}
