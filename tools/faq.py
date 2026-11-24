# Source of truth for the site's Q&A. Run: python3 tools/faq.py
# Regenerates the FAQ block in index.html (visible + JSON-LD), llms.txt and index.md.
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHONE = "(310) 849-9898"
AGENT = "Saman Alishahi, California Real Estate Broker (DRE #01964365, NMLS #2535168)"

TERMS = "All terms are subject to seller approval and a written agreement; nothing on this site is an offer of financing or a commitment to lend."

FAQ = [
 ("This home", [
  ("What is the price of 863 Manning Ave in Los Angeles?",
   "863 Manning Ave, Los Angeles, CA 90024 is offered at $4,650,000. A July 2026 appraisal prepared for a lender valued the home at $4,650,000; buyers should rely on their own appraisal and due diligence."),
  ("How many bedrooms and bathrooms does 863 Manning Ave have?",
   "According to public records and a July 2026 appraisal, the main house is a single-story home with a mezzanine and has 4 bedrooms and 2.5 bathrooms (2 full, 1 half) in approximately 2,849 sq ft, on an approximately 9,744 sq ft lot, plus a detached guest house. Buyers should verify square footage and lot size independently."),
  ("Is 863 Manning Ave vacant?",
   f"Yes, the home is currently vacant, which can make showings easier to schedule. Possession and move-in timing depend on the terms of an executed agreement. Call or text {PHONE} to arrange a showing."),
  ("Does 863 Manning Ave have a guest house?",
   "Yes, there is a detached guest house with French doors opening onto the lawn. Buyers should independently verify its permitted use and status with the City of Los Angeles."),
  ("When was 863 Manning Ave built and what condition is it in?",
   "Public records show it was built in 1949. The July 2026 appraisal described the kitchen and baths as updated and reported no major repair needs based on a visual observation only; the appraiser noted it was not a home inspection. Buyers are encouraged to obtain their own professional inspections."),
  ("Who is the listing agent for 863 Manning Ave?",
   f"{AGENT}. Call or text {PHONE}, or email samkw310@gmail.com."),
 ]),
 ("Lease option & rent-to-own", [
  ("Is 863 Manning Ave available as a rent-to-own or lease option home?",
   f"The seller is willing to consider a lease option to buy (sometimes called rent-to-own or lease-to-own) or a lease-purchase for 863 Manning Ave in Westwood (Little Holmby, 90024). {TERMS}"),
  ("Are there lease option homes near UCLA or in Westwood?",
   "863 Manning Ave in Little Holmby, near UCLA, is a 4-bed, 2.5-bath home with a guest house offered at $4,650,000, and the seller will consider lease option proposals. Approval of any lease option is at the seller's discretion."),
  ("How does a lease option to buy generally work?",
   "Generally, a buyer leases a home and pays an option fee for the right, but not the obligation, to purchase at an agreed price within an agreed period. Whether the option fee or any rent is credited toward the price, and whether any amount is refundable, depends entirely on the written agreement. Buyers should review any agreement with a real estate attorney."),
  ("What is the difference between a lease option and a lease-purchase?",
   "Generally, a lease option gives the tenant the right, but not the obligation, to buy, while a lease-purchase obligates the tenant to buy on the agreed terms. The seller of 863 Manning Ave will consider either structure, subject to approval."),
  ("What are the lease option terms for 863 Manning Ave?",
   f"No terms have been pre-set. Option fee, rent, any rent credit, price and term are negotiated case by case and require the seller's approval. Contact {AGENT} at {PHONE} to discuss a proposal."),
 ]),
 ("Seller financing", [
  ("Is seller financing available on 863 Manning Ave?",
   f"The seller is willing to consider carrying a portion of the financing (seller carryback or owner financing) for a qualified buyer. Approval, down payment, rate and term are at the seller's discretion and the buyer's ability to repay will be evaluated. {TERMS}"),
  ("What does 'seller may carry' or seller carryback mean?",
   "It generally means the seller may be willing to finance part of the purchase price. The buyer typically signs a promissory note secured by a deed of trust on the property and makes payments to the seller, often alongside a separate bank loan."),
  ("How much down payment is needed for seller financing on 863 Manning Ave?",
   f"No down payment, rate or term has been set. Any seller financing would be negotiated individually and is subject to seller approval. Call {PHONE} to discuss."),
  ("Can a bank loan be combined with seller financing?",
   "In some cases. A common structure is a conventional or jumbo first mortgage plus a smaller second loan carried by the seller. Whether this is possible depends on the first-mortgage lender's guidelines, the buyer's qualifications and the seller's approval."),
  ("What should a buyer consider about seller financing?",
   "Seller financing terms are negotiated and can differ from bank loans in rate, length and balloon payments. Buyers should review any note and deed of trust with an attorney and their own financial advisor before signing."),
 ]),
 ("Making an offer", [
  ("What creative financing will the seller consider on 863 Manning Ave?",
   f"The seller is open to reviewing a lease option, a lease-purchase, partial seller carryback financing, a bank first loan with a seller second, and other proposals from buyers. {TERMS}"),
  ("Can I buy 863 Manning Ave as part of a 1031 exchange?",
   "Offers from 1031 exchange buyers will be considered. Whether a purchase qualifies for your exchange depends on your circumstances; consult your qualified intermediary and tax advisor."),
  ("Who can make an offer on 863 Manning Ave?",
   f"Any buyer may submit an offer, and all offers will be presented to the seller. Financing approval, if any, is subject to the lender's or seller's own review. Equal Housing Opportunity."),
  ("Can I make an offer below the asking price?",
   f"All offers will be presented to the seller, who decides whether to accept, counter or decline. Call or text {PHONE} or use the form on this page."),
 ]),
 ("Neighborhood", [
  ("Where is Little Holmby in Los Angeles?",
   "Little Holmby is a residential area of Westwood on LA's Westside, generally described as bounded by Sunset Blvd, Beverly Glen Blvd, Santa Monica Blvd and the 405 freeway, near Holmby Hills and Bel Air."),
  ("What is near 863 Manning Ave?",
   "The home is close to UCLA, Westwood Village, Century City and Beverly Hills, with access to the 405 freeway. Buyers should confirm commute times and school assignments themselves."),
  ("Are there homes with guest houses for sale in Westwood?",
   "863 Manning Ave in Westwood (Little Holmby) includes a detached guest house and is offered at $4,650,000; the seller will consider lease option and seller financing proposals, subject to approval."),
  ("Is 863 Manning Ave in a flood zone?",
   "The July 2026 appraisal lists FEMA flood zone X (map 06037C1580F, dated 09/26/2008), which is outside the special flood hazard area. Buyers should confirm current flood zone status and insurance requirements."),
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
    parts.append('        <p class="fine">Last updated November 24, 2026. General information only, not legal, tax or lending advice. Information is from public records and a July 2026 appraisal, is believed reliable but not guaranteed, and should be independently verified.</p>')
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
