"""Inject the Reverse Engineering sections (classic tools through time, plus a
separate block of current AI-assisted tools) into index.html. Re-runnable.

Usage:  python scripts/add_reverse_engineering.py
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
START = "<!-- REVERSE ENGINEERING SECTIONS -->"
END = "<!-- /REVERSE ENGINEERING SECTIONS -->"
ANCHOR = "<!-- /ESOLANGS SECTION -->"
SKULL = ' <button type="button" class="skull-key" aria-label="Automation map">&#9760;</button>'
e = html.escape

# name, era, platform, license, focus, features, status, docs[(label,url)], download(url|None), pop, note, skull
TOOLS = [
    ("SoftICE", "1987 - 2006", "Windows (DOS, 9x, NT)", "Commercial (NuMega / Compuware, discontinued)", "Kernel-mode debugging",
     "Ring-0 debugger that froze the whole OS; the staple of driver developers and crackers of its day.", "Discontinued in 2006",
     [("History", "https://en.wikipedia.org/wiki/SoftICE")], None, "legacy", "Historic; replaced by WinDbg and x64dbg", False),
    ("IDA Pro", "1991", "Windows, macOS, Linux", "Commercial (Hex-Rays; limited free edition)", "Disassembly and decompilation",
     "Interactive disassembler, Hex-Rays decompiler, FLIRT signatures, very wide CPU support, IDAPython plugins.", "Active",
     [("Docs", "https://docs.hex-rays.com/")], "https://hex-rays.com/ida-pro/", "dominant", "Long-time industry standard", False),
    ("OllyDbg", "2000", "Windows (32-bit)", "Freeware", "User-mode debugging",
     "Friendly assembler-level debugger with a large plugin scene. Last release 2.01 (2013); no 64-bit support.", "Unmaintained",
     [("Homepage", "https://www.ollydbg.de/")], "https://www.ollydbg.de/", "legacy", "Beloved classic, superseded by x64dbg", False),
    ("Radare2", "2006", "Cross-platform", "LGPL (open source)", "CLI reverse-engineering framework",
     "Scriptable disassembler, debugger and hex editor with r2pipe bindings for many languages.", "Active",
     [("Book", "https://book.rada.re/")], "https://github.com/radareorg/radare2", "medium", "Power-user favourite", False),
    ("Immunity Debugger", "2007", "Windows", "Free (Immunity Inc.)", "Exploit development debugging",
     "OllyDbg-based debugger with a Python API (PyCommands) and the mona.py exploit helper.", "Rarely updated",
     [("Product page", "https://www.immunityinc.com/products/debugger/")], "https://www.immunityinc.com/products/debugger/", "niche", "Exploit-dev niche", False),
    ("Hopper", "2010", "macOS, Linux", "Commercial (trial available)", "Disassembly and decompilation",
     "Native macOS interface with strong Objective-C support and a pseudo-code view.", "Active",
     [("Docs", "https://www.hopperapp.com/")], "https://www.hopperapp.com/", "medium", "Popular on Apple platforms", False),
    ("Frida", "2010", "Windows, macOS, Linux, iOS, Android", "wxWindows Library Licence (open source)", "Dynamic instrumentation",
     "Inject JavaScript into running processes to hook functions, trace calls and patch behaviour live.", "Active",
     [("Docs", "https://frida.re/docs/home/")], "https://github.com/frida/frida", "high", "Standard for mobile and runtime RE", False),
    ("ILSpy", "2011", "Windows, Linux, macOS", "MIT (open source)", ".NET decompilation",
     "Decompiles .NET assemblies back to C#; built by the ICSharpCode (SharpDevelop) team.", "Active",
     [("Repo", "https://github.com/icsharpcode/ILSpy")], "https://github.com/icsharpcode/ILSpy", "high", "Default .NET decompiler", False),
    ("x64dbg", "2013", "Windows (32 / 64-bit)", "GPL v3 (open source)", "User-mode debugging",
     "Open-source debugger with plugins and scripting; the modern spiritual successor to OllyDbg.", "Active",
     [("Docs", "https://help.x64dbg.com/")], "https://x64dbg.com/", "veryhigh", "Go-to free Windows debugger", False),
    ("JADX", "2013", "Cross-platform", "Apache 2.0 (open source)", "Android decompilation",
     "Turns Dalvik bytecode and APKs into readable Java; GUI and CLI.", "Active",
     [("Repo", "https://github.com/skylot/jadx")], "https://github.com/skylot/jadx", "high", "Top APK decompiler", False),
    ("dnSpy", "2014", "Windows", "GPL v3 (open source)", ".NET debugging and editing",
     "Decompile, edit and debug .NET assemblies without source.", "Archived (2020)",
     [("Repo", "https://github.com/dnSpy/dnSpy")], "https://github.com/dnSpy/dnSpy", "low", "Archived; forks continue", False),
    ("Binary Ninja", "2016", "Windows, macOS, Linux", "Commercial (free tiers available)", "IL-based binary analysis",
     "Multi-level intermediate languages (LLIL / MLIL / HLIL), Python API and a modern UI.", "Active",
     [("Docs", "https://docs.binary.ninja/")], "https://binary.ninja/", "high", "Rising commercial challenger", False),
    ("Cutter", "2017", "Windows, macOS, Linux", "GPL (open source)", "GUI for Rizin",
     "Qt-based GUI (originally Iaito) built on Rizin with an integrated Ghidra decompiler.", "Active",
     [("Docs", "https://cutter.re/docs/")], "https://cutter.re/", "medium", "Friendly open-source GUI", False),
    ("Ghidra", "2019", "Windows, macOS, Linux (Java)", "Apache 2.0 (open source)", "Disassembly, decompilation, collaboration",
     "NSA software-reverse-engineering suite open-sourced in 2019: decompiler, SLEIGH processor specs, scripting and a shared server.", "Active",
     [("Docs", "https://ghidra-sre.org/"), ("Repo", "https://github.com/NationalSecurityAgency/ghidra")],
     "https://github.com/NationalSecurityAgency/ghidra/releases", "veryhigh", "Top free RE suite", True),
]

# name, era, works_with, license, what, workflow, releases_url, docs[(label,url)], source, pop, note
AI_TOOLS = [
    ("GhidraMCP", "2025", "Ghidra + any MCP client", "Open source (see repo)", "Exposes Ghidra to LLM clients through the Model Context Protocol.",
     "Ask the model to list functions, read decompiled code, rename symbols and add comments.",
     "https://github.com/LaurieWired/GhidraMCP/releases", [("Repo", "https://github.com/LaurieWired/GhidraMCP")],
     "https://github.com/LaurieWired/GhidraMCP", "medium", "Popular way to drive Ghidra with AI"),
    ("GhidrAssist", "2024", "Ghidra plugin", "Open source (see repo)", "LLM assistant panel inside Ghidra for explaining and renaming code.",
     "Select a function, request an explanation, accept suggested names and types.",
     "https://github.com/jtang613/GhidrAssist/releases", [("Repo", "https://github.com/jtang613/GhidrAssist")],
     "https://github.com/jtang613/GhidrAssist", "niche", "Community plugin"),
    ("ReVA", "2024", "Ghidra plugin + chat client", "Open source (see repo)", "Reverse Engineering Assistant giving a model tool access to a Ghidra project.",
     "Chat with the binary; the agent calls Ghidra tools to answer.",
     "https://github.com/cyberkaida/reverse-engineering-assistant/releases", [("Repo", "https://github.com/cyberkaida/reverse-engineering-assistant")],
     "https://github.com/cyberkaida/reverse-engineering-assistant", "niche", "Agent-style Ghidra helper"),
    ("Gepetto", "2023", "IDA Pro plugin", "GPL v3 (open source)", "Uses LLMs to explain functions and suggest variable names in IDA.",
     "Right-click a function in the disassembly or pseudocode view and ask for an explanation.",
     "https://github.com/JusticeRage/Gepetto/releases", [("Repo", "https://github.com/JusticeRage/Gepetto")],
     "https://github.com/JusticeRage/Gepetto", "medium", "Early LLM plugin for IDA"),
    ("Binary Ninja Sidekick", "2023", "Binary Ninja", "Commercial add-on", "AI assistant integrated into Binary Ninja from Vector 35.",
     "Summarise functions, recover names and ask questions in context.",
     "https://binary.ninja/", [("Vendor site", "https://binary.ninja/")],
     "https://binary.ninja/", "niche", "Vendor-backed assistant"),
]


def pop(cls, note):
    label = {"dominant": "Dominant", "veryhigh": "Very High", "high": "High", "medium": "Medium",
             "low": "Low", "niche": "Niche", "legacy": "Legacy"}[cls]
    return f'<td><span class="pop pop-{cls}">{label}</span><br><span class="pop-note">{e(note)}</span></td>'


def links(items):
    return "<td>" + " ".join(
        f'<a href="{e(u, quote=True)}" target="_blank" rel="noopener" class="faq-btn">{e(l)}</a>' for l, u in items) + "</td>"


def dl(url, label="Download"):
    if not url:
        return "<td>&mdash;</td>"
    return f'<td><a href="{e(url, quote=True)}" target="_blank" rel="noopener" class="link-btn">{label}</a></td>'


def tool_row(t):
    n, era, plat, lic, focus, feat, status, docs, down, p, note, skull = t
    return ("<tr>"
            f"<td><strong>{e(n)}</strong>{SKULL if skull else ''}<br>({e(era)})</td>"
            f'<td><span class="badge">{e(plat)}</span></td><td>{e(lic)}</td><td>{e(focus)}</td>'
            f"<td>{e(feat)}</td><td>{e(status)}</td>{links(docs)}{dl(down)}{pop(p, note)}</tr>")


def ai_row(t):
    n, era, works, lic, what, flow, rel, docs, src, p, note = t
    return ("<tr>"
            f"<td><strong>{e(n)}</strong><br>({e(era)})</td>"
            f'<td><span class="badge">{e(works)}</span></td><td>{e(lic)}</td><td>{e(what)}</td><td>{e(flow)}</td>'
            f'<td><a href="{e(rel, quote=True)}" target="_blank" rel="noopener" class="faq-btn">Latest release</a></td>'
            f"{links(docs)}{dl(src, 'Source')}{pop(p, note)}</tr>")


def build():
    tr = "\n".join(tool_row(t) for t in TOOLS)
    ar = "\n".join(ai_row(t) for t in AI_TOOLS)
    return f"""{START}
    <section id="reverse">
        <h2>10. Reverse Engineering Tools Through Time</h2>
        <p>Disassemblers, debuggers and decompilers from the DOS-era kernel debuggers to today's open-source suites, in the order they appeared.</p>
        <div class="table-wrapper">
            <table class="compact">
                <thead><tr><th>Tool &amp; Era</th><th>Platform</th><th>License / Cost</th><th>Primary Use</th><th>Notable Features</th><th>Status</th><th>Docs / KB</th><th>Download</th><th>Popularity</th></tr></thead>
                <tbody>
{tr}
                </tbody>
            </table>
        </div>
    </section>

    <section id="reverse-ai" class="ai-section">
        <h2>11. AI-Assisted Reverse Engineering (Current)</h2>
        <p>Plugins and bridges that connect language models to the tools above. These projects move quickly, so each row links to its releases page for the current version.</p>
        <div class="table-wrapper">
            <table class="compact">
                <thead><tr><th>Tool &amp; Era</th><th>Works With</th><th>License / Cost</th><th>What It Does</th><th>Typical Workflow</th><th>Current Version</th><th>Docs / KB</th><th>Source</th><th>Popularity</th></tr></thead>
                <tbody>
{ar}
                </tbody>
            </table>
        </div>
    </section>
    {END}"""


def main():
    with open(INDEX, encoding="utf-8", newline="") as fh:
        doc = fh.read()
    block = build()
    if START in doc:
        doc = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, doc, flags=re.S)
    else:
        i = doc.index(ANCHOR) + len(ANCHOR)
        doc = doc[:i] + "\n\n    " + block + doc[i:]
    if 'href="#reverse"' not in doc:
        toc = ('\n            <li><a href="#reverse">10. Reverse Engineering Tools</a></li>'
               '\n            <li><a href="#reverse-ai">11. AI-Assisted Reverse Engineering</a></li>')
        doc = re.sub(r'(<li><a href="#esolangs">[^<]*</a></li>)', lambda m: m.group(1) + toc, doc, count=1)
    with open(INDEX, "w", encoding="utf-8", newline="") as fh:
        fh.write(doc)
    print(f"Injected {len(TOOLS)} tools and {len(AI_TOOLS)} AI tools")


if __name__ == "__main__":
    main()

