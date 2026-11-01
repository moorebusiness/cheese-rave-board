# Cheese Rave Board

Projector visuals for **The Election Night Show and Cheese Rave** (Tower Theatre, Oklahoma City, Nov. 3, 2026), presented by Let's Fix This. One page: the show's home screen, then the Cheese Rave results board.

## In the booth

1. Open the site in Chrome on the booth computer. Move the mouse to show the controls and click **Full screen**.
2. Press **W** to open the control window on the laptop screen (allow pop-ups if Chrome asks).
3. Press **B** once and allow the microphone, so the rave board pulses to the music. Do this before doors: the prompt shows on the projector.
4. On the rave board, the status chip at the top should read **LIVE · UPDATED** with a recent time.

Nothing switches on its own. The page opens on the home screen; press **R** for the rave board.

## Keys

| Home screen | |
|---|---|
| H | Home screen |
| 1 / 2 / 3 | Sponsors 1 / Sponsors 2 / Food sponsors |
| 4 | John Shack |
| 5 | Wait, Wait...I know this! |
| 6 | Top 10 (each press adds a line) |
| 7 / 8 | AJ Griffin / Erika Lucas |
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
