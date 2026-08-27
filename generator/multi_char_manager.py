class MultiCharManager:
    """
    Collects multi-codepoint confusable mappings. Unlike single-codepoint homoglyphs
    (where a group of characters are mutually confusable), a multi-codepoint confusable
    maps a single 'glyph' character to a *sequence* of prototype characters that it
    resembles - for example 'ﬃ' (U+FB03) looks like the three characters "ffi", and
    the letter 'm' looks like the two characters "rn".
    """
    def __init__(self):
        self.glyph_to_prototypes = {}

    def add(self, glyph, prototype):
        # A glyph should never resemble itself as a longer sequence.
        if prototype == glyph:
            return
        self.glyph_to_prototypes.setdefault(glyph, set()).add(prototype)

    def get_prototypes_for_glyph(self, glyph):
        return sorted(self.glyph_to_prototypes.get(glyph, set()))

    def get_list_of_mappings(self):
        # Deterministic, sorted list of (glyph, [prototype, ...]) so generated output is stable.
        return [
            (glyph, sorted(prototypes))
            for glyph, prototypes in sorted(self.glyph_to_prototypes.items())
        ]
