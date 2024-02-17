// ./next-server-bugfix.ts
import {
  NextRequest as NextRequest1,
  NextResponse as NextResponse1,
} from "next/server";

export type NextRequest = NextRequest1;

const NextResponseBase = NextResponse1;
export class NextResponse extends NextResponseBase {}
