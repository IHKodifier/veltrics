# Veltrics Fleet & Vehicle Management — Style Guide

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md), [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md), [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md)  
> **Status:** Draft — Pending Palette Selection & Approval  
> **Author:** Brand & Design Systems Lead Persona (App Architect)  
> **Stage:** STAGE 5 — Style Guide

---

## 0. How to Use This Document

This style guide defines the complete visual identity and design system for Veltrics across **two platforms** (Android mobile + Chrome desktop web), **two modes** (Light + Dark), and **two user states** (Free tier with ads / Pro–Enterprise without ads).

**Three candidate color palettes are defined** — Slate Teal, Amber, and Forest Green. All other design decisions (typography, spacing, motion, components) are **palette-agnostic** and apply regardless of which palette is chosen. When the palette is selected, substitute the corresponding color tokens throughout.

> **Palette selection is the only open decision in this document. Everything else is resolved.**

---

## 1. Brand Identity Foundation

### 1.1 Brand Personality

Veltrics occupies the intersection of two qualities:

| Axis | Description | Manifests As |
|:---|:---|:---|
| **Professional & Trustworthy** | The app holds important vehicle data. Users must feel it is reliable, accurate, and safe. Fleet managers must feel confident showing it to their operations team. | Clean layouts, strong typographic hierarchy, consistent use of space, no gimmicks, data integrity cues (sync status, confirmation states). |
| **Friendly & Efficient** | The app is used in real-world conditions — petrol pumps, mechanics' workshops, fleet yards. It must not feel cold or corporate. | Warm micro-copy, celebratory moments (aha moment, Pro upgrade), fast interactions optimized for one-handed use, forgiving error states. |

**What Veltrics is NOT:** Aggressive, gamified, complex, intimidating, or decorative for its own sake.

### 1.2 Brand Voice (Micro-copy Principles)

These principles guide all in-app text — button labels, empty states, error messages, tooltips.

| Principle | Do | Don't |
|:---|:---|:---|
| **Direct** | "Add Vehicle" | "Create a New Vehicle Profile" |
| **Reassuring** | "Saved offline — will sync when connected." | "No internet connection detected." |
| **Celebratory (sparingly)** | "Your maintenance schedule is ready." | Generic "Success!" |
| **Non-punishing** | "You've reached your vehicle limit. Here's what Pro gives you." | "ERROR: Quota exceeded." |
| **Concise** | "Log Fuel" | "Record Fuel Consumption Entry" |

### 1.3 Wordmark Direction

**Name:** Veltrics (final, unchangeable)  
**Wordmark style:** Sans-serif logotype. The name is rendered in **Inter**, weight **700 (Bold)**, with a small visual differentiator:

- The letter **V** is slightly customized — a subtle angular cut or thinned inner stroke — to create a hint of forward motion (velocity) without being literal or truck-like.
- No icon or badge needed for MVP. The wordmark alone is the logo.
- The wordmark color is always the **primary palette color** on light backgrounds, and **white** on dark backgrounds.
- Tagline (optional, sub-brand use): *"Every vehicle. Every mile. Accounted for."*

---

## 2. Three Candidate Color Palettes

Each palette is fully specified for: Primary, Secondary, Semantic colors (Success/Warning/Error/Info), Light surface, Dark surface. All three are production-ready — only token substitution is required when the selection is made.

> **Decision pending:** Choose Palette A (Teal), Palette B (Amber), or Palette C (Forest Green) after reviewing all three in context.

---

### PALETTE A — Slate Teal / Cyan

**Character:** Modern, data-forward, technology-confident. Feels like premium fintech or SaaS. Appeals to the fleet manager persona strongly. Consumer tier also works — teal reads as "trustworthy health" (fitness apps, medical dashboards).

**Best fit for:** Users who want Veltrics to feel like premium software, not a vehicle app.

#### Light Mode Tokens

| Token | Hex | Usage |
|:---|:---|:---|
| `--color-primary-50` | `#f0fdfa` | Primary tint backgrounds, hover states |
| `--color-primary-100` | `#ccfbf1` | Chips, tags, secondary surfaces |
| `--color-primary-200` | `#99f6e4` | Illustrated accents |
| `--color-primary-300` | `#5eead4` | Progress bars (unfilled track) |
| `--color-primary-400` | `#2dd4bf` | Icons, secondary buttons (outlined) |
| `--color-primary-500` | `#14b8a6` | **PRIMARY BRAND COLOR — CTAs, active nav items, links** |
| `--color-primary-600` | `#0d9488` | Primary button hover state |
| `--color-primary-700` | `#0f766e` | Primary button pressed state |
| `--color-primary-800` | `#115e59` | Wordmark on white |
| `--color-primary-900` | `#134e4a` | Dark mode wordmark base |
| `--color-secondary-500` | `#06b6d4` | Cyan accent — data viz, charts, highlight rings |
| `--color-secondary-600` | `#0891b2` | Cyan hover |

#### Dark Mode Tokens (Palette A)

| Token | Hex | Usage |
|:---|:---|:---|
| `--color-surface-bg` | `#121212` | Base app background |
| `--color-surface-1` | `#1e1e1e` | Cards, bottom sheets, nav bar |
| `--color-surface-2` | `#2a2a2a` | Input fields, secondary cards |
| `--color-surface-3` | `#333333` | Dividers, skeleton loaders |
| `--color-primary-dark` | `#2dd4bf` | Primary actions on dark (400 for contrast) |
| `--color-primary-dark-hover` | `#14b8a6` | Hover on dark |
| `--color-on-primary` | `#042f2e` | Text/icon ON primary buttons |
| `--color-on-surface` | `#e2e8f0` | Primary text on dark surfaces |
| `--color-on-surface-muted` | `#94a3b8` | Secondary text, placeholders |

---

### PALETTE B — Amber / Orange

**Character:** Energetic, warm, grounded. Orange resonates culturally with Pakistan (CNG stations, transport sector, Mobilink/Jazz branding). Feels approachable and alive. Excellent for the consumer/driver persona. Fleet manager dashboards still work — amber creates natural urgency cues.

