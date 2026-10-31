import type { Config } from "tailwindcss";
const config: Config = { content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"], theme: { extend: { colors: { paper: "#F8F7F2", ink: "#25332E", forest: "#2D6654", mint: "#DDEBE2", sand: "#EEE9DD", muted: "#68766F" }, fontFamily: { sans: ["Arial", "Helvetica", "sans-serif"] } } }, plugins: [] };
export default config;
