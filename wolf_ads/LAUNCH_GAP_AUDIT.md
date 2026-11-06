# Wolf launch gap audit (6 Nov 2026)

Not legal advice. Run against ROADMAP.md, VETTING_GATE.md, the Drive index (00 START HERE) and the app as it stands.
Chief of Staff and the Drive 05 vetting teams still need to review this list.

## Blockers (nothing can be sold until these exist)
1. No customer-facing app. The prototype only opens inside Claude and needs a Claude sign-in plus Share access. Customers cannot use it.
2. No real calendar, email or storage connection. The standard package promises calendar and email checks. The app uses sample data.
3. No accounts or real privacy between families. The family code is a prototype lock only.
4. No way to pay or take delivery: Stripe not set up, no checkout, no onboarding after payment, nobody named to set up each family.
5. Seller identity missing: legal name and postal address are still {{merge tags}}. VAT decision recorded (not registered).
6. Privacy notice and terms of sale not finished. No refund or cancellation wording. Free-use clause drafted, quota missing, not checked.

## Legal and compliance
- ICO registration (UK data controller fee) not done. Check.
- Children's data and calendar/email access are high risk. Parents' consent and the age line (18+ vs under 16s need a parent) still conflict.
- Third-party AI services process family data. The privacy notice must say so.
- Gmail and Google Drive access for the public normally needs Google's app verification (likely a security review). Not started. Same idea for Microsoft.
- Cooling-off rights for digital purchases: UK consumer rules apply, and small print cannot waive them. Needs wording and a solicitor.
- Written supplier confirmation of "no monthly fees" still wanted.
- Marketing emails need consent (PECR). First send is to Jay only.

## Money
- Cost per active family (AI, storage) against a one-off £69 is unknown. Biggest money risk.
- Family add-on price open. Alerts add-on unpriced. £69, £179 and add-on prices still need Jay's final confirmation.
- Meta ad budget not set.

## Marketing and creative
- Paid Facebook and Instagram ads stay BLOCKED until the product is real and the screens show something that works as filmed.
- Ad end card still has the old age line, the old seller line and "link in bio" with no link. Needs Ajax, 18+, and a real link.
- No landing page or demo page. Second source for the trend claim missing.
- TikTok AI label and library music pick are posting-day tasks for Jay.

## Support and operations
- No support email or phone, no response times, no complaints process.
- No backups, data export or delete-my-data process.
- Reminders only fire while the app is open. Voice is unreliable inside Claude's page.

## Teams still to review
Chief of Staff, psychology, legal, trend and illustration teams (Drive folder 05). Re-run the vetting gate on the real product, not the prototype.

## Update 6 Nov (later)
Done since the first audit:
- Customer-facing app built (wolf_site): family accounts, shared lists, notes, chores, meals, photos, AI via each family's own free key, calendar by private link, set-up guide with pictures, deploy steps. Tested in a simulated setup, not yet on Hostinger or real phones.
- Postal address: Jay is arranging a UK virtual office. Contact by email only. Placeholder stays until given.
- Ad end cards in neo.py now say Ajax, 18+ and "Supplied by a third-party partner" (not re-rendered yet).

New finding (important):
- The ads and the prototype recording show Wolf finding train times, taxis and cinema times. The real app has no live data and says so. Either remove "finds options" from ads and product claims until built, or build and test search-based answers first. Do not post any ad showing those answers until then.
- The prototype recording (shots/screen_8.mp4) shows scripted answers. Re-record from the real site once it is live, showing only what works: calendar link events, lists, reminders, notes, chores, voice.

Still open: Hostinger plan and upload, ICO registration, privacy notice, terms, Stripe, ad link, quota figure for fair use, solicitor check, testing on real phones.
