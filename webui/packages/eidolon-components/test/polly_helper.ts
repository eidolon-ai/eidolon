// @ts-ignore
import path from "path";
import {Polly, PollyConfig} from "@pollyjs/core";
import FSPersister from "@pollyjs/persister-fs";
import FetchAdapter from "@pollyjs/adapter-fetch";
import {setupPolly} from 'setup-polly-jest';

Polly.register(FetchAdapter);
Polly.register(FSPersister);

let recordIfMissing = true;
let mode: PollyConfig['mode'] = 'replay';

/*
switch (process.env.POLLY_MODE) {
  case 'record':
    mode = 'record';
    break;
  case 'replay':
    mode = 'replay';
    break;
  case 'offline':
    mode = 'replay';
    recordIfMissing = false;
    break;
}
*/

export default function autoSetupPolly() {
  /**
   * This persister can be adapted for both Node.js and Browser environments.
   *
   */
  return setupPolly({
    adapters: [require("@pollyjs/adapter-fetch")],
    mode,
    recordIfMissing,
    logging: false,
    flushRequestsOnStop: true,
    recordFailedRequests: true,
    persister: require("@pollyjs/persister-fs"),
    persisterOptions: {
      fs: {
        recordingsDir: path.resolve(__dirname, "./__recordings__"),
      },
    },
  });
}