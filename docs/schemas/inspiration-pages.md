# inspiration_pages — schema reference

`inspiration_pages` is a catalog of analyzed real-world reference pages — one row per screenshot, each tagged for `page_type`, style family, mood, audience and structural signals so an agent can find similar examples before scaffolding a new page.

The catalog ships **405 rows** spanning 11 page types (marketing landings, signups, blog indexes, pricing, portfolios, ecommerce home, careers, about, etc.). Every row includes the ordered section list, role-mapped palette, typography choice, primary CTA, and a generation prompt for landing/signup pages.

→ Query via [`list_inspiration_pages`](#list_inspiration_pages--get_inspiration_page) · See also [data-model.md](../data-model.md)

---

## Row shape

### Identification

| Field | Type | Notes |
|---|---|---|
| `id` | `TEXT` (PK) | Slug like `page_<descriptor>` |
| `source` | `TEXT` | Origin of the screenshot (e.g. `land-book`) |
| `url_guess` | `TEXT?` | Best-effort original URL when known |
| `captured_at` | `DATE` | When the screenshot was taken |
| `screenshot_path` | `TEXT` | Reference path; not a publicly served asset in v1 |

### Classification (filterable scalars)

| Field | Type | Valid values |
|---|---|---|
| `page_type` | `TEXT` | `marketing_landing`, `about`, `blog_index`, `blog_post`, `careers`, `ecommerce_home`, `portfolio`, `pricing`, `product_listing`, `product_page`, `signup` |
| `landing_pattern_id` | `TEXT?` | Soft reference to `landing_patterns`. Non-null only when `page_type = 'marketing_landing'` |
| `style_family` | `TEXT?` | Visual family descriptor (e.g. `editorial_serif`, `tactile_neo`) |
| `industry` | `TEXT?` | Industry tag (e.g. `fintech`, `healthcare`, `developer_tools`) |
| `product_category` | `TEXT?` | Product-shape tag (e.g. `saas`, `marketplace`, `agency_site`) |
| `audience` | `TEXT?` | Target audience descriptor |
| `appearance` | `TEXT` | `light` · `dark` · `mixed` |
| `density` | `TEXT?` | `compact` · `comfortable` · `spacious` |

### Tag arrays (GIN-filterable, lowercased at ingest)

| Field | Type | Cardinality |
|---|---|---|
| `mood` | `TEXT[]` | 2–6 |
| `visual_signatures` | `TEXT[]` | unconstrained |
| `keywords` | `TEXT[]` | 8–20 |
| `good_for_product_types` | `TEXT[]` | 2–6 |
| `good_for_moods` | `TEXT[]` | 2–6 |
| `good_for_stages` | `TEXT[]` | 1–5 |
| `section_order` | `TEXT[]` | ordered section types as they appear on the page |

### Structured (JSONB)

| Field | Shape |
|---|---|
| `palette` | `{ role_intent: { primary_accent, ink, ... }, palette_strategy, contrast_character, notes }` |
| `typography` | `{ heading: {...}, body: {...}, treatments, eyebrow_pattern }` with open-source equivalents |
| `primary_cta` | `{ label_example, placements[], style }` (nullable) |
| `sections` | Ordered array of section objects matching `section_order` |
| `inspiration_metadata` | Mirrors the tag arrays + `standout_qualities`, `not_recommended_for` |
| `reference_for` | `{ styles[], domains[], moods[] }` — what this page is a good reference *for* |
| `effects` | List of effect descriptors (e.g. parallax, scroll-driven) |
| `interaction_cues` | Notable interaction patterns observed |
| `generation_constraints` | `{ hard_rules, soft_guidance }` — populated only for `marketing_landing` and `signup` |

### Prose

| Field | When populated |
|---|---|
| `description` | Always — neutral 2–4 sentence summary |
| `why_it_works` | Always — 2–4 sentence UX rationale |
| `use_when` | When known — 1–3 sentence "situational call" for picking this reference over similar ones |
| `generation_prompt` | Required for `marketing_landing` and `signup`; optional elsewhere |
| `notes` | Free-form |

---

## Querying via MCP

### `list_inspiration_pages` · `get_inspiration_page`

```text
list_inspiration_pages(
  page_type?, appearance?, style_family?, industry?, density?,
  mood?, keyword?, signature?,
  good_for_product_type?, good_for_stage?,
  limit=25, offset=0
) -> { items: [...], total_count, limit, offset, meta }

get_inspiration_page(page_id: str) -> full row | NOT_FOUND
```

**Filter semantics:**

- Scalar args (`page_type`, `appearance`, `style_family`, `industry`, `density`) are exact-match.
- Tag-array args (`mood`, `keyword`, `signature`, `good_for_product_type`, `good_for_stage`) match a single value against the corresponding `TEXT[]` column. Pass values lowercased — that is the ingest convention.
- All filters AND together. There is no OR / negation operator in v1.

`get_inspiration_page` returns the full row (including all JSONB fields) or a structured `NOT_FOUND` error when the id is unknown.

### `list_inspiration_page_facets`

```text
list_inspiration_page_facets() -> {
  page_types: [...],
  style_families: [...],
  industries: [...],
  appearances: [...],
  densities: [...],
  moods: [...],
  signatures: [...],
  good_for_product_types: [...],
  good_for_stages: [...],
  ...
}
```

Use this once at the start of a session to discover valid filter values. The facets list is the source of truth — it reflects the values actually present in the catalog, not just the schema-allowed vocabulary.

---

## Examples

### Find dark, "moody" landing pages for a fintech product

```text
list_inspiration_pages(
  page_type="marketing_landing",
  appearance="dark",
  industry="fintech",
  mood="moody",
  limit=10
)
```

Returns up to 10 summaries. Each item includes `id`, `style_family`, `mood`, `keywords`, and a short `description`. Drill into a specific page with `get_inspiration_page(page_id="page_…")` to read the full sections array, palette, typography, and `generation_prompt`.

### Discover what moods exist before filtering

```text
list_inspiration_page_facets()
```

Read `moods` from the response, then issue a `list_inspiration_pages` call with the chosen value as `mood=…`.

### Find signup pages that work for early-stage products

```text
list_inspiration_pages(
  page_type="signup",
  good_for_stage="pre_seed",
  limit=5
)
```

Each result will include a `generation_prompt` and `generation_constraints` (`hard_rules` + `soft_guidance`) — both required for signup pages — that an agent can paste into a generation step.
