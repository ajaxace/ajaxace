You are continuing the Wolf adverts build for Jay. Work on branch ccr-5715d2ea-nti1xk of ajaxace/ajaxace (check it out first: git fetch origin ccr-5715d2ea-nti1xk and git checkout it).

STEP 0, read, in this order: wolf_ads/HANDOFF.md, wolf_ads/ROADMAP.md, wolf_ads/PERSUASION_AUDIT.md, wolf_ads/VETTING.md, wolf_ads/EMAIL_AND_CAPTIONS.md, then CLAUDE.md (lean mode, spelling MASKA/TWIX/JAY, Tre is T-R-E).

HARD RULES: Never post, send, publish or email anything. Jay does that. No vidIQ. No paid credits or subscriptions: if something costs money, state the cost in one line and ask first. Free tools only. Adults only in images; children only from behind. Show only what Wolf really does (standard package: AI, calendar, email checks; add-ons are separate). Do not invent features, prices, testimonials, counts or capabilities for the Wolf Box. Do not claim "No credits. No limits." Keep "AI-generated dramatisation. Screens simulated." and the disclaimer line on everything.

STEP 1, environment check, report in one short block before building:
a) ffmpeg, Pillow, numpy installed and wolf_ads/neo.py runs: python3 -I wolf_ads/neo.py ad1 --preview 1.0
b) Hugging Face connector named "Hugging Face 2": run one FLUX call (mcp-tools/FLUX.1-Krea-dev, tool FLUX_1_Krea_dev_infer, 576x1024, seed 201). If invoke is refused or quota is exceeded, say which and continue with everything that does not need it.
c) Can this box reach huggingface.co and *.hf.space? If not, tell Jay to add them under Allowed domains and start a new session, then carry on without them.

STEP 2, ask Jay ONE message with these open questions, then continue working on everything that does not depend on them: which add-ons are live now; family add-on price; the age rule (18+ vs under-16 with parent's OK); how Wolf works abroad and its limits; is 69 pounds the only individual price; demo page link; privacy and unsubscribe links; sending address, trading name, postal address, data controller.

STEP 3, build, in order, committing and pushing to the branch after each:
1. Apply the fix list from PERSUASION_AUDIT.md in wolf_ads/neo.py as soon as answers arrive: call to action ("Watch the full video: link in bio" using Jay's real link), one clear age line, "69 per person" if it is the only price, "Standard package: AI, calendar and email checks" on the end card, add-on prices as agreed (Google Drive 25, OneDrive 25, Send emails 30, buy two of the same type get one free; family add-on price once given).
2. If Hugging Face works: animate the stills with Wan 2.2 (zerogpu-aoti/wan2-2-fp8da-aoti-faster, input_image = the Image URL FLUX returns, 3.5 s, steps 6). Download the clips (needs *.hf.space allowed), put them in wolf_ads/shots/ as mp4, extend neo.py so photo segments use the mp4 when present, and glitch-check every frame (hands, faces, text, warped objects). Regenerate any bad shot. Stay inside the free quota and stop when it is out.
3. Re-render ad1-ad4, dan, mum, family, inbox and long; decode-check each (ffmpeg -v error -i file -f null -); look at sample frames before claiming anything works; send the files to Jay with SendUserFile.
4. Re-run the ASA/CAP check on AI-generated people in ads; update VETTING.md.
5. Finalise the sample email text in EMAIL_AND_CAPTIONS.md with Jay's details. Do not send. Do not create Gmail drafts unless Jay asks.
6. Update ROADMAP.md and wolf_flowchart.png (python3 -I on the flow script if present, otherwise rebuild) so every box is honest.

DEFINITION OF DONE: every box in ROADMAP.md is ticked or clearly marked "Jay only", all videos decode, nothing posted or sent, branch pushed, and Jay has a short list of what he must press or approve. Report in short plain sentences, answer first, no padding.
