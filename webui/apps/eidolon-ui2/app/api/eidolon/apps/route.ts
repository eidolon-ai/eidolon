import {getAppRegistry} from "@/utils/eidolon-apps";

export async function GET() {
  return Response.json(getAppRegistry());
}
