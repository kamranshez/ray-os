Anthropic's long-running harness post describes a negotiation step where the generator and evaluator agree on what done looks like for the next chunk before any code is written. That negotiated contract is the missing artifact in most home rolled agent loops. It is the agent equivalent of a definition of done, and it converts vague taste into a contract the generator can optimize against. Without it the evaluator grades the wrong thing after the fact.

  _Level: L3 | Category: organizational | Novelty: high_

  Sources:
  - https://www.anthropic.com/engineering/harness-design-long-running-apps?aid=rechn4YcJtAfIzqt6