---
title: FileMemoryBase Overview
description: Overview of FileMemoryBase components
---

Abstract base class representing the file memory interface for an agent.

This class defines the essential file operations that an agent's memory component
must support. It includes starting and stopping the file memory processes,
reading from a file, and writing to a file within the agent's operational context.

All methods in this class are abstract and must be implemented by a subclass
that provides the specific logic for handling file operations related to the
agent's memory.

## Builtins
* [FileMemory](/docs/components/filememorybase/filememory/)
* [LocalFileMemory](/docs/components/filememorybase/localfilememory/)
* [S3FileMemory](/docs/components/filememorybase/s3filememory/)