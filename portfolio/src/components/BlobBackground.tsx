"use client"

import { useTheme } from "next-themes"
import { useEffect, useState } from "react"

/**
 * BlobBackground — renders Vector.svg shapes faithfully and prominently.
 *
 * The SVG contains:
 *  • Path 1 (outer ring): large organic donut — dominant hero element
 *  • Path 2 (inner crescent): sits inside the ring
 *  • Path 3 (teardrop): upper accent shape
 *  • Path 4 (wave): lower-left accent shape
 *
 * In dark mode : yellow (#FFDA3D) shapes, high contrast on #0D0C08 bg.
 * In light mode: same yellow shapes, slightly lower opacity on #FEFCF0 bg.
 */
export function BlobBackground() {
  const { resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  useEffect(() => { setMounted(true) }, [])
  if (!mounted) return null

  const isDark = resolvedTheme === "dark"

  // Ring is the hero element — large, sits top-right, clearly visible
  const ringOpacity    = isDark ? 0.55 : 0.30
  // Inner accent shapes — clearly visible but subordinate to the ring
  const accentOpacity  = isDark ? 0.45 : 0.22

  return (
    <div
      className="fixed inset-0 pointer-events-none overflow-hidden"
      style={{ zIndex: 0 }}
      aria-hidden="true"
    >
      {/*
        ── RING (Path 1) ──────────────────────────────────────────────────
        The main organic ring from the SVG. Scaled to ~85vh, anchored to
        the top-right. This is the single most prominent design element,
        exactly as it appears in the SVG file.
      */}
      <svg
        viewBox="0 0 389 421"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          position: "absolute",
          height: "85vh",
          width: "auto",
          top: "-8%",
          right: "-18%",
          opacity: ringOpacity,
          animation: "ringDrift 22s ease-in-out infinite",
        }}
      >
        <path
          d="M389 137.24C387.048 177.831 381.788 215.918 367.74 252.886C358.546 277.077 347.174 299.836 331.92 320.013C308.09 351.543 281.419 380.268 244.092 396.539C225.718 404.544 208.37 414.234 188.082 417.65C144.982 424.92 103.51 420.875 64.7054 400.4C22.065 377.894 -7.206 342.189 -27.652 298.35C-44.993 261.175 -49.8841 222.046 -48.8742 181.424C-48.0377 147.796 -39.8231 115.715 -29.001 84.5988C-22.2259 65.1189 -11.2982 46.7726 -0.15202 29.2919C26.3305 -12.2342 62.0451 -43.9552 106.268 -64.5918C165.956 -92.4521 225.59 -90.3838 283.009 -57.9581C322.914 -35.4217 349.668 -0.705521 367.974 41.893C381.388 73.1008 384.448 105.91 389 137.255V137.24ZM-27.8555 188.939C-25.2404 209.667 -23.5824 230.58 -19.7539 251.071C-15.6919 272.857 -8.01239 294.229 4.2944 312.192C18.5079 332.943 33.49 353.611 55.6392 367.706C83.2673 385.286 111.815 399.25 145.042 398.783C205.438 397.941 255.879 374.837 296.695 328.922C334.475 286.423 356.526 237.252 364.168 180.727C370.431 134.39 364.266 89.7848 345.613 47.508C331.732 16.0397 311.602 -10.6945 281.962 -29.9446C263.347 -42.0325 243.964 -52.0827 222.953 -56.4873C185.203 -64.4003 148.969 -59.2756 112.712 -42.9747C79.5594 -28.0679 53.9963 -6.00639 31.9752 21.7773C13.2852 45.3631 -2.7219 71.1398 -11.675 99.8273C-20.598 128.4 -29.3703 157.731 -27.8705 188.931L-27.8555 188.939Z"
          fill="#FFDA3D"
        />
      </svg>

      {/*
        ── CRESCENT (Path 2) ──────────────────────────────────────────────
        Inner arc shape — sits in the lower-center, echoing the ring.
      */}
      <svg
        viewBox="0 0 389 421"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          position: "absolute",
          height: "45vh",
          width: "auto",
          bottom: "5%",
          left: "-5%",
          opacity: accentOpacity,
          transform: "rotate(180deg) scaleX(-1)",
          animation: "crescentDrift 28s ease-in-out infinite",
        }}
      >
        <path
          d="M307.096 179.234C304.956 196.04 298.949 210.395 290.169 223.234C266.37 258.004 237.928 287.542 198.309 303.881C160.65 319.408 125.931 312.077 95.7402 286.822C79.183 272.972 66.0698 254.664 57.5538 233.958C52.6929 222.139 48.043 210.181 44.2522 197.978C40.5594 186.067 42.8957 178.828 49.4975 176.79C56.8077 174.538 60.4477 177.824 64.9921 191.253C72.0687 212.165 81.0746 231.905 93.5246 250.321C113.059 279.2 144.455 294.352 178.067 287.319C197.149 283.329 214.09 273.815 228.907 260.608C242.736 248.283 256.392 235.827 265.669 219.381C271.313 209.361 277.139 199.372 281.751 188.855C287.697 175.281 289.966 173.841 307.088 179.241L307.096 179.234Z"
          fill="#FFDA3D"
        />
      </svg>

      {/*
        ── TEARDROP (Path 3) ──────────────────────────────────────────────
        Elongated accent shape — upper left, smaller.
      */}
      <svg
        viewBox="0 0 389 421"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          position: "absolute",
          height: "32vh",
          width: "auto",
          top: "8%",
          left: "4%",
          opacity: accentOpacity,
          animation: "teardropDrift 18s ease-in-out infinite",
        }}
      >
        <path
          d="M222.423 44.5319C221.36 61.9666 220.041 78.1374 219.559 94.3311C219.371 100.612 220.192 107.285 222.257 113.16C223.553 116.852 227.744 121.356 231.158 121.862C234.345 122.329 239.297 118.813 241.603 115.65C253.103 99.8388 258.439 81.4312 261.725 62.3113C262.712 56.5891 263.006 50.5758 265.056 45.2673C266.322 41.9964 270.143 37.9441 273.112 37.6837C275.923 37.4309 279.443 41.3529 282.005 44.0646C283.429 45.5737 284.364 48.4846 284.092 50.5835C280.302 80.1214 275.433 109.322 255.349 133.008C254.972 133.452 254.701 133.988 254.302 134.402C235.566 154.05 215.829 150.703 204.313 125.96C203.107 123.371 200.854 120.973 200.568 118.315C198.149 95.8478 193.521 73.3344 202.316 51.0584C206.793 39.7136 207.787 39.0395 222.415 44.5243L222.423 44.5319Z"
          fill="#FFDA3D"
        />
      </svg>

      {/*
        ── WAVE (Path 4) ──────────────────────────────────────────────────
        Small wave accent — lower right area.
      */}
      <svg
        viewBox="0 0 389 421"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          position: "absolute",
          height: "28vh",
          width: "auto",
          bottom: "18%",
          right: "3%",
          opacity: accentOpacity * 0.7,
          transform: "rotate(-20deg)",
          animation: "waveDrift 24s ease-in-out infinite",
        }}
      >
        <path
          d="M39.8324 71.3236C42.1309 63.8242 43.9547 55.9572 47.0973 48.6799C48.1675 46.2057 53.1791 43.2642 55.2516 43.9689C58.4621 45.0643 62.3282 48.7565 62.9989 51.9738C64.4082 58.7302 63.6546 65.9231 64.2726 72.8939C65.094 82.1245 65.3578 91.5849 67.7016 100.448C71.108 113.363 78.6217 116.373 89.4966 108.698C106.853 96.4491 117.773 78.9838 124.028 58.5463C125.045 55.2218 125.709 51.7594 126.198 48.3123C127.193 41.3108 129.507 35.4584 137.865 36.5078C144.76 37.3734 149.704 46.0065 147.564 54.1187C145.499 61.9551 142.959 69.8528 139.312 77.0381C129.884 95.6372 119.401 113.562 102.904 126.967C82.2617 143.743 56.9699 137.998 48.16 113.018C43.5854 100.057 42.5982 85.8014 39.8324 71.3159V71.3236Z"
          fill="#FFDA3D"
        />
      </svg>

      <style>{`
        @keyframes ringDrift {
          0%, 100% { transform: translate(0, 0) rotate(0deg); }
          33%       { transform: translate(-12px, 18px) rotate(1.5deg); }
          66%       { transform: translate(8px, -10px) rotate(-1deg); }
        }
        @keyframes crescentDrift {
          0%, 100% { transform: rotate(180deg) scaleX(-1) translate(0, 0); }
          50%       { transform: rotate(180deg) scaleX(-1) translate(14px, -20px); }
        }
        @keyframes teardropDrift {
          0%, 100% { transform: translate(0, 0); }
          50%       { transform: translate(6px, 12px); }
        }
        @keyframes waveDrift {
          0%, 100% { transform: rotate(-20deg) translate(0, 0); }
          50%       { transform: rotate(-18deg) translate(-8px, 10px); }
        }
      `}</style>
    </div>
  )
}
