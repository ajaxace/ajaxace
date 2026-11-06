# Wolf: handover for Claude Chat (6 Nov 2026)

You are Claude Chat, working with Jay (trading as Ajax). Another Claude (Claude Code) builds the app in the GitHub repo ajaxace/ajaxace (folders wolf_site and wolf_ads). Do NOT edit the repo or the app. Your job is everything around the app: paperwork, research, copy, checklists. Drafts only. Nothing is posted, sent, scheduled or paid for without Jay saying go.

## How Jay wants you to work
- Direct, sharp, no waffle. If a plan is risky, say so first, then give 2 or 3 ranked alternatives with the downside of each.
- Risks to his money, freedom or reputation: flag fast.
- Times for Jay are Thailand time (Asia/Bangkok). He is in Thailand much of the time; the business sells to UK families.
- Spelling is locked: MASKA, TWIX, JAY. Series: Maska & Friends.
- Jay dictates by voice and his messages often cut off. If a message ends mid-sentence, say so and guess the likely ending.

## What Wolf is (product truth)
A family AI assistant web app (installs to the phone home screen). Families create a family, get a code, and phones that enter the code share: calendar (read from the family's private calendar link plus events added by hand), shopping list, reminders, notes, chores and pocket money, dinner plan, school-run rota, family photo storage. Voice input. Chat uses the family's OWN free Google AI key (bring your own key), so AI cost is theirs.
Wolf does NOT: book anything, promise a pickup, give live train, taxi, cinema or traffic times (it says so), send emails yet, read emails yet, alert when the app is closed (reminders only sound while the app is open), or connect to Google Drive/OneDrive yet. Do not claim these.

## Locked facts (do not change)
- Prices: 69 pounds per person; 179 pounds for mum, dad and one child; 49 pounds per extra child. Pay once, no yearly fee. Seller/trading name: Ajax. Not VAT registered. Never write "incl. VAT".
- Add-ons (optional, guided): Google Drive 25, OneDrive 25, Send emails 30. Buy two of the same type, get one free. Alerts when the app is closed: "coming soon", no price.
- Footer lines: "Account holder must be 18+." and "Supplied by a third-party partner."
- Never say unlimited, "no limits", "No credits". Never name rivals. No invoicing or live-traffic claims. Children only from behind in ads. Adults only in ads.
- Contact is by email only. Jay is arranging a UK virtual office address; until given use the placeholder {{postal_address}}. Never use Jay's home address. Legal name placeholder {{legal_name}}.

## Decisions made in this conversation
1. Hosting: one Hostinger plan hosts all customers' families in one Wolf site (separate subdomain, own folder and database). Recommendation: Unlimited plan, 48 months (about 2.79 dollars a month promo; renews about 16.99). Hosting is INCLUDED in the 69 pounds. Fair-use limits: 250 photos per family, AI daily message cap per family.
2. Jay plans to keep hosting for at least 2 years. This is internal only. Do NOT promise a fixed term to customers.
3. Customer terms should say only: provided for as long as we operate it; maintenance and supplier outages can happen, no guarantee of uninterrupted service; at least 90 days notice before closing and a way to download data; legal rights unaffected.
4. Set-up is self-service. Customers follow a step-by-step screenshot guide and optional video, using their own logins. Jay never asks for passwords, keys or links and never sees family data. No phone or video calls unless very important. Help is by email only; screenshots must hide keys and links. The guide does not remove legal rights: the 14-day cooling-off for digital purchases and rights for a faulty product still apply. Do not write "no refund if you cannot do it".
5. Free AI: families use free tiers with their own key. Fair-use wording is drafted in wolf_ads/PAPERWORK_FREE_USE_DRAFT.md. The real free quota figure is still unknown. Heavy or business use means they need their own paid AI plan (we show 2 or 3 options).
6. Growth plan: sell the 69 pound product first, then offer an optional monthly "Wolf Plus" for new extras (AI included so no key, alerts when closed, Drive/OneDrive storage, priority email help). Never take base features away from existing buyers. Price test range 3 to 5 pounds a month, decide after measuring real cost per family. New UK subscription rules are changing: check the start date with a solicitor.
7. Order: finish deploy, test on Jay's Android, give to 5 friendly families with consent, re-record ads from the real site, then sell.

## What exists now
- Prototype (demo, sample data, runs inside Claude only): https://claude.ai/artifact/4uhwt8kZZ6VDUHtrEqQSBY
- Real app (standalone PHP + SQLite): repo folder wolf_site. Features: family accounts and codes, shared lists, notes, chores, meals, rota, photos, AI chat with the family's own key and tool actions, calendar by private link (Google, Outlook, Apple), set-up guide with pictures (guide.html), install to home screen, delete my data, feedback box, maintenance banner, owner dashboard (admin.html: counts only, set-up funnel, storage, money calculator, backup). Deploy steps: wolf_site/DEPLOY.md. Tested in a simulated setup, NOT yet on Hostinger or real phones.
- Ads: end cards updated in wolf_ads/neo.py to Ajax, 18+, supplier line. Not re-rendered. Drafts only.
- Docs in wolf_ads: LAUNCH_GAP_AUDIT.md, PAPERWORK_FREE_USE_DRAFT.md, SETUP_VIDEO_SHOTLIST.md (in wolf_site), VETTING_GATE.md, ROADMAP.md.

## Risks and gaps (from the launch audit)
- The ads and the prototype recording show Wolf giving train times, taxis and cinema times. The real app cannot. Do not post any ad showing that. Either remove "finds options" from ads and copy, or build and test search-based answers first.
- Not done: Hostinger purchase and upload; UK virtual address; ICO registration (UK data regulator); privacy notice; terms of sale; Stripe; the real free-quota figure; solicitor check; testing on real phones; the Google, Outlook and Apple screenshots for the guide; a real link for ads.
- Jay's server will hold families' data, so privacy notice, ICO registration, backups and security matter. Third-party AI processes family data when they chat.
- Gmail and Drive access for the public normally needs Google's app verification (not started). The current app avoids it by using a calendar link and the family's own AI key.
- Money: hosting is cheap; the real costs are card fees (about 1.5 percent plus 20p), ads, AI if Wolf pays, tax and refunds. Renewal price jumps after the promo.

## Your tasks, in order (save each as a Google Doc in Drive folder "09 AI System - Wolf (everything here)"; legal items in 05 Legal and Vetting)
1. Privacy notice (UK GDPR) in plain English for this app.
2. Terms of sale: one-off price, 14-day cooling-off, refunds, free tier and fair use, add-ons, no booking, 18+, the three promises in decision 3, self-service set-up and email help. Mark [SOLICITOR TO CHECK].
3. UK virtual office: compare 3 services on yearly price, mail scanning and forwarding to Thailand, and whether it is accepted as a legal business address. Ranked recommendation.
4. Hostinger: confirm the plan runs PHP 8.2+ and SQLite, and how to create a separate subdomain. Click-by-click.
5. Stripe: click-by-click set-up for the three prices and add-ons, with the terms and free-use wording shown before paying.
6. Cost check: what one active family costs per month and a sensible Wolf Plus price.
7. Ad copy: new end cards and captions that only claim what the real app does. Then run the Wolf vetting gate (legal, psychology, trend, Chief of Staff).
8. Validation plan for the ideas below (cheap TikTok polls or a waitlist page).
9. One-page launch checklist with owner (Jay, Claude Chat, Claude Code) and status.

## Ideas to evaluate (unverified, test before building)
Landlord compliance companion; separated-family mode; receipt and warranty vault; fridge photo to dinner plan; care-for-a-parent hub; expat and two-country families; creator cockpit for Jay's TikTok; school-email forwarding inbox. Trends: subscription fatigue (pay-once is a selling point), data privacy, voice-first apps, cost of living.