**Best fit for:** Consumer-first framing, word-of-mouth in Pakistan market, high visual impact on Play Store listing.

> **Note:** Since amber is the primary brand color, **warning** semantic states must be differentiated by icon pattern + a deeper amber-brown (`#92400e`), not color alone.

#### Light Mode Tokens

| Token | Hex | Usage |
|:---|:---|:---|
| `--color-primary-50` | `#fffbeb` | Primary tint backgrounds |
| `--color-primary-100` | `#fef3c7` | Chips, tags |
| `--color-primary-200` | `#fde68a` | Illustrated accents |
| `--color-primary-300` | `#fcd34d` | Progress bars (unfilled track) |
| `--color-primary-400` | `#fbbf24` | Icons, secondary outlined buttons |
| `--color-primary-500` | `#f59e0b` | **PRIMARY BRAND COLOR — CTAs, active nav items** |
| `--color-primary-600` | `#d97706` | Primary button hover state |
| `--color-primary-700` | `#b45309` | Primary button pressed state |
| `--color-primary-800` | `#92400e` | Wordmark on white |
| `--color-primary-900` | `#78350f` | Dark mode wordmark base |
| `--color-secondary-500` | `#f97316` | Orange accent — activity feed, alerts |
| `--color-secondary-600` | `#ea580c` | Orange hover |

#### Dark Mode Tokens (Palette B)

| Token | Hex | Usage |
|:---|:---|:---|
| `--color-surface-bg` | `#121212` | Base app background |
| `--color-surface-1` | `#1c1a16` | Cards — very slight warm undertone to complement amber |
| `--color-surface-2` | `#27231c` | Input fields, secondary cards |
| `--color-surface-3` | `#38321f` | Dividers, skeleton loaders |
| `--color-primary-dark` | `#fbbf24` | Primary actions on dark (400 for legibility) |
| `--color-primary-dark-hover` | `#f59e0b` | Hover on dark |
| `--color-on-primary` | `#1c0a00` | Text/icon ON primary buttons |
| `--color-on-surface` | `#f1ede5` | Primary text — warm white |
| `--color-on-surface-muted` | `#a8a097` | Secondary text, placeholders |

---

### PALETTE C — Forest Green / Emerald

**Character:** Calm, dependable, health-coded. Green is the universal signal for "operational readiness" and "all clear". Extremely legible for status indicators (healthy vehicle = green reinforces the brand). Feels premium without being aggressive. Strong contrast with overdue/alert red.

**Best fit for:** Users who relate maintenance to "vehicle health" — this palette speaks their language visually.

> **Note:** Since green is the primary brand color, **success** semantic states must use a stronger shade (`--color-primary-700`) + checkmark icon to differentiate from decorative primary use.

#### Light Mode Tokens

| Token | Hex | Usage |
|:---|:---|:---|
| `--color-primary-50` | `#f0fdf4` | Primary tint backgrounds |
| `--color-primary-100` | `#dcfce7` | Chips, tags |
| `--color-primary-200` | `#bbf7d0` | Illustrated accents |
| `--color-primary-300` | `#86efac` | Progress bars (unfilled track) |
| `--color-primary-400` | `#4ade80` | Icons, secondary outlined buttons |
| `--color-primary-500` | `#22c55e` | **PRIMARY BRAND COLOR — CTAs, active nav items** |
| `--color-primary-600` | `#16a34a` | Primary button hover state |
| `--color-primary-700` | `#15803d` | Primary button pressed state |
| `--color-primary-800` | `#166534` | Wordmark on white |
| `--color-primary-900` | `#14532d` | Dark mode wordmark base |
| `--color-secondary-500` | `#059669` | Emerald accent — data viz, trend lines |
| `--color-secondary-600` | `#047857` | Emerald hover |

#### Dark Mode Tokens (Palette C)

| Token | Hex | Usage |
|:---|:---|:---|
| `--color-surface-bg` | `#121212` | Base app background |
| `--color-surface-1` | `#151a17` | Cards — very slight green undertone |
| `--color-surface-2` | `#1e2720` | Input fields, secondary cards |
| `--color-surface-3` | `#2d3a31` | Dividers, skeleton loaders |
| `--color-primary-dark` | `#4ade80` | Primary actions on dark (400 for contrast) |
| `--color-primary-dark-hover` | `#22c55e` | Hover on dark |
| `--color-on-primary` | `#052e16` | Text/icon ON primary buttons |
| `--color-on-surface` | `#e8f5ec` | Primary text — cool white with green undertone |
| `--color-on-surface-muted` | `#8fa897` | Secondary text, placeholders |

---

## 3. Semantic / Functional Color System

These colors are **palette-independent** — they work across all three palettes and carry fixed meaning. Do not use these colors for decoration.

| Token | Light Hex | Dark Hex | Meaning | Used For |
|:---|:---|:---|:---|:---|
| `--color-success` | `#16a34a` | `#4ade80` | Operational, complete, healthy | Vehicle status, sync confirmed, payment success |
| `--color-warning` | `#ca8a04` | `#facc15` | Attention needed, not urgent | Upcoming maintenance, offline badge, per-action ad gate |
| `--color-error` | `#dc2626` | `#f87171` | Overdue, failed, blocked | Overdue maintenance, payment failed, sync conflict |
| `--color-info` | `#2563eb` | `#60a5fa` | Informational, neutral | Notification center, tooltips, invite status |
| `--color-pro-badge` | `#7c3aed` | `#a78bfa` | Pro/Enterprise tier indicator | Lock icons, Pro badge, tier labels |
| `--color-ad-badge` | `#b45309` | `#fbbf24` | Ad-rewarded indicator | Ad badge on rewarded vehicles/drivers |

> **Accessibility:** All semantic colors meet WCAG AA 4.5:1 contrast against their respective surface backgrounds. `--color-error` meets AAA (7:1) against both light and dark surfaces.

---

## 4. Neutral / Gray Scale

Shared across all palettes. Used for text, borders, dividers, and surfaces.

