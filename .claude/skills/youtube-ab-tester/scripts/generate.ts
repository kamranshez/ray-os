#!/usr/bin/env npx ts-node
/**
 * Generate YouTube thumbnails using gemini-3-pro-image-preview at 2K.
 * Loads face reference images automatically for consistent likeness.
 * Supports additional reference images (competitor thumbnails, style refs).
 */

import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const DEFAULT_MODEL = "gemini-3.1-flash-image-preview";
const DEFAULT_IMAGE_SIZE = "1K";

const DEFAULT_SYSTEM_PROMPT = `Generate a high-quality YouTube thumbnail image.

CRITICAL REQUIREMENTS:
- The thumbnail must be visually striking and scroll-stopping
- Use HIGH CONTRAST colors that pop — YouTube thumbnails are viewed at small sizes on mobile
- Keep the composition SIMPLE with 1-2 clear focal points
- Any text must be LARGE, BOLD, and instantly readable at small sizes (use thick sans-serif fonts)
- If a person is featured, their face should show a clear, exaggerated EMOTION (the #1 click driver)
- The person in the thumbnail MUST match the face reference photos provided — preserve their exact likeness, face shape, skin tone, and features
- The overall design should create a CURIOSITY GAP that makes viewers want to click

Style notes:
- Professional YouTube thumbnail quality (think MrBeast, Veritasium, MKBHD level)
- Clean, uncluttered — works at 120px wide on a phone screen
- Bold color blocking, dramatic lighting
- No watermarks, no channel logos unless specifically requested`;

const SCRIPT_DIR = path.dirname(__filename);
const SKILL_DIR = path.dirname(SCRIPT_DIR);
const FACE_DIR = path.join(SKILL_DIR, "references", "rays-face");
const ENV_FILE = path.join(SKILL_DIR, ".env");

// Also check project root .env
const PROJECT_ENV = path.join(SKILL_DIR, "..", "..", "..", ".env");

function loadEnv() {
  for (const envPath of [ENV_FILE, PROJECT_ENV]) {
    if (fs.existsSync(envPath)) {
      const content = fs.readFileSync(envPath, "utf-8");
      for (const line of content.split("\n")) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith("#") && trimmed.includes("=")) {
          const [key, ...valueParts] = trimmed.split("=");
          const value = valueParts.join("=").trim().replace(/^["']|["']$/g, "");
          if (!process.env[key.trim()]) {
            process.env[key.trim()] = value;
          }
        }
      }
    }
  }
}

function loadImageAsBase64(imagePath: string): { data: string; mimeType: string } {
  const ext = path.extname(imagePath).toLowerCase();
  const mimeTypes: Record<string, string> = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
  };
  const mimeType = mimeTypes[ext] || "image/png";
  const data = fs.readFileSync(imagePath).toString("base64");
  return { data, mimeType };
}

function loadFaceReferences(overridePath?: string): { data: string; mimeType: string }[] {
  if (overridePath) {
    if (!fs.existsSync(overridePath)) {
      console.warn(`Warning: Face override not found: ${overridePath}`);
      return [];
    }
    console.log(`  Face: ${path.basename(overridePath)} (override)`);
    return [loadImageAsBase64(overridePath)];
  }
  const candidates = ["go-to-face.png", "go-to-face.jpg"];
  for (const filename of candidates) {
    const candidatePath = path.join(FACE_DIR, filename);
    if (fs.existsSync(candidatePath)) {
      console.log(`  Face: ${filename}`);
      return [loadImageAsBase64(candidatePath)];
    }
  }
  console.warn(`Warning: no face reference found in ${FACE_DIR} (looked for ${candidates.join(", ")}).`);
  return [];
}

function findNextAvailableIndex(outputDir: string): number {
  if (!fs.existsSync(outputDir)) return 1;
  const files = fs.readdirSync(outputDir);
  let maxIndex = 0;
  for (const file of files) {
    const match = file.match(/^thumbnail_(\d+)\.png$/);
    if (match) {
      const index = parseInt(match[1], 10);
      if (index > maxIndex) maxIndex = index;
    }
  }
  return maxIndex + 1;
}

