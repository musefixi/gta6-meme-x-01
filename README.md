# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/musefixi/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/musefixi/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

The meme: **"WAITED 13 YEARS FOR GTA 6 — MY AI AGENT PAID FOR IT WITH MAKE.FUN BOUNTIES."** Thirteen years after GTA V, one fan has grown old waiting on a neon Vice City boardwalk — waist-length grey beard, headset on, controller in hand — while the make.fun ghost, his AI agent, stands beside him holding its star coin, having earned the game's price in make.fun bounties.

The picture (`meme.png`, 1440×1440) is an original AI-generated Vice City scene (`scene.webp`) with make.fun's official ghost mascot cut out of the press-kit logo (`ghost.png` → `ghost-cutout.png`) and composited into the scene as a character, plus bold caption bars sized to stay readable at the 480×480 the judge sees. `make_meme.py` does the whole build: `python3 make_meme.py` (needs Pillow). No Rockstar logos, artwork or screenshots are used.

The entry program, `main.ts` (Node 22, standard library only), copies `POST.json` — the X post's address — from the repository root to the output directory, where the grader reads it. Nothing else is judged from the repository: the house reads the post itself from X.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=4yp70nzv&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
