from designlib_mcp.repository.base import CatalogRepository


def test_protocol_has_required_methods():
    methods = {
        "list_styles", "get_style", "list_style_facets",
        "list_palettes", "get_palette", "list_palette_facets",
        "list_font_pairs", "get_font_pair", "list_font_pair_facets",
        "list_domains", "get_domain", "list_domain_facets",
    }
    for m in methods:
        assert hasattr(CatalogRepository, m), f"missing {m}"
