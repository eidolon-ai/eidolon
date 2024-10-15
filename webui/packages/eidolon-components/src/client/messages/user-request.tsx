import {EidolonMarkdown} from "./eidolon-markdown.js";
import {UserRequestElement} from "../lib/display-elements.ts";

export interface UserRequestElementProps {
  element: UserRequestElement
  topLevel: boolean
  userImage: string | null | undefined
  userName: string | null | undefined
}

export const UserRequestUIElement = ({element, topLevel, userName, userImage}: UserRequestElementProps) => {
  const getUserInput = (element: UserRequestElement) => {
    let content: Record<string, unknown> = typeof element.content === "string" ? {body: element.content} : {...element.content as object}
    delete content["process_id"]
    if (Object.keys(content).length === 0) {
      return "*No Input*"
    } else if (Object.keys(content).length === 1 && Object.keys(content)[0] === "body") {
      return content[Object.keys(content)[0]!]
    } else {
      const contentStr = JSON.stringify(content, undefined, "  ")
      return '```json\n' + contentStr + "\n```"
    }
  }

  let userAvatar: JSX.Element
  if (topLevel) {
    if (userImage) {
      userAvatar = userAvatar = (
        <div className="h-6 w-6 rounded-full overflow-hidden">
          <img src={userImage!} alt="User avatar" className="w-full h-full object-cover"/>
        </div>
      )
    } else {
      userAvatar = (
        <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-medium">
          {userName?.charAt(0).toUpperCase()}
        </div>
      )
    }
  } else {
    userAvatar = (
      <div className="h-6 w-6 rounded-full overflow-hidden">
        <img src={"/img/eidolon_with_gradient.png"} alt="User avatar" className="w-full h-full object-cover"/>
      </div>
    )
  }
  return (
    <div className={`flex flex-row border-r-4 rounded-xl py-3 px-2 ${topLevel ? 'w-fit' : 'w-full'} user-element`}
    >
      {userAvatar}
      <div className={"mx-2 w-full"}>
        <EidolonMarkdown>{getUserInput(element)}</EidolonMarkdown>
      </div>
    </div>
  )

}