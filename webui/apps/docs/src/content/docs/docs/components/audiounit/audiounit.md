---
title: AudioUnit
description: "Description of AudioUnit component"
---
# AudioUnit

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property text_to_speech_model](#text_to_speech_model)
- [3. [Optional] Property text_to_speech_voice](#text_to_speech_voice)
- [4. [Optional] Property speech_to_text_model](#speech_to_text_model)
- [5. [Optional] Property speech_to_text_temperature](#speech_to_text_temperature)

**Title:** AudioUnit

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

Specific value: `"AudioUnit"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="text_to_speech_model"></a>2. [Optional] Property text_to_speech_model</strong>  

</summary>
<blockquote>

**Title:** Text To Speech Model

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"tts-1-hd"`       |

**Description:** The model to use for text to speech.

Must be one of:
* "tts-1"
* "tts-1-hd"

</blockquote>
</details>

<details>
<summary>
<strong> <a name="text_to_speech_voice"></a>3. [Optional] Property text_to_speech_voice</strong>  

</summary>
<blockquote>

**Title:** Text To Speech Voice

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"alloy"`          |

**Description:** The voice to use for text to speech.

Must be one of:
* "alloy"
* "echo"
* "fable"
* "onyx"
* "nova"
* "shimmer"

</blockquote>
</details>

<details>
<summary>
<strong> <a name="speech_to_text_model"></a>4. [Optional] Property speech_to_text_model</strong>  

</summary>
<blockquote>

**Title:** Speech To Text Model

|              |               |
| ------------ | ------------- |
| **Type**     | `const`       |
| **Required** | No            |
| **Default**  | `"whisper-1"` |

**Description:** The model to use for speech to text.

Must be one of:
* "whisper-1"
Specific value: `"whisper-1"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="speech_to_text_temperature"></a>5. [Optional] Property speech_to_text_temperature</strong>  

</summary>
<blockquote>

**Title:** Speech To Text Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

**Description:** The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
