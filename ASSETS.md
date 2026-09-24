# Asset Source & License Documentation

Every visual/media asset used in this project is either **self-authored
specifically for this project** or a **widely-used open-source library
distributed under a permissive license**. No copyrighted, purchased, or
unlicensed third-party photography/artwork is used anywhere.

| Asset                                                               | Source                                                                                 | License                                                      | Notes                                                                                                                                                   |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `static/js/three.min.js` (loaded via CDN in `templates/index.html`) | [Three.js](https://threejs.org/) v0.128, served from cdnjs.cloudflare.com              | MIT License                                                  | Used for the interactive 3D hero scene (`static/js/scene.js`).                                                                                          |
| Company logo mark ("SI" square, favicon)                            | Self-authored inline SVG, created for this project                                     | N/A — original work, free to reuse/modify                    | Located inline in `templates/index.html` `<head>` and `.logo-mark` CSS. Replace with your real logo.                                                    |
| Product/service icons (`static/img/icons.svg`)                      | Self-authored SVG line icons, hand-drawn for this project                              | N/A — original work, free to reuse/modify                    | Simple geometric line icons (cloud, cube, chart, shield, bolt, mobile) created specifically for this site.                                              |
| Team member avatars                                                 | Generated locally via CSS gradients + initials (no image files)                        | N/A — original work                                          | See `.team-avatar` in `static/css/style.css` and `TEAM` in `config.py`. No external photos are downloaded or embedded.                                  |
| Fonts                                                               | System font stack (`-apple-system, Segoe UI, Roboto, Inter, Arial, sans-serif`)        | N/A — uses fonts already licensed/installed on the user's OS | No web font files are downloaded, avoiding any font-licensing concerns. Optionally add a Google Fonts (Open Font License) `<link>` yourself if desired. |
| Background gradients, patterns, animations                          | Authored in `static/css/style.css` and `static/js/scene.js` using CSS/WebGL primitives | N/A — original work                                          | No image textures used; all visuals are procedurally generated (geometry, particles, gradients).                                                        |

## Why no stock photography is included

To guarantee zero copyright risk out of the box, this project avoids stock
photo placeholders entirely (even "free" stock photo sites have attribution
or usage caveats that can change). Instead:

- The **team section** uses generated initial-avatars (CSS gradients).
- The **product cards** use hand-drawn SVG icons instead of photos.
- The **hero section** uses a procedural 3D scene instead of a background photo/video.

## If you want to add real photos later

When you replace placeholder content with your own branding:

1. Add your images to `static/img/` (e.g. `static/img/team/jane.jpg`).
2. Update `config.py` (`TEAM`, `PRODUCTS`) to reference the new file paths.
3. Update `templates/index.html` to use `<img src="{{ url_for('static', filename='img/team/jane.jpg') }}">` instead of the generated avatar `<div>`.
4. Confirm you have the rights/license to use any photo you add, and record its source/license in this file.
