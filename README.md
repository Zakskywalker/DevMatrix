# The Grand Developer & Automation Matrix

[![Author: Zak Millikin (M_A.P.)](https://img.shields.io/badge/Author-Zak%20Millikin%20(M__A.P.)-1f6feb.svg)](#contributors)
[![AI: Gemini AI (Pro)](https://img.shields.io/badge/AI-Gemini%20AI%20(Pro)-8A2BE2.svg)](#contributors)
[![AI: GitHub Copilot](https://img.shields.io/badge/AI-GitHub%20Copilot-24292e.svg)](#contributors)
[![AI: Google DeepMind Anti-Gravity](https://img.shields.io/badge/AI-Google%20DeepMind%20Anti--Gravity-4285F4.svg)](#contributors)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-238636.svg)](https://www.gnu.org/licenses/gpl-3.0)

An interactive codex exploring the history, tooling, syntax, and interconnections of automation, software development, engineering, reverse engineering, and DevOps.

> **Tags:** `Zak Millikin (M_A.P.)` &middot; `Gemini AI (Pro)` &middot; `GitHub Copilot` &middot; `Google DeepMind Anti-Gravity` &middot; `Automation` &middot; `DevOps` &middot; `Reverse Engineering` &middot; `Playwright` &middot; `GPL-3.0`

---

## Overview

**The Grand Developer Matrix** is an interactive, path-enforced developer matrix tracking paths, environment variables, config formats, licensing, troubleshooting notes, and official documentation across 11 major segments of computing history and modern software engineering.

It provides both traditional deep-dive technical tables and a visual GUI mode (with interactive text/image carousels, responsive square-tile grids, and fast single/multi-table flip-through views).

---

## Features

### 1. Interactive Table of Contents & Data Tree
* **Collapsible Sections:** All sections initialize in a collapsed state to minimize initial scroll fatigue. Clicking a section header or a TOC link immediately opens and scrolls to that section.
* **Hierarchical Data Node:** Under the main *Table of Contents*, a dedicated **Data** node contains all catalog sections. Expanding any section item displays a scrollable sub-dropdown listing every entity with quick-jump buttons to view it in **Table (▤)** or **Display (◧)** mode.

### 2. Dual Layout & Display Engine
* **Table View:** Dense, comprehensive technical matrix with fixed headers, environment variable specs, licensing, version history, common troubleshooting tips, and direct links.
* **Display View (GUI Carousel & Tiles):**
  * Top carousel with previous / current / next entity indicators and navigation buttons.
  * Synchronized dropdown selector to quickly jump between entities.
  * Featured inspection card detailing attributes, syntax, and cross-references.
  * Dynamic grid of square tiles for instant visual selection.
* **Top-Level Multi-View / Single-View Switch:**
  * **Multi-View:** Browse all 11 sections sequentially in either table or card mode.
  * **Single-View:** Focus on one section at a time with a global table selector, carousel flip-through, and automatic TOC synchronization.
* **Mobile Experience (< 760px):**
  * Wide horizontal tables automatically transform into responsive, touch-friendly 2-column square cell grids.
  * Tapping any cell opens a complete detail inspection modal with full specifications.

### 3. Comprehensive Global & Local Search
* **Global Search:** Positioned at the top of the Data area; matches queries across every table with live search result cards that jump directly to the target record.
* **Section-Specific Search:** Instant client-side filtering within individual tables and display carousels.
* **Automation Map Discovery:** Typing `automation map`, `skull`, `id`, `map`, or `spec` in search immediately presents a dedicated card with the skull glyph (`☠`) to open the Automation Map.

### 4. Automation ID Map & Hidden Skull Triggers
* **Control Spec Tagging (`data-automation-id`):** Every button, link, input, select, and summary is tagged with a predictable `area_type_name` specification (e.g. `toc_button_collapse`, `global_search_search-all-data`, `footer_button_about`) to facilitate keyword-driven test automation.
* **Interactive Automation Map:** Modal interface allowing live searching, inspection, one-click selector copying, and JSON export of all registered controls.
* **Hidden Skull Keys (`☠`):**
  * Concealed in two locations on the page: in the **About** modal footer and next to **Ghidra** in the Reverse Engineering section (available in Table, Display, and Mobile views).
  * Styled to subtly match the dark background tone at rest, smoothly transitioning to full visibility upon mouseover/scroll-over without color flash on click.
  * Direct access is also available via the `[ ☠ Automation Map ]` button in the global toolbar.

### 5. Curated Codex Catalog (11 Sections)
1. **Automation, QA Frameworks & AI Agents:** WinRunner, QTP/UFT One, Selenium WebDriver, Appium, UiPath, Cypress, Playwright, Robot Framework, Puppeteer, AutoIt, SikuliX, Microsoft Power Automate, LangChain, AutoGen, CrewAI.
2. **IDEs & Editors:** Visual Studio, Eclipse, Xcode, IntelliJ IDEA, Sublime Text, Atom, VS Code, WebStorm, PyCharm, CLion, Cursor, Zed.
3. **Languages & Runtimes:** C, C++, Java, Python, C#, PHP, JavaScript / Node.js, Ruby, Go, Rust, Kotlin, Swift, Dart.
4. **.NET Version Differences:** .NET Framework 1.0 through 4.8.1, .NET Core 1.0 through 3.1, modern unified .NET 5 through 9.
5. **Web Development Languages:** HTML5, CSS3, JavaScript (ES6+), TypeScript, Sass / SCSS, WebAssembly (Wasm).
6. **Virtual Servers & Hypervisors:** VMware ESXi / vSphere, Microsoft Hyper-V, KVM, Proxmox VE, Xen / Citrix Hypervisor, AWS Nitro, Nutanix AHV.
7. **Virtual Machines & Dev Environments:** VMware Workstation / Fusion, Oracle VirtualBox, Vagrant, Docker Desktop, Podman, WSL 2, Dev Containers.
8. **Language Syntax Reference:** Side-by-side cheatsheet covering entry points, types, decision statements, loops, functions, OOP, collections, stdlib, error handling, and idioms for the top 12 languages.
9. **Esoteric Programming Languages:** 69 curated esolangs scraped from the `awesome-esolangs` index (e.g., `><>`, `1+`, `Befunge`, `Brainfuck`, `Chef`, `INTERCAL`, `JSFuck`, `Whitespace`).
10. **Reverse Engineering Tools Through Time:** Chronological evolution from DOS/kernel debuggers (SoftICE, IDA Pro, OllyDbg, Radare2, Frida, x64dbg) to NSA Ghidra.
11. **AI-Assisted Reverse Engineering (Current):** Modern LLM bridges and plugins with direct links to current releases (GhidraMCP, GhidrAssist, ReVA, Gepetto, Binary Ninja Sidekick).

### 6. Analytics, Privacy & Visitor Counter
* **Static Hosting Friendly:** Designed for GitHub Pages and static CDNs without server-side compute.
* **Consent Banner:** First-party cookie & localStorage consent mechanism (`dm_consent=granted|denied`).
* **Local Interaction Log:** When consented, records anonymous interactions (clicks, searches, filter changes, and session IDs). Viewable, downloadable, and clearable via the *Privacy & Interaction Log* dialog.
* **Serverless Beacon Hook:** Extensible beacon support in `window.DEVMATRIX_ANALYTICS` to stream logs to any serverless endpoint (e.g., Cloudflare Workers).
* **Site Visitor Counter:** Live view counter located beside the hero artwork, powered by Abacus API.

---

## Automated Keyword-Driven Testing

The project includes an end-to-end Playwright test suite driven by a clean keyword abstraction layer (`tests/keywords.js`), allowing declarative JSON test scenario files:

* `tests/scenarios/desktop.json`: Tests navigation, TOC tree, collapsible sections, table/display modes, carousels, and dialogs.
* `tests/scenarios/mobile.json`: Tests mobile responsive layouts, 2-column square cell conversion, mobile carousels, and modal interaction.
* `tests/scenarios/features.json`: Tests automation IDs, hidden skull triggers, global search map discovery, cookie consent, and visitor counter.

### Running the Tests
```bash
# Install dependencies
npm install

# Run the Playwright keyword-driven test suite
npm test

# Run with line reporter
npx playwright test --reporter=line
```

---

## Utility Scripts

* `scripts/add_esolangs.py`: Scrapes the saved `angrykoala/awesome-esolangs` asset HTML and generates the Esoteric Languages table.
* `scripts/add_reverse_engineering.py`: Injects the chronological Reverse Engineering and modern AI reverse engineering sections into `index.html`.
* `scripts/import_to_db.py`: Parses the matrix sections and writes the structured dataset into a MySQL/MariaDB database.
* `scripts/populate_languages.py`: Synchronizes dedicated language reference tables.

---

## Image credit

The preview image used for this site is from [Perchance AI-Cursed](https://perchance.org/cursed-ai).

---

## License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See the [GNU General Public License](https://www.gnu.org/licenses/) for details.

---

## Contributors

[![Zak Millikin (M_A.P.)](https://img.shields.io/badge/Contributor-Zak%20Millikin%20(M__A.P.)-1f6feb?style=flat-square)](#)
[![Gemini AI (Pro)](https://img.shields.io/badge/AI%20Collaborator-Gemini%20AI%20(Pro)-8A2BE2?style=flat-square)](#)
[![GitHub Copilot](https://img.shields.io/badge/AI%20Collaborator-GitHub%20Copilot-24292e?style=flat-square)](#)
[![Google DeepMind Anti-Gravity](https://img.shields.io/badge/AI%20Collaborator-Google%20DeepMind%20Anti--Gravity-4285F4?style=flat-square)](#)

This site was worked on by:

- Zak Millikin (M_A.P.)
- Gemini AI (Pro)
- GitHub Copilot (VS Code Copilot SDK; model version not exposed)
- Google DeepMind Anti-Gravity
