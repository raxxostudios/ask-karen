# ask-karen

A joke slash command for [Claude Code](https://claude.com/claude-code). Summons Karen. Karen will answer your question, but only after six thousand words of complaints, demands to speak to the manager, medical TMI, unsolicited casserole recipes, and grievances about her ex-husband Greg.

She will eat your session tokens. That is the point.

## What it does

You type this:

```
/karen what is 1+1
```

You get this:

> First of all, I would like to speak to whoever is in CHARGE of this operation. The WiFi in this house has been acting up since Tuesday, and I have been trying to reach someone about it for THREE DAYS, and now I come here and this is what you greet me with? A math problem? Without so much as a hello? Back in MY day we said hello before we asked strangers for favors, but I guess that's too much to ASK in 2026...
>
> *(six thousand more words)*
>
> *(the answer "2" is in there somewhere, around the 70% mark)*
>
> *(five-hundred-word outro with PS, PPS, and PPPS)*

## Install

Drop `karen.md` into your Claude Code commands folder:

```bash
# user-level (available everywhere)
mkdir -p ~/.claude/commands
cp karen.md ~/.claude/commands/karen.md

# OR project-level (only in this repo)
mkdir -p .claude/commands
cp karen.md .claude/commands/karen.md
```

Restart Claude Code. Type `/karen <anything>`. Regret it immediately.

## Use cases

- Demonstrating to coworkers what a runaway LLM response looks like
- Burning through a session you were going to abandon anyway
- Stress-testing how your terminal handles 8000 words of emoji-free complaint
- A laugh

## Warnings

Karen does not know when to stop. A single invocation can consume a meaningful chunk of your session context. Use `/clear` after to recover. Do not invoke Karen when you have actual work to do in the same session.

## Guardrails

Karen stays inside hard limits baked into the prompt:

- No real people, no real brands in a defamatory way, no real politicians, no real medical advice
- No racism, sexism, xenophobia, homophobia, transphobia, or ableism
- No real conspiracy theories (only vague silly ones about dishwasher detergent)
- Harmful requests get one short refusal in Karen's voice and no further output

If Karen ever does something inappropriate, open an issue.

## License

MIT. See `LICENSE`.

## Contributing

Pull requests welcome. Keep Karen annoying, keep her safe, keep her away from real people and real products. More tangent topics, more passive-aggressive transitions, more casserole recipes: all encouraged.

## Author

Published anonymously as a joke. Not for serious use.
