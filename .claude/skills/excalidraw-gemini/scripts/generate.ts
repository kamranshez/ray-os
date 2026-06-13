#!/usr/bin/env npx ts-node
/**
 * Generate excalidraw-style explanation images using Gemini API.
 * Supports parallel generation with timeout.
 */

import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const MODEL_NAME = "gemini-3-pro-image-preview";

const DEFAULT_SYSTEM_PROMPT = `Generate an Excalidraw-style explanation image matching the reference images. This is for visual explanations that teach concepts clearly.

IMPORTANT: Use the EXACT cute light blue robot character shown in the reference images for any people, avatars, or characters. Copy the robot design directly from the references - it's a friendly light blue robot with a rounded head, glowing blue eyes, and a small screen on its chest.

Match the Excalidraw aesthetic from the references: DARK MODE — a near-black charcoal background (#0E1116), chalk-style off-white hand-drawn sketch lines, soft glowing accent color palette, light annotations and labels, arrows showing flow. Use split comparison layouts when appropriate.`;

const SCRIPT_DIR = path.dirname(__filename);
const SKILL_DIR = path.dirname(SCRIPT_DIR);
const ASSETS_DIR = path.join(SKILL_DIR, "assets");
const ENV_FILE = path.join(SKILL_DIR, ".env");

