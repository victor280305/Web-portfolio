import html
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


timeline_items = [
    ("Week 1", "Lead developer planning", "Served as lead developer, organized the front-end work, and clarified how the main project screens would connect across the app."),
    ("Week 2", "map.tsx implementation", "Worked on map.tsx, focusing on the map screen structure, route visibility, and how location-based project information should be presented."),
    ("Week 3", "schedule.tsx implementation", "Worked on schedule.tsx, building the schedule view so users could scan project activities, times, and planned tasks clearly."),
    ("Week 4", "layout.tsx integration", "Worked on layout.tsx to connect navigation, page structure, and shared layout behavior across the project."),
    ("Week 5", "Lead review and coordination", "Reviewed front-end consistency, helped align team contributions, and checked that the project screens worked together smoothly."),
]

matlab_certificates = [
    ("MATLAB Onramp", "matlab-onramp.png", "Completed"),
    ("Explore Data", "explore-data.png", "Completed"),
    ("Calculation with Vectors", "calculation-with-vectors.png", "Completed"),
    ("Make and Manipulate Matrices", "make-and-manipulate-matrices.png", "Completed"),
    ("The How and Why", "how-and-why.png", "Completed"),
    ("Certificate 6", None, "Pending upload"),
    ("Certificate 7", None, "Pending upload"),
    ("Certificate 8", None, "Pending upload"),
]

blog_posts = [
    ("Loops and Summation", "Total Cost = sum(Q_i x P_i) + Overheads", "Loops repeat the same engineering calculation across many materials."),
    ("Functions", "Efficiency = Useful Output Power / Input Power", "Functions keep formulas separate, reusable, and easier to test."),
    ("Conditional Logic", "If V > V_max, status = unsafe", "Conditions help an app reject unsafe or incomplete values."),
]

commits = [
    ("map.tsx", "Lead development work on the map screen"),
    ("schedule.tsx", "Schedule page implementation and task display"),
    ("layout.tsx", "Shared app layout and navigation structure"),
]

pull_requests = [
    ("Lead role", "Coordinated front-end responsibilities"),
    ("Review", "Checked screen consistency and usability"),
    ("Merge prep", "Prepared layout, map, and schedule work for integration"),
]


def esc(value):
    return html.escape(str(value), quote=True)


