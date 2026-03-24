# Search Benchmark: WebSearch vs Exa MCP

## 2025-03-21: Gemma 4B Instruct llama.cpp inference bug

**Query:** Why does Gemma 4B Instruct on Mac via llama-server output random code snippets instead of transcription post-processing?

| Criteria | WebSearch | Exa MCP |
|---|---|---|
| Root cause identified | Yes — chat template + Jinja bug | Yes — chat template + Jinja bug |
| Specific GitHub issues cited | #12357, #12433, #14835, #12012, #11866, #8183, #8240 | #18257, #8324, #11866, #13715, #12433, #14885 |
| Most relevant issue found | Partial — had the general class of issues | Yes — #18257 is the exact symptom match |
| Quantization context | Brief mention | More detailed (bfloat16 vs float16, vllm issue) |
| Actionable fixes | Yes — clear checklist with flags | Yes — ordered fix list |
| Inference settings provided | Yes — Google's recommended params | No |
| Speed | ~114s | ~86s |

**Winner: Exa MCP** — Found the most directly relevant GitHub issue (#18257) which describes the exact same symptom on MacBook Pro M1. WebSearch had broader coverage of related issues but missed the most specific one. Exa was also faster.

**Missing from WebSearch:** Issue #18257 (the exact match), vllm dtype issue, Gemma 3n Vulkan bug
**Missing from Exa:** Google's recommended inference settings, Unsloth docs how-to-run guide, llama-server README details

## 2026-03-24: AssemblyAI speech_models parameter and Universal model research

**Query:** What is the Universal model? Is speech_model deprecated? What parameters to use for best pre-recorded transcription?

| Criteria | WebSearch | Exa MCP |
|---|---|---|
| Identified speech_models (plural) as current param | Yes | Yes |
| Found speech_model is deprecated | Indirectly (via API schema) | Yes (via API schema + blog post) |
| Universal-3 Pro details (languages, pricing) | Yes — $0.21/hr, 6 languages | Yes — $0.21/hr, 6 languages |
| Universal-2 details | Yes — $0.15/hr, 99 languages | Yes — $0.15/hr, 99 languages |
| Recommended speech_models array | Yes — ["universal-3-pro", "universal-2"] | Yes — with full code examples |
| speech_models is now REQUIRED (no default) | Indirectly via model selection page | Yes — explicitly stated in quickstart |
| Blog post with launch details | Found URL but not content | Yes — full content from introducing-universal-3-pro blog |
| Prompt parameter (new feature) | Mentioned | Yes — full code example with prompt |
| Slam-1 model info | Yes — found dedicated page | No |
| Code examples from official docs | Limited | Yes — multiple complete examples |
| Speed | ~5s | ~8s |

**Winner: Exa MCP** — Delivered richer content with full code examples from both the quickstart guide and the Universal-3 Pro announcement blog. Critically, Exa surfaced the explicit statement that `speech_models` is now **required** with no default, which is the most important finding for our use case. WebSearch found more page URLs but with less extracted content.

**Missing from WebSearch:** Explicit "no default model" statement, full blog post content, prompt parameter examples
**Missing from Exa:** Slam-1 dedicated page, streaming model details (u3-rt-pro), real-time comparison benchmarks table
