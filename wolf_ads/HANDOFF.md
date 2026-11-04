# Wolf ads: hand-off for the next Claude Code session (4 Nov 2026)

Read this first. Then wolf_ads/ROADMAP.md (what is done), VETTING.md, PERSUASION_AUDIT.md, EMAIL_AND_CAPTIONS.md.
Repo rules still apply: CLAUDE.md lean mode, spelling MASKA / TWIX / JAY, Tre is T-R-E.

## Goal
Make Wolf adverts (short 15s hooks plus one ~2 min film) and a sample email, vet them, then Jay approves and Jay posts and sends. NOTHING is posted or sent by Claude. No vidIQ. No paid credits: ask Jay first with the cost in one line.

## What Wolf is (Jay's words, treat as the only verified product facts)
- Standard package: use the AI, calendar, and check emails. Works wherever the customer is in the world (Jay confirmed; wording and limits still to confirm).
- Wolf can also send things and read folders, but those are ADD-ONS, not standard.
- Prices (one-off): 69 GBP per person; 179 GBP for mum, dad and one child. Add-ons: Google Drive 25, OneDrive 25, Send emails 30 GBP. Buy two of the same type, get a third of that type free. Family add-on covers every connected Wolf; price not set. Add-ons not live/priced everywhere: confirm which are live.
- Wolf Box: "coming soon" concept only. No spec or photo. Never invent features.
- Disclaimers always: Over 18 only. Under 16s need a parent's OK (conflicts, see open questions). Made and shipped by a third party. Jay does not personally do the work. AI-generated dramatisation. Screens simulated.
- Do NOT claim: "No credits. No limits." (unprovable), invoicing/pricing jobs, live traffic, folder access or sending as standard.
- Phone while driving: only parked or mounted/hands-free (GOV.UK). Children only from behind, never clear faces. Adults only.

## Files (all in wolf_ads/)
- neo.py: the renderer. `python3 -I wolf_ads/neo.py NAME` makes a video in wolf_ads/out_neo/. NAME: long (use --parallel), demo, ad1-ad4, dan, mum, family, inbox. `--preview 1.0,2.5` writes stills only. Needs ffmpeg, Pillow, numpy, Liberation and DejaVu fonts.
- shots/: FLUX stills (dan, mum, mumpark, mirror, dash, couple, holiday). assets/wolf_mark_v4_512.png is the logo (from Drive).
- wolf_flowchart.png and ROADMAP.md: the 26-box progress chart.

## Tools that worked
- Hugging Face connector named "Hugging Face 2" (claude.ai custom connector, https://huggingface.co/mcp). Old connector had gradio=none and could not run Spaces. New sessions load connectors at start.
- FLUX: space mcp-tools/FLUX.1-Krea-dev, tool FLUX_1_Krea_dev_infer, 576x1024, 28 steps, guidance 4.5. Seeds: dan 201, mum 301/402, mirror 302, dash 303, couple 304, holiday 401.
- Wan 2.2: space zerogpu-aoti/wan2-2-fp8da-aoti-faster, tool wan2_2_fp8da_aoti_faster_generate_video, input_image = the Image URL returned by FLUX. 3 test clips were made but the cloud box cannot download them (network blocks huggingface.co and *.hf.space).
- ZeroGPU free quota runs out after about 8 images and 3 clips and resets daily. Hugging Face PRO would raise it (paid: ask Jay).
- Mixkit is blocked from the cloud box. Music in the films is synthesised in ffmpeg. For posting use a TikTok Commercial Music Library sound.

## Blocked until Jay acts
1. Environment settings > Allowed domains: add *.hf.space and huggingface.co, then start a NEW session. Then download Wan clips and glitch-check frame by frame.
2. Answers: which add-ons are live; family add-on price; how Wolf works abroad; the age rule (18+ vs under-16 parent OK); is 69 the only individual price (for "from" wording).
3. Demo page link, privacy notice link, unsubscribe link, sending address, trading name, postal address, data controller (for the email).
4. Chief of Staff review cannot run from the cloud session.

## Fix list before anything goes live (from PERSUASION_AUDIT.md)
Add a call to action ("Watch the full video: link in bio"); resolve the age line; change "from 69" to "69 per person" if it is the only individual price; add "Standard package: AI, calendar and email checks" to the end card; hold evidence for every capability claim; keep Dan, Sarah labelled as fictional.

## Next steps for the new session
1. Test one FLUX call; if invoke is refused, stop and tell Jay the connector setting.
2. Apply the fix list in neo.py (draw_end, end_sprites, tier_card) once Jay answers, re-render ad1-ad4, dan, mum, family, inbox, long.
3. Pull Wan clips if the domains are allowed; add motion shots; glitch-check frames.
4. Run the formal checks again (ASA/CAP guidance on AI-generated people).
5. Prepare, do not send, the sample email from EMAIL_AND_CAPTIONS.md.

## Paste into the new session
"Read wolf_ads/HANDOFF.md and ROADMAP.md on this branch. Continue the Wolf ads build exactly from there. Do not post or send anything. Ask me for the open answers listed in HANDOFF.md first."
