# UMP-0001 Verification

Run the following commands:
```bash
cd chapters/brain/topic-orchestration
npm install
npm run build
npm run test
```

Expected Output:
* `build` transpiles `src/` to `dist/src/` and `test/` to `dist/test/`.
* `test` executes successfully and prints native Node test runner validation for `GET /healthz returns 200 ok`.
