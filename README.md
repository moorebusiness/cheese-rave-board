# Cheese Rave Board

Projector visuals for **The Election Night Show and Cheese Rave** (Tower Theatre, Oklahoma City, Nov. 3, 2026), presented by Let's Fix This. One page: the show's home screen, then the Cheese Rave results board.

## In the booth

1. Open the site in Chrome on the booth computer. Move the mouse to show the controls and click **Full screen**.
2. Press **W** to open the control window on the laptop screen (allow pop-ups if Chrome asks).
3. Press **B** once and allow the microphone, so the rave board pulses to the music. Do this before doors: the prompt shows on the projector.
4. On the rave board, the status chip at the top should read **LIVE · UPDATED** with a recent time.

The mouse pointer hides after 4 seconds without movement. Nothing switches on its own. The page opens on the home screen; press **R** for the rave board.

## Keys

| Home screen | |
|---|---|
| H | Home screen |
| 1 / 2 / 3 | Sponsors 1 / Sponsors 2 / Food sponsors |
| 4 | John Shack |
| 5 | Wait, Wait...I know this! |
| 6 | Top 10 (each press adds a line; if another cue cuts in, 6 brings it back where it left off) |
| 7 / 8 | AJ Griffin / Erika Lucas |
| 9 | Into the Cheese Rave: the sky turns turquoise, the moon turns pink, the cheese rises from behind the buildings. Press R from here to fade into the rave board |
| L | Sponsor loop (slides 1–3, 12 seconds each) |
| P / I | Send an airplane / the ISS across |

| Rave board | |
|---|---|
| R | Rave board |
| C | Congress board |
| F | Flip a tile |
| B | Beat sync on/off |
| D | Demo speed |
| E | Backup results on/off (switches to ElectionHub by hand) |
| X | Skip the phone push that's showing |
| M | Pause or resume phone pushes |
| Shift+X | Clear every push waiting in line |

## Phone pushes

People with the push link can send a photo or short clip from their phone (`push.html`). On the rave board, two stacked tiles in the middle columns flip away and one box (about 4:5) flips in with it, cropped to fill and tinted turquoise, pink or yellow in turn, then the tiles flip back to results. Race calls and the Congress board go first; anything sent during the show waits for the rave board. From 6 p.m. on Nov. 3, anything sent before 6 p.m. (testing) is ignored.

The push code is private and is not in this repository: the booth opens the board with `?push=CODE`, and senders get `push.html#CODE`. Files travel through the free public relay ntfy.sh (15 MB per file, so clips under about 15 seconds; files expire after 3 hours).

**Saving pushes to Google Drive:** a small Google Apps Script in Andy's account (`src/drive-archive.gs`, deployed as a web app) saves every push the board receives, original and untinted, to a Drive folder called **Cheese Rave pushes**, named by time. Pushes sent before showtime go in its **Testing** subfolder. The booth opens the board once with `&archive=DEPLOYMENT_ID` (remembered after that; `?archive=off` forgets it). Everything is saved, including pushes that get skipped or cleared. The board downloads each file from the relay and sends it to the script, since Google's servers can't reach the relay (a 15 MB clip takes about half a minute, in the background). The control window's phone-push line shows the count ("Drive: 12 saved"), any files missed, or **NOT SAVING** with the reason if saving has stopped.

## Celebrations

For a result worth cheering (say, a state question going down), every open board drops a full-screen rave moment over whatever is up: a riser, then the drop (one big flash, the headline slams in), then lasers from the DJ booth, a neon tunnel, a headline that punches and splits pink and teal, and two Cheese Rave logos bouncing like hype men, all on the beat (the room's beat when beat sync hears it, otherwise 128 BPM). A subline and the race's current split can sit under the headline. Flashes stay under three a second. It holds 25 seconds; **X** ends it early. Race calls and phone pushes wait until it's done.

To send one, ask Claude ("push a big victory for the defeat of SQ 845"), or run:

```
python3 tools/cheer.py "SQ 845 DEFEATED" --kicker "OKLAHOMA VOTERS SAY NO" --race SQ845
```

That writes `cheer.json` at the site root and pushes it. Boards check the file every 20 seconds, and GitHub Pages takes about a minute to publish, so it appears one to two minutes later. Without a computer, edit `cheer.json` on github.com: set a new `id` (anything not used before) and a `headline`, then commit. A board that opens more than 10 minutes after a celebration was sent doesn't replay it.

## Data

Live results come from [civicAPI](https://civicapi.org) and refresh every minute. Seat charts count the way DDHQ does: seats not on the ballot, plus each Senate and House race called tonight.

**Backup:** press **E** to switch to [ElectionHub](https://electionhub.org) for the races it carries, and **E** again to switch back. The board never switches on its own. The cue is the status chip turning pink ("RESULTS DELAYED") or a race that's plainly stuck. The credit line shows which source is on. ElectionHub doesn't carry OK-5, SQ 847, the U.S. Senate race or the county races, so those hold their last numbers while the backup is on. If electionhub.org itself is down, the board reads the same files from ElectionHub's GitHub repository.

- Add `#rehearse` to the address to replay the Aug. 25, 2026 runoff results.
- Add `#sample` for invented numbers (demos only).

## Updating the page

The page is built from `src/`. Edit `src/board.src.html` (show content such as the Top 10, titles and sponsors is near the top of its script), then:

```
cd src && python3 build_pages.py && cp cheese-rave-block-live.html ../index.html
```

and push. GitHub Pages republishes in about a minute. `cheese-rave-block.html` is the same page with invented numbers, for previews.
