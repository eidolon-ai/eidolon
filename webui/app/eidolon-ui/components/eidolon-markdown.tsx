import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from 'rehype-raw'
// @ts-ignore
import rehypeWrap from "rehype-wrap-all";
import {Prism as SyntaxHighlighter} from "react-syntax-highlighter";
import {materialLight} from "react-syntax-highlighter/dist/esm/styles/prism";
import * as React from "react";
import "@/components/eidolon-markdown.css"

interface EidolonMarkdownProps {
  children: string | string[]
}

export const EidolonMarkdown = ({children}: EidolonMarkdownProps) => {
  // noinspection JSUnusedGlobalSymbols
  return <Markdown
    className={"markdown"}
    // @ts-ignore
    rehypePlugins={[[rehypeRaw], [rehypeWrap, {selector: 'table', wrapper: 'div.responsive-table'}]]}
    remarkPlugins={[remarkGfm]}
    components={{
      code(props) {
        const {children, className, node, ...rest} = props
        const match = /language-(\w+)/.exec(className || '')
        return match ? (
          <SyntaxHighlighter
            {...rest}
            PreTag="div"
            language={match[1]}
            style={materialLight}
          >
            {String(children).replace(/\n$/, '')}
          </SyntaxHighlighter>
        ) : (
          <code {...rest} className={className}>
            {children}
          </code>
        )
      }
    }}
  >{Array.isArray(children) ? children.join("\n") : children}</Markdown>
}