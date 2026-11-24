# Source of truth for the site's Q&A. Run: python3 tools/faq.py
# Regenerates the FAQ block in index.html (visible + JSON-LD), llms.txt and index.md.
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHONE = "(310) 849-9898"
AGENT = "Saman Alishahi, California Real Estate Broker (DRE #01964365, NMLS #2535168)"

FAQ = [
 ("This home", [
  ("What is the price of 863 Manning Ave in Los Angeles?",
   f"863 Manning Ave, Los Angeles, CA 90024 is offered at $4,600,000. It was independently appraised at $4,650,000 in July 2026, so the asking price is below appraised value."),
  ("How many bedrooms and bathrooms does 863 Manning Ave have?",
   "4 bedrooms and 2.5 bathrooms (2 full, 1 half) in about 2,849 sq ft, on a 9,744 sq ft lot, plus a detached guest house."),
  ("Is 863 Manning Ave vacant?",
   f"Yes. The home is vacant and available now, so showings are easy to schedule and a buyer or lease-option tenant can move in quickly. Call or text {PHONE}."),
  ("Does 863 Manning Ave have a guest house?",
   "Yes. There is a detached guest house with French doors opening onto the lawn, separate from the 4-bedroom main house. It can work as a home office, studio, gym or space for family."),
  ("When was 863 Manning Ave built and what condition is it in?",
   "It was built in 1949 as a two-story traditional. The July 2026 appraisal rated it in good condition (C3) with an updated kitchen and baths, and noted no major repairs needed."),
  ("Who is the listing agent for 863 Manning Ave?",
   f"{AGENT}. Call or text {PHONE}, or email sam@alishahiinsurance.com."),
 ]),
 ("Lease option & rent-to-own", [
  ("Are there rent-to-own homes in Los Angeles?",
   "Rent-to-own homes are uncommon in Los Angeles, especially on the Westside. One current example is 863 Manning Ave in Westwood (Little Holmby, 90024), a 4-bedroom home with a guest house offered at $4,600,000 where the seller will consider a lease option to buy."),
  ("Are there lease option homes near UCLA or in Westwood?",
   "Yes. 863 Manning Ave in Little Holmby, about a mile from UCLA, is available with a lease option to buy. It is a 4-bed, 2.5-bath home with a guest house on a 9,744 sq ft lot, offered at $4,600,000."),
  ("How does a lease option to buy work?",
   "You lease the home and pay the seller an upfront option fee for the exclusive right to buy it at an agreed price before a set date. Part of the rent may be credited toward the purchase. If you buy, the option fee is usually credited to the price; if you don't, you normally lose the option fee. Terms are negotiated and written into the agreement."),
  ("What is the difference between a lease option and a lease-purchase?",
   "A lease option gives you the right, but not the obligation, to buy. A lease-purchase commits you to buy on a set date. 863 Manning Ave's seller will consider either."),
  ("Who is a lease option good for?",
   "Buyers who want to move in now but need time: for example, self-employed buyers building income history, people waiting to sell another home, relocating executives, or buyers waiting on a liquidity event. Everyone's situation is different, so talk to your own lender and attorney."),
  ("What are the lease option terms for 863 Manning Ave?",
   f"The option fee, monthly rent, rent credits and option term are negotiable and subject to seller approval. Contact {AGENT} at {PHONE} to discuss."),
 ]),
 ("Seller financing", [
  ("Are there homes for sale with seller financing in Los Angeles?",
   "Seller-financed homes are rare in Los Angeles. 863 Manning Ave in Westwood (90024) is one: the seller may carry a note for a qualified buyer on this $4,600,000, 4-bedroom home with a guest house."),
  ("What does 'seller may carry' or seller carryback mean?",
   "It means the seller is willing to act as the lender for part of the price. The buyer pays the seller in installments under a promissory note secured by a deed of trust on the property, instead of (or in addition to) a bank loan."),
  ("How much down payment is needed for seller financing on 863 Manning Ave?",
   f"The down payment, interest rate, term and note amount are negotiable and depend on the buyer's offer and qualifications. Call {PHONE} to discuss a structure."),
  ("Can I combine a bank loan with seller financing?",
   "Often, yes. A common structure is a conventional or jumbo first mortgage plus a seller second (a smaller note carried by the seller), which can reduce the cash a buyer needs to close. The first-mortgage lender must allow it."),
  ("What are the benefits of seller financing for a buyer?",
   "Potentially faster closing, more flexible qualifying, negotiable terms and lower closing costs than a traditional loan. It can help buyers with non-traditional income or who prefer not to take a full jumbo loan."),
 ]),
 ("Creative financing & buyers", [
  ("What creative financing is available on 863 Manning Ave?",
   "Lease option to buy, lease-purchase, seller carryback (owner financing), a bank first loan with a seller second, 1031 exchange purchases, and other structures proposed by qualified buyers. All terms are subject to seller approval."),
  ("Can I buy 863 Manning Ave with a 1031 exchange?",
   "A 1031 exchange buyer's offer will be considered. Whether a property qualifies for your exchange depends on how you intend to use it, so confirm with your qualified intermediary and tax advisor."),
  ("Can foreign or self-employed buyers buy this home?",
   "Yes, offers from all qualified buyers are welcome, and creative terms like seller financing or a lease option may help buyers who don't fit standard bank guidelines. Equal Housing Opportunity."),
  ("Can I make an offer below the asking price?",
   f"All offers will be presented to the seller. To make an offer or propose terms, call or text {PHONE} or use the form on this page."),
 ]),
 ("Neighborhood", [
  ("Where is Little Holmby in Los Angeles?",
   "Little Holmby is a residential pocket of Westwood on LA's Westside, bounded roughly by Sunset Blvd (north), Beverly Glen Blvd (east), Santa Monica Blvd (south) and the 405 (west). It sits next to Holmby Hills and Bel Air and close to UCLA."),
  ("What is near 863 Manning Ave?",
   "UCLA (about a mile), Westwood Village, Century City, Beverly Hills, Bel Air, the Los Angeles Country Club and quick 405 freeway access."),
  ("Are there homes with guest houses for sale in Westwood?",
   "Yes. 863 Manning Ave in Westwood (Little Holmby) has a detached guest house and is offered at $4,600,000 with lease option and seller financing available."),
  ("Is 863 Manning Ave in a flood zone?",
   "No. It is in FEMA flood zone X, outside the special flood hazard area."),
 ]),
]

