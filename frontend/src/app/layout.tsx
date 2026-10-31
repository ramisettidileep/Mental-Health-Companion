import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
export const metadata: Metadata = { title: "Stillwell — a little room to breathe", description: "A thoughtful AI companion for everyday emotional support." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en" data-scroll-behavior="smooth"><body><div className="min-h-screen md:flex"><Sidebar /><main className="min-w-0 flex-1">{children}</main></div></body></html>; }
