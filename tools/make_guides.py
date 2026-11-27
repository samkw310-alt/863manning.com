# Builds the buyer guide pages for 863manning.com from index.html's styles.
# Run from the site root:  python3 tools/make_guides.py
import json, pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = "https://863manning.com"
TODAY = "2026-11-26"
index = (ROOT / "index.html").read_text()
STYLE = re.search(r"<style>.*?</style>", index, re.S).group(0)
FAB = re.search(r'<div class="fab">.*?</div>', index, re.S).group(0)

EXTRA_CSS = """<style>
.art{max-width:780px;margin:0 auto;padding:8px 0 40px}
.crumbs{font-size:.82rem;color:var(--muted);margin:16px 0 4px}
.crumbs a{color:var(--muted)}
.art h1{font-size:clamp(1.7rem,4.5vw,2.4rem);line-height:1.15;margin:8px 0 12px}
.art .lede{font-size:1.08rem;color:var(--muted)}
.art figure{margin:18px 0}
.art figure img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:10px}
.art figcaption{font-size:.8rem;color:var(--muted);margin-top:4px}
.art h2{font-size:1.35rem;margin:28px 0 8px}
.art li{margin-bottom:6px}
.feat{border:1px solid var(--line);border-radius:12px;padding:18px;margin:24px 0;background:var(--soft)}
.feat h2{margin-top:0}
.feat .price{font-size:1.6rem;font-weight:700;margin:4px 0}
.feat .cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
.feat .cta a{flex:1;min-width:150px;text-align:center;padding:11px 14px;border-radius:8px;font-weight:600;text-decoration:none}
.feat .cta .p{background:var(--brand);color:#fff}
.feat .cta .s{border:1px solid var(--brand);color:var(--brand);background:#fff}
.art details{border-bottom:1px solid var(--line);padding:10px 0}
.art summary{font-weight:600;cursor:pointer}
.related{display:grid;gap:8px;padding:0;list-style:none}
.related a{display:block;border:1px solid var(--line);border-radius:8px;padding:12px 14px;text-decoration:none;font-weight:600}
.related a:hover{background:var(--chip)}
.guides-foot a{margin-right:14px}
</style>"""

AGENT = {"@type": "RealEstateAgent", "@id": f"{B}/#agent", "name": "Saman Alishahi",
         "telephone": "+1-310-849-9898", "email": "samkw310@gmail.com", "url": f"{B}/"}

FEATURE = """<div class="feat">
  <h2>Featured: 863 Manning Ave, Little Holmby</h2>
  <p class="price">$4,650,000</p>
  <p>4 bed · 2.5 bath · ~2,849 sq ft · one story with a mezzanine · detached guest house · ~9,744 sq ft R1 lot · built 1949 · vacant. The seller will consider a lease option, seller carryback financing and other creative terms, subject to approval.</p>
  <div class="cta"><a class="p" href="/">See the listing, photos &amp; video</a><a class="s" href="tel:+13108499898">Call (310) 849-9898</a></div>
</div>"""

DISCLAIM = ("This guide is general information, not legal, tax or lending advice. Nothing on this site is an offer of financing "
            "or a commitment to lend. Terms for 863 Manning Ave are subject to seller approval and a written agreement. "
            "Consult a California real estate attorney and your own tax and financial advisors before signing.")

