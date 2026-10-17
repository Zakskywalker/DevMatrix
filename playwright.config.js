const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  testMatch: '*.spec.js',
  timeout: 30000,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: { browserName: 'chromium', trace: 'retain-on-failure' },
});