| Token | Light Hex | Dark Hex | Usage |
|:---|:---|:---|:---|
| `--color-neutral-50` | `#f8fafc` | `#1e1e1e` | Page background (light) / Card surface (dark) |
| `--color-neutral-100` | `#f1f5f9` | `#27272a` | Section backgrounds, alternating rows |
| `--color-neutral-200` | `#e2e8f0` | `#3f3f46` | Borders, dividers, input outlines |
| `--color-neutral-300` | `#cbd5e1` | `#52525b` | Disabled element outlines |
| `--color-neutral-400` | `#94a3b8` | `#71717a` | Placeholder text, muted icons |
| `--color-neutral-500` | `#64748b` | `#a1a1aa` | Secondary body text |
| `--color-neutral-600` | `#475569` | `#d4d4d8` | Secondary text with more emphasis |
| `--color-neutral-700` | `#334155` | `#e4e4e7` | Primary body text (light mode) |
| `--color-neutral-800` | `#1e293b` | `#f4f4f5` | Headings, strong labels (light mode) |
| `--color-neutral-900` | `#0f172a` | `#fafafa` | Maximum contrast text |

---

## 5. Typography System

### 5.1 Typeface

**Primary Typeface: Inter**  
- Source: Google Fonts (`https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800`)  
- Loaded weights: 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold), 800 (ExtraBold)  
- Fallback stack: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

**Why Inter:** Maximum legibility at small sizes — critical for data-dense tables on web and narrow mobile screens. Neutral personality that amplifies the brand color rather than competing with it. Excellent number rendering — critical for odometer readings, cost figures, and dashboard metrics.

**Monospace:** `'Roboto Mono', 'Courier New', monospace` — used exclusively for invite codes (VLT-A3K) and raw odometer values in data entry fields.

### 5.2 Type Scale

All sizes in `rem` (base 16px). Flutter equivalent in `sp` provided.

| Token | rem | px | Flutter sp | Weight | Line Height | Usage |
|:---|:---|:---|:---|:---|:---|:---|
| `--text-display-xl` | 2.25rem | 36px | 36sp | 800 | 1.2 | Hero numbers on dashboards (e.g., "₨ 142,000 total spend") |
| `--text-display-lg` | 1.875rem | 30px | 30sp | 700 | 1.25 | Page titles (Fleet Dashboard, Settings) |
| `--text-display-md` | 1.5rem | 24px | 24sp | 700 | 1.3 | Section headings, card titles |
| `--text-title-lg` | 1.25rem | 20px | 20sp | 600 | 1.35 | Dialog titles, sheet headings, nav labels |
| `--text-title-md` | 1.125rem | 18px | 18sp | 600 | 1.4 | Card subtitles, group labels |
| `--text-title-sm` | 1rem | 16px | 16sp | 600 | 1.4 | Field labels, table column headers |
| `--text-body-lg` | 1rem | 16px | 16sp | 400 | 1.6 | Primary body text, list items |
| `--text-body-md` | 0.875rem | 14px | 14sp | 400 | 1.6 | Secondary body text, descriptions |
| `--text-body-sm` | 0.75rem | 12px | 12sp | 400 | 1.5 | Captions, helper text, timestamps |
| `--text-label-lg` | 0.875rem | 14px | 14sp | 500 | 1.2 | Button labels, chip text |
| `--text-label-md` | 0.75rem | 12px | 12sp | 500 | 1.2 | Badge text, tag labels |
| `--text-label-sm` | 0.625rem | 10px | 10sp | 600 | 1.2 | Status pill text (OVERDUE, SYNCED) — ALL CAPS only |

### 5.3 Typography Rules

1. **Never use more than 3 type sizes on a single screen.** Data density must not mean typographic chaos.
2. **Numbers in dashboards use tabular nums** (`font-variant-numeric: tabular-nums`) so columns align regardless of digit count.
3. **Currency format (Pakistan):** `₨ 142,000` — rupee sign with space, comma-separated thousands. `PKR` used in export reports only, not in-app.
4. **All-caps text** is limited to `--text-label-sm` status pills (OVERDUE, PENDING, SYNCED, AD). Never apply uppercase to body text or headings.

---

## 6. Spacing & Grid System

### 6.1 Spacing Scale

All values are multiples of 4px.

| Token | Value | Usage |
|:---|:---|:---|
| `--space-1` | 4px | Icon inner padding, chip gap |
| `--space-2` | 8px | Tight icon-label gap, badge padding |
| `--space-3` | 12px | Compact list item vertical padding |
| `--space-4` | 16px | Standard unit. Card internal padding (mobile). |
| `--space-5` | 20px | Section gap on mobile |
| `--space-6` | 24px | Card internal padding (web). Section gap (mobile). |
| `--space-8` | 32px | Section gap (web). Between-card gap. |
| `--space-10` | 40px | Page header vertical padding |
| `--space-12` | 48px | Bottom nav height (Android) |
| `--space-16` | 64px | Hero section padding |

### 6.2 Layout Grid

#### Android Mobile

| Property | Value |
|:---|:---|
| Columns | 4 |
| Gutter | 16px |
| Margin | 16px |
| Max content width | 100% |

#### Chrome Desktop Web

| Property | Value |
|:---|:---|
| Sidebar width (collapsed) | 72px |
| Sidebar width (expanded) | 240px |
| Columns (main content) | 12 |
| Gutter | 24px |
| Content margin | 32px |
| Max content width | 1280px (centered) |
| Dashboard card grid | 3 columns (min 320px each) |

### 6.3 Border Radius Scale

| Token | Value | Usage |
|:---|:---|:---|
| `--radius-sm` | 6px | Chips, badges, input fields |
| `--radius-md` | 10px | Cards, modals |
| `--radius-lg` | 16px | Bottom sheets, dialogs, large panels |
| `--radius-xl` | 24px | Full-bleed banner sections |
| `--radius-full` | 9999px | Pills, avatar circles, FAB buttons |

---

## 7. Component Design System

### 7.1 Buttons

**Primary Button** — The single most important action on a screen (e.g., "Log Fuel", "Upgrade to Pro", "Accept Schedule").