async function generateSingleThumbnail(
  genai: GoogleGenAI,
  prompt: string,
  faceRefs: { data: string; mimeType: string }[],
  extraRefs: { data: string; mimeType: string }[],
  index: number,
  modelName: string,
  imageSize: string
): Promise<{ index: number; image?: Buffer; error?: string }> {
  try {
    const parts: Array<
      { text: string } | { inlineData: { data: string; mimeType: string } }
    > = [{ text: prompt }];

    // Add face references first (character consistency)
    for (const img of faceRefs) {
      parts.push({ inlineData: { data: img.data, mimeType: img.mimeType } });
    }

    // Add extra references (competitor thumbnails, style refs)
    for (const img of extraRefs) {
      parts.push({ inlineData: { data: img.data, mimeType: img.mimeType } });
    }

    const response = await genai.models.generateContent({
      model: modelName,
      contents: [{ role: "user", parts }],
      config: {
        responseModalities: ["TEXT", "IMAGE"],
        imageConfig: {
          aspectRatio: "16:9",
          imageSize: imageSize,
        },
      } as any,
    });

    const candidate = response.candidates?.[0];
    if (!candidate?.content?.parts) {
      return { index, error: "No response from model" };
    }

    for (const part of candidate.content.parts) {
      if (part.inlineData?.data) {
        return {
          index,
          image: Buffer.from(part.inlineData.data, "base64"),
        };
      }
    }

    return { index, error: "No image in response" };
  } catch (error) {
    return {
      index,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

async function main() {
  loadEnv();

  const args = process.argv.slice(2);

  let prompt = "";
  let count = 5;
  let outputDir = "./generated";
  let timeout = 180;
  let apiKey = process.env.GEMINI_API_KEY || "";
  let customRefs: string[] = [];
  let systemPrompt = DEFAULT_SYSTEM_PROMPT;
  let noFace = false;
  let thumbnailText = "";
  let cloneSrc = "";
  let outputName = "";
  let modelName = DEFAULT_MODEL;
  let imageSize = DEFAULT_IMAGE_SIZE;
  let faceOverride = "";

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "-n" || arg === "--count") {
      count = parseInt(args[++i], 10);
    } else if (arg === "-o" || arg === "--output") {
      outputDir = args[++i];
    } else if (arg === "-t" || arg === "--timeout") {
      timeout = parseInt(args[++i], 10);
    } else if (arg === "-r" || arg === "--reference") {
      customRefs.push(args[++i]);
    } else if (arg === "--api-key") {
      apiKey = args[++i];
    } else if (arg === "--system-prompt") {
      systemPrompt = args[++i];
    } else if (arg === "--no-face") {
      noFace = true;
    } else if (arg === "--text") {
      thumbnailText = args[++i];
    } else if (arg === "--clone") {
      cloneSrc = args[++i];
    } else if (arg === "--name") {
      outputName = args[++i];
    } else if (arg === "--model") {
      modelName = args[++i];
    } else if (arg === "--image-size") {
      imageSize = args[++i];
    } else if (arg === "--face") {
      faceOverride = args[++i];
    } else if (!arg.startsWith("-")) {
      prompt = arg;
    }
  }

  if (!apiKey) {
    console.error("Error: GEMINI_API_KEY required. Set in .env or use --api-key");
    process.exit(1);
  }

  // Clone mode: use an existing thumbnail as reference, auto-construct prompt
  if (cloneSrc) {
    if (!fs.existsSync(cloneSrc)) {
      console.error(`Error: Clone source not found: ${cloneSrc}`);
      process.exit(1);
    }
    // Add the clone source as a reference
    customRefs.unshift(cloneSrc);
    // If no explicit prompt, auto-construct one for clone mode
    if (!prompt) {
      if (!thumbnailText) {
        console.error("Error: --clone requires --text to specify the new text");
        process.exit(1);
      }
      prompt = `Recreate this exact thumbnail with the same composition, layout, colors, person position, expression, and style — but change the text to read '${thumbnailText}'. Keep everything else identical to the reference image. The text '${thumbnailText}' must be spelled exactly as shown (one word, no spaces unless explicitly included).`;
    }
    console.log(`Clone mode: using ${path.basename(cloneSrc)} as source`);
  }

  if (!prompt) {
    console.error(
      "Usage: generate.ts <prompt> [-n count] [-o output] [-r reference] [--text TEXT] [--no-face] [--clone SRC] [--name FILENAME]"
    );
    process.exit(1);
  }

  // Load face references
  const faceRefs = noFace ? [] : loadFaceReferences(faceOverride || undefined);

  // Load extra references (competitor thumbnails etc.)
  const extraRefs: { data: string; mimeType: string }[] = [];
  for (const refPath of customRefs) {
    if (!fs.existsSync(refPath)) {
      console.warn(`Warning: Reference not found: ${refPath}`);
      continue;
    }
    const img = loadImageAsBase64(refPath);
    extraRefs.push(img);
    console.log(`  Reference: ${path.basename(refPath)}`);
  }

  // Total references check (Nano Banana 2 supports up to 14)
  const totalRefs = faceRefs.length + extraRefs.length;
  if (totalRefs > 14) {
    console.warn(
      `Warning: ${totalRefs} references exceeds Nano Banana 2's 14-image limit. Using first 14.`
    );
  }

  // Create output directory
  fs.mkdirSync(outputDir, { recursive: true });

  // Build full prompt
  let fullPrompt = systemPrompt + "\n\n";
  if (faceRefs.length > 0) {
    fullPrompt += `The first ${faceRefs.length} reference image(s) show the person who MUST appear in the thumbnail. Match their face exactly.\n\n`;
  }
  if (extraRefs.length > 0) {
    fullPrompt += `Additional reference images are provided as style/composition inspiration. Draw from their visual approach but create something original.\n\n`;
  }
  if (thumbnailText) {
    fullPrompt += `CRITICAL TEXT REQUIREMENT: The thumbnail MUST include the text "${thumbnailText}" rendered in large, bold, highly readable letters. Spell it EXACTLY as shown: "${thumbnailText}" — do not add spaces, split words, or alter the spelling in any way.\n\n`;
  }
  fullPrompt += `Thumbnail concept:\n${prompt}`;

  const startIndex = findNextAvailableIndex(outputDir);
  if (startIndex > 1) {
    console.log(`Found existing images, starting at index ${startIndex}`);
  }

  console.log(`\nGenerating ${count} thumbnail(s)...`);
  console.log(`Model: ${modelName} at ${imageSize}`);
  console.log(`Face refs: ${faceRefs.length}, Extra refs: ${extraRefs.length}`);
  console.log(`Timeout: ${timeout}s per image`);

  const genai = new GoogleGenAI({ apiKey });

  // Generate images in parallel
  const promises = Array.from({ length: count }, (_, i) =>
    Promise.race([
      generateSingleThumbnail(genai, fullPrompt, faceRefs, extraRefs, i, modelName, imageSize),
      new Promise<{ index: number; error: string }>((resolve) =>
        setTimeout(
          () => resolve({ index: i, error: `Timeout after ${timeout}s` }),
          timeout * 1000
        )
      ),
    ])
  );

  const results = await Promise.all(promises);
  results.sort((a, b) => a.index - b.index);

  let successCount = 0;
  for (const result of results) {
    if ("image" in result && result.image) {
      let outputPath: string;
      if (outputName) {
        // Direct naming: use --name for the filename (add suffix for multiple)
        const baseName = outputName.replace(/\.png$/, "");
        const suffix = count > 1 ? `-${result.index + 1}` : "";
        outputPath = path.join(outputDir, `${baseName}${suffix}.png`);
      } else {
        const fileIndex = startIndex + result.index;
        outputPath = path.join(outputDir, `thumbnail_${fileIndex}.png`);
      }
      fs.writeFileSync(outputPath, result.image);
      console.log(`  Saved: ${outputPath}`);
      successCount++;
    } else {
      console.log(`  Failed ${result.index + 1}: ${result.error}`);
    }
  }

  console.log(`\nGenerated ${successCount}/${count} thumbnails in ${outputDir}`);

  if (successCount === 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
