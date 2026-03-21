# Design System Document

## 1. Overview & Creative North Star: "The Digital Curator"
This design system moves away from the "template" aesthetic of academic portfolios to embrace the feel of a high-end, curated editorial. Our Creative North Star is **The Digital Curator**: a philosophy that treats information not as a list, but as a prestigious collection. 

We achieve this through **Intentional Asymmetry**. Rather than a rigid, centered grid, we use a dominant sidebar and staggered content blocks to create a sense of intellectual movement. The interaction between the authoritative **Noto Serif** and the functional **Inter** creates a "Scholar-meets-Modernist" tension that feels both established and cutting-edge. We reject traditional structural lines in favor of "Tonal Depth," where sections are defined by the weight of their background color rather than the thickness of a border.

---

## 2. Colors
Our palette is rooted in a "Deep Scholarly" spectrum. It uses the weight of navy and the warmth of gold to convey a sense of history and prestige, balanced by expansive "Air" (whitespace).

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to define sections. Layout boundaries must be established solely through background color shifts. 
*   *Example:* A `surface-container-low` (#f6f3f2) section should sit directly against a `surface` (#fbf9f8) background. The subtle shift in hex value is enough to cue the eye to a new content area without creating the "boxed-in" feeling of a legacy template.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of fine paper. 
*   **Base:** `surface` (#fbf9f8) for the overall page.
*   **The Sidebar:** Use `primary` (#000666) or `surface-container-high` (#eae8e7) to create a definitive anchor for profile information.
*   **Content Cards:** Use `surface-container-lowest` (#ffffff) to make research papers or project cards "float" naturally above the page.

### The "Glass & Gradient" Rule
To elevate the experience, apply **Glassmorphism** to floating navigation bars or sidebar overlays. Use semi-transparent `surface` colors with a `backdrop-blur` of 12px–20px. 
*   **Signature Textures:** For primary CTAs (e.g., "Download CV"), use a subtle linear gradient from `primary` (#000666) to `primary_container` (#1a237e). This adds a three-dimensional "soul" to the button that flat color cannot replicate.

---

## 3. Typography
The typography system is a dialogue between the traditional (Serif) and the technological (Sans-Serif).

*   **Display & Headlines (Noto Serif):** Used for the academic's name, publication titles, and section headers. The serif carries the weight of authority.
    *   *Scale:* Use `display-lg` (3.5rem) for the landing hero name to create an immediate editorial impact.
*   **Title & Body (Inter):** Used for metadata, descriptions, and long-form research text. Inter provides maximum readability at smaller scales.
    *   *Scale:* `title-md` (1.125rem) is the workhorse for publication abstracts.
*   **Labels (Inter):** Used for tags (e.g., "Published," "Peer Reviewed") in `label-md` (0.75rem), often in uppercase with increased letter-spacing (0.05rem) for a premium feel.

---

## 4. Elevation & Depth
Hierarchy is achieved through **Tonal Layering**, not structural scaffolding.

*   **The Layering Principle:** Stack `surface-container` tiers. A `surface-container-lowest` (#ffffff) card placed on a `surface-container-low` (#f6f3f2) background creates a "soft lift."
*   **Ambient Shadows:** For elevated elements like hovered cards, use an extra-diffused shadow: `box-shadow: 0 10px 40px rgba(0, 7, 103, 0.06);`. Note the use of a tinted shadow (using the `on_primary_fixed` navy) rather than a neutral grey.
*   **The "Ghost Border" Fallback:** If a boundary is strictly required for accessibility, use the `outline-variant` token (#c6c5d4) at **15% opacity**. Never use 100% opaque borders.
*   **Glassmorphism Depth:** Utilize `surface-variant` with 70% opacity and a blur to allow background colors to bleed through, ensuring the UI feels integrated and high-end.

---

## 5. Components

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary_container`), white text, `md` (0.375rem) roundedness.
*   **Tertiary (The "Editorial" Link):** No background. `primary` text with a 1px underline that expands on hover.

### Cards (Publications/Projects)
*   **Rule:** No divider lines.
*   **Style:** Use `surface-container-lowest` (#ffffff) with a `3.5` (1.2rem) padding scale. Use vertical whitespace to separate the Title (Serif) from the Metadata (Sans).

### Chips (Research Interests)
*   **Style:** `secondary_container` (#cfe6f2) background with `on_secondary_container` (#526772) text. Use `full` (9999px) roundedness for a pill shape that contrasts against the rectangular grid.

### Input Fields
*   **Style:** Minimalist. Only a bottom-border using `outline` (#767683) at 30% opacity. Upon focus, the border transitions to `primary` (#000666).

### Additional Component: The "Curated Sidebar"
A fixed or sticky sidebar using `surface_container_low`. It houses the `avatar.jpg` with a custom `xl` (0.75rem) roundedness and the academic’s core contact info. This acts as the "Anchor" for the fluid content area.

---

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical margins. If the left margin is `20` (7rem), the right can be `10` (3.5rem) to create a dynamic, modern layout.
*   **Do** prioritize white space. If in doubt, increase the spacing to the next tier in the scale (e.g., move from `8` to `10`).
*   **Do** use `tertiary` (#241900) as a "Highlight" color for micro-interactions or small icons to add warmth to the navy/slate palette.

### Don't
*   **Don't** use standard 1px borders to separate list items. Use the `2` (0.7rem) or `3` (1rem) spacing scale instead.
*   **Don't** use pure black (#000000) for text. Always use `on_surface` (#1b1c1c) to maintain the sophisticated, scholarly tone.
*   **Don't** use "Drop Shadows" that are visible. Shadows should be felt, not seen—ambient and deeply diffused.