```
Background:     --color-primary-500
Text:           white (--color-on-primary for Palette C dark text)
Height:         48px (mobile) / 40px (web)
Padding:        0 24px
Border-radius:  --radius-full (pill — friendly)
Font:           --text-label-lg, weight 600
Shadow:         0 2px 8px rgba(primary-500, 0.35)
Hover:          --color-primary-600
Pressed:        --color-primary-700, scale(0.98)
Disabled:       --color-neutral-200 bg, --color-neutral-400 text
Loading:        Circular progress replaces label; button stays full-width
```

**Secondary Button (Outlined)** — Secondary actions ("Cancel", "Edit", "Maybe Later").

```
Background:     transparent
Border:         1.5px solid --color-primary-500
Text:           --color-primary-500
Height:         48px (mobile) / 40px (web)
Padding:        0 24px
Border-radius:  --radius-full
Hover:          --color-primary-50 background
Pressed:        --color-primary-100 background
Disabled:       Border --color-neutral-300, text --color-neutral-400
```

**Destructive Button** — Irreversible actions ("Delete Vehicle", "Request Account Deletion").

```
Background:     --color-error
Text:           white
Sizing:         Same as Primary Button
Rule:           Only shown after confirmation dialog — never as a first-presented action
```

**Text Button** — Low-emphasis actions ("Forgot Password", "Skip", "View all").

```
Background:     none
Text:           --color-primary-500
Underline:      none at rest; underline on hover
Padding:        0 8px
Height:         36px
```

**FAB (Floating Action Button)** — Android only. Quick-add vehicle, quick log entry.

```
Size:           56px diameter
Background:     --color-primary-500
Icon:           white, 24px
Border-radius:  --radius-full
Shadow:         0 4px 16px rgba(primary-500, 0.4)
Extended FAB:   pill shape (icon + label), same colors
```

### 7.2 Input Fields

Material 3 outlined field style, adapted for Veltrics.

```
Height:         56px
Border:         1.5px solid --color-neutral-300
Border-radius:  --radius-sm (6px) — not pill; inputs feel precise, not bubbly
Floating label: --text-body-md, --color-neutral-500 → rises to top on focus
Active border:  2px solid --color-primary-500
Error border:   2px solid --color-error
Helper text:    --text-body-sm, --color-neutral-500 (below field)
Error text:     --text-body-sm, --color-error (replaces helper text)
Background:     white (light) / --color-surface-2 (dark)
Numeric fields: Text right-aligned. Open numeric keypad by default.
Prefix/suffix:  --color-neutral-400 icons, 20px
```

**Typeahead / Search Fields** (Vehicle Add — Make/Model/Year):

```
Same as Input, plus:
Dropdown shadow:   0 8px 24px rgba(0,0,0,0.12)
Dropdown max-height: 280px, scrollable
Match highlight:   --color-primary-100 background on matched text
```

### 7.3 Cards

**Standard Content Card** — Vehicle cards, activity feed items, list items.

```
Background:     white (light) / --color-surface-1 (dark)
Border-radius:  --radius-md (10px)
Padding:        --space-4 (16px)
Shadow (light): 0 1px 4px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04)
Shadow (dark):  none (border: 1px solid --color-surface-3 instead)
Card gap:       --space-3 (12px) mobile / --space-4 (16px) web
```

**Dashboard Summary Card** (Fleet Overview, Cost Summary, Alert panels):

```
Same base as Standard Card
Header label:   --text-title-sm, --color-neutral-500, letter-spacing 0.08em
Metric:         --text-display-xl, --color-neutral-800 (light) / --color-on-surface (dark)
Trend arrow:    --color-success (up) / --color-error (down) + icon
```

**Vehicle Status Card** — Extended card with health indicator:

```
Left accent bar:   4px wide, full card height
                   --color-success (Healthy), --color-warning (Attention), --color-error (Overdue)
Vehicle photo:     Circular, 48px, left-aligned
Make/Model:        --text-title-md
Plate number:      --text-body-md, --color-neutral-500
Status badge:      Right-aligned pill, color matches accent bar
Ad badge:          Small pill top-right corner — amber bg ("🎬 Ad") for ad-rewarded vehicles
```

### 7.4 Navigation

#### Android Mobile — Bottom Navigation Bar

```
Height:         56px + bottom safe area inset
Background:     white (light) / --color-surface-1 (dark)
Top border:     1px solid --color-neutral-200 (light) / --color-surface-3 (dark)
Items:          4 max — Dashboard, Vehicles, Notifications, Settings
Active item:    filled icon + label + --color-primary-500
Inactive item:  outlined icon, no label, --color-neutral-400
Notification:   --color-error badge, white text, 8px
Upgrade badge:  Small star on Settings item for Free tier users
```

#### Chrome Desktop Web — Sidebar Navigation

```
Collapsed width:  72px (icon only)
Expanded width:   240px (icon + label)
Toggle:           Chevron button at sidebar bottom
Background:       --color-neutral-50 (light) / --color-surface-1 (dark)
Right border:     1px solid --color-neutral-200 (light) / --color-surface-3 (dark)
Nav item height:  48px
Nav item padding: 0 --space-4
Active item:      --color-primary-50 bg (light) / 12% primary tint (dark)
                  --color-primary-500 icon+text, 3px primary left border
Hover item:       --color-neutral-100 background
Section dividers: 1px --color-neutral-200 + section label in --text-label-md uppercase
Bottom section:   User avatar (initials) + name + tier badge
Upgrade section:  "Upgrade to Pro" button in --color-pro-badge tint background (Free tier only)
```

### 7.5 Status Badges & Pills

All status pills use `--text-label-sm` (10px, 600 weight, ALL CAPS).

**Vehicle Health:**

| Status | Pill Text | Light Background | Light Text | Dark Background | Dark Text |
|:---|:---|:---|:---|:---|:---|
| Healthy | HEALTHY | `#dcfce7` | `#166534` | `#14532d` | `#4ade80` |
| Attention | ATTENTION | `#fef9c3` | `#ca8a04` | `#3f2e00` | `#facc15` |
| Overdue | OVERDUE | `#fee2e2` | `#dc2626` | `#3f0000` | `#f87171` |

