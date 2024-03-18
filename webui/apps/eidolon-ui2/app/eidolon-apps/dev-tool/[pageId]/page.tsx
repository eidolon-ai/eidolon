import {Box} from "@mui/material";
import {notFound} from "next/navigation";

export interface ProcessPageProps {
    params: {
    processId: string
  }
}
export default function({params}: ProcessPageProps) {
  const chat = await getChat(params.processId)
  if (!chat) {
    notFound()
  }

  return (
    <Box sx={{
      display: 'flex'
    }}>
      Here
    </Box>
  );
}
