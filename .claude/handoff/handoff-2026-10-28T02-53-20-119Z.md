# Handoff brief

Written 2026-10-28T02:53:20.119Z at 60% context. Session c83bc727-9c59-55a1-8e3a-42c87c33a035. Project /home/user/ajaxace.

## Goal
Jay (Thailand, UTC+7) wants his whole system run lean and finished: Claude scheduled tasks, n8n on his Hostinger server (97 workflows), and uploaded skills. Spelling is locked as MASKA (never Masca), TWIX, JAY; series "Maska & Friends". Repo `ajaxace/ajaxace`; work branch `ccr-7d0361cf-yyrgit`.

## Work in progress
- **PR #1 merged** (commit `ceab2314`) into `claude/hostinger-mcp-servers-8gpvn9`: adds `CLAUDE.md` with lean rules and the MASKA lock.
- **Claude tasks:** Chief of Staff `trig_016k4p8ihmSSNFehpRFDW1KD` model changed Opus to Sonnet by me; its once-daily 09:55 Bangkok schedule and prompt were edited by someone else at 08:06 on 28 Oct. Auditor `trig_01YAFX7mTTg7tsEWkrXK43cX` runs 12:17, model unset (probably Opus). Box reminder `trig_01XRwdrBN6msXvEG4QCddNVd` set to Haiku.
- **Clip desk** `trig_01YCkyY4eYSshXQK952nG4Zx`: new, Haiku, 17:23 Bangkok, **disabled, no connectors**. It books clips from "YES – post it" and edits at most one clip a day (40-credit cap).
- **Restore log:** n8n data table `lean_changes` (`WFDTlzpcChmZ0AXc`, project `vQlqixidnpQyrAdP`), 7 rows with revert methods. Nothing watches it; Jay says "REVERT LEAN" and I undo.
- **Baselines, 27 Oct UTC:** 1,394 n8n executions. Dashboard 296, Health Check 281, Claude to Jarvis 280, Reminders 97, Cheap Brain Router 50, Live Link Guard 24; Discord Reader, Watchdog and Maid Heartbeat 1 each; Search Router, Illustrator Brain, Illustration v1 and Self-Heal 0.
- **Illustration v2** `Ia83OxujMLgX05YU`: live version `1c253831` (old upload code); finished draft `93aa45f2` (upload fix, settings table `GNH89rFUUS1gsqzx`). Jay says FINISHED, and history confirms the last save at 01:45Z and one run since. That run (`107803`) failed the Gate (extra head, TWIX collar missing), about $0.25 per job.
- **Skill fixes:** the file `/tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/skill-fixes.md` holds Fixes 1–6 (backups in `skill-backup`). Sent to Jay; not yet applied.
- **Masca scan (subagent, counts estimated):** about 33 matches in 8 workflows: Studio `phdC131RSbK7RWgv`, Writer `VuyhrpSbs5xs00r4`, Reviewer `VJVJ6h0DPmU61UV0`, v2, Gate `1pHxxsjf5JvMO0BG`, old 12-illustrator `4o7a75diSHUoAIum`, Brain `BP5bCbJyoEK7hJb9`, Dashboard `C2UonLGLmM5DPCs1`.

## Decisions made
- MASKA final; the Drive folder is already "Maska & Friends".
- The 72-hour clock starts only after the Clip desk has run once and no one else is editing.
- Brain Log dropped; the Private Queue test worked (job `Pmvrhjkn99t0`, row appeared).
- Keep "LEAN:" lines in every task prompt until a test proves skills reach scheduled tasks.
- No comment replier built.
- Fix 6 (`explain-usage` link) is required. Don't touch "twix n masca files book".
- Proposed MASKA change set: change display text, add `maska` beside `masca`, leave keys and slugs, change the Gate allow-list last.

## Assumptions to verify
- The other n8n editor is Jay's Cowork or desktop chat (none of his cloud sessions touched v2).
- Clip desk steps are my design; the original Editor and Publisher prompts weren't found.
- Skills load in scheduled tasks (untested).
- The Auditor default model is Opus.

## Dead ends (do not retry)
- `create_trigger` can't attach connectors; it needs the claude.ai UI.
- Blotato can't read TikTok comments; Instagram BOOK comments are handled by Blotato DM automation `19454`.
- `get_trigger` returned not found for the old Post Performance and Inspection tasks.
- Restoring v2 by version would wipe the other editor's work.
- `get_workflow_execution` with data and no node filter returns megabytes.

## Last request and whether it was answered
Jay asked for this brief. Before it, the Masca scan report was relayed and summarised. Awaiting his replies on the open items below.

## Next step
1. Get Jay's answers: "go MASKA fixes", "publish v2" (revert: republish `1c253831`), "Auditor to Sonnet".
2. Confirm he pasted the Cowork steps (Clip desk connectors then enable, Chief of Staff connectors cut to 8, skill fixes).
3. After the Clip desk has run once, start the 72-hour clock, then slow Health Check `nREyDHXe3L9JilLV` from 5 to 15 minutes, logging each change in `lean_changes`.

## Files changed this session
- /home/user/ajaxace/CLAUDE.md
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/skill-fixes.md

## Last user message (verbatim, cut at 1500 characters)
FINISHED. I’m making no further changes to it.

I made no edits in this session. The workflow’s history shows its last saved edit at 08:45 Thailand time today, which rewired the new reference-image setting nodes. A manual run right after that edit succeeded, and nothing has changed since.