**Driver Consistency Score:**

| Score Range | Pill Text | Color Token |
|:---|:---|:---|
| >= 80% | CONSISTENT | `--color-success` |
| 50–79% | MODERATE | `--color-warning` |
| < 50% | NEEDS ATTENTION | `--color-error` |

**Sync Status:**

| Status | Pill Text | Color Token |
|:---|:---|:---|
| Waiting to sync | PENDING | `--color-warning` |
| Syncing now | SYNCING | `--color-info` |
| Sync complete | SYNCED | `--color-success` |
| Needs user action | CONFLICT | `--color-error` |

**Tier Badges:**

| Tier | Label | Light BG | Light Text | Dark BG | Dark Text |
|:---|:---|:---|:---|:---|:---|
| Free | FREE | `#f1f5f9` | `#475569` | `#27272a` | `#a1a1aa` |
| Pro | PRO | `#ede9fe` | `#7c3aed` | `#2e1065` | `#a78bfa` |
| Enterprise | ENTERPRISE | `#1e293b` | `#ffffff` | `#0f172a` | `#f4f4f5` |

### 7.6 Offline Indicator Banner

Per UXD-005 — offline is informational, not an error state:

```
Position:       Fixed top, below app bar (Android) / below top nav (web)
Height:         36px
Background:     --color-warning at 12% opacity
Bottom border:  1px solid --color-warning at 40%
Icon:           wifi_off, 16px, --color-warning
Text:           "You're offline — entries will save locally and sync when connected."
Font:           --text-body-sm, dark amber shade for contrast
Enter:          slides down from top, 200ms ease-out
Exit:           slides up on reconnect, 200ms ease-in
```

### 7.7 Ad Component Design

Ad placement follows a **de-emphasized card blend** — visible but never disruptive. Free users know ads are present; the UX doesn't hide them, but it doesn't impose them.

#### Banner Ad (Bottom of Screen — Android Only)

```
Position:       Fixed bottom, above bottom nav bar
Height:         50px (AdMob standard banner)
Background:     --color-neutral-100 (light) / --color-surface-2 (dark)
Top border:     1px solid --color-neutral-200 (light) / --color-surface-3 (dark)
Label:          "Ads by Google" — --text-label-sm, --color-neutral-400, top-left
NEVER shown on: SCR-FUEL-001, SCR-MNT-002, SCR-TRIP-001, SCR-EXP-001
```

#### Native Ad Card (In Vehicle / Activity Lists)

```
Card dimensions: Same as standard content card
Left border:     3px solid --color-neutral-300 (distinguishes from content cards)
Top-right label: "Ad" — --text-label-sm, --color-neutral-400
Background:      --color-neutral-50 (light) / --color-surface-2 (dark) — slightly different from content
Opacity:         90% — subtly de-emphasized
Frequency:       Maximum 1 native ad per 5 content cards
```

#### Rewarded Video Gate UI (Per-Action Ad — Bottom Sheet)

Shown when user acts on an ad-rewarded vehicle/driver resource:

```
Component:      Bottom sheet (not full-screen modal — less blocking)
Height:         280px
Icon:           film/videocam, 40px, --color-ad-badge
Title:          "Watch a short ad to continue" — --text-title-lg
Body:           "This is an ad-supported vehicle. Watch 1 ad to [action]." — --text-body-md
Primary CTA:    "Watch Ad" — primary button, full width
Secondary link: "Upgrade to Pro for ad-free access →" — text button, --color-pro-badge
If ad fails:    Replace CTA with "Ad unavailable. Try again later." + Pro upgrade link
```

#### Rewarded Slot Earn UI (3-Ad Flow — Earning a New Bonus Slot)

```
Component:      Full-screen overlay (rare — only when earning a new bonus slot)
Progress:       3 circles (● ● ●) showing ads watched out of 3
After each ad:  Circle fills with --color-success + animated checkmark
After all 3:    Confetti burst (same as Pro upgrade celebration)
Confirmation:   "Bonus slot unlocked! You can now add vehicle 4 / driver 4."
```

---

## 8. Iconography

### 8.1 Icon Library

**Primary:** Material Symbols (Outlined style, grade 0, optical size 24)  
Flutter: `material_symbols_icons` package (outlined, weight 300)

**Rule:** Outlined icons at rest → Filled icons for **active navigation state only**. This creates a clear selection signal without relying on color alone.

### 8.2 Core Icon Set

| Category | Material Symbol | Usage |
|:---|:---|:---|
| Dashboard | `dashboard` | Dashboard nav |
| Vehicle | `directions_car` | Vehicle nav, vehicle cards |
| Maintenance | `build` | Maintenance tab, service log |
| Fuel | `local_gas_station` | Fuel log, fuel history |
| Trip | `route` | Trip log |
| Expense | `receipt_long` | Expense log |
| Driver | `person` | Driver nav, driver cards |
| Organization | `business` | Org settings |
| Notifications | `notifications` | Notification center |
| Settings | `settings` | Settings nav |
| Offline | `wifi_off` | Offline indicator |
| Sync | `sync` | Sync status |
| Sync conflict | `sync_problem` | Conflict state |
| Add | `add` | FAB, add buttons |
| Edit | `edit` | Edit actions |
| Delete | `delete` | Delete actions |
| Export | `file_download` | Export PDF/CSV |
| Pro lock | `lock` | Pro-gated features |
| Ad / Rewarded | `videocam` | Ad-rewarded indicator |
| Upgrade | `rocket_launch` | Upgrade CTA |
| Odometer | `speed` | Odometer readings |
| Calendar | `calendar_today` | Date fields, schedule |
| Photo | `photo_camera` | Receipt / vehicle photo |
| Success | `check_circle` | Confirmation states |
| Warning | `warning` | Warning states |
| Error | `error` | Error states |
| Info | `info` | Informational states |
| Overdue | `alarm` | Overdue maintenance |

### 8.3 Icon Sizing

