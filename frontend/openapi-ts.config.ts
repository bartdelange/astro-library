import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  input: 'http://127.0.0.1:8000/openapi.json',
  output: {
    path: 'src/shared/api/generated',
    clean: true,
  },
  plugins: [
    '@hey-api/client-fetch',
    '@hey-api/typescript',
    {
      name: '@hey-api/sdk',
      operations: 'flat',
      responseStyle: 'data',
    },
  ],
});
