# Handoff brief

Written 2026-11-05T05:46:36.902Z at 60% context. Session 50b91fe8-1eb1-5658-b67c-c43641615820. Project /home/user/ajaxace.

## Goal
Produce Wolf (Jay's family AI assistant) adverts and a sample email: a 15s hook plus a ~2 min film, vetted. Jay approves, posts and sends. Claude never posts or sends anything. Free tools only, no vidIQ, no paid spend without asking.

## Work in progress
- Repo `ajaxace/ajaxace`, branch `ccr-5715d2ea-nti1xk`, folder `wolf_ads/`: `neo.py` (renderer), `shots/` (7 FLUX stills), `shots_v2/`, `assets/wolf_mark_v4_512.png`, `tools/screen_recorder.html`, plus HANDOFF, ROADMAP, VETTING, VETTING_GATE, PERSUASION_AUDIT, EMAIL_AND_CAPTIONS, NEW_SESSION_PROMPT, wolf_flowchart.png. All pushed.
- A Windows PC Claude session also pushes to this branch. Always `git pull --rebase` before pushing. A rejected push happened once.
- Rendered drafts (neon long film 1:55, short ads, native cuts `native_dan`, `native_mum`) are only in the cloud scratchpad and chat, not git. Re-render with `python3 -I wolf_ads/neo.py NAME` (`long --parallel`).
- Native cuts accept a real recording at `wolf_ads/shots/screen_8.*` (Dan) or `screen_9.*` (mum); tested with a dummy clip only.
- Roadmap, last count: 10 done, 6 part done, 10 not done.

## Decisions made
- Locked prices: £69 per person, £179 mum+dad+one child, £49 per extra child, pay once, no yearly fee.
- Jay approved add-ons: Google Drive £25, OneDrive £25, Send emails £30, buy two of the same type get one free; family add-on covers every connected Wolf (no price).
- Standard package: AI, calendar, email checks. Sending and folder access are add-ons.
- Never claim "No credits. No limits.", invoicing or live traffic. No rivals named. Children only from behind. Adults only. Disclaimers: "AI-generated dramatisation. Screens simulated.", "Made and shipped by a third party. Jay does not personally do the work."
- Wolf Box is "coming soon", concept only, no specs.
- Jay's music folder rejected; own synthesised track used; TikTok Commercial Music Library at posting.
- Vetting gate verdict: neon films FIX; paid Facebook/Instagram ads BLOCKED until a real screen recording and native look exist.

## Assumptions to verify
- Reminders, shared family calendar, "works wherever you are" (Jay said yes; limits unknown).
- All demo screen content is invented sample data.
- Which add-ons are live now; add-on prices are not in the locked price list.
- Wolf Box is genuinely planned.
- Traffic, folder reading by standard package: unanswered.
- "Watch the full video: link in bio" is a placeholder; no link exists.
- The age line conflicts ("Over 18 only" vs "Under 16s need a parent's OK").
- ASA/CAP guidance on AI-generated people was not found.
- Recorder button untested with real screen capture.

## Dead ends (do not retry)
- Old Hugging Face connector (`gradio=none`) refuses invoke; use "Hugging Face 2".
- Cloud box blocks huggingface.co, *.hf.space, mixkit.co; Wan clip links can't be downloaded here. The Windows PC reaches hf.space.
- Free ZeroGPU quota ran out after about 8 images and 3 clips; resets daily.
- TikTok Creative Center fetch fails (login-gated). Parallel Search free tier rate-limits.
- Uploading videos to Drive via connector is infeasible.

## Last request and whether it was answered
Jay asked for an app to screen-record Wolf. Answered: sent `screen_recorder.html` (Chrome/Edge) and phone built-in recorder steps. Not yet confirmed working on his machine.

## Next step
`git pull --rebase`, read `wolf_ads/HANDOFF.md` and `ROADMAP.md`. Wait for Jay's recordings and answers (age rule, link, add-on live status, Box info). Then drop recordings into `shots/`, re-render native ads, apply the fix list, re-run vetting, and prepare (not send) the sample email.

## Files changed this session
- /tmp/claude-0/-home-user-ajaxace/50b91fe8-1eb1-5658-b67c-c43641615820/scratchpad/wolf_A1/build.py
- /tmp/claude-0/-home-user-ajaxace/50b91fe8-1eb1-5658-b67c-c43641615820/scratchpad/wolf_A1/build_demo.py
- /tmp/claude-0/-home-user-ajaxace/50b91fe8-1eb1-5658-b67c-c43641615820/scratchpad/wolf_A1/build_wolf.py
- /tmp/claude-0/-home-user-ajaxace/50b91fe8-1eb1-5658-b67c-c43641615820/scratchpad/wolf_A1/neo.py

## Last user message (verbatim, cut at 1500 characters)
You sign record both. So give me an app that I can run. Where is the app that I can run to record the screen?
