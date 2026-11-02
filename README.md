# Pitch Smart ⚽

Soccer positioning for 11–13 year olds, plus a coach's lineup and match-day manager.
Works in 7 v 7, 8 v 8, 9 v 9 and 11 v 11.

**Web app:** https://davepomerlo.github.io/pitch-smart/
**Android app:** [download pitch-smart.apk](https://github.com/davepomerlo/pitch-smart/releases/latest/download/pitch-smart.apk)

| Tab | What it does |
|---|---|
| **Learn** | Drag the ball and watch the whole team shift: wide when we have the ball, compact when they do, the nearest player pressing, nobody offside. Tap a player to read their job. Show opponents (✖), team lines and the offside line. **Set pieces**: corners, free kicks (central and wide) and throw-ins, ours or theirs, left or right side, with each player's job and the defensive wall. |
| **Play** | "Where should I stand?" 10 rounds: you get a position and a situation (open play, set pieces or a mix) and tap or drag yourself to the right spot. Points, an explanation, and a best score per team size. |
| **Coach** | **Squad** (names, numbers, positions, absent/available), **Lineup** (formation, tap-to-place, auto-fill, bench) and **Match** (clock with halves/quarters, score and scorers, planned subs made at the next stoppage, minutes played per player with a fair-share bar, match log and a copyable match report). |

Everything is saved on the device. **Squad → Backup** copies all coach data as text so you can
move it to another phone or browser (**Restore from backup** there).

## Android app

GitHub builds a real Android app from this repository every time the app's files change.

- Open the download link above on the phone, then open the downloaded file. Android asks
  once to allow installing apps from Chrome.
- When a newer build exists, the app shows "A new version of the app is ready" with a
  download link. Installing it replaces the old one and keeps your squad and lineups.
- Built with [Capacitor](https://capacitorjs.com) 8 from the `docs/` folder by
  `.github/workflows/android.yml`; the Android project is generated fresh in each build.
  `android-build/` holds the icon script, the version-number script and the signing key.
- The signing key is committed to this public repo with its password, so anyone could
  sign an app that installs over yours. That's fine for a personal app, but only ever
  install the APK from this repository's Releases page.

## Use it as an app on your phone (browser version)

The page is an installable web app: home-screen icon, full screen, and it works offline
at the pitch once it has been opened once.

- **Android:** open it in **Chrome** → tap **Install app** at the top of the page
  (or ⋮ menu → *Install app* / *Add to Home screen*).
- **iPhone:** open it in **Safari** → Share → **Add to Home Screen**.
- **Mac/PC:** Chrome or Edge show an install icon in the address bar.

Long-pressing the icon (Android) offers *Play* and *Match day* shortcuts.

## Set up (already done for this repo)

1. **Settings → Pages** → Source: *Deploy from a branch* → Branch `main`, folder `/docs` → Save.
2. **Actions → Build Android app → Run workflow** builds the APK (about 10 minutes) and
   publishes it as the latest Release.

## Working on it

Everything is in `docs/index.html` (one file: page, styles and script).

```bash
cd docs && python -m http.server     # view at http://localhost:8000
```

When you change anything in `docs/`, bump `VERSION` in `docs/sw.js` so installed web-app
copies pick up the new version on their next launch. Pushing to `main` rebuilds the
Android app automatically.

```
docs/index.html             the whole app
docs/manifest.webmanifest   app name, icons, shortcuts for installing
docs/sw.js                  offline support (service worker)
docs/icons/                 icons (drawn by android-build/make_assets.py web docs/icons)
.github/workflows/android.yml   builds and publishes the Android app
capacitor.config.json, package.json, android-build/   Android app setup
```
