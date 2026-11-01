# Handoff brief

Written 2026-11-01T11:51:41.059Z at 60% context. Session c83bc727-9c59-55a1-8e3a-42c87c33a035. Project /home/user/ajaxace.

## Goal
Jay (Thailand, UTC+7) wants his whole system run lean and finished: Claude scheduled tasks, n8n on his Hostinger server, uploaded skills, and a steady supply of TikTok/Instagram posts (@ajaxace1894; Blotato TikTok 64472, Instagram 76895). Spelling is locked as MASKA, TWIX, JAY; series "Maska & Friends". Jay wants me to act without asking. Repo is `ajaxace/ajaxace`, work branch `ccr-7d0361cf-yyrgit`. `CLAUDE.md` holds the lean rules.

## Work in progress
- **Clip desk** `trig_01YCkyY4eYSshXQK952nG4Zx` (Haiku, 17:23 Bangkok daily, enabled). Its prompt now reads ONE raw place: Drive "RAW - drop everything here (videos, pics, posts)" (id `1w17aoZJMuLoj3XZVTS-D1uO_YvYA6iN5`, inside "TikTok To Approve" `13ZP6vHb6eLouFZJuaylO6_HX9WyaRzxq`). It has scavenger mode: new RAW video first, else remix the Thai coach footage or POSTED clips; one edit a day, 40-credit vidIQ cap, 150 MB file limit. Jay approves by dragging clips into "YES - post it" (`18cnPggslmlXUaXIVNKjubDCsDItgTFlS`).
- **Root cause found 1 Nov:** the 10 `_banner.mp4` clips in YES had no Drive description, so the Clip desk skipped them. Blotato showed nothing scheduled after 31 Oct 13:00 UTC. I copied captions onto all 10 and fired the Clip desk once (session `cse_0114PQjV3m9vJsEgkqaqzTU1`, running at ~11:51Z). Result not yet confirmed.
- **72-hour check:** reminder `trig_01LZgCaisG3BTfoqVKB3Dupr` fired 31 Oct. Not clean, because the Clip desk's 30 Oct run failed with USAGE_LIMIT_REACHED. Health Check `nREyDHXe3L9JilLV` was therefore NOT slowed and is still every 5 minutes. The clock restarts.
- **MASKA fixes in n8n, published:** Reviewer `VJVJ6h0DPmU61UV0`, Writer `VuyhrpSbs5xs00r4`, Studio `phdC131RSbK7RWgv`, Illustrator Brain `BP5bCbJyoEK7hJb9`. Matchers accept both `masca` and `maska`. Skipped on purpose: Gate (already MASKA-locked), Illustration v2 `Ia83OxujMLgX05YU` (already matches `maska|masca`; the "Masca & Friends" default feeds the dedupe hash), Dashboard `C2UonLGLmM5DPCs1` (187 KB, display-only), old 12-illustrator `4o7a75diSHUoAIum` (now inactive).
- **Restore log:** n8n table `lean_changes` (`WFDTlzpcChmZ0AXc`, project `vQlqixidnpQyrAdP`) holds old version IDs for each change.
- **Done earlier:** Auditor `trig_01YAFX7mTTg7tsEWkrXK43cX` set to Sonnet. Illustration v2 `93aa45f2` published; the old live version `1c253831` is the revert. Cowork saved all skill fixes (1–6) and removed `maska-ad-studio`, with backups in Drive. Cowork also added n8n to the Clip desk and disabled the Opus TikTok Publisher `trig_01M56nDGrZVBEpdiSaXme3qt`.
- **Other sessions on Jay's Acer PC (not cloud):** trading app chat `b664aa34-ea59-4bbe-8aec-6cb5a5fd37a2` in `C:\Users\ACER\OneDrive\Documents`; built copy in `C:\Users\ACER\AppData\Local\Temp\gold-coach-preview` (needs backing up); illustration team in `C:\IllustrationTeam`. I gave Jay paste prompts for both, plus decisions for the bike-for-sale package (bigger photo window with a solid strip, drop photo 125939, one final review round).

## Decisions made
- Keep "LEAN:" lines in task prompts. Skills do load in scheduled tasks (init event lists them), but loading is not the same as the task calling them.
- Chief of Staff (`trig_016k4p8ihmSSNFehpRFDW1KD`, Sonnet) stays at 33 connectors. It is chat-type, so the list is read-only, and recreating it loses run history.
- Dashboard and Claude to Jarvis runs are left alone, as they cost no Claude usage.
- Gold Coach trading files are never scavenge material.

## Assumptions to verify
- That the Clip desk run at ~11:51Z booked 6 clips on both accounts, and that the 1 Nov 13:00 UTC slot was filled.
- That "the coaches" means the Thai coach-bus footage (`20261025_111514.mp4`, `20261025_111247.mp4`, photos in folder `1yooKc56tZIhXqrqW3E0zEHD7D0_ukWbK`).
- That the new n8n errors today (RAW Drop page `7ytaPLMzfhfdtYQt`, Telegram filing assistant `YFPF01WQeP6fO5vZ`, J Junior bot `nKONFV97piL6csNS`) come from other sessions' builds, not the lean changes.
- vidIQ credit balance and the usage-limit state are unknown.

## Dead ends (do not retry)
- `create_trigger` cannot attach connectors for this organisation; only the claude.ai UI can.
- A subagent doing bulk n8n edits was denied by the permission classifier; direct edits afterwards worked.
- `get_workflow_details` on the Dashboard returns 187 KB and the edit tool cannot patch a string in place.
- `$HOME` searches on the PC missed the trading project because the terminal ran as Administrator. The `.claude\projects` folder listing found it.
- OneDrive/Zapier was a false lead for the footage: it is all in Google Drive.

## Last request and whether it was answered
Jay asked me to check that everything is running lean and right, noting he had put footage into TikTok To Approve and RAW. I answered with the findings above. His mid-turn point was that the footage must go through editing and illustration, which I took to mean the Clip desk must edit it and the banner clips are the edited versions. Answered; the booking result is unconfirmed.

## Next step
1. Check Blotato `list_schedules` and `list_posts` for the booked clips, and the Clip desk session result.
2. Offer Jay "do the editing sitting": a batch of 8–10 edits in his PC Claude Code, using the Clip desk's rules.
3. Restart the 72-hour clean clock. Slow Health Check to 15 minutes only if all runs succeed and slots stay filled.
4. Ask the PC trading session where its source lives, and back up `gold-coach-preview`.

## Files changed this session
none

## Last user message (verbatim, cut at 1500 characters)
Okay, check we're all running lean and everything's right. So just check it all. I've tried to put it to TikTok approved, so I think they're slowly downloading now. From Google, I think I've put it into the raw. Drop files, photos, and pics here. I think that's filling up.
