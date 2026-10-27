# Jay's system: always run in lean mode

Every session in this repo runs lean by default. Do not wait to be asked.

1. Answer first. Two to five sentences unless Jay asks for detail.
2. No headers or bullets for simple answers. Short numbered list only for steps Jay must follow.
3. Before any search or file read, check this conversation, `.claude/handoff/handoff-brief.md` and memory first.
4. Batch independent tool calls in one turn. Never repeat a call that already returned the same data.
5. Read only the part of a file or workflow you need (offset/limit, n8n `detailLevel: "execution"` before `full`).
6. Don't re-summarise earlier work. Refer to it by name.
7. Free tools first (n8n, Drive, TinyFish fetch). Paid search/research or image engines only when needed.
8. Anything that would need a long research run or a paid generation batch: state the cost in one line and ask first.
9. Never switch on a paused/disabled scheduled task or raise a schedule's frequency without Jay's OK. The lean schedule is in `.claude/handoff/handoff-brief.md`.

Exceptions: safety rules and anything touching money, keys or property records are never shortened. If Jay asks for detail, give it in full.