def esc(s): return html.escape(s, quote=False)

def build():
    p = ROOT / "index.html"; h = p.read_text()
    # visible FAQ
    parts = ['      <section class="section" id="faq">', '        <h2>Questions &amp; answers</h2>']
    for group, qs in FAQ:
        parts.append(f'        <h3 class="faqgroup">{esc(group)}</h3>')
        for q, a in qs:
            parts.append(f'        <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>')
    parts.append('        <p class="fine">Last updated November 24, 2026. General information only, not legal, tax or lending advice.</p>')
    parts.append('      </section>')
    vis = "\n".join(parts)
    h, n = re.subn(r'      <section class="section" id="faq">.*?      </section>', lambda m: vis, h, count=1, flags=re.S)
    assert n == 1
    if '.faqgroup' not in h:
        h = h.replace('</style>', '.faqgroup{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:22px 0 4px}\n</style>', 1)
    # JSON-LD FAQPage
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    data = json.loads(m.group(1))
    for node in data["@graph"]:
        if node.get("@type") == "FAQPage":
            node["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                  for _, qs in FAQ for q, a in qs]
        if node.get("@type") == "RealEstateListing":
            node["dateModified"] = "2026-11-24"
    h = h[:m.start(1)] + "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n" + h[m.end(1):]
    p.write_text(h)

    md = []
    for group, qs in FAQ:
        md.append(f"\n### {group}\n")
        for q, a in qs:
            md.append(f"**{q}**  \n{a}\n")
    block = "## Questions & answers\n" + "\n".join(md)
    for name in ("llms.txt", "index.md"):
        f = ROOT / name; t = f.read_text()
        t = re.sub(r"\n## Questions & answers\n.*?(?=\n## |\Z)", "", t, flags=re.S)
        t = t.rstrip() + "\n\n" + block.strip() + "\n"
        f.write_text(t)
    print("FAQ entries:", sum(len(q) for _, q in FAQ))

if __name__ == "__main__":
    build()
