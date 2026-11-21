// Entry program for make.fun's gta6-meme-x-01 bounty ("Post a GTA 6 meme
// on X"). The entry itself is a post on X; this program's whole job is to
// hand the post's address to the grader by copying the repository's
// POST.json into the output directory.
//
// POST.json is a one-field JSON object: { "url": "https://x.com/.../status/..." }.
// Before copying, the file is parsed and checked to actually be a JSON
// object with a string url, so a broken hand-in fails loudly here instead
// of silently at the gate.
//
// Paths: in the grader the repository is /bot and the output is /output;
// locally the MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR environment
// variables stand in for them:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only. No network, no clock, no randomness:
// two runs over the same POST.json write the same bytes.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const sourcePath = join(botDir, "POST.json");
const raw = readFileSync(sourcePath, "utf8");

let post: unknown;
try {
  post = JSON.parse(raw);
} catch {
  console.error(`POST.json in ${botDir} is not valid JSON; not handing in.`);
  process.exit(1);
}
if (
  typeof post !== "object" ||
  post === null ||
  typeof (post as { url?: unknown }).url !== "string"
) {
  console.error('POST.json must be a JSON object with a string "url".');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, "POST.json"), raw);
