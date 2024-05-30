---
title: OpenAiSpeech
description: Description of OpenAiSpeech component
---

| Property                                                     | Pattern | Type             | Deprecated | Definition | Title/Description          |
| ------------------------------------------------------------ | ------- | ---------------- | ---------- | ---------- | -------------------------- |
| - [text_to_speech_model](#text_to_speech_model )             | No      | enum (of string) | No         | -          | Text To Speech Model       |
| - [text_to_speech_voice](#text_to_speech_voice )             | No      | enum (of string) | No         | -          | Text To Speech Voice       |
| - [speech_to_text_model](#speech_to_text_model )             | No      | const            | No         | -          | Speech To Text Model       |
| - [speech_to_text_temperature](#speech_to_text_temperature ) | No      | number           | No         | -          | Speech To Text Temperature |

## <a name="text_to_speech_model"></a>1. Property `text_to_speech_model`

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

## <a name="text_to_speech_voice"></a>2. Property `text_to_speech_voice`

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

## <a name="speech_to_text_model"></a>3. Property `speech_to_text_model`

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

## <a name="speech_to_text_temperature"></a>4. Property `speech_to_text_temperature`

**Title:** Speech To Text Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

**Description:** The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

----------------------------------------------------------------------------------------------------------------------------
