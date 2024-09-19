import * as React from "react";
import {FunctionComponent, PropsWithChildren, useEffect, useState} from "react";
import '@docsearch/css';
import "./search.css"
import {Menu} from 'lucide-react';
import {useIsAuthenticated} from "../hooks/index.ts";
import {UserProfile} from "../components/UserProfile/UserProfile.tsx";
import GitLogo from "../images/github-mark.svg"
import DiscordLogo from "../images/discord-mark-blue.svg"
import Image from "next/image";
import {useHeader} from "./HeaderContext.tsx";


export const Header: FunctionComponent<PropsWithChildren> = () => {
  const [isHelpOpen, setIsHelpOpen] = useState(false);
  const isAuthenticated = useIsAuthenticated()
  const { headerCenter } = useHeader()

  const toggleMenu = () => setIsHelpOpen(!isHelpOpen);

  useEffect(() => {
    // docsearch({
    //   appId: "EEA60PZVA2",
    //   apiKey: "6bbd9d76e8fc77e3e7744c572534d1dd",
    //   indexName: "eidolonai",
    //   container: '#docsearchbtn',
    //   placeholder: 'Search documentation',
    // } as any);
  }, []);

  const menuItems = [
    {label: "Docs", href: "/docs"},
    {label: "API", href: "/api"},
  ]

  const githubIcon = `<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 98 96" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" 
d="M48.854 0C21.839 0 0 22 0 49.217c0 21.756 13.993 40.172 33.405 46.69 2.427.49 3.316-1.059 3.316-2.362 0-1.141-.08-5.052-.08-9.127-13.59 2.934-16.42-5.867-16.42-5.867-2.184-5.704-5.42-7.17-5.42-7.17-4.448-3.015.324-3.015.324-3.015 4.934.326 7.523 5.052 7.523 5.052 4.367 7.496 11.404 5.378 14.235 4.074.404-3.178 1.699-5.378 3.074-6.6-10.839-1.141-22.243-5.378-22.243-24.283 0-5.378 1.94-9.778 5.014-13.2-.485-1.222-2.184-6.275.486-13.038 0 0 4.125-1.304 13.426 5.052a46.97 46.97 0 0 1 12.214-1.63c4.125 0 8.33.571 12.213 1.63 9.302-6.356 13.427-5.052 13.427-5.052 2.67 6.763.97 11.816.485 13.038 3.155 3.422 5.015 7.822 5.015 13.2 0 18.905-11.404 23.06-22.324 24.283 1.78 1.548 3.316 4.481 3.316 9.126 0 6.6-.08 11.897-.08 13.526 0 1.304.89 2.853 3.316 2.364 19.412-6.52 33.405-24.935 33.405-46.691C97.707 22 75.788 0 48.854 0z" 
fill="currentColor"/></svg>`
  const githubText = `<div style="height: 24px; width: 24px">${githubIcon}</div>`

  return (
    <header className="p-2 pb-0 flex flex-row justify-between items-center">
      <a className={"flex flex-row w-full justify-start items-center"} href="/">
        <Image src={"/img/eidolon_with_gradient.png"} alt={"eidolon"} height={32} width={32}/>
        <h1 className="text-xl ml-1 font-bold hidden md:block">Eidolon</h1>
      </a>
      <div>{headerCenter}</div>
      <div className={"flex flex-col justify-end items-end w-full overflow-hidden"}>
        <div className={"flex flex-row justify-end items-center gap-2"}>
          <div className="relative">
            <button
              onClick={toggleMenu}
              className="p-0"
              aria-expanded={isHelpOpen}
              aria-controls="menu-items"
            >
              <Menu className="text-gray-400" strokeWidth={2}/>
            </button>

            {isHelpOpen && (
              <nav
                id="menu-items"
                className="absolute right-0 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
              >
                <ul className="py-1">
                  {menuItems.map((item, index) => (
                    <li key={index}>
                      <a
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
            <Image src={DiscordLogo} alt={"discord"} height={16}/>
          </a>
          <a href="https://discord.gg/6kVQrHpeqG">
            <Image src={GitLogo} alt={"git"} height={16}/>
          </a>

          <UserProfile/>
        </div>
        <div className="md:flex flex-row flex-no-wrap justify-end items-end gap-0.5 md:gap-1 pt-1 md:pt-0 w-full max-w-[350px] overflow-hidden hidden">
          <a className="w-full sm:w-auto" href="https://pypi.org/project/eidolon-ai-sdk/">
            <img className="w-full h-auto" alt="PyPI - Version" src="https://img.shields.io/pypi/v/eidolon-ai-sdk?style=flat&label=eidolon-ai-sdk"/>
          </a>
          <a className="w-full sm:w-auto" href="https://pypi.org/project/eidolon-ai-sdk/">
            <img className="w-full h-auto" alt="PyPI - Version" src="https://img.shields.io/docker/v/eidolonai/webui?sort=semver&label=eidolon-ai-webui"/>
          </a>
          <a className="w-full sm:w-auto" href="https://github.com/eidolon-ai/eidolon/actions/workflows/test_python.yml?query=branch%3Amain">
            <img className="w-full h-auto" alt="GitHub Test Status"
                 src="https://img.shields.io/github/actions/workflow/status/eidolon-ai/eidolon/test_python.yml?style=flat&logo=github&label=test"/>
          </a>
        </div>
      </div>
    </header>
  )
}