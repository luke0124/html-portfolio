#!/usr/bin/env python3
"""Generate terms-conditions.html and privacy-policy.html.

Edit the text below and re-run:  python3 manterfield/_build/build_legal.py
"""
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "27 November 2026"
CO = "Manterfield Building &amp; Roofing Ltd"
EMAIL = "manterfield1@btinternet.com"

HEAD = '''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Manterfield Building &amp; Roofing</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#221c29">
  <link rel="icon" href="images/favicon-round.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css?v=29">
</head>
<body data-page="legal">
  <a class="skip" href="#main">Skip to content</a>
  <main id="main">
    <section class="page-hero">
      <div class="wrap">
        <span class="crumb reveal">Legal</span>
        <h1 class="reveal">{h1}</h1>
        <p class="reveal">Last updated: {updated}</p>
      </div>
    </section>
    <section class="pad" style="padding-top:0">
      <div class="wrap"><div class="legal">
'''
TAIL = '''      </div></div>
    </section>
  </main>
  <script src="js/main.js?v=14"></script>
</body>
</html>
'''


def page(fname, title, h1, desc, body):
    html = HEAD.format(title=title, h1=h1, desc=desc, updated=UPDATED) + body + TAIL
    with open(os.path.join(SITE, fname), "w") as f:
        f.write(html)


TERMS = f'''
        <p>These terms explain how you may use this website. By using it you agree to them. If you do not agree, please do not use the site.</p>

        <h2>1. About us</h2>
        <p>This website is run by {CO} ("we", "us", "our"), a company registered in England and Wales, company number 08779779, VAT number 184 2696 75. Our registered office is 259a Pontefract Road, Cudworth, Barnsley, South Yorkshire S72 8AQ. You can contact us on 01226 781344 or at <a class="inline-link" href="mailto:{EMAIL}">{EMAIL}</a>.</p>

        <h2>2. Using this website</h2>
        <p>You may view this website and its pages for your own personal or business use, to find out about us and to get in touch. You must not misuse it. In particular, you must not try to interfere with how it works, try to gain unauthorised access to it or its servers, or use it to send us anything unlawful, abusive or misleading.</p>

        <h2>3. Information on this website</h2>
        <p>We try to make sure the information on this site is accurate and up to date, but we do not promise that it is complete or free from error. Descriptions of our services, project photographs and project descriptions are examples of the kind of work we do. They are not a promise that we will deliver the same result, specification, cost or timescale on your property.</p>
        <p>Nothing on this website is professional, legal, structural or planning advice. Every property is different, so please speak to us about your own project.</p>

        <h2>4. Quotes and work for customers</h2>
        <p>This website is not an offer to carry out work, and using it does not create a contract between you and us. We offer free, no-obligation quotations. Any work we do for you will be carried out under the written quotation or contract we agree with you, and the terms of that quotation or contract will apply to that work. If those terms conflict with these website terms, the quotation or contract terms win.</p>

        <h2>5. Our content and intellectual property</h2>
        <p>The text, photographs, video, logo and design of this website belong to us or to the people who license them to us, and are protected by copyright and other laws. You may view the site and, if you wish, print or share a page for your own non-commercial use, but you must not copy, reproduce, republish or use our content or logo for any other purpose without our written permission.</p>
        <p>The names and logos of other organisations shown on this site, such as the Federation of Master Builders, belong to those organisations and are used to show our membership or accreditation.</p>

        <h2>6. Customer reviews and third-party content</h2>
        <p>The reviews shown on this website are reviews that customers have chosen to post publicly, for example on Google. We show them as written. If you posted a review and would like it removed from this website, please contact us.</p>

        <h2>7. Links to other websites</h2>
        <p>This website links to other websites, such as Google, Facebook, Instagram and the Federation of Master Builders. We do not control these websites and are not responsible for their content or how they use your information. Using them is at your own risk, and their own terms and privacy policies apply.</p>

        <h2>8. Our responsibility to you</h2>
        <p>We do not exclude or limit our liability for death or personal injury caused by our negligence, for fraud or fraudulent misrepresentation, or for anything else that the law does not allow us to exclude or limit.</p>
        <p>Subject to that, this website is provided "as is". We are not liable for any loss or damage you suffer because you used or relied on this website, or because it was unavailable, contained an error, or was affected by a virus or similar problem. This does not affect any of your legal rights as a consumer, or any rights you have under a contract with us for building or roofing work.</p>

        <h2>9. Changes to the website and these terms</h2>
        <p>We may change this website, and these terms, at any time. The date at the top of this page shows when the terms were last updated. By continuing to use the website after a change, you accept the updated terms.</p>

        <h2>10. Which law applies</h2>
        <p>These terms, and any dispute about them or this website, are governed by the law of England and Wales, and the courts of England and Wales have jurisdiction. If you are a consumer, this does not take away any right you have to bring proceedings in the courts of the part of the United Kingdom where you live.</p>

        <h2>11. Contact us</h2>
        <p>If you have any question about these terms, please email <a class="inline-link" href="mailto:{EMAIL}">{EMAIL}</a>, call 01226 781344, or write to us at 259a Pontefract Road, Cudworth, Barnsley, South Yorkshire S72 8AQ.</p>
'''

