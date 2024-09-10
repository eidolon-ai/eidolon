// @ts-ignore
import Markdown, {uriTransformer} from "react-markdown";
// @ts-ignore
import remarkGfm from "remark-gfm";
// @ts-ignore
import rehypeRaw from 'rehype-raw'
// @ts-ignore
import rehypeWrap from "rehype-wrap-all";
import {Prism as SyntaxHighlighter} from "react-syntax-highlighter";
import {materialLight} from "react-syntax-highlighter/dist/esm/styles/prism";
import styles from "./eidolon-markdown.module.css";
import {Link} from "@mui/material";

interface EidolonMarkdownProps {
  machineUrl: string
  children: any
  showLineNumbers?: boolean
}

export const EidolonMarkdown = ({machineUrl, children, showLineNumbers}: EidolonMarkdownProps) => {
  const pattern = /(https?:\/\/[^/]+)\/processes\/([^/]+)\/files\/([^/\s]+)/;
  const transformURL = (url: string) => {
    const match = url.match(pattern)
    if (match) {
      const processId = match[2]!
      const fileId = match[3]!
      return `/api/eidolon/process/${processId}/files/${fileId}?machineURL=${machineUrl}`
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
          <SyntaxHighlighter
            {...rest}
            PreTag="div"
            language={match[1]}
            showLineNumbers={showLineNumbers}
            style={{...materialLight,
              "pre[class*=\"language-\"]": {...materialLight["pre[class*=\"language-\"]"], padding: "8px", "lineHeight": "1.25em"},
              "code[class*=\"language-\"]": {...materialLight["code[class*=\"language-\"]"], "lineHeight": "1.25em"}
          }}
          >
            {String(children).replace(/\n$/, '')}
          </SyntaxHighlighter>
        ) : (
          <code {...rest} className={className}>
            {children}
          </code>
        )
      },
      a(props) {
        if (props.href) {
          return <Link href={props.href} title={props.title}>{props.children}</Link>
        } else {
          return <Link title={props.title}>{props.children}</Link>
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
  >{Array.isArray(children) ? children.join("\n") : children}</Markdown>
}