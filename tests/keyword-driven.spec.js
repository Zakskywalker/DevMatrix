const { test } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const { runSteps } = require('./keywords');

// Every *.json file in tests/scenarios is a suite:
// { "suite": "name", "viewport": {width,height}?, "scenarios": [ { "name": "...", "steps": [[keyword, ...args], ...] } ] }
const dir = path.join(__dirname, 'scenarios');

for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.json'))) {
    const suite = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
    test.describe(suite.suite, () => {
        if (suite.viewport) test.use({ viewport: suite.viewport });
        for (const scenario of suite.scenarios) {
            test(scenario.name, async ({ page }) => {
                await runSteps(page, scenario.steps);
            });
        }
    });
}
