-- ============================================================
-- Design Builder v2 — Initial Schema
-- 15 tables + 3 views + RLS policies
-- ============================================================

-- 1. style_families (9 rows)
CREATE TABLE style_families (
  id          TEXT PRIMARY KEY,
  name_en     TEXT NOT NULL,
  description TEXT,
  sort_order  INTEGER NOT NULL DEFAULT 0,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. domain_categories (15 rows)
CREATE TABLE domain_categories (
  id           TEXT PRIMARY KEY,
  name_en      TEXT NOT NULL,
  description  TEXT,
  domain_count INTEGER NOT NULL DEFAULT 0,
  sort_order   INTEGER NOT NULL DEFAULT 0,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. font_pair_categories (7 rows)
CREATE TABLE font_pair_categories (
  id          TEXT PRIMARY KEY,
  name_en     TEXT NOT NULL,
  description TEXT,
  sort_order  INTEGER NOT NULL DEFAULT 0,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4. domains (134 rows)
CREATE TABLE domains (
  id           TEXT PRIMARY KEY,
  category_id  TEXT NOT NULL REFERENCES domain_categories(id) ON DELETE RESTRICT,
  name_en      TEXT NOT NULL,
  ui_patterns  TEXT[] NOT NULL DEFAULT '{}',
  tone         TEXT[] NOT NULL DEFAULT '{}',
  data_density TEXT NOT NULL,
  audience     TEXT NOT NULL,
  examples     TEXT[] NOT NULL DEFAULT '{}',
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT valid_data_density CHECK (
    data_density IN ('very_high','high','medium_high','medium','low_medium','low')
  )
);

CREATE INDEX idx_domains_category ON domains(category_id);
CREATE INDEX idx_domains_data_density ON domains(data_density);

-- 5. design_styles (47 rows)
CREATE TABLE design_styles (
  id                  TEXT PRIMARY KEY,
  family_id           TEXT NOT NULL REFERENCES style_families(id) ON DELETE RESTRICT,
  name_en             TEXT NOT NULL,
  description         TEXT NOT NULL,
  visual_signatures   TEXT[] NOT NULL DEFAULT '{}',
  emotional_keywords  TEXT[] NOT NULL DEFAULT '{}',
  anti_patterns       TEXT[] NOT NULL DEFAULT '{}',
  tokens              JSONB NOT NULL,
  reference_products  JSONB NOT NULL DEFAULT '[]',
  domain_fit          JSONB NOT NULL DEFAULT '{}',
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_design_styles_family ON design_styles(family_id);

-- 6. color_palettes (87 rows — brand + collection unified)
CREATE TABLE color_palettes (
  id              TEXT PRIMARY KEY,
  palette_type    TEXT NOT NULL,
  family_id       TEXT REFERENCES style_families(id) ON DELETE SET NULL,
  name            TEXT NOT NULL,
  colors          JSONB NOT NULL,
  tags            TEXT[] NOT NULL DEFAULT '{}',
  style_fit       TEXT[] NOT NULL DEFAULT '{}',
  wcag_aa         BOOLEAN,
  dark_mode_first BOOLEAN NOT NULL DEFAULT false,
  sort_order      INTEGER NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT valid_palette_type CHECK (palette_type IN ('brand', 'collection'))
);

CREATE INDEX idx_color_palettes_type ON color_palettes(palette_type);
CREATE INDEX idx_color_palettes_family ON color_palettes(family_id) WHERE family_id IS NOT NULL;
CREATE INDEX idx_color_palettes_style_fit ON color_palettes USING GIN(style_fit);

-- 7. color_psychology (14 rows)
CREATE TABLE color_psychology (
  id                   TEXT PRIMARY KEY,
  name                 TEXT NOT NULL,
  name_en              TEXT NOT NULL,
  hue_range            INTEGER[] NOT NULL,
  emotions             TEXT[] NOT NULL DEFAULT '{}',
  psychological_effect TEXT NOT NULL,
  best_for             TEXT[] NOT NULL DEFAULT '{}',
  avoid_for            TEXT[] NOT NULL DEFAULT '{}',
  brands               TEXT[] NOT NULL DEFAULT '{}',
  family_affinity      JSONB NOT NULL DEFAULT '{}',
  ui_usage             JSONB NOT NULL DEFAULT '{}',
  real_product_usage   TEXT[] NOT NULL DEFAULT '{}',
  created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 8. font_pairs (28 rows)
CREATE TABLE font_pairs (
  id             TEXT PRIMARY KEY,
  name           TEXT NOT NULL,
  category_id    TEXT NOT NULL REFERENCES font_pair_categories(id) ON DELETE RESTRICT,
  heading        JSONB NOT NULL,
  body           JSONB NOT NULL,
  mono           JSONB,
  import_url     TEXT NOT NULL,
  size_kb        INTEGER NOT NULL,
  variable_font  BOOLEAN NOT NULL DEFAULT false,
  line_heights   JSONB NOT NULL,
  letter_spacing JSONB NOT NULL,
  mood           TEXT[] NOT NULL DEFAULT '{}',
  use_cases      TEXT[] NOT NULL DEFAULT '{}',
  style_fit      TEXT[] NOT NULL DEFAULT '{}',
  domain_fit     TEXT[] NOT NULL DEFAULT '{}',
  used_by        TEXT[] NOT NULL DEFAULT '{}',
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_font_pairs_category ON font_pairs(category_id);
CREATE INDEX idx_font_pairs_style_fit ON font_pairs USING GIN(style_fit);

-- 9. icon_libraries (13 rows)
CREATE TABLE icon_libraries (
  id              TEXT PRIMARY KEY,
  name            TEXT NOT NULL,
  url             TEXT NOT NULL,
  license         TEXT NOT NULL,
  license_notes   TEXT,
  icon_count      INTEGER NOT NULL,
  icon_count_pro  INTEGER,
  total_variations INTEGER,
  icon_type       TEXT,
  packages        JSONB NOT NULL DEFAULT '{}',
  install         TEXT NOT NULL,
  import_example  TEXT NOT NULL,
  visual          JSONB NOT NULL,
  technical       JSONB NOT NULL,
  character       JSONB NOT NULL,
  tags            JSONB NOT NULL,
  notes           TEXT,
  unique_features JSONB,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 10. animation_presets (50 rows)
CREATE TABLE animation_presets (
  id                 TEXT PRIMARY KEY,
  category           TEXT NOT NULL,
  name               TEXT NOT NULL,
  description        TEXT,
  preview            TEXT,
  css                JSONB NOT NULL,
  tailwind           TEXT,
  framer_motion      JSONB NOT NULL,
  gsap               TEXT,
  parameters         JSONB NOT NULL DEFAULT '{}',
  intensity          TEXT,
  feel               TEXT[] DEFAULT '{}',
  style_fit          TEXT[] DEFAULT '{}',
  use_for            TEXT[] DEFAULT '{}',
  performance_impact TEXT,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT valid_animation_category CHECK (
    category IN ('entrance','exit','hover','loading','microInteractions','decorative')
  )
);

CREATE INDEX idx_animation_presets_category ON animation_presets(category);

-- 11. animation_themed_collections (8 rows)
CREATE TABLE animation_themed_collections (
  id                    TEXT PRIMARY KEY,
  name                  TEXT NOT NULL,
  description           TEXT,
  style_family_id       TEXT REFERENCES style_families(id) ON DELETE SET NULL,
  style_ids             TEXT[] NOT NULL DEFAULT '{}',
  characteristics       JSONB NOT NULL,
  included_animations   TEXT[] NOT NULL DEFAULT '{}',
  avoid_animations      TEXT[] NOT NULL DEFAULT '{}',
  optional_animations   TEXT[] DEFAULT '{}',
  css_variables         JSONB NOT NULL DEFAULT '{}',
  framer_motion_preset  JSONB NOT NULL DEFAULT '{}',
  real_evidence         JSONB,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 12. background_types (28 rows)
CREATE TABLE background_types (
  id              TEXT PRIMARY KEY,
  category        TEXT NOT NULL,
  name            TEXT NOT NULL,
  implementation  JSONB NOT NULL,
  customization   JSONB NOT NULL,
  character       JSONB NOT NULL,
  performance     JSONB NOT NULL,
  combinations    JSONB NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT valid_bg_category CHECK (
    category IN ('solidsAndGradients','geometricPatterns','noiseAndTexture','decorative','specialEffects')
  )
);

CREATE INDEX idx_background_types_category ON background_types(category);

-- 13. ui_libraries (6 rows)
CREATE TABLE ui_libraries (
  id                    TEXT PRIMARY KEY,
  name                  TEXT NOT NULL,
  framework             TEXT[] NOT NULL DEFAULT '{}',
  styling               TEXT NOT NULL,
  bundle_size           TEXT NOT NULL,
  bundle_size_note      TEXT,
  description           TEXT NOT NULL,
  pros                  TEXT[] NOT NULL DEFAULT '{}',
  cons                  TEXT[] NOT NULL DEFAULT '{}',
  install_command       TEXT NOT NULL,
  documentation         TEXT NOT NULL,
  variants              JSONB NOT NULL,
  style_recommendations TEXT[] NOT NULL DEFAULT '{}',
  best_for              TEXT[] NOT NULL DEFAULT '{}',
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 14. recommendation_scores (~500 rows)
CREATE TABLE recommendation_scores (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  matrix_type TEXT NOT NULL,
  key_a       TEXT NOT NULL,
  key_b       TEXT NOT NULL,
  score       INTEGER NOT NULL,
  refs        TEXT,

  CONSTRAINT valid_score CHECK (score BETWEEN -2 AND 2),
  CONSTRAINT valid_matrix_type CHECK (
    matrix_type IN ('style_domain', 'style_audience', 'style_tone')
  ),
  UNIQUE(matrix_type, key_a, key_b)
);

CREATE INDEX idx_rec_scores_lookup ON recommendation_scores(matrix_type, key_a);

-- 15. app_config (key-value store for misc config)
CREATE TABLE app_config (
  key         TEXT PRIMARY KEY,
  data        JSONB NOT NULL,
  description TEXT,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- Views
-- ============================================================

-- Replaces design_mappings.by_density
CREATE VIEW domain_density_mapping AS
SELECT
  data_density,
  array_agg(id ORDER BY id) AS domain_ids
FROM domains
GROUP BY data_density;

-- Replaces design_mappings.by_tone_category
CREATE VIEW domain_tone_mapping AS
SELECT
  tone_keyword,
  array_agg(d.id ORDER BY d.id) AS domain_ids
FROM domains d, unnest(d.tone) AS tone_keyword
GROUP BY tone_keyword;

-- Style family counts (replaces hardcoded count field)
CREATE VIEW style_family_counts AS
SELECT
  sf.id,
  sf.name_en,
  sf.description,
  sf.sort_order,
  COALESCE(c.cnt, 0)::INTEGER AS count
FROM style_families sf
LEFT JOIN (
  SELECT family_id, COUNT(*) AS cnt
  FROM design_styles
  GROUP BY family_id
) c ON c.family_id = sf.id
ORDER BY sf.sort_order;

-- ============================================================
-- Row Level Security — public read, no write via API
-- ============================================================

ALTER TABLE style_families ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON style_families FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE domain_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON domain_categories FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE font_pair_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON font_pair_categories FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE domains ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON domains FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE design_styles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON design_styles FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE color_palettes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON color_palettes FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE color_psychology ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON color_psychology FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE font_pairs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON font_pairs FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE icon_libraries ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON icon_libraries FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE animation_presets ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON animation_presets FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE animation_themed_collections ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON animation_themed_collections FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE background_types ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON background_types FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE ui_libraries ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON ui_libraries FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE recommendation_scores ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON recommendation_scores FOR SELECT TO anon, authenticated USING (true);

ALTER TABLE app_config ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON app_config FOR SELECT TO anon, authenticated USING (true);