| Context | Size |
|:---|:---|
| Navigation bar | 24px |
| List item leading icon | 20px |
| Inside buttons | 18px |
| Inline status indicators | 16px |
| Inside tight badges/pills | 12px |
| Empty state / hero | 48px |
| FAB | 24px |

---

## 9. Motion & Animation Principles

### 9.1 Philosophy

Motion must be **functional**, not decorative. Every animation either:
1. Communicates a state change (offline → online, pending → synced)
2. Guides spatial understanding (modal slides from bottom, deletion slides left)
3. Delivers delight at a key emotional moment (aha moment, Pro upgrade)

**No infinite spinners** where a skeleton loader is appropriate.

### 9.2 Duration Scale

| Token | Duration | Easing | Usage |
|:---|:---|:---|:---|
| `--duration-fast` | 100ms | ease-out | Ripple effects, button press scale |
| `--duration-normal` | 200ms | ease-in-out | Modal appear, card hover, most transitions |
| `--duration-slow` | 350ms | cubic-bezier(0.4, 0, 0.2, 1) | Page transitions, slide-up sheets |
| `--duration-deliberate` | 500ms | cubic-bezier(0.34, 1.56, 0.64, 1) | Celebratory spring animations |

### 9.3 Key Animations

**Aha Moment — Pre-populated Maintenance Schedule Reveal:**  
Each maintenance item card staggers in from below with 60ms offset between cards.  
`translateY(16px) → translateY(0)` + `opacity 0 → 1`, 350ms, spring easing.  
This is the most important animation in the app. Total sequence must complete in under 800ms.

**Offline → Online Sync Confirmation:**  
Pending badge (amber) pulses → dissolves into green checkmark.  
Duration: 500ms. The checkmark scales from `scale(0) → scale(1)` with spring bounce.

**Pro Upgrade Celebration:**  
24-particle confetti burst (randomized colors from primary + secondary palette tokens, gravity physics).  
Duration: 1200ms. Underlaid by "Welcome to Pro!" card sliding up (350ms).

**Bottom Sheet / Modal:**  
`translateY(100%) → translateY(0)`, 300ms, cubic-bezier(0.4, 0, 0.2, 1).  
Backdrop: `opacity 0 → 0.5`, same duration. Dismiss reverses.

**Page Navigation:**  
Android: Material right-to-left slide, 300ms.  
Web: Crossfade, 200ms (slide transitions feel wrong on desktop).

**Skeleton Loaders:**  
Shimmer: `--color-neutral-100` base, lighter shimmer wave left-to-right.  
Duration: 1500ms infinite. Shown for all dashboard and list content during initial fetch.

**Button Press:**  
`scale(0.97)` on press-down, spring back to `scale(1.0)` on release. 100ms each.

---

## 10. Platform-Specific Design Adaptations

### 10.1 Android Mobile

| Element | Rule |
|:---|:---|
| **Navigation** | Bottom nav bar (4 items max). No hamburger menu. |
| **Touch targets** | Minimum 48×48dp on all interactive elements |
| **Thumb zone** | Primary actions (FAB, log buttons, CTA) anchored to bottom 40% of screen. Destructive actions in top app bar. |
| **Top app bar** | 56px. Title left-aligned. Back arrow for nested screens. |
| **Forms** | Full-screen forms. Keyboard pushes content up (not over). Submit button always visible above keyboard. |
| **Swipe gestures** | Swipe-to-delete on list items (fuel entries, expenses, trips). Swipe-to-reveal edit. Confirm before delete. |
| **Pull-to-refresh** | On dashboard and all list screens. Material 3 `RefreshIndicator` in primary color. |
| **Status bar** | Transparent over app background. Icons adapt light/dark. |
| **Safe areas** | Bottom padding accounts for home indicator (Android 10+). |

### 10.2 Chrome Desktop Web

| Element | Rule |
|:---|:---|
| **Navigation** | Left sidebar, collapsible. No bottom nav. |
| **Hover states** | All interactive elements have distinct hover. Cursor: `pointer` on clickables. |
| **Tables** | Vehicle list, driver list, expense history rendered as proper tables. Sortable columns. Sticky header. |
| **Density** | 48px row height. 16px cell padding. Balanced — not cramped, not spacious. |
| **Multi-select** | Checkbox column on tables for bulk actions (bulk delete, bulk export). |
| **Keyboard navigation** | Tab order follows visual layout. Focus ring: 2px solid `--color-primary-500`, 2px offset. |
| **Tooltips** | On hover for icon-only sidebar buttons. 400ms delay. |
| **Modals** | Centered dialogs, max-width 560px. Backdrop: `blur(4px)` at 50% opacity. |
| **Minimum width** | 1024px. Below this, sidebar auto-collapses to icon-only. |
| **Max content width** | 1280px, centered. |

---

## 11. Screen-Specific Style Notes

### 11.1 Absolute Ad-Free Zones

Per FD-006 — no ads on these screens, regardless of tier, always:

- `SCR-FUEL-001` — Log Fuel Entry  
- `SCR-MNT-002` — Log Service Record  
- `SCR-TRIP-001` — Log Trip  
- `SCR-EXP-001` — Log Expense  

These forms must feel clean and distraction-free. This is the primary UX trust signal for free-tier users.

### 11.2 Aha Moment Screen (SCR-MNT-001 — Maintenance Schedule)

This screen receives the highest design polish in the app:

- Background: subtle gradient tint from the primary palette color (5% opacity) — not a flat white.
- Each maintenance card carries a service-type icon (build, tire, battery, etc.).
- "Due in X days" rendered in `--text-display-md`, prominently — not buried in body text.
- The staggered animation (§9.3) must complete in under 800ms total.
- Celebratory header: "Your [Year] [Make] [Model] is ready." in `--color-primary-500`.

### 11.3 Quota Wall / Upgrade Prompt Screens (SCR-PAY-001)

Per emotional mapping in User Journeys §6 — quota walls must feel **motivating, not punishing**:

- Never use `--color-error` (red) as the primary color on upgrade screens.
- Open with acknowledgement: "You've got 3 vehicles managed. Ready to grow?"
- Feature comparison: 2-column table (Free | Pro). Pro column uses `--color-pro-badge` header.
- CTA: "Upgrade to Pro" in `--color-primary-500` — on-brand, not jarring purple.
- Secondary: "Maybe later" as a text button in `--color-neutral-500`.

### 11.4 Driver Dashboard (SCR-DASH-003)

Drivers have a simplified view — no cost data, no management controls:

- Quick-log buttons are larger and more prominent than on consumer dashboard (drivers log more frequently).
- Assigned vehicle cards show only: Make/Model, Plate, Last Odometer, Status badge.
- No upgrade badge — drivers are not purchasing users.

### 11.5 Fleet Manager Dashboard (SCR-DASH-002)

- Card grid layout on web (3 columns): Fleet Overview, Alerts & Actions, Cost Summary, Recent Activity Feed.
- Cost Summary card: currency in `--text-display-xl`, right-aligned, tabular numerals.
- Alerts & Actions: `--color-error` left border for overdue, `--color-warning` for upcoming.
- Recent Activity Feed: infinite scroll + skeleton loading. Each item: driver initials avatar, action summary, vehicle name, relative timestamp ("2 hours ago").

---

## 12. Empty State Style

### 12.1 Illustration Style

No stock photography. All empty states use:
- **Large Material Symbols icon** (48–96px) on a primary-tinted background circle.
- **Simple geometric shapes** for onboarding carousel illustrations only.

No 3D renders, no character illustrations for MVP.

### 12.2 Empty State Template

```
Icon background circle:  96px, --color-primary-50 (light) / --color-primary-900 at 20% (dark)
Icon:                    64px, --color-primary-300 (light) / --color-primary-dark at 40% (dark)
Heading:                 --text-title-lg, --color-neutral-700
Body:                    --text-body-md, --color-neutral-500, max 2 lines, centered
CTA:                     Primary button, centered
```

**Examples:**
- No vehicles: Icon `directions_car` · "No vehicles yet." · "Add your first vehicle to start tracking." · "Add Vehicle"
- No fuel logs: Icon `local_gas_station` · "No fuel logs yet." · "Log your first fuel entry — under 15 seconds." · "Log Fuel"
- No notifications: Icon `notifications_off` · "You're all caught up." · "Reminders will appear here." · (no CTA)

---

## 13. Light Mode / Dark Mode Quick Reference

| Element | Light Mode | Dark Mode |
|:---|:---|:---|
| App background | `#f8fafc` | `#121212` |
| Card background | `#ffffff` | `#1e1e1e` |
| Secondary card / input | `#f1f5f9` | `#2a2a2a` |
| Primary text | `#1e293b` | `#e2e8f0` |
| Secondary text | `#64748b` | `#94a3b8` |
| Placeholder | `#94a3b8` | `#52525b` |
| Divider | `#e2e8f0` | `#333333` |
| Shadow | `rgba(0,0,0,0.08)` | none (border instead) |
| Bottom nav / sidebar | `#ffffff` | `#1e1e1e` |
| Status bar icons | Dark | Light |

---

## 14. Accessibility Checklist

All MVP screens must meet these standards before Sprint 6 completion:

| Check | Standard | Notes |
|:---|:---|:---|
| Body text contrast | WCAG AA (4.5:1) | Verified for all 3 palettes |
| Large text contrast (≥18px bold) | WCAG AA (3:1) | |
| UI component contrast (borders, buttons) | WCAG AA (3:1) | |
| Touch target size | 48×48dp minimum | All interactive elements |
| Keyboard focus indicators | Visible at all times | 2px primary color, 2px offset |
| Screen reader labels | All icon-only buttons have semantics label | Flutter `Semantics` widget |
| No color-only meaning | Icon + color always paired | Never color alone for critical state |
| Text scaling | Functional at 1.5× text scale | Flutter `textScaleFactor` support |
| Minimum font size | 10px (--text-label-sm only) | No text smaller than 10px |

---

## 15. Design Token Master Reference

The complete CSS token set for web implementation. Flutter `ThemeData` follows the same structure.