def build_page():
    certs = [
        {
            "course": course,
            "preview": f"/assets/certificates/{preview}" if preview else "",
            "status": status,
        }
        for course, preview, status in matlab_certificates
    ]
    first_cert = next((cert for cert in certs if cert["preview"]), certs[0])

    timeline_html = "".join(
        f"""
        <article class="card timeline-card">
          <span class="eyebrow">{esc(week)}</span>
          <h3>{esc(title)}</h3>
          <p>{esc(body)}</p>
        </article>
        """
        for week, title, body in timeline_items
    )

    cert_cards = []
    for index, cert in enumerate(certs, 1):
        if cert["preview"]:
            preview = f'<img src="{esc(cert["preview"])}" alt="{esc(cert["course"])} certificate preview">'
            disabled = ""
        else:
            preview = "<span>Pending upload</span>"
            disabled = "disabled"
        cert_cards.append(
            f"""
            <button class="cert-card" type="button" data-course="{esc(cert["course"])}" data-preview="{esc(cert["preview"])}" {disabled}>
              <div class="cert-thumb">{preview}</div>
              <strong>{index:02d}. {esc(cert["course"])}</strong>
              <span>{esc(cert["status"])}</span>
            </button>
            """
        )
    cert_cards_html = "".join(cert_cards)

    blog_html = "".join(
        f"""
        <article class="card blog-card">
          <h3>Confidence in {esc(title)}</h3>
          <div class="formula"><span>S</span>{esc(formula)}</div>
          <p>{esc(body)}</p>
        </article>
        """
        for title, formula, body in blog_posts
    )

    commit_items = "".join(f"<li><strong>{esc(name)}</strong><span>{esc(body)}</span></li>" for name, body in commits)
    pr_items = "".join(f"<li><strong>{esc(name)}</strong><span>{esc(body)}</span></li>" for name, body in pull_requests)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mariano Makai | Web Portfolio 2026</title>
  <link rel="icon" href="data:,">
  <style>
    :root {{
      --cyan: #00f0ff;
      --cyan-soft: #0dbec7;
      --bg: #070b0d;
      --header: #030505;
      --panel: #11181b;
      --text: #f8fafc;
      --muted: #a9b7bc;
      --line: #2d444a;
    }}

    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.5;
    }}

    header {{
      position: sticky;
      top: 0;
      z-index: 10;
      background: var(--header);
      border-bottom: 1px solid var(--line);
      padding: 14px 34px;
    }}

    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      flex-wrap: wrap;
    }}

    .brand {{
      color: var(--text);
      font-size: 20px;
      font-weight: 800;
      text-decoration: none;
    }}

    .brand span, h1 span, h2 span, .accent {{ color: var(--cyan); }}
    nav {{ display: flex; gap: 4px; flex-wrap: wrap; }}
    nav a {{
      color: var(--text);
      text-decoration: none;
      font-size: 12px;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 4px;
    }}
    nav a:hover, nav a:focus {{ color: var(--cyan); background: #082d31; }}

    main {{ padding: 34px; max-width: 1210px; }}
    section {{ padding: 18px 0 34px; border-bottom: 1px solid var(--line); scroll-margin-top: 84px; }}
    section:last-child {{ border-bottom: 0; }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{ font-size: 54px; line-height: 1.05; margin-bottom: 16px; }}
    h2 {{ font-size: 30px; margin-bottom: 4px; }}
    h3 {{ font-size: 18px; margin-bottom: 10px; }}
    p {{ color: var(--muted); }}

    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 370px;
      gap: 26px;
      align-items: center;
      background: #0a1012;
      border: 1px solid var(--cyan-soft);
      border-radius: 4px;
      padding: 30px;
      margin-bottom: 18px;
    }}
    .pill {{
      display: inline-flex;
      color: var(--cyan);
      border: 1px solid var(--cyan-soft);
      background: #062f33;
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 14px;
    }}
    .stats, .role-grid, .cert-grid, .evidence-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .stat {{
      width: 150px;
      min-height: 64px;
      border: 1px solid var(--line);
      background: #0f1d20;
      border-radius: 4px;
      padding: 10px;
    }}
    .stat strong {{ display: block; color: var(--cyan); font-size: 22px; }}
    .stat span {{ color: var(--muted); font-size: 11px; }}

    .portrait {{
      overflow: hidden;
      border: 2px solid var(--cyan-soft);
      border-radius: 4px;
      background: #101415;
      margin: 0;
    }}
    .portrait img {{ display: block; width: 100%; height: 315px; object-fit: cover; }}
    .portrait-caption {{ background: #050707; padding: 12px 14px; }}
    .portrait-caption strong {{ display: block; color: var(--cyan); }}

    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 18px;
    }}
    .role-card {{ width: 360px; min-height: 120px; border-color: var(--cyan-soft); }}
    .role-card strong {{ color: var(--cyan); font-size: 16px; }}
    .timeline-card {{ max-width: 900px; margin-bottom: 12px; }}
    .eyebrow {{ color: var(--cyan); font-size: 13px; font-weight: 800; }}

    .cert-viewer {{
      display: grid;
      grid-template-columns: minmax(0, 690px) 330px;
      gap: 22px;
      align-items: start;
      max-width: 1080px;
      margin-bottom: 16px;
    }}
    .cert-viewer-frame {{
      height: 500px;
      background: #080d0f;
      border: 1px solid var(--cyan-soft);
      border-radius: 4px;
      display: grid;
      place-items: center;
      overflow: hidden;
    }}
    .cert-viewer-frame img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      background: white;
    }}
    .cert-card {{
      width: 315px;
      min-height: 305px;
      text-align: left;
      color: var(--text);
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 18px;
      cursor: pointer;
      font: inherit;
    }}
    .cert-card:hover:not(:disabled), .cert-card:focus:not(:disabled) {{ border-color: var(--cyan); }}
    .cert-card:disabled {{ cursor: default; opacity: .72; }}
    .cert-card strong, .cert-card span {{ display: block; }}
    .cert-card span {{ color: var(--muted); font-size: 12px; }}
    .cert-thumb {{
      height: 178px;
      background: #0f1517;
      border: 1px solid var(--line);
      border-radius: 4px;
      display: grid;
      place-items: center;
      overflow: hidden;
      margin-bottom: 12px;
    }}
    .cert-thumb img {{ width: 100%; height: 100%; object-fit: contain; background: white; }}

    .blog-layout {{
      display: grid;
      grid-template-columns: minmax(0, 640px) 360px;
      gap: 20px;
      align-items: start;
      max-width: 1040px;
    }}
    .blog-card {{ margin-bottom: 16px; }}
    .formula {{
      border: 1px solid var(--cyan);
      border-radius: 4px;
      background: #0f1517;
      padding: 12px 14px;
      color: var(--text);
      font-size: 13px;
      font-weight: 700;
      overflow-wrap: anywhere;
    }}
    .formula span {{ color: var(--cyan); font-size: 22px; margin-right: 12px; }}
    .video-panel {{ position: sticky; top: 90px; }}
    .video-frame {{
      background: #071011;
      border: 1px solid var(--cyan);
      border-radius: 4px;
      padding: 8px;
    }}
    video {{
      display: block;
      width: 100%;
      aspect-ratio: 16 / 9;
      background: #000;
      border-radius: 4px;
    }}

    .evidence-grid .card {{ width: 430px; }}
    li {{ margin-bottom: 10px; color: var(--muted); }}
    li strong {{ display: block; color: var(--text); }}
    input, textarea {{
      width: 100%;
      color: var(--text);
      background: #0f1517;
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 12px;
      margin-bottom: 10px;
      font: inherit;
    }}
    button.submit {{
      background: var(--cyan);
      color: var(--bg);
      border: 0;
      border-radius: 4px;
      padding: 11px 18px;
      font-weight: 800;
    }}

    @media (max-width: 900px) {{
      main, header {{ padding-left: 18px; padding-right: 18px; }}
      h1 {{ font-size: 42px; }}
      .hero, .cert-viewer, .blog-layout {{ grid-template-columns: 1fr; }}
      .role-card, .cert-card {{ width: 100%; }}
      .video-panel {{ position: static; }}
      .cert-viewer-frame {{ height: 360px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="topbar">
      <a class="brand" href="#home">Mariano Makai<span>.</span></a>
      <nav aria-label="Portfolio sections">
        <a href="#home">Home</a>
        <a href="#timeline">Timeline</a>
        <a href="#matlab">MATLAB</a>
        <a href="#blog">Blog</a>
        <a href="#github">GitHub</a>
        <a href="#contact">Contact</a>
      </nav>
    </div>
  </header>

  <main>
    <section id="home">
      <div class="hero">
        <div>
          <span class="pill">Lead Developer | Web Portfolio 2026</span>
          <h3>Hello, It's Me</h3>
          <h1><span>Mariano Makai</span></h1>
          <h3>I'm an <span class="accent">Electrical Engineering Student</span></h3>
          <p>Lead developer for the group project, assigned to map.tsx, schedule.tsx, and layout.tsx. This web portfolio follows the Web Portfolio 2026 PDF with project timeline, MATLAB certificates, technical blog/video evidence, and GitHub documentation.</p>
          <div class="stats">
            <div class="stat"><strong>5</strong><span>Timeline entries</span></div>
            <div class="stat"><strong>5</strong><span>Certificates added</span></div>
            <div class="stat"><strong>3</strong><span>Key TSX files</span></div>
          </div>
        </div>
        <figure class="portrait">
          <img src="/assets/profile-hero.jpeg" alt="Mariano Makai portrait">
          <figcaption class="portrait-caption"><strong>Electrical Engineering</strong><span>Computer Programming I Portfolio</span></figcaption>
        </figure>
      </div>
      <div class="role-grid">
        <article class="card role-card"><strong>map.tsx</strong><p>Map screen structure and location-based project view.</p></article>
        <article class="card role-card"><strong>schedule.tsx</strong><p>Schedule screen for activities, times, and planned tasks.</p></article>
        <article class="card role-card"><strong>layout.tsx</strong><p>Shared navigation and page layout for the application.</p></article>
      </div>
    </section>

    <section id="timeline">
      <h2>Project <span>Timeline</span></h2>
      <p>Weekly log of Mariano's specific contributions.</p>
      {timeline_html}
    </section>

    <section id="matlab">
      <h2>MATLAB <span>Achievement Hub</span></h2>
      <p>Certificates are viewed directly inside the portfolio web view.</p>
      <div class="card cert-viewer">
        <div class="cert-viewer-frame">
          <img id="certificatePreview" src="{esc(first_cert["preview"])}" alt="{esc(first_cert["course"])} certificate">
        </div>
        <div>
          <h3 class="accent">Certificate Viewer</h3>
          <h3 id="certificateTitle">{esc(first_cert["course"])}</h3>
          <p>The selected certificate is displayed here inside the page. Use the cards below to switch certificates without opening a new page.</p>
        </div>
      </div>
      <div class="cert-grid">{cert_cards_html}</div>
    </section>

    <section id="blog">
      <h2>Technical <span>Blog</span></h2>
      <p>Confidence in Concepts posts with notation and an embedded local video player.</p>
      <div class="blog-layout">
        <div>{blog_html}</div>
        <aside class="video-panel">
          <div class="video-frame">
            <video controls preload="metadata">
              <source src="/assets/blog-video.mp4" type="video/mp4">
              Your browser does not support embedded video playback.
            </video>
          </div>
          <h3 class="accent">Embedded Blog Video</h3>
          <p>The video plays directly inside this portfolio page from the local assets folder.</p>
        </aside>
      </div>
    </section>

    <section id="github">
      <h2>GitHub <span>Evidence</span></h2>
      <p>Commit history, pull request logs, reviews, merges, and impact summary.</p>
      <div class="evidence-grid">
        <article class="card"><h3 class="accent">Commit History</h3><ul>{commit_items}</ul></article>
        <article class="card"><h3 class="accent">Pull Request Logs</h3><ul>{pr_items}</ul></article>
      </div>
      <article class="card" style="max-width: 900px; margin-top: 14px;">
        <h3 class="accent">Impact Summary</h3>
        <p>Mariano's lead developer work helped the group project function as a coherent application. His assigned work on map.tsx, schedule.tsx, and layout.tsx supported navigation, location-based project views, and planned activity displays used by the engineering modules.</p>
      </article>
    </section>

    <section id="contact">
      <h2>Contact <span>Evidence Notes</span></h2>
      <p>Reference-style contact block adapted for portfolio submission notes.</p>
      <div class="evidence-grid">
        <form class="card">
          <input aria-label="Your Name" placeholder="Your Name">
          <input aria-label="Your Email" placeholder="Your Email">
          <textarea aria-label="Evidence Note" rows="4" placeholder="Evidence Note"></textarea>
          <button class="submit" type="button">Submit</button>
        </form>
        <article class="card"><h3 class="accent">Submission Checklist</h3><p>Replace GitHub placeholders</p><p>Add remaining MathWorks certificates</p><p>Add real weekly project evidence</p><p>Confirm video plays in the Blog section</p></article>
      </div>
    </section>
  </main>

  <script>
    const preview = document.getElementById("certificatePreview");
    const title = document.getElementById("certificateTitle");
    document.querySelectorAll(".cert-card[data-preview]").forEach((card) => {{
      card.addEventListener("click", () => {{
        if (!card.dataset.preview) return;
        preview.src = card.dataset.preview;
        preview.alt = `${{card.dataset.course}} certificate`;
        title.textContent = card.dataset.course;
        document.getElementById("matlab").scrollIntoView({{ behavior: "smooth", block: "start" }});
      }});
    }});
  </script>
</body>
</html>"""


os.makedirs("assets", exist_ok=True)
os.makedirs("assets/certificates", exist_ok=True)

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get("/", response_class=HTMLResponse)
async def portfolio_home():
    return HTMLResponse(build_page())


if __name__ == "__main__":
    import uvicorn

    os.makedirs("assets", exist_ok=True)
    os.makedirs("assets/certificates", exist_ok=True)
   uvicorn.run(app, host="0.0.0.0", port=10000)
