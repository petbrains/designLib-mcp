-- ============================================================
-- Animations catalog (~120 rows initial)
-- ============================================================

CREATE TABLE IF NOT EXISTS animations (
  id                 TEXT PRIMARY KEY,
  title              TEXT NOT NULL,
  description        TEXT NOT NULL,
  use_when           TEXT[] NOT NULL DEFAULT '{}',
  category           TEXT NOT NULL,
  framework          TEXT NOT NULL,
  libraries          TEXT[] NOT NULL DEFAULT '{}',
  interactivity      TEXT NOT NULL,
  complexity         TEXT NOT NULL,
  style_tags         TEXT[] NOT NULL DEFAULT '{}',
  placement          TEXT[] NOT NULL DEFAULT '{}',
  keyword            TEXT[] NOT NULL DEFAULT '{}',
  component_filename TEXT NOT NULL,
  prompt_text        TEXT NOT NULL,
  source_file        TEXT NOT NULL,
  source_index       INTEGER NOT NULL,
  sort_order         INTEGER NOT NULL DEFAULT 0,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT animations_category_valid CHECK (
    category IN ('background','hero','loader','text_effect','element',
                 'cursor_effect','overlay','decoration')
  ),
  CONSTRAINT animations_framework_valid CHECK (
    framework IN ('react','vanilla_html')
  ),
  CONSTRAINT animations_interactivity_valid CHECK (
    interactivity IN ('static','hover','click','cursor_track','scroll','mount_only')
  ),
  CONSTRAINT animations_complexity_valid CHECK (
    complexity IN ('light','medium','heavy')
  )
);

CREATE INDEX IF NOT EXISTS idx_animations_category    ON animations(category);
CREATE INDEX IF NOT EXISTS idx_animations_framework   ON animations(framework);
CREATE INDEX IF NOT EXISTS idx_animations_keyword     ON animations USING GIN(keyword);
CREATE INDEX IF NOT EXISTS idx_animations_use_when    ON animations USING GIN(use_when);
CREATE INDEX IF NOT EXISTS idx_animations_style_tags  ON animations USING GIN(style_tags);
CREATE INDEX IF NOT EXISTS idx_animations_libraries   ON animations USING GIN(libraries);
CREATE INDEX IF NOT EXISTS idx_animations_placement   ON animations USING GIN(placement);

ALTER TABLE animations ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read" ON animations;
CREATE POLICY "public_read" ON animations FOR SELECT TO anon, authenticated USING (true);
