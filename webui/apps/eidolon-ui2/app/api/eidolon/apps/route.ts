import {getAppRegistry} from "@/utils/eidolon-apps";

export const revalidate=0

export async function GET() {
  return Response.json(getAppRegistry());
}
