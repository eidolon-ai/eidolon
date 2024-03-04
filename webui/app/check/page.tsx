'use client'

import { redirect } from 'next/navigation';
import React from 'react';

export default function PreviewPage() {
    React.useEffect(() => {
        fetch('/api/users', {
            method: 'POST'
            })
            .then((response) => response.json())
            .then((data) => {
            console.log(data);
            }).then(redirect('/check'))
    }, [])
    return (
        <></>
    );
    }
  
  
  
  
  
  
  
  
  