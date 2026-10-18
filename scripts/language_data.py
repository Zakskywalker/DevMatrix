"""Language reference content for the prog_toolbox per-language tables.

Line format (separator '§', newline marker '¶'):
    key§example§syntax                         - standard topic (see STD)
    Custom Topic§example§syntax§description§category   - language specific topic
Standard keys get their name / description / category from STD.
"""

KB_PATTERN = "https://refactoring.guru/design-patterns/"

# key: (topic name, description template, category, kb override)
STD = {
    "basic":    ("Basic Syntax", "Basic {L} syntax", "Basics", None),
    "comment":  ("Comments", "Writing comments in {L}", "Basics", None),
    "var":      ("Variables", "Declaring and using variables in {L}", "Variables & Types", None),
    "types":    ("Data Types", "Core data types in {L}", "Variables & Types", None),
    "str":      ("Strings", "Working with strings in {L}", "Variables & Types", None),
    "if":       ("Conditional Statements", "Using if/else statements in {L}", "Decisions", None),
    "switch":   ("Switch / Match", "Multi-way branching (switch / match) in {L}", "Decisions", None),
    "for":      ("Loops", "Using for loops in {L}", "Loops", None),
    "while":    ("While Loops", "Using while loops in {L}", "Loops", None),
    "func":     ("Functions", "Declaring and using functions in {L}", "Functions", None),
    "lambda":   ("Lambdas & Closures", "Anonymous functions and closures in {L}", "Functions", None),
    "list":     ("Lists / Arrays", "Working with lists and arrays in {L}", "Collections", None),
    "map":      ("Maps / Dictionaries", "Working with maps and dictionaries in {L}", "Collections", None),
    "oop":      ("Object-Oriented Programming", "Declaring and using objects in {L}", "OOP", None),
    "inherit":  ("Inheritance & Interfaces", "Inheritance and interfaces in {L}", "OOP", None),
    "err":      ("Error Handling", "Error and exception handling in {L}", "Error Handling", None),
    "file":     ("File I/O", "Reading and writing files in {L}", "I/O", None),
    "mod":      ("Modules & Imports", "Modules, imports and packages in {L}", "Modules", None),
    "async":    ("Async & Concurrency", "Async and concurrency in {L}", "Concurrency", None),
    "single":   ("Singleton Pattern", "Singleton design pattern in {L}", "Design Patterns", KB_PATTERN + "singleton"),
    "factory":  ("Factory Pattern", "Factory design pattern in {L}", "Design Patterns", KB_PATTERN + "factory-method"),
    "observer": ("Observer Pattern", "Observer design pattern in {L}", "Design Patterns", KB_PATTERN + "observer"),
    "strategy": ("Strategy Pattern", "Strategy design pattern in {L}", "Design Patterns", KB_PATTERN + "strategy"),
    "rest":     ("REST API Template", "Popular template: minimal REST API in {L}", "Templates", None),
    "test":     ("Unit Test Template", "Popular template: unit test in {L}", "Templates", None),
}

# slug -> (display name, year, popularity, kb url, data)
LANGS = {}


def lang(slug, name, year, pop, kb, data):
    LANGS[slug] = dict(name=name, year=year, popularity=pop, kb=kb, data=data)


lang("python", "Python", 1991, "Dominant", "https://docs.python.org/3/tutorial/index.html", r'''
basic§print("Hello World!")§print()
comment§# single line¶"""docstring / multi-line text"""§# comment
var§x = 5¶name = "Ada"¶pi = 3.14§name = value
types§n = 42  # int¶f = 3.14  # float¶ok = True  # bool¶s = "txt"  # str¶z = None§type(x)
str§s = f"Hi {name}"¶s.upper(); s.split(","); s[1:3]; len(s)§f"{expr}"
if§if x > 5:¶    print("big")¶elif x == 5:¶    print("five")¶else:¶    print("small")§if cond: ... elif: ... else: ...
switch§match cmd:¶    case "go": run()¶    case "stop": halt()¶    case _: pass§match value: case pattern: ...
for§for i in range(5):¶    print(i)¶for item in ["a", "b"]:¶    print(item)§for var in iterable:
while§n = 3¶while n > 0:¶    n -= 1§while condition:
func§def greet(name: str = "World") -> str:¶    return f"Hello, {name}!"§def name(args): return val
lambda§sq = lambda x: x * x¶def counter():¶    c = 0¶    def inc():¶        nonlocal c; c += 1; return c¶    return inc§lambda args: expr
list§xs = [3, 1, 2]¶xs.append(4); xs.sort()¶[x * 2 for x in xs]§[expr for x in xs if cond]
map§d = {"a": 1}¶d["b"] = 2¶for k, v in d.items(): print(k, v)§{key: value}
oop§class Person:¶    def __init__(self, name: str):¶        self.name = name¶    def greet(self) -> str:¶        return f"Hi, {self.name}"§class Name: def __init__(self):
inherit§class Animal:¶    def speak(self): ...¶class Dog(Animal):¶    def speak(self): return "Woof"§class Child(Parent):
err§try:¶    int("x")¶except ValueError as e:¶    print(e)¶finally:¶    print("done")§try: ... except E as e: ... finally: ...
file§with open("a.txt") as f:¶    text = f.read()¶with open("b.txt", "w") as f:¶    f.write(text)§with open(path, mode) as f:
mod§import os¶from pathlib import Path¶import numpy as np§import module  |  from m import x
async§import asyncio¶async def main():¶    await asyncio.sleep(1)¶asyncio.run(main())§async def f(): await x
single§class Config:¶    _inst = None¶    def __new__(cls):¶        if cls._inst is None:¶            cls._inst = super().__new__(cls)¶        return cls._inst§__new__ returns shared instance
factory§def make(kind):¶    return {"dog": Dog, "cat": Cat}[kind]()§factory function returning objects
observer§class Subject:¶    def __init__(self): self._subs = []¶    def subscribe(self, f): self._subs.append(f)¶    def emit(self, v): [f(v) for f in self._subs]§subscribe / emit callbacks
strategy§def run(data, algo): return algo(data)¶run([3, 1, 2], sorted)§pass behavior as a function
rest§from fastapi import FastAPI¶app = FastAPI()¶@app.get("/items/{id}")¶def item(id: int): return {"id": id}§uvicorn main:app --reload
test§def add(a, b): return a + b¶def test_add(): assert add(1, 2) == 3§pytest -q
Dataclass§from dataclasses import dataclass¶@dataclass¶class Point:¶    x: int¶    y: int = 0§@dataclass class Name:§Concise classes with generated __init__ / __repr__ / __eq__§OOP
Decorator§def timed(fn):¶    def wrap(*a, **k):¶        return fn(*a, **k)¶    return wrap¶@timed¶def work(): ...§@decorator§Wrap a function to add behavior (Decorator pattern)§Design Patterns
Generator§def count(n):¶    for i in range(n):¶        yield i¶list(count(3))§yield value§Lazy iteration with generators§Functions
Virtual Environment§python -m venv .venv¶.venv\Scripts\activate¶pip install -r requirements.txt§python -m venv .venv§Isolate project dependencies§Templates
CLI Template§import argparse¶p = argparse.ArgumentParser()¶p.add_argument("name")¶args = p.parse_args()¶print(args.name)§argparse.ArgumentParser()§Popular template: command line tool§Templates
''')

