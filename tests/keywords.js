// Keyword library for the DevMatrix keyword-driven Playwright suite.
// Each keyword is a function (page, ...args). Scenarios (tests/scenarios/*.json)
// are lists of [keyword, ...args] steps, so new tests need no new code.
const { expect } = require('@playwright/test');
const path = require('path');
const { pathToFileURL } = require('url');

const T = (page, id) => page.getByTestId(id);

const keywords = {
    // ---- navigation / environment ----
    open: async (page, hash = '') =>
        page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href + hash),
    viewport: async (page, w, h) => page.setViewportSize({ width: w, height: h }),

    // ---- actions ----
    click: async (page, id) => T(page, id).first().click(),
    clickNth: async (page, id, n) => T(page, id).nth(n).click(),
    clickText: async (page, text) => page.getByText(text, { exact: true }).first().click(),
    clickRole: async (page, role, name) => page.getByRole(role, { name }).first().click(),
    fill: async (page, id, value) => T(page, id).first().fill(value),
    select: async (page, id, value) => T(page, id).first().selectOption(value),
    press: async (page, id, key) => T(page, id).first().press(key),

    // ---- assertions ----
    visible: async (page, id) => expect(T(page, id).first()).toBeVisible(),
    hidden: async (page, id) => expect(T(page, id).first()).toBeHidden(),
    text: async (page, id, value) => expect(T(page, id).first()).toContainText(value),
    textExact: async (page, id, value) => expect(T(page, id).first()).toHaveText(value),
    value: async (page, id, value) => expect(T(page, id).first()).toHaveValue(value),
    count: async (page, id, n) => expect(T(page, id)).toHaveCount(n),
    countAtLeast: async (page, id, n) =>
        expect.poll(() => T(page, id).count()).toBeGreaterThanOrEqual(n),
    attr: async (page, id, name, value) => expect(T(page, id).first()).toHaveAttribute(name, value),
    sectionOpen: async (page, id) =>
        expect(T(page, `section-${id}`)).toHaveJSProperty('open', true),
    sectionClosed: async (page, id) =>
        expect(T(page, `section-${id}`)).toHaveJSProperty('open', false),
    pageHasText: async (page, text) => expect(page.locator('body')).toContainText(text),
    pageLacksText: async (page, text) => expect(page.locator('body')).not.toContainText(text),
    dialogOpen: async (page, id) => expect(page.locator('#' + id)).toHaveJSProperty('open', true),
    inViewport: async (page, id) => expect(T(page, id).first()).toBeInViewport(),
};

async function runSteps(page, steps) {
    for (const [name, ...args] of steps) {
        const fn = keywords[name];
        if (!fn) throw new Error(`Unknown keyword: ${name}`);
        await test_step(name, args, () => fn(page, ...args));
    }
}

async function test_step(name, args, body) {
    const { test } = require('@playwright/test');
    return test.step(`${name} ${args.map(a => JSON.stringify(a)).join(' ')}`, body);
}

module.exports = { keywords, runSteps };
