# Privacy and safety rules

Applies to every folder, every agent and every published file. Longer discussion in `06-extras.md`.

## Recording
- Process on the device. Keep raw video private; delete recordings you no longer need.
- Do not film or keep military vehicles, convoys, checkpoints, air-defence activity, critical infrastructure or strike aftermath. If it appears, delete it.

## Publishing
- Faces and licence plates are blurred in every image or GIF that leaves the machine.
- No identification of people: no face recognition, no long-term re-identification. Re-identification embeddings live in memory for seconds only.
- Nothing that reveals the location: recognisable buildings, street signs, shop names, GPS logs, map registration, EXIF GPS, hostnames or addresses.
- Published media lives only in `docs/media/`. Raw video and data never enter git.

## Third-party tools (Hasty, W&B, cloud GPUs)
- Upload only selected frames with faces and plates already blurred.
- No raw continuous video; no frames with location clues.
- Do not log images with identifiable people to experiment trackers.

## Secrets
- Keys live in `.env` (git-ignored). `.env_template` lists the names only.
- Run `/privacy-check` before commits that include media, maps or logs.

## Hardware
- Power servos from a separate 5 V supply; connect grounds. Use the official 27 W Pi supply.
- No outdoor drone flights; navigation tests use the desk rig and PX4 simulation.
