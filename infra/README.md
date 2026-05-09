# Linket Agent — infra

Bootstrap files for the public install endpoints.

## `redirect-worker.js`

A 60-line Cloudflare Worker that powers `https://linket.com.br/install.sh`,
`/install.ps1`, `/install.cmd`, and `/docs`. It is a thin 302 redirector to
the canonical raw GitHub paths on `github.com/robertbr123/Linket-Agent`.

### One-time deploy

1. Buy / point the domain `linket.com.br` to Cloudflare (free plan is fine).
2. Cloudflare dashboard → **Workers & Pages → Create application → Worker**.
3. Replace the starter source with the contents of `redirect-worker.js`.
4. **Settings → Triggers → Custom domains → Add custom domain → `linket.com.br`**.
   (Optional: also add `get.linket.com.br` if you want a `get.` subdomain.)
5. Save & deploy.

### Verifying

```bash
curl -fsSLI https://linket.com.br/install.sh
# Should return: HTTP/2 302
# location: https://raw.githubusercontent.com/robertbr123/Linket-Agent/main/scripts/install.sh
```

If the `Location` header points where you expect, the install one-liner in
the README will Just Work.

### Pinning a branch / tag

Edit the `LINKET_BRANCH` constant at the top of `redirect-worker.js`. Use a
tag string (e.g. `"v0.13.0"`) when you want a stable install URL, or keep
`"main"` for rolling installs.

### Why a Worker and not a static `_redirects` file?

Cloudflare Pages and `_redirects` work too — the Worker is here because it
keeps everything in one file we can version-control alongside the code. If
you'd rather use Pages, the file you'd commit instead is `_redirects`:

```
/install.sh   https://raw.githubusercontent.com/robertbr123/Linket-Agent/main/scripts/install.sh   302
/install.ps1  https://raw.githubusercontent.com/robertbr123/Linket-Agent/main/scripts/install.ps1  302
/install.cmd  https://raw.githubusercontent.com/robertbr123/Linket-Agent/main/scripts/install.cmd  302
/             https://github.com/robertbr123/Linket-Agent#readme                                   302
```
