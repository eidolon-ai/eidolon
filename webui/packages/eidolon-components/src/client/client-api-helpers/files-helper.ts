import {FileHandle} from "@eidolon-ai/client";
import {SelectedFile} from "../file-upload/file-upload.js";

export async function uploadFiles(machineURL: string, process_id: string, files: SelectedFile[]) {
  const fileHandles: FileHandle[] = [];
  for (const blob of files) {
    const fileHandle = await uploadFile(machineURL, process_id, blob.blob);
    if (fileHandle) {
      const fh_with_md = await setMetadata(machineURL, process_id, fileHandle.file_id, {...fileHandle.metadata, name: blob.name});
      fileHandles.push(fh_with_md ? fh_with_md : fileHandle);
    }
  }

  return fileHandles;
}

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
      return resp.json().then((json) => json as FileHandle)
    })
}

export async function setMetadata(machineUrl: string, process_id: string, file_id: string, metadata: Record<string, unknown>) {
  return fetch(`/api/eidolon/process/${process_id}/files/${file_id}?machineURL=${machineUrl}`, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(metadata),
  })
    .then(resp => {
      if (resp.status === 404) {
        return null
      }
      return resp.json().then((json) => json as FileHandle)
    })
}

export async function downloadFile(machineUrl: string, process_id: string, file_id: string) {
  return await fetch(`/api/eidolon/process/${process_id}/files/${file_id}?machineURL=${machineUrl}`, {
    method: "GET",
  }).then(resp => {
    if (resp.status === 404) {
      return null
    }
    return {data: resp.blob(), mimetype: resp.headers.get("Content-Type")}
  })
}

export async function deleteFile(machineUrl: string, process_id: string, file_id: string) {
  await fetch(`/api/eidolon/process/${process_id}/files/${file_id}?machineURL=${machineUrl}`, {
    method: "DELETE",
  })
}
