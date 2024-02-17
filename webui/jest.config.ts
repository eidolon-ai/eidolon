import nextJest from "next/jest";
import {pathsToModuleNameMapper} from "ts-jest";
import {compilerOptions} from "./tsconfig.test.json"

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})


const config = {
  preset: 'ts-jest',

  globals: {
    'ts-jest': {
      tsconfig: 'tsconfig.test.json',
    },
  },

  // Automatically clear mock calls and instances between every test
  clearMocks: true,

  // A list of paths to modules that run some code to configure or set up the testing framework before each test
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'/*, '@testing-library/jest-dom/extend-expect'*/],

  moduleNameMapper: pathsToModuleNameMapper(compilerOptions.paths)
}

export default createJestConfig(config)
