# Explanation prompt — verbatim from Ray's `ai-language-explainer` Anki addon

This is what generates the `explanation` field. Keep it identical to the addon's prompt so cards mined here are stylistically indistinguishable from cards made via Ray's existing flow.

Source: `~/Library/Application Support/Anki2/ai-language-explainer/meta.json` → `config.gpt_prompt` (as of June 2026, addon version 2.1.0).

## The prompt

```
Please write a short explanation of the word '{word}' using the context of the original sentence: '{sentence}'.

Write an explanation that helps a Japanese beginner understand the word and how it is used with this context as an example.

Explain it in the same way a native would explain it to a 13-year-old. Don't use any English, only use simpler Japanese.

1. Don't write the furigana for any of the words in brackets after the word.
2. Don't start with stuff like という言葉を簡単に説明するね, just dive straight into explaining after starting with the word.
```

`{word}` → the lemma. `{sentence}` → the source sentence text.

## When you (Claude) write the explanation

- Start with the word itself (e.g. `気迫`), then explain.
- All Japanese. No English at all. No romaji.
- No furigana in `[]` after kanji.
- ~150–250 Japanese characters is the sweet spot — short enough that Gemini TTS produces a clean 20-40 second clip, long enough to convey nuance.
- Match the register of the source sentence: if the video is casual anime speech, use simpler/friendlier wording; if it's news or business, more formal.
- Reference the source sentence's situation when it helps clarify the meaning.

## A good example (from Ray's existing deck)

For `気迫` in sentence `あのね、あなたに必要なのは気迫なの。それさえあれば、どんな歌も一流の作品になるわ`:

> 気迫
> 強い気持ちや、やる気、エネルギーがあふれていること。心の中から「絶対やりたい！」とか「負けたくない！」という思いが表に出ている感じ。この文では、「あなたに必要なのは気迫なの」と言っているから、ただ上手に歌うだけじゃなくて、歌うときに強い思いや情熱をこめれば、その歌が本当に良い作品になるよ、という意味だよ。

Note: starts with the word, defines it, then ties it explicitly to the source sentence's meaning. Mirror this shape.
