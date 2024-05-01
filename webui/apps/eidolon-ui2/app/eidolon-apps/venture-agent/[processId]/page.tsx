import {redirect} from "next/navigation";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  redirect(`/eidolon-apps/venture-agent/${params.processId}/choose`)
}