PRIVACY = f'''
        <p>This policy explains how {CO} ("we", "us", "our") collects and uses your personal information when you visit this website, contact us, or ask us for a quote or work. We take your privacy seriously and only use your information in ways the law allows.</p>

        <h2>1. Who we are</h2>
        <p>We are the "data controller" for the information described in this policy. Our registered office is 259a Pontefract Road, Cudworth, Barnsley, South Yorkshire S72 8AQ (company number 08779779). To ask a question about your information, contact us at <a class="inline-link" href="mailto:{EMAIL}">{EMAIL}</a> or on 01226 781344.</p>

        <h2>2. What information we collect</h2>
        <ul>
          <li><strong>When you contact us or ask for a quote</strong> (by phone, email, the enquiry form on this site, social media, or in person): your name, email address, phone number, the address of the property, and anything you tell us about your project.</li>
          <li><strong>If you become a customer:</strong> the details above plus information we need to do the work and run our business, such as quotations, plans, correspondence, site photographs, invoices, payment records and any insurance or guarantee paperwork.</li>
          <li><strong>When you visit this website:</strong> very little. We do not ask you to create an account, and we do not use analytics or advertising cookies on this site. Our website host may keep standard server records, such as your IP address, browser type and the pages you requested, for security and to keep the site running.</li>
        </ul>

        <h2>3. The enquiry form on this website</h2>
        <p>When you fill in the enquiry form and press "Send enquiry", your name, email address, phone number (if you give one), the service you are interested in and your message are emailed to us by the website's hosting server. We do not store them on the website, and we use them only to reply to you and handle your enquiry, as described in this policy. If you would rather not use the form, you can phone or email us instead.</p>

        <h2>4. How we use your information, and our legal reasons</h2>
        <ul>
          <li><strong>To reply to your enquiry, arrange a visit and prepare a quotation.</strong> This is necessary to take steps at your request before entering into a contract, and is in our legitimate interest in responding to people who contact us.</li>
          <li><strong>To carry out work and look after you as a customer</strong>, including scheduling, invoicing and aftercare. This is necessary to perform our contract with you.</li>
          <li><strong>To keep records and meet legal duties</strong>, such as tax, accounting and insurance requirements. This is a legal obligation.</li>
          <li><strong>To run and protect our business</strong>, for example keeping our website secure, dealing with complaints or disputes, and keeping evidence of our work. This is in our legitimate interests.</li>
          <li><strong>To show examples of our work</strong> on this website and our social media (see section 7). This is in our legitimate interests in promoting our business, and we will respect any request to remove a photograph.</li>
        </ul>
        <p>We do not sell your information, and we do not use it to make automated decisions about you. We will only send you marketing if you have asked us to.</p>

        <h2>5. Who we share your information with</h2>
        <p>We only share your information where we need to, with:</p>
        <ul>
          <li>subcontractors, tradespeople and suppliers who help us carry out your work;</li>
          <li>our accountants, insurers and professional advisers;</li>
          <li>building control, planning authorities and similar bodies, where your project needs them;</li>
          <li>our IT, email and website hosting providers, who handle information on our behalf; and</li>
          <li>the police, courts or other authorities, if the law requires it.</li>
        </ul>

        <h2>6. Cookies and other websites</h2>
        <p>This website does not set cookies of its own for tracking or advertising. However, some content on the site is provided by Google, which may receive information such as your IP address and browser details when the content loads:</p>
        <ul>
          <li>the website text is displayed using fonts supplied by Google Fonts; and</li>
          <li>the Contact page shows a Google Map, which may set cookies and collect information under Google's own privacy policy.</li>
        </ul>
        <p>This website also links to other sites, such as Google reviews, Facebook, Instagram and the Federation of Master Builders. Those sites have their own privacy policies, and we are not responsible for how they use your information.</p>

        <h2>7. Photographs and reviews on this website</h2>
        <p>We photograph our projects, including work in progress, and show some of these photographs on this website and our social media. We try to avoid showing people's faces, house numbers and vehicle number plates. If you or your property appear in a photograph and you would like it blurred or removed, email us and we will deal with it promptly.</p>
        <p>The customer reviews on this website were posted publicly by customers, for example on Google, and are shown with the name that appeared on the review. If you would like your review taken off this website, please contact us.</p>

        <h2>8. How long we keep your information</h2>
        <ul>
          <li><strong>Enquiries that do not lead to work:</strong> up to 12 months, then deleted.</li>
          <li><strong>Customer records, quotations, invoices and project files:</strong> up to six years after the work finishes, so we can meet tax and accounting rules and deal with any claim or guarantee issue.</li>
          <li><strong>Project photographs:</strong> kept for as long as we use them to show our work, unless you ask us to remove them.</li>
        </ul>
        <p>We may keep information for longer if the law requires it or we need it to deal with a dispute.</p>

        <h2>9. Keeping your information safe</h2>
        <p>We take sensible steps to protect your information, including keeping it in password-protected systems and only letting people who need it see it. No system is completely secure, so please take care about what you send us by email.</p>

        <h2>10. Your rights</h2>
        <p>Under UK data protection law you have the right to:</p>
        <ul>
          <li>ask for a copy of the personal information we hold about you;</li>
          <li>ask us to correct anything that is wrong or incomplete;</li>
          <li>ask us to delete your information, in some circumstances;</li>
          <li>ask us to restrict how we use your information, in some circumstances;</li>
          <li>object to us using your information where we rely on our legitimate interests; and</li>
          <li>ask for your information in a portable format, in some circumstances.</li>
        </ul>
        <p>To use any of these rights, email <a class="inline-link" href="mailto:{EMAIL}">{EMAIL}</a>. We will reply within one month. You will not normally have to pay a fee.</p>

        <h2>11. Complaints</h2>
        <p>If you are unhappy with how we have handled your information, please tell us first so we can put it right. You also have the right to complain to the Information Commissioner's Office (ICO), the UK's data protection regulator, at <a class="inline-link" href="https://ico.org.uk/make-a-complaint/" target="_blank" rel="noopener">ico.org.uk</a> or on 0303 123 1113.</p>

        <h2>12. Changes to this policy</h2>
        <p>We may update this policy from time to time. The date at the top of this page shows when it was last changed.</p>
'''

page("terms-conditions.html", "Terms & Conditions", "Terms &amp; Conditions",
     "The terms for using the Manterfield Building & Roofing website.", TERMS)
page("privacy-policy.html", "Privacy Policy", "Privacy Policy",
     "How Manterfield Building & Roofing collects and uses your personal information.", PRIVACY)
print("legal pages written")

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo
seo.apply()
