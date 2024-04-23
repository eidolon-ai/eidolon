import {HttpException} from "@eidolon/client";
import {EidolonApp} from "@eidolon/components";

export async function getApps() {
  return fetch(`/api/eidolon/apps`, {
    method: "GET"
  })
    .then(resp => {
      if (resp.status !== 200) {
        throw new HttpException(`Failed to fetch processes: ${resp.statusText}`, resp.status)
      }
      return resp.json().then((json: Record<string, any>) => json as EidolonApp[])
    })
}
