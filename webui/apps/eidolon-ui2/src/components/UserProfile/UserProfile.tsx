'use client'

import { useState } from "react";
import { signOut, useSession } from "next-auth/react";
import Image from "next/image";
import { CircleUserRound, X } from "lucide-react";
import { ToggleTheme } from "./ToggleTheme";

export const UserProfile = () => {
  const { data: session } = useSession();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleSignout = async () => {
    await signOut({ callbackUrl: "/" });
  };

  const getIcon = () => {
    if (!session?.user?.image) {
      return <CircleUserRound className="w-5 h-5" />;
    } else {
      return <Image height={16} width={16} src={session.user.image} alt="User" />;
    }
  };

  const toggleDrawer = (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
    if (
      event.type === 'keydown' &&
      ((event as React.KeyboardEvent).key === 'Tab' ||
        (event as React.KeyboardEvent).key === 'Shift')
    ) {
      return;
    }

    setDrawerOpen(open);
  };

  const list = () => (
    <div className="w-64 h-full flex flex-col justify-between bg-white dark:bg-gray-800 shadow-lg mt-20">
      <div>
        <div className="p-4 flex justify-between items-center border-b">
          <span className="text-lg font-semibold">Profile</span>
          <button
            onClick={toggleDrawer(false)}
            className="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            aria-label="close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="border-b">
          <div className="p-4">
            <ToggleTheme />
          </div>
        </div>
        {/* Uncomment and adjust as needed
        <div className="border-b">
          <div className="p-4">
            <h3 className="text-lg font-semibold mb-2">Eidolon Time</h3>
            <UsageIndicator />
          </div>
          <div className="p-4">
            <button className="w-full py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              Request more Time
            </button>
          </div>
        </div>
        */}
      </div>
      {session && (
        <div className="p-4">
          <button
            onClick={handleSignout}
            className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Sign out
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="flex flex-col items-center justify-center">
      <button
        className="p-0 m-0 focus:outline-none"
        aria-label="account of current user"
        aria-controls="menu-appbar"
        aria-haspopup="true"
        onClick={toggleDrawer(true)}
        title="User Settings"
      >
        {getIcon()}
      </button>
      {drawerOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50" onClick={toggleDrawer(false)}>
          <div className="absolute right-0 h-full" onClick={(e) => e.stopPropagation()}>
            {list()}
          </div>
        </div>
      )}
    </div>
  );
};