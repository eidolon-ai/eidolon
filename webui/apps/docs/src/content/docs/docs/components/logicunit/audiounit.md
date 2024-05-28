---
title: AudioUnit
description: Description of AudioUnit component
---
## Properties

- **`text_to_speech_model`** *(string)*: The model to use for text to speech. Must be one of: `["tts-1", "tts-1-hd"]`. Default: `"tts-1-hd"`.
- **`text_to_speech_voice`** *(string)*: The voice to use for text to speech. Must be one of: `["alloy", "echo", "fable", "onyx", "nova", "shimmer"]`. Default: `"alloy"`.
- **`speech_to_text_model`** *(string)*: The model to use for speech to text. Must be one of: `["whisper-1"]`. Default: `"whisper-1"`.
- **`speech_to_text_temperature`** *(number)*: The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit. Default: `0.3`.
