'use client'

import React from 'react';
import { useRouter } from "next/navigation";
import Image from 'next/image';
import { EidolonApp } from "@eidolon-ai/components/client";

export interface EidolonAppItemProps {
  path: string;
  app: EidolonApp;
}

export function EidolonAppItem({ path, app }: EidolonAppItemProps) {
  const router = useRouter();

  return (
    <div
      className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer transition-transform duration-300 hover:scale-105"
      onClick={() => router.push(`/eidolon-apps/${path}`)}
    >
      <div className="relative h-48 w-full">
        <Image
          src={app.image}
          alt={app.name}
          layout="fill"
          objectFit="cover"
        />
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2">{app.name}</h3>
        <p className="text-sm text-gray-600">{app.description}</p>
      </div>
    </div>
  );
}
