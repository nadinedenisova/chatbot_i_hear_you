import type { ConfigFile } from '@rtk-query/codegen-openapi';

const config: ConfigFile = {
  schemaFile: './openapi.yaml',
  apiFile: './src/store/baseApi.ts',
  apiImport: 'api',
  outputFile: './src/store/api.ts',
  exportName: 'api',
  hooks: true,
};

export default config;
