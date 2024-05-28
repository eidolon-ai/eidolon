---
title: OpenAIImageUnit
description: Description of OpenAIImageUnit component
---
## Properties

- **`image_to_text_prompt`** *(string)*: The prompt to use for the conversion. The text should be very verbose and detailed. Default: `"Use the following prompt to describe the image:"`.
- **`text_to_image_prompt`** *(string)*: The prompt to use for the conversion. The text should be very verbose and detailed. Default: `"Use the provided text to create an image:"`.
- **`connection_handler`** *(Reference[OpenAIConnectionHandler])*: Default: `"OpenAIConnectionHandler"`.
- **`image_to_text_model`** *(string)*: The model to use for the vision LLM. Default: `"gpt-4-turbo"`.
- **`text_to_image_model`** *(string)*: The model to use for the vision LLM. Default: `"dall-e-3"`.
- **`temperature`** *(number)*: Default: `0.3`.
- **`image_to_text_system_prompt`** *(string)*: The system prompt to use for text to image. Default: `"You are an expert at answering questions about images. You are presented with an image and a question and must answer the question based on the information in the image."`.
