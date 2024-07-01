// import * as path from 'path';

import $RefParser from "@apidevtools/json-schema-ref-parser";
import {FileInfo} from "@apidevtools/json-schema-ref-parser/lib/types/index";

const jsonFiles = require.context('./schema', true, /\.json$/);

export class ResourceGroup {
  [key: string]: Record<string, any>;
}

export class ResourceGroupReference {
  _resourceGroup: ResourceGroup
  _defaultValue: string

  constructor(resourceGroup: ResourceGroup, defaultValue: string) {
    this._resourceGroup = resourceGroup;
    this._defaultValue = defaultValue;
  }

  get(value: string) {
    return this._resourceGroup[value];
  }
}

async function _parse() {
  const directoryRE = /\/([^/]+)\/([^/]+\.json)$/;
  const referenceRE = /file:[.]*[/]*([^/]+)\/overview\.json/;
  const eidolonTypes: Record<string, ResourceGroup> = {}

  const fileResolver = {
    order: 1,
    canRead: /file:\/\/[.]*[/]([^/]+)\/overview\.json/,
    read(file: FileInfo, callback: (err: Error | null, data: string | null) => void) {
      const match = file.url.match(referenceRE);
      if (!match) {
        callback(new Error(`Invalid file path: ${file.url}`), null);
      } else {
        const directory = match[1]!;
        callback(null, JSON.stringify({"$eidolon": file.url}));
      }
    }
  }

  function parseValue(value: any) {
    if (value && typeof value === 'object') {
      if (value['$ref']) {
        const match = value['$ref'].match(referenceRE);
        if (match) {
          const directory = match[1];
          if (!eidolonTypes[directory]) {
            eidolonTypes[directory] = new ResourceGroup();
          }
          return new ResourceGroupReference(eidolonTypes[directory]!, value['default']);
        } else {
          return value;
        }
      } else {
        for (const key in value) {
          value[key] = parseValue(value[key]);
        }
      }
    } else if (value && Array.isArray(value)) {
      for (let i = 0; i < value.length; i++) {
        value[i] = parseValue(value[i]);
      }
    }
    return value;
  }

  for (const filePath of jsonFiles.keys()) {
    let jsonFile = jsonFiles(filePath);
    const match = filePath.match(directoryRE);
    if (!match) {
      throw new Error(`Invalid file path: ${filePath}`);
    }
    const directory = match[1]!;
    const filename = match[2]!;
    if (!eidolonTypes[directory]) {
      eidolonTypes[directory] = new ResourceGroup();
    }
    const dir = eidolonTypes[directory]!;
    if (filename !== 'overview.json') {
      jsonFile = parseValue(jsonFile)
      jsonFile = await $RefParser.dereference(jsonFile, {
        continueOnError: true,
        resolve: {
          file: fileResolver
        },
        dereference: {
          excludedPathMatcher: (path: string) => {
            return path.indexOf('overview.json') !== -1;
          }
        }
      });
      dir[filename.slice(0, -5)] = jsonFile;
    }
  }

  return eidolonTypes
}

const eidolonTypes = await _parse();

export default eidolonTypes;