PAGES = [
 dict(slug="little-holmby-homes-for-sale",
  title="Little Holmby Homes for Sale | Westwood, Los Angeles 90024",
  h1="Little Holmby homes for sale",
  desc="Buying a home in Little Holmby, Westwood (90024)? Where the neighborhood is, what's nearby, what to check before you buy, and a single-story 4 bed home with a guest house offered at $4,650,000.",
  short="Little Holmby homes for sale",
  img=("46-Neighborhood-Skyline.jpg", "Aerial view of the Little Holmby neighborhood in Westwood, Los Angeles"),
  lede="Little Holmby is a small, mostly single-family neighborhood in Westwood on LA's Westside, between UCLA and Holmby Hills. Homes here don't come up often. Here's a quick guide for buyers, plus a home that's available now.",
  body="""
<h2>Where is Little Holmby?</h2>
<p>Little Holmby sits in Westwood, in the 90024 zip code. It's generally described as bounded by Sunset Blvd, Beverly Glen Blvd, Santa Monica Blvd and the 405 freeway. Holmby Hills and Bel Air are to the north, and Century City and Beverly Hills are a short drive east.</p>
<h2>What's nearby</h2>
<ul>
<li><b>UCLA</b> and the UCLA medical campus</li>
<li><b>Westwood Village</b> shops, restaurants and theaters</li>
<li><b>Century City</b> offices and shopping</li>
<li><b>Beverly Hills</b>, <b>Holmby Hills</b> and <b>Bel Air</b></li>
<li>Quick access to the <b>405</b> and Wilshire Blvd</li>
</ul>
<h2>What homes are like</h2>
<p>The neighborhood is largely single-family residential, with tree-lined streets and a mix of older homes and newer rebuilds. Styles vary from street to street. One-story homes and homes with a guest house are less common, which is part of what makes 863 Manning Ave stand out.</p>
{FEATURE}
<h2>What to check before you buy in Little Holmby</h2>
<ul>
<li><b>Permits and zoning.</b> Confirm the permitted status of any additions or guest house with the City of Los Angeles (LADBS).</li>
<li><b>Inspections.</b> Many homes here are decades old. Plan for a general home inspection plus sewer line, roof and foundation checks.</li>
<li><b>Schools.</b> Confirm school assignments directly with LAUSD for the specific address.</li>
<li><b>Commute.</b> Test the drive to work at rush hour; the 405 and Wilshire corridor can be busy.</li>
<li><b>Insurance.</b> Get homeowners insurance quotes early; availability and cost in Los Angeles have changed in recent years.</li>
</ul>
<h2>Want a list of every Little Holmby home on the market?</h2>
<p>I can send you a current MLS list of homes for sale in Little Holmby and Westwood, including ones that are coming soon. Call or text (310) 849-9898 or <a href="mailto:samkw310@gmail.com">email me</a>.</p>
""",
  faq=[
   ("What zip code is Little Holmby in?", "Little Holmby is in Westwood, Los Angeles, in the 90024 zip code."),
   ("Where is Little Holmby in Los Angeles?", "It's a residential area of Westwood on LA's Westside, generally described as bounded by Sunset Blvd, Beverly Glen Blvd, Santa Monica Blvd and the 405 freeway, near UCLA, Holmby Hills and Bel Air."),
   ("Is there a home for sale in Little Holmby right now?", "Yes. 863 Manning Ave, a single-story 4 bed, 2.5 bath home with a mezzanine and a detached guest house, is offered at $4,650,000. The seller will consider a lease option or seller financing, subject to approval."),
   ("Can I get a list of other homes for sale in Little Holmby?", "Yes. Call or text Saman Alishahi at (310) 849-9898 for a current MLS list of Little Holmby and Westwood homes for sale."),
  ]),
 dict(slug="lease-option-los-angeles",
  title="Lease Option to Buy a Home in Los Angeles (Rent-to-Own) | How It Works",
  h1="Lease option to buy a home in Los Angeles: how rent-to-own works",
  desc="How a lease option (rent-to-own) works in Los Angeles: option fee, rent credit, term, the difference from a lease-purchase, risks to watch, and a Westwood home where the seller will consider one.",
  short="How a lease option works in Los Angeles",
  img=("01-Front-Exterior.jpg", "Front of 863 Manning Ave, a traditional home in Little Holmby, Westwood"),
  lede="A lease option lets you move into a home now and buy it later at a price agreed today. It can help if you need time to sell another property, build income history, or line up a loan. Here's how it generally works.",
  body="""
<h2>What is a lease option?</h2>
<p>A lease option combines two agreements: a <b>lease</b> of the home and an <b>option</b> to buy it. You pay the seller an <b>option fee</b> for the right, but not the obligation, to purchase at an agreed price within an agreed period. If you decide not to buy, you generally walk away and the seller keeps the option fee.</p>
<h2>The key terms you'll negotiate</h2>
<ul>
<li><b>Purchase price.</b> Usually fixed up front, so you know what you'll pay later.</li>
<li><b>Option fee.</b> Paid at the start. Whether it is credited toward the price, and whether any of it is refundable, depends entirely on the agreement.</li>
<li><b>Term.</b> How long you have to exercise the option, often one to three years.</li>
<li><b>Rent and rent credit.</b> Monthly rent, and whether any part of it is credited toward the purchase.</li>
<li><b>Repairs and maintenance.</b> Who handles what while you're living there.</li>
<li><b>How you exercise the option.</b> Written notice deadlines and closing timelines.</li>
</ul>
<h2>Lease option vs. lease-purchase</h2>
<p>With a <b>lease option</b> you have the right to buy but don't have to. With a <b>lease-purchase</b> you agree up front that you will buy, so walking away can mean breaching the contract. Make sure you know which one you're signing.</p>
<h2>Who a lease option can suit</h2>
<ul>
<li>Buyers who need to sell another home first</li>
<li>Self-employed buyers building the income history lenders want</li>
<li>Buyers relocating to Los Angeles who want to live in the area before committing</li>
<li>Buyers waiting on a bonus, equity event or 1031 exchange timing</li>
</ul>
<h2>Risks to watch</h2>
<ul>
<li>You can lose the option fee and any rent credit if you don't buy in time.</li>
<li>You'll usually still need a mortgage or cash at the end, so talk to a lender early.</li>
<li>Run a title search at the start, and ask your attorney about recording a memorandum of option to protect your rights.</li>
<li>Get every term in writing, and have a California real estate attorney review the agreement.</li>
</ul>
{FEATURE}
<h2>A lease option on a Westwood home</h2>
<p>The seller of 863 Manning Ave in Little Holmby will consider lease option proposals. No terms are pre-set; option fee, rent, any rent credit, price and term are negotiated case by case and require the seller's approval. Call or text (310) 849-9898 to discuss a proposal.</p>
""",
  faq=[
   ("Is rent-to-own available on higher-end homes in Los Angeles?", "Sometimes. It depends on the seller. The seller of 863 Manning Ave in Westwood, offered at $4,650,000, will consider lease option proposals, subject to approval."),
   ("Is the option fee refundable?", "Usually not, but it depends on the written agreement. Many agreements credit the option fee toward the price if you buy."),
   ("Does my rent count toward the purchase?", "Only if the agreement says so. Any rent credit is negotiated between buyer and seller."),
   ("Do I still need a mortgage at the end of a lease option?", "Usually yes, unless you pay cash or the seller agrees to carry financing. Talk to a lender early so you know what you'll need to qualify."),
   ("What is the difference between a lease option and a lease-purchase?", "A lease option gives you the right, but not the obligation, to buy. A lease-purchase obligates you to buy on the agreed terms."),
  ]),
 dict(slug="seller-financing-westwood",
  title="Seller Financing on a Westwood Home | Owner Will Carry | Los Angeles 90024",
  h1="Seller financing on a Westwood home",
  desc="How seller financing (owner will carry, seller carryback) works when buying a home in Westwood, Los Angeles: common structures, the paperwork, California disclosures, and a 90024 home where the seller will consider it.",
  short="Seller financing on a Westwood home",
  img=("43-Front-Lawn.jpg", "Front lawn and landscaping at 863 Manning Ave in Westwood"),
  lede="With seller financing, the seller acts as the lender for part or all of the price. It can open doors when bank loans are hard to get or slow. Here's how it generally works in California.",
  body="""
<h2>What is seller financing?</h2>
<p>Seller financing, also called owner financing, seller carryback or "owner will carry," means the seller lends you part of the purchase price. You sign a <b>promissory note</b> to the seller, secured by a <b>deed of trust</b> on the property, and make payments to the seller instead of (or in addition to) a bank.</p>
<h2>Common structures</h2>
<ul>
<li><b>Bank first loan + seller second.</b> A conventional or jumbo lender makes the first loan and the seller carries a smaller second. The first lender has to allow it.</li>
<li><b>Seller carries a larger share.</b> The seller finances most of the balance after your down payment, often with a balloon payment after a few years.</li>
<li><b>Short-term bridge.</b> The seller carries for a limited period while you sell another property or refinance.</li>
</ul>
<h2>Terms you'll negotiate</h2>
<ul>
<li>Down payment</li>
<li>Interest rate and payment schedule</li>
<li>Loan length and any balloon payment</li>
<li>Prepayment terms</li>
<li>What happens if a payment is late</li>
</ul>
<h2>The paperwork</h2>
<p>A seller-financed purchase normally closes through escrow with title insurance, like any other sale. The note and deed of trust are recorded, and the buyer's ability to repay is evaluated. In California, when an arranger of credit (such as a real estate agent) is involved in seller financing on a 1–4 unit home, a written seller financing disclosure statement is generally required (Cal. Civ. Code §2956 and following). Federal and state lending rules can also apply, so buyer and seller should each use their own attorney.</p>
{FEATURE}
<h2>Seller financing at 863 Manning Ave</h2>
<p>The seller of 863 Manning Ave in Little Holmby will consider carrying part of the financing for a qualified buyer. No down payment, rate or term has been set; any seller financing is negotiated individually and subject to the seller's approval. A bank first loan with a seller second will also be considered.</p>
""",
  faq=[
   ("What does 'owner will carry' mean?", "It means the seller may be willing to finance part of the purchase price. The buyer signs a promissory note secured by a deed of trust and makes payments to the seller."),
   ("Can I combine a bank loan with seller financing?", "Often, if the first-mortgage lender allows a seller second. Whether it works depends on the lender's guidelines, your qualifications and the seller's approval."),
   ("Is there a home in Westwood with seller financing?", "The seller of 863 Manning Ave, Los Angeles 90024, offered at $4,650,000, will consider carrying part of the financing for a qualified buyer, subject to approval."),
   ("How much down payment is needed for seller financing?", "There's no standard amount. It's negotiated between buyer and seller. For 863 Manning Ave, no down payment, rate or term has been set."),
  ]),
 dict(slug="westwood-home-with-guest-house",
  title="Westwood Home with Guest House for Sale | 863 Manning Ave, Los Angeles 90024",
  h1="Westwood home with a guest house for sale",
  desc="A single-story 4 bed, 2.5 bath home with a detached guest house in Little Holmby, Westwood (90024), offered at $4,650,000. What the guest house offers and what buyers should verify.",
  short="Westwood home with a guest house",
  img=("50-Aerial-Rear.jpg", "Aerial view of the rear yard at 863 Manning Ave in Westwood, Los Angeles"),
  lede="Homes in Westwood with a separate guest house are hard to find. 863 Manning Ave in Little Holmby has one: a detached guest house with French doors that open onto the lawn, behind a single-story main home.",
  body="""
<h2>The guest house at 863 Manning Ave</h2>
<ul>
<li>Detached from the main house</li>
<li>French doors opening onto the rear lawn</li>
<li>On a ~9,744 sq ft R1 lot with a rear patio, covered porch, mature landscaping and perimeter fencing</li>
</ul>
<p>See the guest house in the <a href="/#photos">photo gallery</a> and <a href="/#video">video tour</a>.</p>
<h2>How buyers use a guest house</h2>
<p>Depending on its permitted use, a guest house can work as a home office, a studio, a place for visiting family, or space for a caregiver or older child. Some buyers also look at rental use.</p>
<h2>What to verify</h2>
<ul>
<li><b>Permitted status and use.</b> Check permits with the City of Los Angeles (LADBS). Whether it can be used as a separate dwelling or rented depends on its permits and current rules.</li>
<li><b>Utilities and size.</b> Confirm how it's metered and its square footage during your inspection.</li>
<li><b>Insurance.</b> Make sure your homeowners policy covers the detached structure and any planned use.</li>
</ul>
{FEATURE}
<h2>The main house</h2>
<p>The main home is a 1949 traditional on one level with a mezzanine: 4 bedrooms, 2.5 baths (2 full, 1 half), about 2,849 sq ft, two fireplaces, central heating and air, hardwood floors, updated kitchen and baths and a tankless water heater. Parking is an attached carport plus a 2-car driveway. It's vacant, and the seller will consider a lease option or seller financing, subject to approval.</p>
""",
  faq=[
   ("Does 863 Manning Ave have a guest house?", "Yes, a detached guest house with French doors opening onto the lawn. Buyers should independently verify its permitted use and status with the City of Los Angeles."),
   ("Can the guest house be rented out?", "That depends on its permitted status and current City of Los Angeles rules. Buyers should verify with LADBS and their own advisors."),
   ("Where are homes with guest houses for sale in Westwood?", "863 Manning Ave in Little Holmby, Westwood (90024), offered at $4,650,000, includes a detached guest house. Call (310) 849-9898 for other Westwood options."),
  ]),
]

