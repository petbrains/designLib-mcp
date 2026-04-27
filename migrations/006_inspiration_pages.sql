-- ============================================================
-- Inspiration Pages — page-level design analysis catalog
-- One row per analyzed screenshot. Source: extracted/<category>/*.json
-- Schema follows PAGE_ANALYSIS_PROMPT.md §3.
-- ============================================================

CREATE TABLE IF NOT EXISTS inspiration_pages (
  id                 TEXT PRIMARY KEY,                                  -- "page_<slug>"
  source             TEXT NOT NULL,                                      -- e.g. "land-book"
  url_guess          TEXT,
  captured_at        DATE NOT NULL,
  screenshot_path    TEXT NOT NULL,                                      -- relative path under repo (or storage URL later)

  -- Classification (top-level scalars for filtering)
  page_type          TEXT NOT NULL,                                      -- vocab §2.1
  landing_pattern_id TEXT,                                                -- soft reference: JSON-side IDs are descriptive (87 distinct) and don't all map to canonical landing_patterns table (34 rows). Resolve at query time when needed.
  style_family       TEXT,
  industry           TEXT,
  product_category   TEXT,
  audience           TEXT,
  appearance         TEXT NOT NULL,                                      -- light|dark|mixed
  density            TEXT,                                               -- compact|comfortable|spacious
  mood               TEXT[] NOT NULL DEFAULT '{}',                       -- §2.8 moods (2-6)

  -- Tag arrays (GIN-indexed for @> filtering)
  visual_signatures        TEXT[] NOT NULL DEFAULT '{}',                 -- §2.3
  keywords                 TEXT[] NOT NULL DEFAULT '{}',                 -- 8-20
  good_for_product_types   TEXT[] NOT NULL DEFAULT '{}',                 -- §2.8 product_types (2-6)
  good_for_moods           TEXT[] NOT NULL DEFAULT '{}',                 -- §2.8 moods (2-6)
  good_for_stages          TEXT[] NOT NULL DEFAULT '{}',                 -- §2.8 stages (1-5)
  section_order            TEXT[] NOT NULL DEFAULT '{}',                 -- ordered §2.4 section types

  -- Nested structured (JSONB)
  palette                  JSONB NOT NULL,                               -- {role_intent, palette_strategy, contrast_character, notes}
  typography               JSONB NOT NULL,                               -- heading/body family + treatment + eyebrow_pattern
  primary_cta              JSONB,                                        -- {label_example, placements, style} | null
  sections                 JSONB NOT NULL,                               -- ordered array of §3 section objects
  inspiration_metadata     JSONB NOT NULL,                               -- mirror of TEXT[] tag arrays + standout_qualities/not_recommended_for
  reference_for            JSONB NOT NULL,                               -- {styles, domains, moods}
  effects                  JSONB NOT NULL DEFAULT '[]'::jsonb,
  interaction_cues         JSONB NOT NULL DEFAULT '[]'::jsonb,
  generation_constraints   JSONB,                                        -- {hard_rules, soft_guidance} | null

  -- Prose (human-review fields)
  description              TEXT NOT NULL,
  why_it_works             TEXT NOT NULL,
  generation_prompt        TEXT,                                         -- non-null IFF page_type IN (marketing_landing, signup)
  notes                    TEXT,

  created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),

  -- Vocabulary constraints
  CONSTRAINT valid_page_type CHECK (page_type IN (
    'marketing_landing','about','blog_index','blog_post','careers',
    'ecommerce_home','portfolio','pricing','product_listing','product_page','signup'
  )),
  CONSTRAINT valid_appearance CHECK (appearance IN ('light','dark','mixed')),
  CONSTRAINT valid_density CHECK (density IS NULL OR density IN ('compact','comfortable','spacious')),

  -- Schema-level consistency rules from PAGE_ANALYSIS_PROMPT §6
  CONSTRAINT landing_pattern_consistency CHECK (
    (page_type = 'marketing_landing' AND landing_pattern_id IS NOT NULL)
    OR (page_type <> 'marketing_landing' AND landing_pattern_id IS NULL)
  ),
  CONSTRAINT generation_consistency CHECK (
    (page_type IN ('marketing_landing','signup')
       AND generation_prompt IS NOT NULL
       AND generation_constraints IS NOT NULL)
    OR (page_type NOT IN ('marketing_landing','signup')
       AND generation_prompt IS NULL
       AND generation_constraints IS NULL)
  ),
  CONSTRAINT mood_count_2_6        CHECK (cardinality(mood) BETWEEN 2 AND 6),
  CONSTRAINT keywords_count_8_20   CHECK (cardinality(keywords) BETWEEN 8 AND 20),
  CONSTRAINT gfm_count_2_6         CHECK (cardinality(good_for_moods) BETWEEN 2 AND 6),
  CONSTRAINT gfpt_count_2_6        CHECK (cardinality(good_for_product_types) BETWEEN 2 AND 6),
  CONSTRAINT gfs_count_1_5         CHECK (cardinality(good_for_stages) BETWEEN 1 AND 5)
);

-- Filter indexes
CREATE INDEX IF NOT EXISTS idx_insp_pages_page_type        ON inspiration_pages(page_type);
CREATE INDEX IF NOT EXISTS idx_insp_pages_landing_pattern  ON inspiration_pages(landing_pattern_id) WHERE landing_pattern_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_insp_pages_appearance       ON inspiration_pages(appearance);
CREATE INDEX IF NOT EXISTS idx_insp_pages_style_family     ON inspiration_pages(style_family);
CREATE INDEX IF NOT EXISTS idx_insp_pages_industry         ON inspiration_pages(industry);
CREATE INDEX IF NOT EXISTS idx_insp_pages_product_category ON inspiration_pages(product_category);
CREATE INDEX IF NOT EXISTS idx_insp_pages_density          ON inspiration_pages(density);

-- Tag-array GIN indexes (lowercased ingest convention — see scripts/ingest_inspiration_pages.py)
CREATE INDEX IF NOT EXISTS idx_insp_pages_mood             ON inspiration_pages USING GIN(mood);
CREATE INDEX IF NOT EXISTS idx_insp_pages_signatures       ON inspiration_pages USING GIN(visual_signatures);
CREATE INDEX IF NOT EXISTS idx_insp_pages_keywords         ON inspiration_pages USING GIN(keywords);
CREATE INDEX IF NOT EXISTS idx_insp_pages_gf_product_types ON inspiration_pages USING GIN(good_for_product_types);
CREATE INDEX IF NOT EXISTS idx_insp_pages_gf_moods         ON inspiration_pages USING GIN(good_for_moods);
CREATE INDEX IF NOT EXISTS idx_insp_pages_gf_stages        ON inspiration_pages USING GIN(good_for_stages);
CREATE INDEX IF NOT EXISTS idx_insp_pages_section_order    ON inspiration_pages USING GIN(section_order);

-- ============================================================
-- RLS — public read (consistent with rest of catalog)
-- ============================================================

ALTER TABLE inspiration_pages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read" ON inspiration_pages;
CREATE POLICY "public_read" ON inspiration_pages FOR SELECT TO anon, authenticated USING (true);
