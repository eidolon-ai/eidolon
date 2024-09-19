import React from 'react';
import { Metadata, NextPage } from 'next';
import { getAppRegistry } from "@/utils/eidolon-apps";
import { EidolonAppItem } from "./EidolonAppItem";

export const revalidate = 0;

export const metadata: Metadata = {
  title: 'Eidolon',
  description: 'Eidolon Home',
};

/**
 * Main page of the Application
 * @page Home
 */
const Home: NextPage = () => {
  return (
    <div className="p-4 m-4 text-center min-h-screen bg-gray-50">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
        {Object.values(getAppRegistry()).map((app, index) => (
          <div key={index} className="w-full">
            <EidolonAppItem path={app.path} app={app} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
