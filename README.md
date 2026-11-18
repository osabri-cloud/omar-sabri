# Dr. Omar Sabri — academic dashboard

A free website on GitHub Pages. GitHub Actions refreshes the Google Scholar figures through SerpAPI every day.

## What's in this folder

| File | What it does |
|---|---|
| `index.html` | The website. It reads its numbers from `scholar.json`. |
| `scholar.json` | Google Scholar data (citations, h-index, i10-index, citations per year, papers). Replaced automatically every day. |
| `update_scholar.py` | Fetches the Scholar profile (ID `XtvII74AAAAJ`) from SerpAPI and rewrites `scholar.json`. |
| `.github/workflows/update-scholar.yml` | Runs the script every day at 02:17 UTC (05:17 Jazan time) and saves the result. |

## One-time setup (about 10 minutes)

1. **Get a free SerpAPI key.** Sign up at https://serpapi.com/users/sign_up. Then copy your key from https://serpapi.com/manage-api-key. The free plan includes 250 searches a month, and a daily update uses about 30.
2. **Create a GitHub account** at https://github.com if you don't have one.
3. **Create a public repository.** Choose **New repository**. A good name is `omar-sabri`. Set it to **Public** and click **Create repository**.
4. **Upload the files.** On the new repository page, click **uploading an existing file**. Drag in *everything* from this folder, including the `.github` folder. Then click **Commit changes**.
   - The `.github` folder can be hidden in Finder or File Explorer. On a Mac, press Cmd+Shift+. to show it. On Windows, go to View → Show → Hidden items.
   - If dragging doesn't upload `.github/workflows/update-scholar.yml`, create it by hand. Choose **Add file → Create new file**, type `.github/workflows/update-scholar.yml` as the name, paste in the file's contents, and commit.
5. **Add the SerpAPI key as a secret.** In the repository, go to **Settings → Secrets and variables → Actions → New repository secret**. Set the name to `SERPAPI_KEY` and the value to your key, then click **Add secret**.
6. **Turn on GitHub Pages.** Go to **Settings → Pages**. Under *Build and deployment*, set the source to **Deploy from a branch**, the branch to **main** and the folder to **/ (root)**, then click **Save**.
   About a minute later the site is live at `https://YOUR-USERNAME.github.io/omar-sabri/`.
7. **Run the first update by hand.** Go to **Actions → Update Google Scholar data → Run workflow**. A green tick means it worked. The site shows the new numbers and the date in "Last updated".

After that, the update runs by itself every day.

## Editing content

- **CV text** (roles, teaching, leadership, education, skills) lives in plain HTML in `index.html`. Edit it on GitHub with the pencil icon.
- **Papers that aren't on Google Scholar yet**, such as in-press articles, go in the `EXTRA` list near the bottom of `index.html`. Once Scholar lists a paper, the copy in `EXTRA` is skipped automatically.
- **Preferred links for particular papers** go in the `LINKS` list next to `EXTRA`.

## If something goes wrong

- **The Actions run is red:** open it to see the message. "SERPAPI_KEY is not set" means step 5 was missed. "SerpAPI error: …" usually means the key is wrong or the monthly allowance is used up.
- **A failed run never wipes the site.** When the response is empty or broken, the script keeps the previous data.
- **GitHub pauses scheduled workflows** in repositories with no activity for 60 days. The daily commits normally prevent that. If it does happen, click **Enable workflow** on the Actions tab.
