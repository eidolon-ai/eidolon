export async function uploadFile(machineUrl: string, process_id: string, file: Blob) {
  return fetch(`/api/eidolon/process/${process_id}/files?machineURL=${machineUrl}`, {
    headers: {
      "Content-Type": "application/octet-stream",
      "mime-type": file.type
    },
    method: "POST",
    body: file,
  })
    .then(resp => {
      if (resp.status === 404) {
        return null
      }
      return resp.json().then((json: Record<string, any>) => json['file_id'] as string)
    })
}

export async function downloadFile(machineUrl: string, process_id: string, file_id: string) {
  return await fetch(`/api/eidolon/process/${process_id}/files/${file_id}?machineURL=${machineUrl}`, {
    method: "GET",
  }).then(resp => {
    if (resp.status === 404) {
      return null
    }
    return resp.blob()
  })
}

export async function deleteFile(machineUrl: string, process_id: string, file_id: string) {
  await fetch(`/api/eidolon/process/${process_id}/files/${file_id}?machineURL=${machineUrl}`, {
    method: "DELETE",
  })
}