def nav_links(cur):
    return "".join(f'<li><a href="/{p["slug"]}/">{html.escape(p["short"])}</a></li>' for p in PAGES if p["slug"] != cur)

def build(p):
    url = f'{B}/{p["slug"]}/'
    img, alt = p["img"]
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in p["faq"])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": p["h1"], "description": p["desc"],
         "url": url, "mainEntityOfPage": url, "image": f"{B}/images/photos/{img}",
         "datePublished": TODAY, "dateModified": TODAY, "author": AGENT, "publisher": AGENT,
         "about": {"@id": f"{B}/#home"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "863 Manning Ave", "item": f"{B}/"},
            {"@type": "ListItem", "position": 2, "name": p["short"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]}
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p["title"])}</title>
<meta name="description" content="{html.escape(p["desc"])}">
<link rel="canonical" href="{url}">
<meta name="author" content="Saman Alishahi, CA DRE #01964365">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(p["title"])}">
<meta property="og:description" content="{html.escape(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{B}/images/photos/{img}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{json.dumps(ld, indent=1, ensure_ascii=False)}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
{STYLE}
{EXTRA_CSS}
</head>
<body>
<header class="bar">
  <div class="wrap">
    <a class="logo" href="/">863 Manning Ave</a>
    <nav>
      <a href="/#video">Video</a>
      <a href="/#photos">Photos</a>
      <a href="/#financing">Financing</a>
      <a href="/#contact">Contact</a>
      <a class="call" href="tel:+13108499898">Call (310) 849-9898</a>
    </nav>
  </div>