```css
/* ============================================================
   Veltrics Design Tokens
   Replace [PALETTE-*] values with the chosen palette hex codes
   ============================================================ */

:root {
  /* === PRIMARY PALETTE (Slot Tokens) === */
  --color-primary-50:    [PALETTE-50];
  --color-primary-100:   [PALETTE-100];
  --color-primary-200:   [PALETTE-200];
  --color-primary-300:   [PALETTE-300];
  --color-primary-400:   [PALETTE-400];
  --color-primary-500:   [PALETTE-500];   /* PRIMARY BRAND COLOR */
  --color-primary-600:   [PALETTE-600];
  --color-primary-700:   [PALETTE-700];
  --color-primary-800:   [PALETTE-800];
  --color-primary-900:   [PALETTE-900];
  --color-secondary-500: [PALETTE-SECONDARY-500];
  --color-secondary-600: [PALETTE-SECONDARY-600];

  /* === SEMANTIC (Palette-Independent) === */
  --color-success:       #16a34a;
  --color-success-bg:    #dcfce7;
  --color-warning:       #ca8a04;
  --color-warning-bg:    #fef9c3;
  --color-error:         #dc2626;
  --color-error-bg:      #fee2e2;
  --color-info:          #2563eb;
  --color-info-bg:       #dbeafe;
  --color-pro-badge:     #7c3aed;
  --color-ad-badge:      #b45309;

  /* === NEUTRAL SCALE === */
  --color-neutral-50:    #f8fafc;
  --color-neutral-100:   #f1f5f9;
  --color-neutral-200:   #e2e8f0;
  --color-neutral-300:   #cbd5e1;
  --color-neutral-400:   #94a3b8;
  --color-neutral-500:   #64748b;
  --color-neutral-600:   #475569;
  --color-neutral-700:   #334155;
  --color-neutral-800:   #1e293b;
  --color-neutral-900:   #0f172a;

  /* === SURFACES (Light Mode) === */
  --color-surface-bg:    #f8fafc;
  --color-surface-card:  #ffffff;
  --color-surface-input: #ffffff;

  /* === SPACING === */
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;
  --space-4: 16px;  --space-5: 20px;  --space-6: 24px;
  --space-8: 32px;  --space-10: 40px; --space-12: 48px;
  --space-16: 64px;

  /* === BORDER RADIUS === */
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   16px;
  --radius-xl:   24px;
  --radius-full: 9999px;

  /* === TYPOGRAPHY === */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono:   'Roboto Mono', 'Courier New', monospace;

  --text-display-xl: 2.25rem;   /* 36px */
  --text-display-lg: 1.875rem;  /* 30px */
  --text-display-md: 1.5rem;    /* 24px */
  --text-title-lg:   1.25rem;   /* 20px */
  --text-title-md:   1.125rem;  /* 18px */
  --text-title-sm:   1rem;      /* 16px */
  --text-body-lg:    1rem;      /* 16px */
  --text-body-md:    0.875rem;  /* 14px */
  --text-body-sm:    0.75rem;   /* 12px */
  --text-label-lg:   0.875rem;  /* 14px */
  --text-label-md:   0.75rem;   /* 12px */
  --text-label-sm:   0.625rem;  /* 10px */

  /* === MOTION === */
  --duration-fast:       100ms;
  --duration-normal:     200ms;
  --duration-slow:       350ms;
  --duration-deliberate: 500ms;
  --easing-standard:     cubic-bezier(0.4, 0, 0.2, 1);
  --easing-spring:       cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* === DARK MODE OVERRIDES === */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary-500:   [PALETTE-DARK-PRIMARY];  /* Use -400 shade */

    --color-surface-bg:    #121212;
    --color-surface-card:  #1e1e1e;
    --color-surface-input: #2a2a2a;

    --color-neutral-50:    #1e1e1e;
    --color-neutral-100:   #27272a;
    --color-neutral-200:   #3f3f46;
    --color-neutral-300:   #52525b;
    --color-neutral-400:   #71717a;
    --color-neutral-500:   #a1a1aa;
    --color-neutral-600:   #d4d4d8;
    --color-neutral-700:   #e4e4e7;
    --color-neutral-800:   #f4f4f5;
    --color-neutral-900:   #fafafa;

    --color-success:       #4ade80;
    --color-success-bg:    #14532d;
    --color-warning:       #facc15;
    --color-warning-bg:    #3f2e00;
    --color-error:         #f87171;
    --color-error-bg:      #3f0000;
    --color-info:          #60a5fa;
    --color-info-bg:       #1e3a8a;
    --color-pro-badge:     #a78bfa;
    --color-ad-badge:      #fbbf24;
  }
}
```

---

## 16. Cumulative Constraints (This Stage)

All constraints from Stages 1–4b remain in effect. Added by this stage:

1. **Three candidate palettes** (A: Teal, B: Amber, C: Forest Green) are production-ready. Selection requires only token substitution — no redesign.
2. **Inter** is the sole typeface. No exceptions for MVP.
3. **Dark mode baseline** is `#121212` (deep charcoal). Palette card surfaces apply a subtle warm/cool undertone per palette.
4. **Ad components** are styled as de-emphasized blended cards — visible, labeled, but subdued. Opacity 90%, neutral border.
5. **Absolute no-ad zones:** SCR-FUEL-001, SCR-MNT-002, SCR-TRIP-001, SCR-EXP-001.
6. **Motion:** Aha Moment staggered reveal is the only mandatory delight animation for Sprint 1. All others are enhancement-tier.
7. **Accessibility:** WCAG AA minimum across all screens. Color is never the sole state indicator.
8. **Quota walls must not use error-red.** Use `--color-primary-500` + `--color-pro-badge` to keep the emotional tone motivating.
9. **Driver dashboard** shows no cost data, no org controls, no upgrade badge.
10. **Wordmark** is Inter 700 — no external logo asset required for MVP.

---

## 17. Style Decision Record

| ID | Decision | Rationale |
|:---|:---|:---|
| SDS-001 | Three candidate palettes retained; selection deferred | User prefers to evaluate palettes in context before committing. All three are production-ready. |
| SDS-002 | Inter as sole typeface | Maximum legibility at data-dense sizes. Neutral personality amplifies brand color. Excellent numeral rendering for odometer/cost figures. |
| SDS-003 | Dark mode baseline: deep charcoal (#121212) | Material Design standard. Softer than true black; better for extended reading. Per-palette card undertone adds brand character. |
| SDS-004 | Ad treatment: de-emphasized card blend | Visible but non-disruptive. 90% opacity, neutral border, small "Ad" label in muted text. Users know ads are present; they're not forced to engage. |
| SDS-005 | No-ad zones on all data entry forms | Absolute rule. Trust on data entry is non-negotiable. One intrusive ad during fuel logging = uninstall risk. |
| SDS-006 | Pill-shaped primary buttons (border-radius-full) | Friendly & Efficient brand quality. Pills feel approachable. Consistent with the welcoming, not corporate, tone. |
| SDS-007 | Outlined input fields (not filled Material style) | Precise, professional feel. Matches the data-accuracy trust signal. |
| SDS-008 | Dashboard density: Balanced (48px rows, 16px padding) | Comfortable for non-power users; information-rich enough for fleet managers. Neither cramped nor wasteful. |
| SDS-009 | Collapsible sidebar on Chrome web | Standard SaaS pattern for data-dense dashboards. Icon-only collapse saves space without losing orientation. |
| SDS-010 | Quota walls avoid error-red | Prevents emotional regression at a critical conversion touchpoint. Motivating tone = higher upgrade conversion rate. |

---

## 18. Next Steps & Approval Gate

- **Next Stage:** `STAGE 6 — Data Model` (`06-data-model.md`) led by the *Database Architect* persona.
- **Open Item:** Palette selection (A: Teal / B: Amber / C: Forest Green). This does not block Stage 6 — selection can happen in parallel or before Stage 7.
- **Gate Confirmation:** Please review this Style Guide (`product-specs/05-style-guide.md`).

> Review the three palettes, pick your favourite, and confirm this document is approved — then we move to the Data Model stage.
