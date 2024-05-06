---
title: Building Custom Components
description: References - Building Custom Components
---

Customize the server's machine by defining a "Machine" resource.

Like any other resource within Eidolon, you can define your own machine as well. The primary purpose of the machine is to 
define shared singleton concepts like memory. Below we will use mongo for symbolic_memory rather than the in-memory 
implementation. This machine expects mongo to be running locally at 27017.

_machine.yaml_
```yaml
apiVersion: eidolon/v1
kind: Machine
metadata:
  name: mongo_machine

spec:
  symbolic_memory:
    implementation: "MongoSymbolicMemory"
    mongo_database_name: "eidolon"
```

Now you can specify the machine when we start the server.
```bash
poetry run eidolon-server -m mongo_machine resources
```

**Note**: If we leave the name off of our machine resource it will be named "DEFAULT", override the builtin default, and
be used if no machine is specified on startup.
