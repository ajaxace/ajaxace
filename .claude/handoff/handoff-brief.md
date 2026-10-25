# Handoff brief

Written 2026-10-25T00:20:05.554Z at 61% context. Session c83bc727-9c59-55a1-8e3a-42c87c33a035. Project /home/user/ajaxace.

## Goal
Run Jay's system (n8n workflows plus Claude scheduled tasks) lean on Claude credits while it keeps working. Grow TikTok/Instagram @ajaxace1894. Push the Maska & Friends kids' books, including the "Maska & Twix Meet…" range for children with conditions and their families, out to publishers and charities. Keep a ruthless quality-control layer over every department.

## Work in progress
- **Lean mode n8n changes (all live):**
  - Claude to Jarvis: hourly.
  - Illustrator Brain: 08:00 and 20:00.
  - Flight Watch: Tue and Fri 08:00, timezone set to Bangkok.
  - Publisher Intake: 06:00. Writer: 06:30 and 18:30. Reviewer: 07:30 and 19:30.
  - Self-Heal: 07:00.
  - W5 Maid summary: Telegram only when not GREEN/OK.
  - Research HQ Watchman: Sun, Mon, Wed, Fri.
  - Deal Check: Friday only.
  - Maska & Twix Bot: errorWorkflow set to Instant Error Alert.
  - Report doc: 1WwidhdXu92O-VFp_5g2E-SclK2ZxLewLHkE9bM8JHgM. Pre-change JSON snapshots are in the scratchpad.
- **Claude tasks:**
  - Paused: Research deep dive, Book Research Packs, Watchdog, Skill Scout, Comment Engine, Storeroom Sorter.
  - Switched off: hourly Maska bot builder.
  - Publisher now 20:33 only. Inspection now 09:41 only.
  - Re-enabled on 25 Oct (both had been off since 20/21 Oct): Post Performance Watch (trig_01D1pfteb72bmL5tPJVD6cKP) and Inspection (trig_01XPakrxxmz3BBomHzRm9hLu).
- **Chief of Staff** (trig_016k4p8ihmSSNFehpRFDW1KD): rewritten as a quality controller. Runs 08:47, 14:47 and 20:47 Bangkok. At 14:47 he must act on the Auditor's block first.
- **Auditor** (trig_01YAFX7mTTg7tsEWkrXK43cX): runs 12:17 Bangkok and grades the Chief. **Has no connectors.** Jay must add Zapier, Google Drive, Google Docs, n8n, Blotato and Claude Code Remote in the claude.ai Scheduled tasks UI.
- **Publisher pitch deck:** https://claude.ai/artifact/7kTnfgipZAMLUZ1vbmZTVV, 10 slides, local root scratchpad/deck. Numbers are filled in. Author name is still to be chosen: "Ajax" or "Jay Clayton".

## Decisions made
Jay approved all of the following:
- Reminders, both Email Filing workflows, Free Book Machine sweep and Storeroom Mover keep their current frequency.
- Lean cuts as listed above.
- Keep the daily routine reminder, Inspection and Post Performance Watch running.
- Chief of Staff at 3 runs a day, plus one Auditor at lunchtime.
- The deck pitches the books as Jay's text paired with a publisher's human illustrator, and is honest about current AI-made editions.
- Maverick Children's Books is the first submission target.

## Assumptions to verify
- Whether the n8n instance timezone is Bangkok. This was inferred from Morning Briefing running at 00:00 UTC.
- Who disabled Post Performance Watch and Inspection on 21 Oct, and whether that was deliberate.
- Follower counts (4,705 TikTok, 241 Instagram) date from 20 Oct.
- The Google Docs credential error seen on 21 Oct in Free Book Machine may recur.
- More scheduled tasks may exist beyond the pages already read.

## Dead ends (do not retry)
- create_trigger with the connectors parameter: not available for this org.
- Blotato returns no TikTok analytics or comments.
- First update_trigger attempt was blocked by the classifier. It later succeeded after Jay's explicit OK.

## Last request and whether it was answered
"let's go". Answered:
- Re-enabled the two jobs that had been switched off.
- Filled the deck numbers.
- Told Jay that 10,000 followers by 31 Oct is unreachable, that the sign-up funnel is slow (7 real sign-ups, none since 21 Oct), and to price the leads now: 2 want print, 3 want the book club.

## Next step
1. Confirm Jay has added the Auditor's connectors.
2. Check today's 08:47 Chief of Staff run, 09:14 Post Performance Watch and 09:41 Inspection runs, and the log doc 1cLyePU4KzNsJYXkxBhK7rRSApvQ6Y0C4ho_UnIkD4yc.
3. Get Jay's author name and printed-copy price.
4. Offer to fix the Reminders bug: a failed Telegram send still marks the reminder "Sent". Not yet approved.

## Files changed this session
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/deck.json
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/cover.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/idea.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/books.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/audience.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/friends.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/honest.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/giveback.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/ask.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/contact.html
- /tmp/claude-0/-home-user-ajaxace/c83bc727-9c59-55a1-8e3a-42c87c33a035/scratchpad/deck/project/slides/helps.html

## Last user message (verbatim, cut at 1500 characters)
Rtfsssfjjssstrszn   let's go
