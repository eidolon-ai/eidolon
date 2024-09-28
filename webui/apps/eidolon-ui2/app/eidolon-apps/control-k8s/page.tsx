import React from 'react';
import { NextPage } from "next";

const DevTools: NextPage = () => {
  return (
    <main className="flex-grow p-6 flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold text-center">
        Eidolon Kubernetes Controller
      </h1>
    </main>
  );
}

export default DevTools;