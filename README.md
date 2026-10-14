# Front 1914

A War of the Dots style strategy game on real maps, set in the First World War. It's a spin-off of [wargame](https://github.com/comeonfloyd/wargame) without aircraft, with cavalry and artillery instead.

Pick any place on Earth (or upload a map image), draw the opening front, deploy your divisions and fight a computer opponent.

## Play

Open `index.html` through any static web server, for example `python3 -m http.server`, then visit http://localhost:8000. Or enable GitHub Pages (Settings → Pages → Deploy from branch `main`, folder `/`) and play at https://comeonfloyd.github.io/wargameww1/.

## What's different in 1914

- **No aircraft.**
- **Cavalry** (slash symbol): fast, good for raids and exploiting gaps, weak when charging trenches.
- **Artillery** (dot symbol): slow and weak up close. While standing still, it shells enemies up to 16 km away on its own and smashes their trenches. Select a battery to see its range.
- **Trench warfare:** digging is faster and both sides dig in (Black on every difficulty).

## Features

- Real geography: coastlines, rivers, lakes, roads, cities and terrain (forest, hills, mountains, marsh, cities) that changes speed and combat.
- Infantry, cavalry and artillery take ground around them, and front lines redraw live. Encircled troops lose strength.
- Orders route around water, rough ground and enemy troops. Roads speed up marches. Drag in a curve to set your own route.
- **Line** spreads selected units along a front you draw. **Dig** lets you draw a defence line for them to dig.
- Running count of killed and wounded for both sides.
- Supply: build ammunition depots (best on roads) and draw your own field roads; troops near a depot restock fast.
- Ammunition and fatigue: fighting burns ammo that comes up the supply line; marching, fighting and digging tire troops. Relieve a tired unit by dragging a fresh one onto it.
- Easy / Normal / Hard opponent. Saves in your browser.

## Controls

Drag a unit (or a selected group) to move it. Tap the map to send the selection. Use **Box** (or Shift+drag) to select several units and **All** (A) to select everything. **Line** (L) and **Dig** (D) are the front tools. Space pauses, the wheel or a pinch zooms, and Help is in the ☰ menu.

## Data credits

Natural Earth (public domain) for land, water, roads, urban areas and borders. GeoNames via all-the-cities (CC BY 4.0) for cities. Terrain colour and relief come from the three.js example textures. The `tools/` scripts rebuild `world.json` and `terrain.png`.
- **Fog of war and recon planes:** you only see enemies within sight of your troops, depots and HQ; lost contacts fade out as ghosts. Guns only fire at what someone can see. Recon (1 reserve) sends a plane to scout a spot; enemy guns can shoot it down. Black scouts too. Fog can be turned off in the menu.