// Load .env file
function loadEnv() {
  if (fs.existsSync(ENV_FILE)) {
    const content = fs.readFileSync(ENV_FILE, "utf-8");
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

function getDefaultReferences(): string[] {
  const files = fs.readdirSync(ASSETS_DIR);
  return files
    .filter((f) => f.startsWith("reference") && f.endsWith(".png"))
    .sort()
    .map((f) => path.join(ASSETS_DIR, f));
}

function findNextAvailableIndex(outputDir: string, basename: string): number {
  // Find the highest existing <basename>-N.png and return N+1
  if (!fs.existsSync(outputDir)) {
    return 1;
  }
  const escaped = basename.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(`^${escaped}-(\\d+)\\.png$`);
  const files = fs.readdirSync(outputDir);
  let maxIndex = 0;
  for (const file of files) {
    const match = file.match(re);
    if (match) {
      const index = parseInt(match[1], 10);
      if (index > maxIndex) {
        maxIndex = index;
      }
    }
  }
  return maxIndex + 1;
}

async function generateSingleImage(
  genai: GoogleGenAI,
  prompt: string,
  referenceImages: { data: string; mimeType: string }[],
  index: number,
  aspectRatio: string = "16:9",
  imageSize: string = "2K"
): Promise<{ index: number; image?: Buffer; error?: string }> {
  try {
    const parts: Array<{ text: string } | { inlineData: { data: string; mimeType: string } }> = [
      { text: prompt },
    ];

    for (const img of referenceImages) {
      parts.push({
        inlineData: {
          data: img.data,
          mimeType: img.mimeType,
        },
      });
    }

    const response = await genai.models.generateContent({
      model: MODEL_NAME,
      contents: [
        {
          role: "user",
          parts,
        },
      ],
      config: {
        responseModalities: ["TEXT", "IMAGE"],
        imageConfig: {
          aspectRatio,
          imageSize,
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

  // Parse arguments
  let prompt = "";
  let count = 5;
  let outputDir = "./generated";
  let timeout = 180;
  let apiKey = process.env.GEMINI_API_KEY || "";
  let customRefs: string[] = [];
  let systemPrompt = DEFAULT_SYSTEM_PROMPT;
  let aspectRatio = "16:9";
  let imageSize = "2K";
  let basename = "excalidraw";

  const VALID_ASPECT_RATIOS = ["21:9", "16:9", "4:3", "3:2", "1:1", "9:16", "3:4", "2:3", "5:4", "4:5"];

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
    } else if (arg === "--aspect-ratio" || arg === "-a") {
      aspectRatio = args[++i];
      if (!VALID_ASPECT_RATIOS.includes(aspectRatio)) {
        console.error(`Error: Invalid aspect ratio "${aspectRatio}". Supported: ${VALID_ASPECT_RATIOS.join(", ")}`);
        process.exit(1);
      }
    } else if (arg === "--image-size") {
      imageSize = args[++i];
    } else if (arg === "-x" || arg === "--name") {
      basename = args[++i];
    } else if (!arg.startsWith("-")) {
      prompt = arg;
    }
  }

  if (!apiKey) {
    console.error("Error: Gemini API key required. Set GEMINI_API_KEY or use --api-key");
    process.exit(1);
  }

  if (!prompt) {
    console.error("Usage: generate.ts <prompt> [-n count] [-o output] [-t timeout] [-r reference]");
    process.exit(1);
  }

  // Load reference images
  const refPaths = customRefs.length > 0 ? customRefs : getDefaultReferences();
  if (refPaths.length === 0) {
    console.error("Error: No reference images found");
    process.exit(1);
  }

  console.log(`Loading ${refPaths.length} reference image(s)...`);
  const referenceImages: { data: string; mimeType: string }[] = [];
  for (const refPath of refPaths) {
    if (!fs.existsSync(refPath)) {
      console.warn(`Warning: Reference image not found: ${refPath}`);
      continue;
    }
    const img = loadImageAsBase64(refPath);
    referenceImages.push(img);
    console.log(`  Loaded: ${path.basename(refPath)}`);
  }

  if (referenceImages.length === 0) {
    console.error("Error: No valid reference images loaded");
    process.exit(1);
  }

  // Create output directory
  fs.mkdirSync(outputDir, { recursive: true });

  // Build full prompt
  const fullPrompt = `${systemPrompt}\n\nContent to visualize:\n${prompt}`;

  // Find starting index to avoid overwrites
  const startIndex = findNextAvailableIndex(outputDir, basename);
  if (startIndex > 1) {
    console.log(`Found existing images, starting at index ${startIndex}`);
  }

  console.log(`\nGenerating ${count} image(s)...`);
  console.log(`Timeout: ${timeout}s per image`);

  const genai = new GoogleGenAI({ apiKey });

  // Generate images with staggered concurrency (max 2 at a time, 3s delay between launches)
  const CONCURRENCY = 2;
  const STAGGER_MS = 3000;
  const results: Awaited<ReturnType<typeof generateSingleImage>>[] = [];

  for (let batch = 0; batch < count; batch += CONCURRENCY) {
    const batchPromises = [];
    for (let j = 0; j < CONCURRENCY && batch + j < count; j++) {
      const i = batch + j;
      if (j > 0) await new Promise(r => setTimeout(r, STAGGER_MS));
      batchPromises.push(
        Promise.race([
          generateSingleImage(genai, fullPrompt, referenceImages, i, aspectRatio, imageSize),
          new Promise<{ index: number; error: string }>((resolve) =>
            setTimeout(() => resolve({ index: i, error: `Timeout after ${timeout}s` }), timeout * 1000)
          ),
        ])
      );
    }
    results.push(...await Promise.all(batchPromises));
    if (batch + CONCURRENCY < count) await new Promise(r => setTimeout(r, STAGGER_MS));
  }
  results.sort((a, b) => a.index - b.index);

  // Save results with non-conflicting filenames
  let successCount = 0;
  for (const result of results) {
    if ("image" in result && result.image) {
      const fileIndex = startIndex + result.index;
      const outputPath = path.join(outputDir, `${basename}-${fileIndex}.png`);
      fs.writeFileSync(outputPath, result.image);
      console.log(`  Saved: ${outputPath}`);
      successCount++;
    } else {
      console.log(`  Failed image ${result.index + 1}: ${result.error}`);
    }
  }

  console.log(`\nGenerated ${successCount}/${count} images in ${outputDir}`);

  if (successCount === 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
