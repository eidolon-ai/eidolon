import * as React from "react";
import { FunctionComponent, PropsWithChildren, useEffect, useState } from "react";
import '@docsearch/css';
import "./search.css"
import { Menu } from 'lucide-react';
import { useIsAuthenticated } from "../hooks/index.ts";
import { UserProfile } from "../components/UserProfile/UserProfile.tsx";
import GitLogo from "../images/github-mark.svg"
import DiscordLogo from "../images/discord-mark-blue.svg"
import Image from "next/image";
import { useHeader } from "./HeaderContext.tsx";

export const Header: FunctionComponent<PropsWithChildren> = () => {
  const [isHelpOpen, setIsHelpOpen] = useState(false);
  const isAuthenticated = useIsAuthenticated()
  const { headerCenter } = useHeader()

  const toggleMenu = () => setIsHelpOpen(!isHelpOpen);

  useEffect(() => {
    // docsearch implementation (commented out)
  }, []);

  const menuItems = [
    { label: "Documentation", href: "http://www.eidolonai.com/docs/quickstart" },
    { label: "Blog", href: "http://www.eidolonai.com/blog" },
    { label: "FAQs", href: "http://www.eidolonai.com/docs/faq" },
  ]

  return (
    <header className="p-2 pb-0 flex-col justify-between items-center">
      <div className="flex flex-row justify-between items-center w-full">
        <a className="flex flex-row items-center flex-shrink-0 flex-nowrap" href="/">
          <Image src="/img/eidolon_with_gradient.png" alt="eidolon" height={32} width={32} />
          <h1 className="text-xl ml-1 font-bold hidden md:block">Eidolon</h1>
        </a>
        <div className="flex-grow flex justify-center overflow-hidden px-2">
          <div className="max-w-full overflow-hidden">
            {headerCenter}
          </div>
        </div>
        <div className="flex flex-row justify-end items-center gap-2 flex-shrink-0">
          <div className="relative">
            <button
              onClick={toggleMenu}
              className="p-0"
              aria-expanded={isHelpOpen}
              aria-controls="menu-items"
            >
              <Menu className="text-gray-400" strokeWidth={2} />
            </button>

            {isHelpOpen && (
              <nav
                id="menu-items"
                className="absolute right-0 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
              >
                <ul className="py-1">
                  {menuItems.map((item, index) => (
                    <li key={index}>
                      <a
                        target="eidolon_docs"
                        href={item.href}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={toggleMenu}
                      >
                        {item.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </nav>
            )}
          </div>
          <a href="https://discord.gg/6kVQrHpeqG">
            <Image src={DiscordLogo} alt="discord" height={16} />
          </a>
          <a href="https://discord.gg/6kVQrHpeqG">
            <Image src={GitLogo} alt="git" height={16} />
          </a>
          <UserProfile />
        </div>
      </div>

      <div className="flex justify-end">
        <div className="md:flex flex-row flex-no-wrap justify-end items-end gap-0.5 md:gap-1 pt-1 md:pt-0 w-full max-w-[350px] overflow-hidden hidden">
          {/* ... (badge links remain unchanged) ... */}
        </div>
      </div>
    </header>
  )
}