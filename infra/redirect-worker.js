/**
 * Linket Agent — install URL redirect worker
 * ----------------------------------------------------------------------------
 * Maps short, brand-domain URLs (https://linket.com.br/install.sh, etc.) to
 * the canonical raw GitHub paths. Lets us host the brand on linket.com.br
 * without baking raw.githubusercontent.com URLs into the install one-liner.
 *
 * Deploy:
 *   1. Cloudflare → Workers & Pages → Create → "Hello World" worker.
 *   2. Replace the worker source with this file.
 *   3. Settings → Triggers → Custom domain → linket.com.br (and any subdomains
 *      you want to serve installs from, e.g. get.linket.com.br).
 *   4. Optional: lock the upstream branch by setting LINKET_BRANCH below.
 *
 * Routing rules:
 *   /                → README on github.com/robertbr123/Linket-Agent (302)
 *   /install.sh      → raw install.sh on main                       (302)
 *   /install.ps1     → raw install.ps1 on main                      (302)
 *   /install.cmd     → raw install.cmd on main                      (302)
 *   /docs            → docs site (placeholder until Phase 8)        (302)
 *   /docs/*          → docs site under same path                    (302)
 *   anything else    → 404 with a small JSON body
 *
 * The redirects are 302 (not 301) so we can change the upstream owner / branch
 * without poisoning client caches.
 */

const REPO_OWNER = "robertbr123";
const REPO_NAME = "Linket-Agent";
const LINKET_BRANCH = "main"; // change to a tag (e.g. "v0.13.0") to pin
const RAW_BASE = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${LINKET_BRANCH}`;
const REPO_BASE = `https://github.com/${REPO_OWNER}/${REPO_NAME}`;

const ROUTES = new Map([
  ["/", `${REPO_BASE}#readme`],
  ["/install.sh", `${RAW_BASE}/scripts/install.sh`],
  ["/install.ps1", `${RAW_BASE}/scripts/install.ps1`],
  ["/install.cmd", `${RAW_BASE}/scripts/install.cmd`],
  // /docs and /docs/* are forwarded to the GitHub-rendered website folder
  // until the docs site (Phase 8) is published on its own host.
  ["/docs", `${REPO_BASE}/tree/${LINKET_BRANCH}/website/docs`],
]);

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";

    // Exact route match.
    const direct = ROUTES.get(path);
    if (direct) {
      return Response.redirect(direct, 302);
    }

    // /docs/<anything> → website/docs/<anything> on GitHub.
    if (path.startsWith("/docs/")) {
      const sub = path.slice("/docs/".length);
      return Response.redirect(`${REPO_BASE}/tree/${LINKET_BRANCH}/website/docs/${sub}`, 302);
    }

    return new Response(
      JSON.stringify({
        error: "not_found",
        path,
        known_routes: Array.from(ROUTES.keys()).concat(["/docs/<path>"]),
        repo: REPO_BASE,
      }, null, 2),
      {
        status: 404,
        headers: { "content-type": "application/json; charset=utf-8" },
      },
    );
  },
};