lang("js", "JavaScript", 1995, "Dominant", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", r'''
basic§console.log("Hello World!");§console.log()
comment§// line¶/* block */§// comment
var§let x = 5;¶const name = "Ada";¶var legacy = 1;§let / const / var
types§typeof 42; typeof "s"; typeof true;¶typeof undefined; typeof null; // object¶10n // BigInt§typeof value
str§const s = `Hi ${name}`;¶s.toUpperCase(); s.split(","); s.slice(1, 3);§`template ${expr}`
if§if (x > 5) {¶  console.log("big");¶} else if (x === 5) {¶  console.log("five");¶} else {¶  console.log("small");¶}§if (cond) {} else {}
switch§switch (cmd) {¶  case "go": run(); break;¶  default: idle();¶}§switch (v) { case a: break; }
for§for (let i = 0; i < 5; i++) {¶  console.log(i);¶}¶for (const v of [1, 2, 3]) {¶  console.log(v);¶}§for (init; cond; step) {}
while§let n = 3;¶while (n > 0) { n--; }§while (cond) {}
func§function greet(name = "World") {¶  return `Hello, ${name}!`;¶}§function name(args) {}
lambda§const sq = x => x * x;¶const counter = () => { let c = 0; return () => ++c; };§(args) => expr
list§const xs = [3, 1, 2];¶xs.push(4);¶xs.map(x => x * 2).filter(x => x > 2);§arr.map(fn)
map§const m = new Map([["a", 1]]);¶const o = { a: 1 };¶for (const [k, v] of Object.entries(o)) {}§new Map() / { key: value }
oop§class Person {¶  constructor(name) {¶    this.name = name;¶  }¶  greet() {¶    return `Hi, ${this.name}`;¶  }¶}§class Name { constructor() {} }
inherit§class Dog extends Animal {¶  speak() { return "Woof"; }¶}§class B extends A {}
err§try { JSON.parse("x"); } catch (e) { console.error(e.message); } finally { }§try {} catch (e) {} finally {}
file§import { readFile, writeFile } from "node:fs/promises";¶const t = await readFile("a.txt", "utf8");¶await writeFile("b.txt", t);§fs.promises.readFile(path)
mod§import fs from "node:fs";¶import { x } from "./mod.js";¶export const y = 1;§import / export
async§const wait = ms => new Promise(r => setTimeout(r, ms));¶async function main() { await wait(100); }¶main();§async / await
single§export const config = Object.freeze({ url: "x" });§module instance acts as singleton
factory§const make = kind => ({ dog: () => new Dog(), cat: () => new Cat() })[kind]();§factory function
observer§const subs = new Set();¶const subscribe = f => subs.add(f);¶const emit = v => subs.forEach(f => f(v));§subscribe / emit
strategy§const run = (data, algo) => algo(data);¶run([3, 1, 2], a => [...a].sort());§pass behavior as a function
rest§import express from "express";¶const app = express();¶app.get("/items/:id", (req, res) => res.json({ id: req.params.id }));¶app.listen(3000);§node server.js
test§import { test } from "node:test";¶import assert from "node:assert";¶test("add", () => assert.equal(1 + 2, 3));§node --test
Destructuring§const { a, b } = obj;¶const [x, y] = arr;§const { a } = obj§Unpack values from objects and arrays§Variables & Types
Promises§fetch(url).then(r => r.json()).then(console.log).catch(console.error);§promise.then().catch()§Chain asynchronous operations§Concurrency
DOM Events§document.querySelector("#btn").addEventListener("click", () => alert("Hi"));§el.addEventListener(type, fn)§Respond to user events in the browser§Templates
Module Pattern§const counter = (() => { let c = 0; return { inc: () => ++c }; })();§(() => {...})()§Encapsulate state with an IIFE closure§Design Patterns
Package.json§{ "name": "app", "type": "module", "scripts": { "start": "node index.js" } }§npm init -y§Popular template: Node project manifest§Templates
''')

lang("php", "PHP", 1995, "High", "https://www.php.net/manual/en/langref.php", r'''
basic§<?php echo "Hello World!"; ?>§<?php echo ...; ?>
comment§// line¶# also line¶/* block */§// comment
var§$x = 5;¶$name = "Ada";§$name = value;
types§$i = 42; $f = 3.14; $b = true;¶$s = "txt"; $a = [1, 2]; $n = null;§gettype($x)
str§$s = "Hi $name";¶strtoupper($s); explode(",", $s); substr($s, 1, 2);§"text $var"
if§if ($x > 5) { echo "big"; } elseif ($x == 5) { echo "five"; } else { echo "small"; }§if (cond) {} elseif {} else {}
switch§echo match($cmd) { "go" => "run", "stop" => "halt", default => "idle" };§match($v) { a => b }
for§for ($i = 0; $i < 5; $i++) { echo $i; }¶foreach ($items as $item) { echo $item; }§for / foreach
while§$n = 3;¶while ($n > 0) { $n--; }§while (cond) {}
func§function greet(string $name = "World"): string {¶    return "Hello, $name!";¶}§function name(type $arg): type
lambda§$sq = fn($x) => $x * $x;¶$c = function() use (&$n) { return ++$n; };§fn($x) => expr
list§$xs = [3, 1, 2];¶$xs[] = 4; sort($xs);¶array_map(fn($x) => $x * 2, $xs);§array_map(fn, $arr)
map§$m = ["a" => 1];¶$m["b"] = 2;¶foreach ($m as $k => $v) { echo "$k=$v"; }§["key" => value]
oop§class Person {¶    public function __construct(public string $name) {}¶    public function greet(): string { return "Hi, {$this->name}"; }¶}§class Name { public function __construct() {} }
inherit§class Dog extends Animal implements Pet {¶    public function speak() { return "Woof"; }¶}§class B extends A implements I {}
err§try { throw new Exception("x"); } catch (Exception $e) { echo $e->getMessage(); } finally { }§try {} catch (E $e) {} finally {}
file§$t = file_get_contents("a.txt");¶file_put_contents("b.txt", $t);§file_get_contents($path)
mod§namespace App;¶use App\Models\User;¶require __DIR__ . "/vendor/autoload.php";§namespace / use / require
async§$loop = function() { $f = new Fiber(fn() => Fiber::suspend(1)); $f->start(); };§Fiber (8.1+)
single§final class Config {¶    private static ?self $i = null;¶    public static function get(): self { return self::$i ??= new self(); }¶    private function __construct() {}¶}§private constructor + static getter
factory§function make(string $kind) { return match($kind) { "dog" => new Dog(), "cat" => new Cat() }; }§static factory method
observer§class Subject implements SplSubject { /* attach, detach, notify */ }§SplSubject / SplObserver
strategy§function run(array $d, callable $algo) { return $algo($d); }¶run([3,1,2], 'sort');§inject a callable
rest§Route::get('/items/{id}', fn($id) => response()->json(['id' => $id]));§routes/api.php (Laravel)
test§use PHPUnit\Framework\TestCase;¶class AddTest extends TestCase { public function testAdd() { $this->assertSame(3, 1 + 2); } }§vendor/bin/phpunit
Composer§composer init¶composer require guzzlehttp/guzzle¶composer install§composer require vendor/package§Dependency manager and autoloader§Modules
PDO Query§$pdo = new PDO($dsn, $user, $pass);¶$st = $pdo->prepare("SELECT * FROM t WHERE id = ?");¶$st->execute([$id]);§PDO prepared statements§Safe database access§I/O
Traits§trait Logs { public function log($m) { echo $m; } }¶class A { use Logs; }§trait Name {} / use Name;§Reuse methods across classes§OOP
''')

lang("cpp", "C++", 1985, "Very High", "https://en.cppreference.com/w/", r'''
basic§#include <iostream>¶int main() {¶    std::cout << "Hello World!" << std::endl;¶    return 0;¶}§int main() {}
comment§// line¶/* block */§// comment
var§int x = 5;¶double pi = 3.14;¶auto name = "Ada";§type name = value;
types§int i = 42; double d = 3.14; bool b = true;¶char c = 'a'; std::string s = "txt";§sizeof(type)
str§std::string s = "Hi " + name;¶s.size(); s.substr(1, 2); s.find("x");§#include <string>
if§if (x > 5) {¶    std::cout << "big";¶} else if (x == 5) {¶    std::cout << "five";¶} else {¶    std::cout << "small";¶}§if (cond) {} else {}
switch§switch (cmd) {¶  case 1: run(); break;¶  default: idle();¶}§switch (v) { case a: break; }
for§for (int i = 0; i < 5; i++) {¶    std::cout << i;¶}¶for (const auto& item : items) {¶    std::cout << item;¶}§for (init; cond; step) {}
while§int n = 3;¶while (n > 0) { --n; }§while (cond) {}
func§int add(int a, int b) {¶    return a + b;¶}§type name(type a, type b) {}
lambda§auto sq = [](int x) { return x * x; };¶int n = 0; auto inc = [&n]() { return ++n; };§[capture](params) { body }
list§std::vector<int> xs{3, 1, 2};¶xs.push_back(4); std::sort(xs.begin(), xs.end());¶for (int x : xs) {}§std::vector<T>
map§std::map<std::string, int> m;¶m["a"] = 1;¶for (auto& [k, v] : m) {}§std::map<K, V> / std::unordered_map
oop§class Person {¶public:¶    std::string name;¶    Person(std::string n) : name(n) {}¶    std::string greet() const { return "Hi, " + name; }¶};§class Name { public: ... };
inherit§struct Animal { virtual std::string speak() const = 0; virtual ~Animal() = default; };¶struct Dog : Animal { std::string speak() const override { return "Woof"; } };§class B : public A {}
err§try { throw std::runtime_error("x"); } catch (const std::exception& e) { std::cerr << e.what(); }§try {} catch (const E& e) {}
file§std::ifstream in("a.txt");¶std::string line; while (std::getline(in, line)) {}¶std::ofstream("b.txt") << "data";§#include <fstream>
mod§#include <iostream>¶#include "mine.h"¶import std; // C++23§#include / import
async§auto f = std::async(std::launch::async, [] { return 42; });¶int v = f.get();§std::async / std::thread
single§struct Config {¶  static Config& get() { static Config c; return c; }¶private: Config() = default;¶};§Meyers singleton
factory§std::unique_ptr<Animal> make(const std::string& k) {¶  if (k == "dog") return std::make_unique<Dog>();¶  return std::make_unique<Cat>();¶}§return unique_ptr<Base>
observer§std::vector<std::function<void(int)>> subs;¶void emit(int v) { for (auto& f : subs) f(v); }§vector of std::function
strategy§template<class F> int run(int x, F algo) { return algo(x); }¶run(3, [](int v) { return v * 2; });§template or std::function
rest§#include <httplib.h>¶httplib::Server s;¶s.Get("/hi", [](auto&, auto& res) { res.set_content("ok", "text/plain"); });¶s.listen("0.0.0.0", 8080);§cpp-httplib
test§#include <gtest/gtest.h>¶TEST(Math, Add) { EXPECT_EQ(1 + 2, 3); }§ctest / gtest
Smart Pointers§auto p = std::make_unique<Dog>();¶auto s = std::make_shared<Dog>();§std::unique_ptr / shared_ptr§Automatic memory management (RAII)§Memory
Templates§template <typename T> T maxOf(T a, T b) { return a > b ? a : b; }§template <typename T>§Generic programming§Functions
CMake Project§cmake_minimum_required(VERSION 3.20)¶project(app CXX)¶set(CMAKE_CXX_STANDARD 20)¶add_executable(app main.cpp)§cmake -S . -B build§Popular template: CMakeLists.txt§Templates
''')

lang("csharp", "C#", 2000, "Very High", "https://learn.microsoft.com/en-us/dotnet/csharp/", r'''
basic§Console.WriteLine("Hello World!");§Console.WriteLine()
comment§// line¶/* block */¶/// <summary>XML doc</summary>§// comment
var§int x = 5;¶var name = "Ada";¶const double Pi = 3.14;§type name = value;
types§int i = 42; double d = 3.14; bool b = true;¶string s = "txt"; var n = (int?)null;§typeof(T)
str§var s = $"Hi {name}";¶s.ToUpper(); s.Split(','); s.Substring(1, 2);§$"text {expr}"
if§if (x > 5) {¶    Console.WriteLine("big");¶} else if (x == 5) {¶    Console.WriteLine("five");¶} else {¶    Console.WriteLine("small");¶}§if (cond) {} else {}
switch§var r = cmd switch { "go" => "run", "stop" => "halt", _ => "idle" };§value switch { pattern => result }
for§for (int i = 0; i < 5; i++) {¶    Console.WriteLine(i);¶}¶foreach (var v in items) {¶    Console.WriteLine(v);¶}§for / foreach
while§int n = 3;¶while (n > 0) { n--; }§while (cond) {}
func§int Add(int a, int b) => a + b;¶string Greet(string name = "World") {¶    return $"Hello, {name}!";¶}§type Name(args) {}
lambda§Func<int,int> sq = x => x * x;¶int c = 0; Func<int> inc = () => ++c;§(args) => expr
list§var xs = new List<int> { 3, 1, 2 };¶xs.Add(4); xs.Sort();¶var ys = xs.Select(x => x * 2).Where(x => x > 2);§List<T> + LINQ
map§var m = new Dictionary<string,int> { ["a"] = 1 };¶foreach (var (k, v) in m) { }§Dictionary<K,V>
oop§public class Person {¶    public string Name { get; set; }¶    public Person(string name) => Name = name;¶    public string Greet() => $"Hi, {Name}";¶}§public class Name {}
inherit§interface IAnimal { string Speak(); }¶class Dog : IAnimal { public string Speak() => "Woof"; }§class B : A, I {}
err§try { int.Parse("x"); } catch (FormatException e) { Console.WriteLine(e.Message); } finally { }§try {} catch (E e) {} finally {}
file§var t = File.ReadAllText("a.txt");¶File.WriteAllText("b.txt", t);¶using var r = new StreamReader("a.txt");§System.IO.File
mod§using System.Text.Json;¶namespace App.Services;¶global using System.Linq;§using / namespace
async§static async Task Main() { await Task.Delay(100); var r = await http.GetStringAsync(url); }§async Task / await
single§public sealed class Config {¶    private static readonly Lazy<Config> I = new(() => new Config());¶    public static Config Instance => I.Value;¶    private Config() {}¶}§Lazy<T> + private ctor
factory§static IAnimal Make(string k) => k switch { "dog" => new Dog(), _ => new Cat() };§switch expression factory
observer§public event Action<int>? Changed;¶void Raise(int v) => Changed?.Invoke(v);§event + delegate
strategy§static int Run(int x, Func<int,int> algo) => algo(x);¶Run(3, v => v * 2);§inject Func<T>
rest§var app = WebApplication.CreateBuilder(args).Build();¶app.MapGet("/items/{id}", (int id) => new { id });¶app.Run();§dotnet new web
test§public class MathTests { [Fact] public void Add() => Assert.Equal(3, 1 + 2); }§dotnet test (xUnit)
LINQ§var top = people.Where(p => p.Age > 18).OrderBy(p => p.Name).Take(5);§collection.Where().Select()§Query collections declaratively§Collections
Records§public record Point(int X, int Y);¶var p2 = p with { X = 5 };§record Name(props);§Immutable value-like types§OOP
Dependency Injection§builder.Services.AddScoped<IRepo, Repo>();¶public class Svc(IRepo repo) { }§services.AddScoped<I, Impl>()§Constructor injection with the built-in container§Design Patterns
''')

lang("typescript", "TypeScript", 2012, "Very High", "https://www.typescriptlang.org/docs/handbook/intro.html", r'''
basic§console.log("Hello World!");§console.log()
comment§// line¶/* block */¶/** JSDoc */§// comment
var§let x: number = 5;¶const name: string = "Ada";§let name: type = value;
types§let a: number; let b: string; let c: boolean;¶let d: string[]; let e: [number, string]; let f: unknown; let g: any;§type annotation
str§const s = `Hi ${name}`;¶s.toUpperCase().split(",");§`template ${expr}`
if§if (x > 5) { } else if (x === 5) { } else { }¶if (typeof v === "string") { v.length; }§if (cond) {} else {}
switch§type S = "go" | "stop";¶function f(s: S) { switch (s) { case "go": return 1; case "stop": return 2; } }§switch (v) { case a: }
for§for (let i = 0; i < 5; i++) {}¶for (const v of arr) {}§for (init; cond; step) {}
while§let n = 3; while (n > 0) { n--; }§while (cond) {}
func§function add(a: number, b = 0): number { return a + b; }§function name(a: T): R {}
lambda§const sq = (x: number): number => x * x;§(a: T) => R
list§const xs: number[] = [3, 1, 2];¶xs.map(x => x * 2);§T[] / Array<T>
map§const m = new Map<string, number>();¶const o: Record<string, number> = { a: 1 };§Map<K, V> / Record<K, V>
oop§class Person {¶  constructor(public name: string) {}¶  hi(): string { return this.name; }¶}§class Name { constructor(public x: T) {} }
inherit§interface Animal { speak(): string }¶class Dog implements Animal { speak() { return "Woof"; } }§class B extends A implements I {}
err§try { JSON.parse("x"); } catch (e: unknown) { if (e instanceof Error) console.error(e.message); }§catch (e: unknown)
file§import { readFile } from "node:fs/promises";¶const t = await readFile("a.txt", "utf8");§fs/promises
mod§import { x } from "./mod";¶export interface User { id: number }§import / export
async§async function load(): Promise<number> { return await Promise.resolve(1); }§async fn(): Promise<T>
single§class Config { private static i?: Config; static get(): Config { return this.i ??= new Config(); } private constructor() {} }§private ctor + static
factory§function make(k: "dog" | "cat"): Animal { return k === "dog" ? new Dog() : new Cat(); }§typed factory
observer§type Fn<T> = (v: T) => void;¶class Subject<T> { private s: Fn<T>[] = []; on(f: Fn<T>) { this.s.push(f); } emit(v: T) { this.s.forEach(f => f(v)); } }§generic Subject<T>
strategy§type Algo = (n: number) => number;¶const run = (n: number, a: Algo) => a(n);§function type alias
rest§import express from "express";¶const app = express();¶app.get("/items/:id", (req, res) => res.json({ id: req.params.id }));¶app.listen(3000);§ts-node / tsx server.ts
test§import { describe, it, expect } from "vitest";¶describe("add", () => it("adds", () => expect(1 + 2).toBe(3)));§npx vitest
Generics§function identity<T>(v: T): T { return v; }§function f<T>(v: T): T§Reusable typed components§Variables & Types
Union & Narrowing§type R = { ok: true; v: number } | { ok: false; e: string };¶function f(r: R) { return r.ok ? r.v : r.e; }§A | B§Discriminated unions§Variables & Types
tsconfig.json§{ "compilerOptions": { "target": "ES2022", "strict": true, "module": "ESNext" } }§npx tsc --init§Popular template: compiler config§Templates
''')

lang("java", "Java", 1995, "Dominant", "https://dev.java/learn/", r'''
basic§public class Main {¶    public static void main(String[] args) {¶        System.out.println("Hello World!");¶    }¶}§public static void main(String[] args)
comment§// line¶/* block */¶/** Javadoc */§// comment
var§int x = 5;¶String name = "Ada";¶var n = 10; // inferred§Type name = value;
types§int i; long l; double d; boolean b; char c; String s;§primitive types + String
str§String s = "Hi " + name;¶s.toUpperCase(); s.split(","); s.substring(1, 3);¶String.format("%d items", n);§String methods
if§if (x > 5) { } else if (x == 5) { } else { }§if (cond) {} else {}
switch§String r = switch (cmd) { case "go" -> "run"; case "stop" -> "halt"; default -> "idle"; };§switch expression
for§for (int i = 0; i < 5; i++) { }¶for (String s : list) { }§for (init; cond; step) {}
while§int n = 3;¶while (n > 0) { n--; }§while (cond) {}
func§static int add(int a, int b) { return a + b; }§static ReturnType name(params) {}
lambda§Function<Integer,Integer> sq = x -> x * x;¶list.forEach(x -> System.out.println(x));§(args) -> expr
list§List<Integer> xs = new ArrayList<>(List.of(3, 1, 2));¶xs.add(4); Collections.sort(xs);¶xs.stream().map(x -> x * 2).toList();§List<T>
map§Map<String,Integer> m = new HashMap<>();¶m.put("a", 1);¶for (var e : m.entrySet()) { }§Map<K,V>
oop§class Person {¶    private final String name;¶    Person(String name) { this.name = name; }¶    String hi() { return name; }¶}§class Name {}
inherit§interface Animal { String speak(); }¶class Dog implements Animal { public String speak() { return "Woof"; } }§class B extends A implements I
err§try { Integer.parseInt("x"); } catch (NumberFormatException e) { System.out.println(e.getMessage()); } finally { }§try {} catch (E e) {} finally {}
file§String t = Files.readString(Path.of("a.txt"));¶Files.writeString(Path.of("b.txt"), t);§java.nio.file.Files
mod§package com.app;¶import java.util.*;¶import static java.lang.Math.max;§package / import
async§CompletableFuture.supplyAsync(() -> 42).thenAccept(System.out::println);¶try (var ex = Executors.newVirtualThreadPerTaskExecutor()) { ex.submit(() -> {}); }§CompletableFuture / virtual threads
single§public enum Config { INSTANCE; public String url = "x"; }§enum singleton
factory§static Animal make(String k) { return k.equals("dog") ? new Dog() : new Cat(); }§static factory method
observer§interface Listener { void on(int v); }¶List<Listener> subs = new ArrayList<>();¶void emit(int v) { subs.forEach(l -> l.on(v)); }§listener list
strategy§static int run(int x, UnaryOperator<Integer> algo) { return algo.apply(x); }§functional interface
rest§@RestController class Api { @GetMapping("/items/{id}") Map<String,Object> item(@PathVariable int id) { return Map.of("id", id); } }§Spring Boot (spring-boot-starter-web)
test§import org.junit.jupiter.api.Test;¶class MathTest { @Test void add() { assertEquals(3, 1 + 2); } }§mvn test / gradle test
Streams§int sum = list.stream().filter(x -> x > 1).mapToInt(Integer::intValue).sum();§collection.stream().filter().map()§Functional pipelines over collections§Collections
Records§record Point(int x, int y) {}§record Name(components) {}§Immutable data carriers (Java 16+)§OOP
Builder Pattern§Person p = new Person.Builder().name("Ada").age(36).build();§Type.Builder().set().build()§Step-wise object construction§Design Patterns
Maven pom.xml§<project><modelVersion>4.0.0</modelVersion><groupId>com.app</groupId><artifactId>app</artifactId><version>1.0</version></project>§mvn archetype:generate§Popular template: Maven project descriptor§Templates
''')

lang("go", "Go", 2009, "Very High", "https://go.dev/doc/", r'''
basic§package main¶import "fmt"¶func main() { fmt.Println("Hello World!") }§package main; func main() {}
comment§// line¶/* block */§// comment
var§var x int = 5¶name := "Ada"¶const Pi = 3.14§var x T = v  |  x := v
types§var i int; var f float64; var b bool; var s string; var r rune; var by byte§int, float64, bool, string
str§s := "Hi " + name¶strings.ToUpper(s); strings.Split(s, ","); s[1:3]; len(s)§import "strings"
if§if x > 5 { } else if x == 5 { } else { }¶if v, ok := m["a"]; ok { }§if cond {} else {}
switch§switch cmd {¶case "go": run()¶case "stop": halt()¶default: idle()¶}§switch v { case a: }
for§for i := 0; i < 5; i++ { }¶for i, v := range xs { }§for init; cond; post {}
while§n := 3¶for n > 0 { n-- }§for cond {}
func§func add(a, b int) (int, error) { return a + b, nil }§func name(params) (results) {}
lambda§sq := func(x int) int { return x * x }¶func counter() func() int { c := 0; return func() int { c++; return c } }§func(params) result {}
list§xs := []int{3, 1, 2}¶xs = append(xs, 4)¶sort.Ints(xs)§[]T / append()
map§m := map[string]int{"a": 1}¶m["b"] = 2¶for k, v := range m { }§map[K]V
oop§type Person struct { Name string }¶func (p Person) Hi() string { return p.Name }§type T struct{}; func (t T) M() {}
inherit§type Animal interface { Speak() string }¶type Dog struct{}¶func (Dog) Speak() string { return "Woof" }§implicit interfaces + embedding
err§v, err := strconv.Atoi("x")¶if err != nil { return fmt.Errorf("bad: %w", err) }¶defer cleanup()§if err != nil
file§b, err := os.ReadFile("a.txt")¶err = os.WriteFile("b.txt", b, 0o644)§os.ReadFile / WriteFile
mod§import ("fmt"; "net/http")¶// go mod init example.com/app¶// go get github.com/gin-gonic/gin§go.mod / import
async§go func() { ch <- 42 }()¶v := <-ch¶var wg sync.WaitGroup; wg.Add(1); go func() { defer wg.Done() }(); wg.Wait()§go func(); chan T
single§var (inst *Config; once sync.Once)¶func Get() *Config { once.Do(func() { inst = &Config{} }); return inst }§sync.Once
factory§func Make(k string) Animal { if k == "dog" { return Dog{} }; return Cat{} }§return interface
observer§type Fn func(int)¶type Subject struct{ subs []Fn }¶func (s *Subject) Emit(v int) { for _, f := range s.subs { f(v) } }§slice of funcs / channels
strategy§func Run(x int, algo func(int) int) int { return algo(x) }§pass func value
rest§http.HandleFunc("/items", func(w http.ResponseWriter, r *http.Request) { json.NewEncoder(w).Encode(map[string]int{"id": 1}) })¶http.ListenAndServe(":8080", nil)§net/http
test§func TestAdd(t *testing.T) { if 1+2 != 3 { t.Fatal("bad") } }§go test ./...
Goroutines & Channels§ch := make(chan int)¶go func() { ch <- 1 }()¶fmt.Println(<-ch)§make(chan T)§Lightweight concurrency primitives§Concurrency
Defer§f, _ := os.Open("a.txt")¶defer f.Close()§defer call()§Run cleanup when the function returns§Functions
Functional Options§type Opt func(*Server)¶func WithPort(p int) Opt { return func(s *Server) { s.port = p } }§func New(opts ...Opt)§Idiomatic configurable constructors§Design Patterns
''')

lang("rust", "Rust", 2015, "High", "https://doc.rust-lang.org/book/", r'''
basic§fn main() {¶    println!("Hello World!");¶}§fn main() {}
comment§// line¶/* block */¶/// doc comment§// comment
var§let x = 5;¶let mut y = 1;¶const MAX: u32 = 10;§let [mut] name = value;
types§let i: i32 = 1; let f: f64 = 1.0; let b: bool = true;¶let c: char = 'a'; let s: &str = "t"; let t: (i32, f64) = (1, 2.0);§i32, u64, f64, bool, char, &str
str§let s = format!("Hi {name}");¶s.to_uppercase(); s.split(',').collect::<Vec<_>>(); &s[1..3];§String / &str
if§if x > 5 { } else if x == 5 { } else { }¶let v = if c { 1 } else { 2 };§if cond {} else {}
switch§match cmd {¶    "go" => run(),¶    "stop" => halt(),¶    _ => idle(),¶}§match value { pat => expr }
for§for i in 0..5 { }¶for v in &xs { }§for x in iter {}
while§let mut n = 3;¶while n > 0 { n -= 1; }¶loop { break; }§while cond {} / loop {}
func§fn add(a: i32, b: i32) -> i32 { a + b }§fn name(a: T) -> R {}
lambda§let sq = |x: i32| x * x;¶let mut c = 0; let mut inc = || { c += 1; c };§|args| expr
list§let mut xs = vec![3, 1, 2];¶xs.push(4); xs.sort();¶let ys: Vec<_> = xs.iter().map(|x| x * 2).collect();§Vec<T>
map§use std::collections::HashMap;¶let mut m = HashMap::new();¶m.insert("a", 1);¶for (k, v) in &m { }§HashMap<K, V>
oop§struct Person { name: String }¶impl Person { fn hi(&self) -> &str { &self.name } }§struct T {} impl T {}
inherit§trait Animal { fn speak(&self) -> String; }¶struct Dog;¶impl Animal for Dog { fn speak(&self) -> String { "Woof".into() } }§trait + impl Trait for Type
err§fn parse(s: &str) -> Result<i32, std::num::ParseIntError> { s.parse::<i32>() }¶let n = parse("1")?;§Result<T, E> and ?
file§let t = std::fs::read_to_string("a.txt")?;¶std::fs::write("b.txt", t)?;§std::fs
mod§mod util;¶use std::collections::HashSet;¶use crate::util::helper;§mod / use / crate
async§#[tokio::main]¶async fn main() { tokio::time::sleep(std::time::Duration::from_millis(100)).await; }§tokio async runtime
single§use std::sync::OnceLock;¶static CFG: OnceLock<String> = OnceLock::new();¶fn cfg() -> &'static String { CFG.get_or_init(|| "x".into()) }§OnceLock
factory§fn make(k: &str) -> Box<dyn Animal> { if k == "dog" { Box::new(Dog) } else { Box::new(Cat) } }§Box<dyn Trait>
observer§struct Subject { subs: Vec<Box<dyn Fn(i32)>> }¶impl Subject { fn emit(&self, v: i32) { for f in &self.subs { f(v); } } }§Vec<Box<dyn Fn>>
strategy§fn run<F: Fn(i32) -> i32>(x: i32, algo: F) -> i32 { algo(x) }§generic closure parameter
rest§use axum::{routing::get, Router, Json};¶let app = Router::new().route("/items", get(|| async { Json(1) }));§axum + tokio
test§#[cfg(test)]¶mod tests { #[test] fn add() { assert_eq!(1 + 2, 3); } }§cargo test
Ownership & Borrowing§let s = String::from("a");¶let r = &s;¶let t = s; // moved§&T / &mut T§Memory safety without a GC§Variables & Types
Pattern Matching§if let Some(v) = opt { }¶let (a, b) = pair;§if let Pat = value§Destructure enums and structs§Decisions
Cargo.toml§[package]¶name = "app"¶version = "0.1.0"¶edition = "2021"¶[dependencies]¶serde = "1"§cargo new app§Popular template: package manifest§Templates
''')

lang("ruby", "Ruby", 1995, "Medium", "https://www.ruby-lang.org/en/documentation/", r'''
comment§# single line¶=begin¶block¶=end§# comment
types§i = 42; f = 3.14; b = true; s = "txt"; sym = :a; n = nil§obj.class
str§s = "Hi #{name}"¶s.upcase; s.split(","); s[1, 2]§"text #{expr}"
if§if x > 5 then puts "big" elsif x == 5 then puts "five" else puts "small" end¶puts "ok" unless x.zero?§if cond ... elsif ... else ... end
switch§case cmd¶when "go" then run¶when "stop" then halt¶else idle¶end§case v when a then b end
while§n = 3¶while n > 0¶  n -= 1¶end§while cond ... end
lambda§sq = ->(x) { x * x }¶def counter; c = 0; -> { c += 1 }; end§->(args) { expr }
list§xs = [3, 1, 2]¶xs << 4; xs.sort!¶xs.map { |x| x * 2 }.select { |x| x > 2 }§[1, 2].map { |x| ... }
map§m = { "a" => 1, b: 2 }¶m[:c] = 3¶m.each { |k, v| puts "#{k}=#{v}" }§{ key: value }
inherit§class Animal; def speak; end; end¶class Dog < Animal; def speak = "Woof"; end§class Child < Parent
err§begin¶  Integer("x")¶rescue ArgumentError => e¶  puts e.message¶ensure¶  puts "done"¶end§begin ... rescue ... ensure ... end
file§text = File.read("a.txt")¶File.write("b.txt", text)¶File.foreach("a.txt") { |l| puts l }§File.read / File.write
mod§require "json"¶require_relative "util"¶module Helpers; end§require / module
async§t = Thread.new { 42 }¶t.value¶require "async"; Async { sleep 1 }§Thread / Fiber / async gem
single§require "singleton"¶class Config; include Singleton; end¶Config.instance§include Singleton
factory§def make(k) = { dog: Dog, cat: Cat }.fetch(k).new§factory method returning .new
observer§require "observer"¶class Subject; include Observable; end§include Observable
strategy§def run(x, algo) = algo.call(x)¶run(3, ->(v) { v * 2 })§pass a lambda
rest§require "sinatra"¶get("/items/:id") { { id: params[:id] }.to_json }§ruby app.rb (Sinatra)
test§require "minitest/autorun"¶class MathTest < Minitest::Test; def test_add; assert_equal 3, 1 + 2; end; end§ruby test.rb
Blocks & Procs§[1, 2, 3].each { |n| puts n }¶def twice; yield; yield; end§method { |x| ... }§Pass code blocks to methods§Functions
Mixins§module Walk; def walk = "walking"; end¶class Dog; include Walk; end§module M; include M§Share behavior without inheritance§OOP
Gemfile§source "https://rubygems.org"¶gem "rails"¶gem "rspec", group: :test§bundle install§Popular template: dependency manifest§Templates
''')

lang("kotlin", "Kotlin", 2011, "High", "https://kotlinlang.org/docs/home.html", r'''
basic§fun main() { println("Hello World!") }§fun main() {}
comment§// line¶/* block */¶/** KDoc */§// comment
var§val x = 5¶var y = 1¶val name: String = "Ada"§val (immutable) / var (mutable)
types§val i: Int = 1; val l: Long = 1L; val d: Double = 1.0; val b: Boolean = true;¶val s: String = "t"; val n: String? = null§Int, Long, Double, Boolean, String?
str§val s = "Hi $name ${x + 1}"¶s.uppercase(); s.split(","); s.substring(1, 3)§"text $var"
if§if (x > 5) println("big") else if (x == 5) println("five") else println("small")¶val v = if (c) 1 else 2§if (cond) a else b
switch§val r = when (cmd) { "go" -> "run"; "stop" -> "halt"; else -> "idle" }§when (v) { a -> b; else -> c }
for§for (i in 0 until 5) { }¶for (v in list) { }§for (x in range) {}
while§var n = 3¶while (n > 0) { n-- }§while (cond) {}
func§fun add(a: Int, b: Int = 0): Int = a + b§fun name(a: T): R = expr
lambda§val sq = { x: Int -> x * x }¶list.map { it * 2 }§{ args -> expr }
list§val xs = mutableListOf(3, 1, 2)¶xs.add(4); xs.sort()¶val ys = xs.map { it * 2 }.filter { it > 2 }§listOf / mutableListOf
map§val m = mutableMapOf("a" to 1)¶m["b"] = 2¶for ((k, v) in m) { }§mapOf / mutableMapOf
oop§class Person(val name: String) { fun hi() = name }§class Name(val x: T)
inherit§interface Animal { fun speak(): String }¶class Dog : Animal { override fun speak() = "Woof" }§class B : A(), I
err§try { "x".toInt() } catch (e: NumberFormatException) { println(e.message) } finally { }¶val r = runCatching { "1".toInt() }§try / catch / finally
file§val t = File("a.txt").readText()¶File("b.txt").writeText(t)§java.io.File extensions
mod§package com.app¶import kotlin.math.max§package / import
async§suspend fun load(): Int { delay(100); return 1 }¶fun main() = runBlocking { println(load()) }§suspend fun + coroutines
single§object Config { val url = "x" }§object declaration
factory§fun make(k: String): Animal = if (k == "dog") Dog() else Cat()§factory function
observer§class Subject { private val subs = mutableListOf<(Int) -> Unit>(); fun emit(v: Int) = subs.forEach { it(v) } }§list of lambdas / Flow
strategy§fun run(x: Int, algo: (Int) -> Int) = algo(x)§higher-order function
rest§embeddedServer(Netty, 8080) { routing { get("/items/{id}") { call.respond(mapOf("id" to call.parameters["id"])) } } }.start(wait = true)§Ktor
test§class MathTest { @Test fun add() { assertEquals(3, 1 + 2) } }§gradle test (kotlin.test)
Data Classes§data class Point(val x: Int, val y: Int)¶val p2 = p.copy(x = 5)§data class Name(props)§Auto equals / hashCode / copy§OOP
Extension Functions§fun String.shout() = uppercase() + "!"§fun Type.name()§Add methods without inheritance§Functions
build.gradle.kts§plugins { kotlin("jvm") version "2.0.0" }¶repositories { mavenCentral() }¶dependencies { testImplementation(kotlin("test")) }§gradle init§Popular template: Gradle Kotlin DSL§Templates
''')

lang("swift", "Swift", 2014, "High", "https://docs.swift.org/swift-book/", r'''
basic§print("Hello World!")§print()
comment§// line¶/* block */¶/// doc§// comment
var§let x = 5¶var y = 1¶let name: String = "Ada"§let (constant) / var (variable)
types§let i: Int = 1; let d: Double = 1.0; let b: Bool = true¶let s: String = "t"; let o: Int? = nil§Int, Double, Bool, String, Optional
str§let s = "Hi \(name)"¶s.uppercased(); s.split(separator: ","); s.count§"text \(expr)"
if§if x > 5 { } else if x == 5 { } else { }¶guard let v = opt else { return }§if cond {} else {}
switch§switch cmd {¶case "go": run()¶case "stop": halt()¶default: idle()¶}§switch v { case a: ... }
for§for i in 0..<5 { }¶for v in xs { }§for x in sequence {}
while§var n = 3¶while n > 0 { n -= 1 }¶repeat { n += 1 } while n < 3§while cond {}
func§func add(_ a: Int, b: Int = 0) -> Int { a + b }§func name(_ a: T) -> R {}
lambda§let sq = { (x: Int) in x * x }¶xs.map { $0 * 2 }§{ params in expr }
list§var xs = [3, 1, 2]¶xs.append(4); xs.sort()¶let ys = xs.map { $0 * 2 }.filter { $0 > 2 }§[T]
map§var m = ["a": 1]¶m["b"] = 2¶for (k, v) in m { }§[K: V]
oop§struct Person { var name: String; func hi() -> String { name } }¶class Car { var speed = 0 }§struct / class
inherit§protocol Animal { func speak() -> String }¶class Dog: Animal { func speak() -> String { "Woof" } }§class B: A, Protocol
err§enum E: Error { case bad }¶do { try f() } catch { print(error) }§do { try } catch {}
file§let t = try String(contentsOfFile: "a.txt", encoding: .utf8)¶try t.write(toFile: "b.txt", atomically: true, encoding: .utf8)§Foundation
mod§import Foundation¶import SwiftUI§import Module
async§func load() async throws -> Int { try await Task.sleep(nanoseconds: 100_000_000); return 1 }¶Task { print(try await load()) }§async / await / Task
single§final class Config { static let shared = Config(); private init() {} }§static let shared
factory§func make(_ k: String) -> Animal { k == "dog" ? Dog() : Cat() }§factory function
observer§class Subject { var subs: [(Int) -> Void] = []; func emit(_ v: Int) { subs.forEach { $0(v) } } }§closures / Combine
strategy§func run(_ x: Int, algo: (Int) -> Int) -> Int { algo(x) }§closure parameter
rest§import Vapor¶let app = Application()¶app.get("items", ":id") { req in req.parameters.get("id") ?? "" }¶try app.run()§Vapor
test§import XCTest¶final class MathTests: XCTestCase { func testAdd() { XCTAssertEqual(1 + 2, 3) } }§swift test
SwiftUI View§struct ContentView: View { var body: some View { Text("Hello") } }§struct V: View { var body: some View {} }§Popular template: declarative UI§Templates
Optionals§var name: String? = nil¶print(name ?? "none")¶if let n = name { print(n) }§T? / ?? / if let§Safe handling of missing values§Variables & Types
Package.swift§// swift-tools-version:5.9¶import PackageDescription¶let package = Package(name: "App", targets: [.executableTarget(name: "App")])§swift package init§Popular template: Swift Package manifest§Templates
''')

lang("c", "C", 1972, "Very High", "https://en.cppreference.com/w/c", r'''
basic§#include <stdio.h>¶int main(void) { printf("Hello World!\n"); return 0; }§int main(void) {}
comment§// line (C99)¶/* block */§// comment
var§int x = 5;¶const double PI = 3.14;¶#define MAX 10§type name = value;
types§int i; long l; float f; double d; char c; _Bool b;¶int *p = &i; int a[3];§int, char, float, double, pointers
str§char s[] = "Hi";¶strlen(s); strcpy(dst, s); strcmp(a, b); snprintf(buf, n, "%s %d", s, 1);§<string.h>
if§if (x > 5) { } else if (x == 5) { } else { }§if (cond) {} else {}
switch§switch (cmd) {¶case 1: run(); break;¶default: idle();¶}§switch (v) { case a: break; }
for§for (int i = 0; i < 5; i++) { printf("%d", i); }§for (init; cond; step) {}
while§int n = 3;¶while (n > 0) { n--; }¶do { n++; } while (n < 3);§while (cond) {}
func§int add(int a, int b) { return a + b; }§type name(params) {}
list§int xs[3] = {3, 1, 2};¶qsort(xs, 3, sizeof(int), cmp);¶int *h = malloc(3 * sizeof *h); free(h);§type name[size]
map§typedef struct { char key[16]; int val; } Entry;¶Entry table[8];§struct arrays / hash tables (manual)
oop§typedef struct { char name[32]; } Person;¶void hi(const Person *p) { puts(p->name); }§struct + functions
err§FILE *f = fopen("a.txt", "r");¶if (!f) { perror("open"); return 1; }§check return values / errno
file§FILE *f = fopen("a.txt", "r");¶char line[256]; while (fgets(line, sizeof line, f)) { }¶fclose(f);§fopen / fgets / fclose
mod§#include <stdlib.h>¶#include "util.h"§#include / header files
async§#include <pthread.h>¶pthread_t t; pthread_create(&t, NULL, work, NULL); pthread_join(t, NULL);§pthread
single§static Config *cfg(void) { static Config c; return &c; }§static local instance
factory§Shape *make(int k) { return k == 0 ? new_circle() : new_square(); }§constructor functions
observer§typedef void (*cb)(int);¶cb subs[8]; int n;¶void emit(int v) { for (int i = 0; i < n; i++) subs[i](v); }§function pointer array
strategy§int run(int x, int (*algo)(int)) { return algo(x); }§function pointer
rest§// use libmicrohttpd or mongoose¶mg_http_listen(&mgr, "http://0.0.0.0:8000", handler, NULL);§mongoose / libmicrohttpd
test§#include <assert.h>¶int main(void) { assert(1 + 2 == 3); return 0; }§assert / Unity framework
Pointers§int x = 5; int *p = &x; *p = 6;§type *p = &var;§Direct memory addressing§Variables & Types
Makefile§CC=gcc¶CFLAGS=-Wall -O2¶app: main.c¶\t$(CC) $(CFLAGS) -o $@ $<§make§Popular template: build file§Templates
''')

lang("dart", "Dart", 2011, "Medium", "https://dart.dev/language", r'''
basic§void main() { print('Hello World!'); }§void main() {}
comment§// line¶/* block */¶/// doc§// comment
var§var x = 5;¶final name = 'Ada';¶const pi = 3.14;¶String? maybe;§var / final / const
types§int i = 1; double d = 1.0; bool b = true; String s = 't'; List<int> l = [1]; Map<String,int> m = {'a': 1};§int, double, bool, String
str§var s = 'Hi $name ${x + 1}';¶s.toUpperCase(); s.split(','); s.substring(1, 3);§'text $var'
if§if (x > 5) { } else if (x == 5) { } else { }§if (cond) {} else {}
switch§var r = switch (cmd) { 'go' => 'run', 'stop' => 'halt', _ => 'idle' };§switch expression
for§for (var i = 0; i < 5; i++) { }¶for (final v in list) { }§for (init; cond; step) {}
while§var n = 3;¶while (n > 0) { n--; }§while (cond) {}
func§int add(int a, [int b = 0]) => a + b;¶void greet({required String name}) {}§type name(params) => expr
lambda§var sq = (int x) => x * x;¶list.map((x) => x * 2);§(args) => expr
list§var xs = [3, 1, 2];¶xs.add(4); xs.sort();¶var ys = xs.map((x) => x * 2).where((x) => x > 2).toList();§List<T>
map§var m = {'a': 1};¶m['b'] = 2;¶m.forEach((k, v) => print('$k=$v'));§Map<K, V>
oop§class Person { final String name; Person(this.name); String hi() => name; }§class Name { Name(this.x); }
inherit§abstract class Animal { String speak(); }¶class Dog extends Animal { @override String speak() => 'Woof'; }§class B extends A implements I
err§try { int.parse('x'); } on FormatException catch (e) { print(e); } finally { }§try on E catch finally
file§import 'dart:io';¶var t = await File('a.txt').readAsString();¶await File('b.txt').writeAsString(t);§dart:io
mod§import 'package:http/http.dart' as http;¶import 'util.dart';¶export 'src/a.dart';§import / export
async§Future<int> load() async { await Future.delayed(Duration(milliseconds: 100)); return 1; }§Future / async / await / Isolate
single§class Config { static final Config _i = Config._(); Config._(); factory Config() => _i; }§factory constructor
factory§abstract class Animal { factory Animal(String k) => k == 'dog' ? Dog() : Cat(); }§factory constructor
observer§final _ctrl = StreamController<int>();¶_ctrl.stream.listen(print);¶_ctrl.add(1);§Stream / ChangeNotifier
strategy§int run(int x, int Function(int) algo) => algo(x);§function type parameter
rest§import 'package:shelf/shelf_io.dart' as io;¶import 'package:shelf/shelf.dart';¶io.serve((Request r) => Response.ok('hi'), 'localhost', 8080);§shelf package
test§import 'package:test/test.dart';¶void main() { test('add', () => expect(1 + 2, 3)); }§dart test
Flutter Widget§class Home extends StatelessWidget { @override Widget build(BuildContext c) => Text('Hello'); }§class W extends StatelessWidget§Popular template: Flutter UI§Templates
Null Safety§String? n; print(n ?? 'none'); print(n?.length);§T? / ?? / ?.§Sound null safety§Variables & Types
pubspec.yaml§name: app¶environment:¶  sdk: ^3.0.0¶dependencies:¶  http: ^1.0.0§dart create app§Popular template: package manifest§Templates
''')

# ---------------------------------------------------------------- custom sets
lang("html", "HTML", 1993, "Dominant", "https://developer.mozilla.org/en-US/docs/Web/HTML", r'''
Basic Syntax§<!DOCTYPE html>¶<html lang="en">¶<head><meta charset="UTF-8"><title>Hello</title></head>¶<body>¶  <h1>Hello World!</h1>¶</body>¶</html>§<!DOCTYPE html><html>...</html>§HTML5 document structure§Basics
Variables§<!-- Custom Data Attributes & CSS Properties in HTML -->¶<div id="user" data-user-id="42" data-role="admin">Profile</div>¶<p style="--theme-color: #58a6ff;">Custom Property Value</p>§data-*="value"§Store custom data and variables on elements§Variables & Types
Conditional Statements§<!-- Native dialog, details disclosure & template elements -->¶<dialog open><p>Modal active</p></dialog>¶<details><summary>Toggle</summary><p>Expanded content</p></details>¶<template id="card"><div>Dynamic</div></template>§<details><summary>...</summary></details>§Built-in conditional display and hidden templates§Decisions
Loops§<!-- Repeated markup via lists, tables and iterated template elements -->¶<ul>¶  <li>Item 1</li>¶  <li>Item 2</li>¶  <li>Item 3</li>¶</ul>§<ul><li>...</li></ul>§Display collections and repeated items§Loops
Functions§<!-- Form actions, methods and interactive button triggers -->¶<form action="/api/submit" method="post">¶  <label for="name">Name:</label>¶  <input id="name" name="name" required>¶  <button type="submit">Submit</button>¶</form>§<form action="..." method="...">§Collect input and trigger server endpoints§Functions
Object-Oriented Programming§<!-- Custom HTML Web Components (Custom Elements) -->¶<user-avatar username="Ada" size="64"></user-avatar>¶<script>¶class UserAvatar extends HTMLElement {¶  connectedCallback() { this.innerHTML = `<img alt="${this.getAttribute('username')}">`; }¶}¶customElements.define('user-avatar', UserAvatar);¶</script>§customElements.define('tag-name', Class)§Encapsulate reusable custom elements with DOM lifecycle§OOP
Comments§<!-- comment -->§<!-- text -->§Writing comments in HTML§Basics
Document Template§<!DOCTYPE html>¶<html lang="en">¶<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page</title></head>¶<body></body>¶</html>§<!DOCTYPE html><html>...</html>§Popular template: HTML5 page skeleton§Templates
Headings & Paragraphs§<h1>Title</h1>¶<p>Text</p>¶<h2>Sub</h2>§<h1>-<h6>, <p>§Headings and text blocks§Text
Links§<a href="https://example.com" target="_blank" rel="noopener">Link</a>§<a href="url">§Hyperlinks§Navigation
Images§<img src="a.png" alt="Description" width="200" loading="lazy">§<img src alt>§Embedding images§Media
Lists§<ul><li>One</li><li>Two</li></ul>¶<ol><li>First</li></ol>§<ul>, <ol>, <li>§Ordered and unordered lists§Text
Tables§<table><thead><tr><th>A</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>§<table><tr><td>§Tabular data§Text
Forms§<form action="/save" method="post">¶  <label for="n">Name</label><input id="n" name="n" required>¶  <button type="submit">Send</button>¶</form>§<form><input><button>§Collecting user input§Forms
Input Types§<input type="email"> <input type="number" min="0"> <input type="date"> <input type="checkbox"> <select><option>A</option></select>§<input type="...">§Built-in input controls and validation§Forms
Semantic Layout§<header></header><nav></nav><main><article></article><aside></aside></main><footer></footer>§<header> <main> <footer>§Meaningful page structure§Structure
Meta & SEO§<meta name="description" content="Summary">¶<meta property="og:title" content="Title">¶<link rel="canonical" href="https://example.com/">§<meta> <link>§Search and social metadata§SEO
Audio & Video§<video controls src="a.mp4"></video>¶<audio controls src="a.mp3"></audio>§<video> <audio>§Native media elements§Media
Scripts & Styles§<link rel="stylesheet" href="app.css">¶<script src="app.js" defer></script>§<link> <script defer>§Loading CSS and JavaScript§Templates
Accessibility§<button aria-label="Close">x</button>¶<img alt="Logo">¶<a href="#main" class="skip">Skip</a>§aria-* attributes§Accessible markup§Accessibility
Dialog & Details§<dialog open>Hi</dialog>¶<details><summary>More</summary>Text</details>§<dialog> <details>§Interactive elements without JavaScript§Structure
''')

lang("css", "CSS", 1996, "Dominant", "https://developer.mozilla.org/en-US/docs/Web/CSS", r'''
Basic Syntax§p { color: #333; font-size: 16px; }§selector { property: value; }§Rule structure§Basics
Comments§/* comment */§/* text */§Writing comments in CSS§Basics
Selectors§.class { } #id { } div > p { } a:hover { } input[type="text"] { } li:nth-child(2) { }§.class #id element:pseudo§Targeting elements§Selectors
Variables§:root { --accent: #58a6ff; }¶a { color: var(--accent); }§--name: value; var(--name)§Custom properties§Variables & Types
Box Model§.box { margin: 1rem; padding: 1rem; border: 1px solid #ccc; box-sizing: border-box; }§margin padding border§Spacing and sizing§Layout
Flexbox§.row { display: flex; gap: 1rem; justify-content: space-between; align-items: center; }§display: flex§One-dimensional layout§Layout
Grid§.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }§display: grid§Two-dimensional layout§Layout
Media Queries§@media (max-width: 760px) { nav { display: none; } }§@media (condition) {}§Responsive design§Responsive
Container Queries§.card { container-type: inline-size; }¶@container (min-width: 400px) { .card h2 { font-size: 2rem; } }§@container (condition)§Component-level responsiveness§Responsive
Animations§@keyframes fade { from { opacity: 0 } to { opacity: 1 } }¶.box { animation: fade 1s ease-in; }§@keyframes name§Keyframe animation§Effects
Transitions§button { transition: background .2s ease; }¶button:hover { background: #2ea043; }§transition: prop time§Smooth state changes§Effects
Nesting§.card { color: #333; &:hover { color: #000; } .title { font-weight: 700; } }§selector { &:hover {} }§Native CSS nesting§Selectors
Reset Template§*, *::before, *::after { box-sizing: border-box; }¶body { margin: 0; font-family: system-ui, sans-serif; }§reset stylesheet§Popular template: minimal reset§Templates
''')

lang("aspnet", "ASP.NET Core", 2016, "Very High", "https://learn.microsoft.com/en-us/aspnet/core/", r'''
Basic Syntax§var builder = WebApplication.CreateBuilder(args);¶var app = builder.Build();¶app.MapGet("/", () => "Hello World!");¶app.Run();§WebApplication.CreateBuilder(args)§Entry point and web host setup§Basics
Variables§// Configuration & Environment Variables¶var port = builder.Configuration.GetValue<int>("Port", 5000);¶var connStr = builder.Configuration.GetConnectionString("Default");§builder.Configuration[...]§App configuration and environment settings§Variables & Types
Conditional Statements§if (app.Environment.IsDevelopment()) {¶    app.UseDeveloperExceptionPage();¶}¶app.MapGet("/items/{id:int}", (int id) => id > 0 ? Results.Ok(id) : Results.NotFound());§if (app.Environment.IsDevelopment())§Environment-based branching and route constraints§Decisions
Loops§// Iterating in Razor views or streaming async results¶@foreach (var item in Model.Items) {¶    <li>@item.Name</li>¶}¶// Async streaming: await foreach (var chunk in GetChunksAsync())§@foreach (var item in items) { }§Render dynamic collections and stream responses§Loops
Functions§// Minimal API Route Handlers & Controller Actions¶app.MapPost("/items", (ItemDto dto, IItemService svc) => {¶    var created = svc.Create(dto);¶    return Results.Created($"/items/{created.Id}", created);¶});§app.MapGet / app.MapPost§Delegate endpoints and action methods§Functions
Object-Oriented Programming§public record ItemDto(int Id, string Title);¶public interface IItemService { ItemDto Get(int id); }¶public class ItemService : IItemService {¶    public ItemDto Get(int id) => new(id, "Sample");¶}§record / interface / class§Domain models, services, and dependency injection contracts§OOP
Minimal API§var builder = WebApplication.CreateBuilder(args);¶var app = builder.Build();¶app.MapGet("/", () => "Hello World!");¶app.Run();§WebApplication.CreateBuilder(args)§Smallest ASP.NET Core app§Templates
Routing§app.MapGet("/items/{id:int}", (int id) => Results.Ok(new { id }));¶app.MapPost("/items", (Item i) => Results.Created($"/items/{i.Id}", i));§MapGet / MapPost§Endpoint routing§Routing
Controllers§[ApiController]¶[Route("api/[controller]")]¶public class ItemsController : ControllerBase {¶    [HttpGet("{id}")] public IActionResult Get(int id) => Ok(new { id });¶}§[ApiController] [Route]§MVC controllers§Routing
Razor Pages§@page¶@model IndexModel¶<h1>Hello @Model.Name</h1>§@page @model§Page-based UI§Views
Razor Syntax§@{ var n = 5; }¶@if (n > 3) { <p>big</p> }¶@foreach (var i in Model.Items) { <li>@i</li> }§@expression  @{ code }§Mix C# and HTML§Views
Model Binding & Validation§public record Item([Required] string Name, [Range(1, 100)] int Qty);§[Required] [Range]§Bind and validate input§Models
Dependency Injection§builder.Services.AddScoped<IRepo, Repo>();¶app.MapGet("/", (IRepo r) => r.All());§AddSingleton / AddScoped / AddTransient§Built-in IoC container§Design Patterns
Middleware§app.Use(async (ctx, next) => { Console.WriteLine(ctx.Request.Path); await next(); });§app.Use(...)§Request pipeline§Pipeline
Configuration§var cs = builder.Configuration.GetConnectionString("Default");¶// appsettings.json: { "ConnectionStrings": { "Default": "..." } }§builder.Configuration§Settings and secrets§Configuration
Entity Framework Core§public class Db : DbContext { public DbSet<Item> Items => Set<Item>(); }¶var all = await db.Items.Where(i => i.Qty > 0).ToListAsync();§DbContext / DbSet§ORM data access§Data
Authentication§builder.Services.AddAuthentication("Bearer").AddJwtBearer();¶app.UseAuthentication(); app.UseAuthorization();¶app.MapGet("/me", () => "ok").RequireAuthorization();§AddAuthentication / RequireAuthorization§JWT / cookie auth§Security
Logging§app.Logger.LogInformation("Started at {Time}", DateTime.UtcNow);§ILogger<T>§Structured logging§Diagnostics
Error Handling§app.UseExceptionHandler("/error");¶app.MapGet("/error", () => Results.Problem());§UseExceptionHandler§Global error handling§Error Handling
Integration Test§var client = new WebApplicationFactory<Program>().CreateClient();¶var res = await client.GetAsync("/");¶Assert.True(res.IsSuccessStatusCode);§WebApplicationFactory<T>§Popular template: API integration test§Templates
''')

lang("sql", "SQL", 1974, "Dominant", "https://www.postgresql.org/docs/current/sql.html", r'''
Basic Syntax§SELECT name, age FROM users WHERE age > 18 ORDER BY name LIMIT 10;§SELECT cols FROM table WHERE cond§Reading rows§Basics
Comments§-- single line¶/* block */§-- comment§Writing comments in SQL§Basics
Data Types§CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, born DATE, active BOOLEAN DEFAULT TRUE, bio TEXT);§CREATE TABLE t (col TYPE)§Defining tables§Variables & Types
Insert, Update, Delete§INSERT INTO users (name) VALUES ('Ada');¶UPDATE users SET name = 'Bob' WHERE id = 1;¶DELETE FROM users WHERE id = 1;§INSERT / UPDATE / DELETE§Changing data§CRUD
Conditional Statements§SELECT name, CASE WHEN age >= 18 THEN 'adult' ELSE 'minor' END AS grp FROM users;§CASE WHEN cond THEN a ELSE b END§Conditional logic§Decisions
Joins§SELECT u.name, o.total FROM users u INNER JOIN orders o ON o.user_id = u.id;¶LEFT JOIN / RIGHT JOIN / FULL JOIN§JOIN table ON cond§Combining tables§Queries
Aggregation§SELECT dept, COUNT(*) AS n, AVG(salary) FROM staff GROUP BY dept HAVING COUNT(*) > 5;§GROUP BY / HAVING§Summaries§Queries
Subqueries§SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE total > 100);§WHERE col IN (SELECT ...)§Nested queries§Queries
CTEs§WITH recent AS (SELECT * FROM orders WHERE created > NOW() - INTERVAL '7 days')¶SELECT COUNT(*) FROM recent;§WITH name AS (SELECT ...)§Common table expressions§Queries
Window Functions§SELECT name, salary, RANK() OVER (PARTITION BY dept ORDER BY salary DESC) FROM staff;§fn() OVER (PARTITION BY ... ORDER BY ...)§Ranking and running totals§Queries
Loops§-- T-SQL¶DECLARE @i INT = 0;¶WHILE @i < 5 BEGIN SET @i += 1; END;§WHILE cond BEGIN ... END§Procedural loops (T-SQL / PL)§Loops
Views§CREATE VIEW active_users AS SELECT * FROM users WHERE active;§CREATE VIEW v AS SELECT§Saved queries§Objects
Indexes§CREATE INDEX idx_users_name ON users (name);§CREATE INDEX name ON t (col)§Speed up lookups§Performance
Transactions§BEGIN;¶UPDATE acct SET bal = bal - 10 WHERE id = 1;¶UPDATE acct SET bal = bal + 10 WHERE id = 2;¶COMMIT;§BEGIN; ... COMMIT / ROLLBACK;§Atomic changes§Transactions
Stored Procedures§CREATE PROCEDURE add_user(IN n VARCHAR(100)) BEGIN INSERT INTO users (name) VALUES (n); END;§CREATE PROCEDURE name(params)§Reusable server-side logic§Functions
Error Handling§-- T-SQL¶BEGIN TRY SELECT 1/0; END TRY BEGIN CATCH SELECT ERROR_MESSAGE(); END CATCH;§TRY ... CATCH§Handle errors in procedures§Error Handling
Pagination Template§SELECT * FROM items ORDER BY id LIMIT 20 OFFSET 40;¶-- keyset: WHERE id > :last ORDER BY id LIMIT 20§LIMIT n OFFSET m§Popular template: paging§Templates
Upsert Template§INSERT INTO kv (k, v) VALUES ('a', 1) ON CONFLICT (k) DO UPDATE SET v = EXCLUDED.v;¶-- MySQL: ON DUPLICATE KEY UPDATE§INSERT ... ON CONFLICT§Popular template: insert or update§Templates
''')

lang("bash", "Bash", 1989, "Very High", "https://www.gnu.org/software/bash/manual/bash.html", r'''
Basic Syntax§#!/usr/bin/env bash¶echo "Hello World!"§#!/usr/bin/env bash
Comments§# comment§# text§Writing comments in Bash§Basics
Variables§name="Ada"¶echo "Hi $name ${name^^}"¶readonly PI=3.14¶export PATH="$PATH:/opt/bin"§name=value; $name
Strings§s="hello"¶echo ${#s} ${s:1:3} ${s/l/L}¶printf '%s-%d\n' "$s" 5§${var:off:len} ${var/a/b}
Conditional Statements§if [[ $x -gt 5 ]]; then echo big; elif [[ $x -eq 5 ]]; then echo five; else echo small; fi§if [[ cond ]]; then ...; fi
Switch / Match§case "$cmd" in¶  go) run ;;¶  stop) halt ;;¶  *) idle ;;¶esac§case $v in pat) ...;; esac
Loops§for i in 1 2 3; do echo "$i"; done¶for ((i=0;i<5;i++)); do echo "$i"; done¶for f in *.txt; do echo "$f"; done§for x in list; do ...; done
While Loops§n=3¶while [[ $n -gt 0 ]]; do ((n--)); done¶while read -r line; do echo "$line"; done < a.txt§while cond; do ...; done
Functions§greet() { local who="${1:-you}"; echo "Hello, $who!"; }¶greet Ada§name() { ...; }
Arrays§xs=(3 1 2)¶xs+=(4)¶echo "${xs[@]}" ${#xs[@]}§arr=(a b c)
Associative Arrays§declare -A m=([a]=1 [b]=2)¶m[c]=3¶for k in "${!m[@]}"; do echo "$k=${m[$k]}"; done§declare -A name
Error Handling§set -euo pipefail¶trap 'echo failed >&2' ERR¶command || echo "failed"§set -e / trap
File I/O§cat a.txt > b.txt¶echo "more" >> b.txt¶grep -n foo *.log | sort | uniq -c§> >> | redirection and pipes
Modules & Imports§source ./lib.sh¶. ./lib.sh§source file
Concurrency§long_task &¶pid=$!¶wait "$pid"¶xargs -P4 -n1 process < list.txt§cmd & ; wait
Argument Parsing Template§while getopts "n:v" opt; do case $opt in n) name=$OPTARG ;; v) verbose=1 ;; esac; done§getopts
Script Template§#!/usr/bin/env bash¶set -euo pipefail¶main() { echo "run"; }¶main "$@"§set -euo pipefail; main "$@"
Cron Template§# m h dom mon dow command¶0 2 * * * /opt/backup.sh >> /var/log/backup.log 2>&1§crontab -e
''')

lang("powershell", "PowerShell", 2006, "High", "https://learn.microsoft.com/en-us/powershell/scripting/", r'''
Basic Syntax§Write-Host "Hello World!"§Write-Host "text"
Comments§# single line¶<# block #>§# comment
Variables§$name = "Ada"¶$n = 5¶[int]$count = 10¶$env:PATH§$name = value
Strings§$s = "Hi $name $($n + 1)"¶$s.ToUpper(); $s -split ","; $s.Substring(1, 2)§"text $var"
Conditional Statements§if ($x -gt 5) { "big" } elseif ($x -eq 5) { "five" } else { "small" }§if (cond) {} elseif {} else {}
Switch / Match§switch ($cmd) { "go" { "run" } "stop" { "halt" } default { "idle" } }§switch ($v) { pat { } }
Loops§for ($i = 0; $i -lt 5; $i++) { $i }¶foreach ($f in Get-ChildItem) { $f.Name }¶1..5 | ForEach-Object { $_ * 2 }§for / foreach / ForEach-Object
While Loops§$n = 3¶while ($n -gt 0) { $n-- }¶do { $n++ } while ($n -lt 3)§while (cond) {}
Functions§function Get-Greeting { param([string]$Name = "you") "Hello, $Name!" }¶Get-Greeting -Name Ada§function Verb-Noun { param() }
Pipeline§Get-Process | Where-Object CPU -gt 100 | Sort-Object CPU -Descending | Select-Object -First 5§cmd | Where-Object | Select-Object
Arrays & Hashtables§$xs = @(3, 1, 2); $xs += 4¶$m = @{ a = 1; b = 2 }; $m["c"] = 3¶$m.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }§@() / @{}
Classes§class Person { [string]$Name; Person([string]$n) { $this.Name = $n }; [string] Hi() { return $this.Name } }¶[Person]::new("Ada").Hi()§class Name {}
Error Handling§try { Get-Item "missing" -ErrorAction Stop } catch { Write-Error $_.Exception.Message } finally { "done" }§try {} catch {} finally {}
File I/O§$t = Get-Content a.txt -Raw¶Set-Content b.txt $t¶Add-Content b.txt "more"¶Import-Csv data.csv | Export-Json§Get-Content / Set-Content
Modules & Imports§Import-Module Az¶Install-Module Pester -Scope CurrentUser¶. ./lib.ps1§Import-Module Name
Concurrency§Start-Job { Get-Date } | Receive-Job -Wait¶1..5 | ForEach-Object -Parallel { $_ * 2 } -ThrottleLimit 3§Start-Job / ForEach-Object -Parallel
REST API Call Template§$r = Invoke-RestMethod -Uri "https://api.example.com/items" -Headers @{ Authorization = "Bearer $token" }¶$r | ConvertTo-Json§Invoke-RestMethod -Uri url
Script Template§[CmdletBinding()]¶param([Parameter(Mandatory)][string]$Path)¶$ErrorActionPreference = "Stop"¶Write-Verbose "Running on $Path"§[CmdletBinding()] param()
Unit Test Template§Describe "Add" { It "adds" { (1 + 2) | Should -Be 3 } }§Invoke-Pester
''')
