'use client'

import React, {useEffect, useState} from 'react';
import Image from 'next/image';
import {getApp} from "@/utils/eidolon-apps";
import {EidolonApp} from "@eidolon-ai/components/client";

export interface HomePageProps {
  params: {
    app_name: string
  }
}

export default function ChatbotPage({ params }: HomePageProps) {
  const [app, setApp] = useState<EidolonApp | undefined>(undefined)

  useEffect(() => {
    getApp(params.app_name).then(setApp)
  }, []);

  return (
    <main className="flex-grow p-6 flex flex-col items-center justify-center min-h-screen">
      <div className="bg-white rounded-lg shadow-md overflow-hidden max-w-md w-full cursor-pointer transition-transform duration-300 hover:scale-105">
        <div className="relative h-48 w-full">
          <Image
            src={app.image}
            alt={app.name}
            layout="fill"
            objectFit="cover"
          />
        </div>
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-2">{app.name}</h2>
          <p className="text-sm text-gray-600">{app.description}</p>
        </div>
      </div>
    </main>
  );
}