</header>
<main class="wrap">
<article class="art">
  <p class="crumbs"><a href="/">863 Manning Ave</a> › {html.escape(p["short"])}</p>
  <h1>{html.escape(p["h1"])}</h1>
  <p class="lede">{html.escape(p["lede"])}</p>
  <figure><img src="/images/photos/md/{img}" srcset="/images/photos/sm/{img} 640w, /images/photos/md/{img} 960w, /images/photos/{img} 1280w" sizes="(max-width: 800px) 100vw, 780px" alt="{html.escape(alt)}" width="1280" height="720" fetchpriority="high"><figcaption>863 Manning Ave, Little Holmby, Westwood</figcaption></figure>
  {p["body"].replace("{FEATURE}", FEATURE)}
  <h2>Questions &amp; answers</h2>
  {faq_html}
  <h2>More buyer guides</h2>
  <ul class="related">{nav_links(p["slug"])}<li><a href="/">863 Manning Ave listing: photos, video &amp; facts</a></li></ul>
  <p class="fine">{html.escape(DISCLAIM)}</p>
</article>
</main>
{FAB}
<footer>
  <div class="wrap">
    <p class="guides-foot"><a href="/">863 Manning Ave listing</a>{"".join(f'<a href="/{q["slug"]}/">{html.escape(q["short"])}</a>' for q in PAGES)}</p>
    <p>Saman Alishahi, Real Estate Broker, CA DRE #01964365, NMLS #2535168 · (310) 849-9898 · <a href="mailto:samkw310@gmail.com">samkw310@gmail.com</a></p>
    <p>Property information is from public records and a July 2026 appraisal, is deemed reliable but not guaranteed, and should be independently verified. Equal Housing Opportunity.</p>
  </div>
</footer>
</body>
</html>
"""
    d = ROOT / p["slug"]; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(out)
    return url

if __name__ == "__main__":
    for p in PAGES:
        print(build(p))
