---
title: AutonomousSpeechAgent
description: Description of the AutonomousSpeechAgent component
---

| Property                             | Pattern | Type                 | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | -------------------- | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const                | No         | -          | Implementation    |
| - [speech_llm](#speech_llm )         | No      | [Reference[AudioUnit]](/docs/components/audiounit/overview) | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"AutonomousSpeechAgent"`

## <a name="speech_llm"></a>2. Property `speech_llm`

|              |                                   |
| ------------ | --------------------------------- |
| **Type**     | [`Reference[AudioUnit]`](/docs/components/audiounit/overview)            |
| **Required** | No                                |
| **Default**  | `{"implementation": "AudioUnit"}` |

----------------------------------------------------------------------------------------------------------------------------
