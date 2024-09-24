// @ts-ignore
import Markdown, {uriTransformer} from "react-markdown";
// @ts-ignore
import remarkGfm from "remark-gfm";
// @ts-ignore
import rehypeRaw from 'rehype-raw'
// @ts-ignore
import rehypeWrap from "rehype-wrap-all";
import {Prism as SyntaxHighlighter} from "react-syntax-highlighter";
import styles from "./eidolon-markdown.module.css";
import "../eidolon.css"
import {Copy} from 'lucide-react';
import {materialDark} from "react-syntax-highlighter/dist/cjs/styles/prism";
import {useApp} from "../hooks/app-context.js";

interface EidolonMarkdownProps {
  children: any
  showLineNumbers?: boolean
}

export const EidolonMarkdown = ({children, showLineNumbers}: EidolonMarkdownProps) => {
  const pattern = /(https?:\/\/[^/]+)\/processes\/([^/]+)\/files\/([^/\s]+)/;
  const {app} = useApp()

  const transformURL = (url: string) => {
    const match = url.match(pattern)
    if (match) {
      const processId = match[2]!
      const fileId = match[3]!
      return `/api/eidolon/process/${processId}/files/${fileId}?machineURL=${app!.location}`
    }
    return uriTransformer(url)
  }

  // noinspection JSUnusedGlobalSymbols
  return <Markdown
    className={styles.markdown}
    // @ts-ignore
    rehypePlugins={[[rehypeRaw], [rehypeWrap, {selector: 'table', wrapper: `div.${styles.responsiveTable}`}]]}
    remarkPlugins={[remarkGfm]}
    transformImageUri={(src) => transformURL(src)}
    transformLinkUri={(href) => transformURL(href)}
    components={{
      code(props) {
        const {children, className, ...rest} = props
        const match = /language-(\w+)/.exec(className || '')
        return match ? (
          <div className={"eidolon_md-code-block rounded-lg bg-gray-100 my-4"}>
            <div className={"eidolon_md-code-block-header flex flex-row justify-between items-center pt-[0.5em] px-4"}>
              <div className={"text-text-300 text-xs"}>{match[1]}</div>
              <button type="button"
                      onClick={() => {
                        navigator.clipboard.writeText(String(children))
                      }}
                      className="px-2 py-1 gap-1 text-primary text-xs bg-transparent border-none hover:bg-gray-400 font-medium text-center inline-flex items-center"
              >
                <Copy size={16}/>
                Copy
              </button>
            </div>
            <SyntaxHighlighter
              PreTag="div"
              language={match[1]}
              showLineNumbers={showLineNumbers}
              style={{
                ...materialDark,
                "pre[class*=\"language-\"]": {...materialDark["pre[class*=\"language-\"]"]},
                "code[class*=\"language-\"]": {...materialDark["code[class*=\"language-\"]"]},
              }}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          </div>
        ) : (
          <code className={className}>
            {children}
          </code>
        )
      },
      a(props) {
        if (props.href) {
          return <a href={props.href} title={props.title}>{props.children}</a>
        } else {
          return <a title={props.title}>{props.children}</a>
        }
      },
      /*
      annoying but causes the image to flash!!!!! Likely need to create a rehype plugin to handle this
            img(props, element) {
              console.log(props)
              if (props.src) {
                return (
                  <Card>
                    <CardMedia
                      component="img"
                      src={props.src}
                      alt={props.alt}
                      title={props.title}
                      sx={{objectFit: "contain"}}
                    />
                  </Card>
                )
              }
              console.log("here")
              return <img alt={props.alt} title={props.title}/>
            }
      */
    }}
  >{Array.isArray(children) ? children.join("\n") : String(children)}</Markdown>
}