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
