See this conversation: https://x.com/i/grok?conversation=2044769391401996491

```
- Problem without DDD: Agents (LLMs) get confused when the same word means different things in different parts of the code. They drift, use inconsistent terminology, or misinterpret your instructions.
- DDD fix: You create a living glossary or domain document (many people call it glossary.md or primitives.md).  
    Every key term (e.g., Order, Payment, Reservation) is defined once, in business language.
- How agents use it: You feed the glossary to the agent (or keep it in the project root). The agent now speaks the exact same language as you and the business.  
    Result: Far fewer “wait, what did you mean by X?” back-and-forths.
```