import {Button, ButtonProps} from "@mui/material";
import {useAppStore} from "../store/index";

export default function BlackButton({children, ...props}: ButtonProps) {
  const [state] = useAppStore();
  const propsCopy = {...props};
  delete propsCopy.sx;
  return (
    <Button
      variant={"text"}
      {...propsCopy}
      sx={{
        color: state.darkMode ? "white" : "black", ...(props.sx || {})
      }}
    >
      {children}
    </Button>
  );
}