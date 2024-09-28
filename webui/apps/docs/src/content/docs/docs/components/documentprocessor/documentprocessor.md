---
title: DocumentProcessor
description: "Description of DocumentProcessor component"
---
# DocumentProcessor

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property parser](#parser)
- [3. [Optional] Property splitter](#splitter)

**Title:** DocumentProcessor

|                           |                                                         |
| ------------------------- | ------------------------------------------------------- |
| **Type**                  | `object`                                                |
| **Required**              | No                                                      |
| **Additional properties** | [[Not allowed]](# "Additional Properties not allowed.") |

<details>
<summary>
<strong> <a name="implementation"></a>1. [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"DocumentProcessor"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="parser"></a>2. [Optional] Property parser</strong>  

</summary>
<blockquote>

|              |                                        |
| ------------ | -------------------------------------- |
| **Type**     | [`Reference[DocumentParser]`](/docs/components/documentparser/overview)            |
| **Required** | No                                     |
| **Default**  | `{"implementation": "DocumentParser"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="splitter"></a>3. [Optional] Property splitter</strong>  

</summary>
<blockquote>

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | [`Reference[DocumentTransformer]`](/docs/components/documenttransformer/overview)            |
| **Required** | No                                          |
| **Default**  | `{"implementation": "DocumentTransformer"}` |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
