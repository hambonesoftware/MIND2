from __future__ import annotations

import math
import random

from .models import BarModifiers, MelodyContourProfile, RhythmProfile, SectionDef, SongPlan
from .utils import clamp, clamp01, lerp, pick_weighted
from .theory.progression import ProgressionGenerator


def _choose_section_pattern_by_phrases(rng: random.Random, phrase_count: int) -> list[str]:
    """
    Choose a pop-ish section pattern in 4-bar phrases.
    Returns list of section codes with length == phrase_count.
    """
    # V=Verse, C=Chorus, B=Bridge, I=Intro, O=Outro
    library = {
        1: [
            ["C"],
            ["V"],
        ],
        2: [
            ["V", "C"],
            ["C", "C"],
            ["I", "C"],
        ],
        3: [
            ["V", "C", "C"],
            ["V", "C", "V"],
            ["I", "V", "C"],
        ],
        4: [
            ["V", "C", "V", "C"],
            ["I", "V", "C", "C"],
            ["V", "V", "C", "C"],
        ],
        5: [
            ["V", "C", "V", "C", "O"],
            ["I", "V", "C", "V", "C"],
            ["V", "C", "V", "B", "C"],
        ],
        6: [
            ["V", "C", "V", "C", "B", "C"],
            ["I", "V", "C", "V", "B", "C"],
            ["V", "V", "C", "V", "B", "C"],
        ],
        7: [
            ["V", "C", "V", "C", "B", "C", "O"],
            ["I", "V", "C", "V", "C", "B", "C"],
        ],
        8: [
            ["I", "V", "C", "V", "C", "B", "C", "O"],
            ["V", "C", "V", "C", "B", "C", "V", "C"],
        ],
    }

    if phrase_count in library:
        return rng.choice(library[phrase_count])

    # If phrase_count > 8, build a reasonable long form:
    pattern = ["I", "V", "C", "V", "C"]
    # Insert bridge near the end
    while len(pattern) < phrase_count:
        if len(pattern) == phrase_count - 2:
            pattern.append("B")
        else:
            pattern.append("C" if rng.random() < 0.65 else "V")
    pattern = pattern[:phrase_count]
    if len(pattern) < phrase_count:
        pattern += ["C"] * (phrase_count - len(pattern))
    return pattern


def _section_code_to_name(code: str) -> str:
    return {
        "V": "verse",
        "C": "chorus",
        "B": "bridge",
        "I": "intro",
        "O": "outro",
    }.get(code, "verse")


def get_pop_templates(rng: random.Random, mode: str, style_tag: str = "pop"):
    """
    Returns a list of templates, each template is a dict with:
      - name
      - degrees: list of 4 items (int 0..6 or token strings like "bVII", "iv", "V/V")
      - tags: optional tags for filtering
    """
    generator = ProgressionGenerator(rng)
    return generator.templates_for_style(style_tag, mode)


def choose_section_templates(ctrl, rng: random.Random) -> dict:
    """
    Pick chord templates per section type. Returns:
      templates[section] = {"name": ..., "degrees": [...], "source": ...}
    """
    all_templates = get_pop_templates(rng, ctrl.mode, ctrl.derived.progression_style)
    level2 = ctrl.derived.level2
    functional_bias = lerp(0.75, 1.35, level2.functional_clarity)
    mixture_bias = lerp(0.75, 1.40, (level2.chromaticism * 0.65 + level2.extension_richness * 0.35))
    repetition_bias = lerp(0.90, 1.20, level2.motif_repetition)
    form_bias = lerp(0.85, 1.25, level2.form_strictness)
    lift_bias = {
        "lift": 1.20,
        "plateau": 1.00,
        "drop": 0.85,
    }.get(level2.lift_profile, 1.00)

    chorus_pool = []
    verse_pool = []
    bridge_pool = []
    intro_pool = []
    outro_pool = []

    for t in all_templates:
        tags = t.get("tags") or []
        # chorus likes pop/anthem/classic
        wc = 1.0
        if "anthem" in tags:
            wc *= 1.8 * lift_bias
        if "classic" in tags:
            wc *= 1.5 * functional_bias
        if "simple" in tags:
            wc *= 1.2 * form_bias
        if "mixture" in tags:
            wc *= mixture_bias

        # verse likes a bit more functional variety
        wv = 1.0
        if "functional" in tags:
            wv *= 1.6 * functional_bias
        if "smooth" in tags:
            wv *= 1.3
        if "mixture" in tags:
            wv *= mixture_bias

        # bridge likes contrast and mixture/functional
        wb = 1.0
        if "mixture" in tags:
            wb *= 1.8 * mixture_bias
        if "functional" in tags:
            wb *= 1.4 * functional_bias
        if "smooth" in tags:
            wb *= 1.2

        # intro/outro are often simpler
        wi = 1.0
        wo = 1.0
        if "simple" in tags:
            wi *= 1.6 * form_bias
            wo *= 1.6 * form_bias
        if "anthem" in tags:
            wi *= 0.9 * lift_bias
            wo *= 0.9 * lift_bias
        if "mixture" in tags:
            wi *= 0.9 * mixture_bias
            wo *= 1.0 * mixture_bias

        chorus_pool.append((t, wc))
        verse_pool.append((t, wv))
        bridge_pool.append((t, wb))
        intro_pool.append((t, wi))
        outro_pool.append((t, wo))

    def pick_template(pool):
        t = pick_weighted(rng, pool)
        return {"name": t["name"], "degrees": t["degrees"], "source": "seed_library"}

    verse_t = pick_template(verse_pool)
    chorus_t = pick_template(chorus_pool)
    bridge_t = pick_template(bridge_pool)

    # repetition affects template matching
    if level2.motif_repetition >= 0.70 and rng.random() < lerp(0.35, 0.75, level2.motif_repetition):
        anthem_candidates = [t for t in all_templates if "anthem" in (t.get("tags") or [])]
        if anthem_candidates:
            chosen = rng.choice(anthem_candidates)
            chorus_t = {"name": chosen["name"], "degrees": chosen["degrees"], "source": "seed_library_anthem"}

    if level2.motif_repetition >= 0.80 and rng.random() < lerp(0.20, 0.65, level2.motif_repetition):
        chorus_t = verse_t

    return {
        "intro": pick_template(intro_pool),
        "verse": verse_t,
        "chorus": chorus_t,
        "bridge": bridge_t,
        "outro": pick_template(outro_pool),
    }


def build_rhythm_profile(ctrl, rng_master: random.Random) -> RhythmProfile:
    rng = random.Random(rng_master.randint(0, 2**31 - 1))

    groove_map = {
        "straight": "straight_pop",
        "straight_pop": "straight_pop",
        "four_on_floor": "four_on_floor",
        "half_time": "half_time",
        "bouncy": "bouncy",
        "swing": "bouncy",
        "laid_back": "half_time",
        "latin": "bouncy",
        "waltz": "half_time",
        "march": "straight_pop",
    }
    profile = ctrl.derived.style_profile
    swing_min, swing_max = profile.swing_range
    swing_span = max(0.001, swing_max - swing_min)
    swing_norm = clamp01((ctrl.derived.swing - swing_min) / swing_span)

    mapped_weights: dict[str, float] = {}
    for name, weight in profile.groove_archetypes:
        mapped_name = groove_map.get(name, "straight_pop")
        adj = 1.0
        if mapped_name in {"bouncy", "half_time"}:
            adj *= lerp(0.90, 1.15, swing_norm)
        if mapped_name == "four_on_floor":
            adj *= lerp(1.05, 0.90, swing_norm)
        mapped_weights[mapped_name] = mapped_weights.get(mapped_name, 0.0) + weight * adj

    preferred = groove_map.get(ctrl.derived.level2.groove_archetype, "straight_pop")
    mapped_weights[preferred] = mapped_weights.get(preferred, 0.0) + 0.35

    archetypes = sorted(mapped_weights.items())
    archetype = pick_weighted(rng, archetypes)

    base_hat_steps = [0, 2, 4, 6, 8, 10, 12, 14]

    if archetype == "straight_pop":
        base_kick = [0, 8]
        base_snare = [4, 12]
        hat_16th_bias = lerp(0.10, 0.55, ctrl.derived.density) * lerp(0.95, 1.05, swing_norm)
        kick_sync_bias = lerp(0.08, 0.40, ctrl.derived.syncopation)
    elif archetype == "four_on_floor":
        base_kick = [0, 4, 8, 12]
        base_snare = [4, 12]
        hat_16th_bias = lerp(0.10, 0.65, ctrl.derived.density) * lerp(0.90, 1.05, swing_norm)
        kick_sync_bias = lerp(0.05, 0.25, ctrl.derived.syncopation)
    elif archetype == "half_time":
        base_kick = [0, 6, 8]
        base_snare = [8]
        hat_16th_bias = lerp(0.08, 0.55, ctrl.derived.density) * lerp(0.95, 1.10, swing_norm)
        kick_sync_bias = lerp(0.12, 0.55, ctrl.derived.syncopation)
    else:  # bouncy
        base_kick = [0, 7, 10]
        base_snare = [4, 12]
        hat_16th_bias = lerp(0.18, 0.80, ctrl.derived.density) * lerp(1.00, 1.15, swing_norm)
        kick_sync_bias = lerp(0.15, 0.60, ctrl.derived.syncopation)

    fill_style = pick_weighted(rng, [("snare_roll", 0.60), ("tom_fill", 0.40)])

    return RhythmProfile(
        archetype=archetype,
        base_kick_steps=sorted(set(base_kick)),
        base_snare_steps=sorted(set(base_snare)),
        base_hat_steps=base_hat_steps,
        hat_16th_bias=clamp01(hat_16th_bias),
        kick_sync_bias=clamp01(kick_sync_bias),
        fill_style=fill_style,
    )


def build_melody_contour(ctrl, rng_master: random.Random) -> MelodyContourProfile:
    rng = random.Random(rng_master.randint(0, 2**31 - 1))

    style_key = (ctrl.derived.progression_style or "pop").strip().lower()
    if style_key == "pop":
        kinds = [
            ("arch", 0.34),
            ("descending", 0.20),
            ("ascending", 0.20),
            ("wave", 0.16),
            ("plateau", 0.10),
        ]
        intensity_bounds = (0.30, 0.80)
    elif style_key == "jazz":
        kinds = [
            ("arch", 0.26),
            ("descending", 0.16),
            ("ascending", 0.16),
            ("wave", 0.32),
            ("plateau", 0.10),
        ]
        intensity_bounds = (0.45, 1.05)
    elif style_key == "classical":
        kinds = [
            ("arch", 0.45),
            ("descending", 0.20),
            ("ascending", 0.20),
            ("wave", 0.10),
            ("plateau", 0.05),
        ]
        intensity_bounds = (0.35, 0.90)
    else:
        kinds = [
            ("arch", 0.30),
            ("descending", 0.18),
            ("ascending", 0.18),
            ("wave", 0.24),
            ("plateau", 0.10),
        ]
        intensity_bounds = (0.35, 1.00)
    kind = pick_weighted(rng, kinds)

    lift_bias = {
        "lift": 0.12,
        "plateau": 0.00,
        "drop": -0.08,
    }.get(ctrl.derived.level2.lift_profile, 0.0)
    base = (
        ctrl.derived.level2.melodic_range * 0.55
        + (1 - ctrl.derived.level2.motif_repetition) * 0.45
    )
    base = clamp01(base + lift_bias)
    intensity = clamp01(lerp(intensity_bounds[0], intensity_bounds[1], base))
    intensity = clamp01(intensity * lerp(0.88, 1.08, rng.random()))

    return MelodyContourProfile(kind=kind, intensity=intensity)


def build_song_plan(ctrl) -> SongPlan:
    rng = random.Random(ctrl.seed)
    length = max(1, int(ctrl.length_bars))
    level2 = ctrl.derived.level2
    lift_density_bias = {
        "lift": 1.08,
        "plateau": 1.00,
        "drop": 0.92,
    }.get(level2.lift_profile, 1.00)
    lift_energy_bias = {
        "lift": 1.12,
        "plateau": 1.00,
        "drop": 0.90,
    }.get(level2.lift_profile, 1.00)
    motif_density_bias = lerp(1.08, 0.92, level2.motif_repetition)

    phrase_len = 4
    phrase_count = int(math.ceil(length / phrase_len))

    pattern_codes = _choose_section_pattern_by_phrases(rng, phrase_count)
    section_names = [_section_code_to_name(c) for c in pattern_codes]

    sections: list[SectionDef] = []
    bar = 0
    for sec_name in section_names:
        start = bar
        end = min(length, start + phrase_len)
        sections.append(SectionDef(name=sec_name, bar_start=start, bar_end_excl=end))
        bar = end
        if bar >= length:
            break

    bar_mods: list[BarModifiers] = []
    for b in range(length):
        sec = next((s for s in sections if s.bar_start <= b < s.bar_end_excl), sections[-1])
        section = sec.name

        is_phrase_end = ((b + 1) % phrase_len == 0) or (b == length - 1)
        is_section_start = (b == sec.bar_start)
        is_section_end = (b == sec.bar_end_excl - 1)

        if section == "intro":
            density_mul = lerp(0.65, 0.90, rng.random())
            energy_mul = lerp(0.65, 0.95, rng.random())
            sync_mul = lerp(0.75, 1.00, rng.random())
            chord_mul = lerp(0.85, 1.05, rng.random())
            var_mul = lerp(0.85, 1.05, rng.random())
            rep_mul = lerp(1.00, 1.25, rng.random())
            melody_shift = int(round(lerp(-3, +1, rng.random())))
        elif section == "verse":
            density_mul = lerp(0.75, 0.98, rng.random())
            energy_mul = lerp(0.78, 0.98, rng.random())
            sync_mul = lerp(0.85, 1.05, rng.random())
            chord_mul = lerp(0.90, 1.10, rng.random())
            var_mul = lerp(0.85, 1.05, rng.random())
            rep_mul = lerp(1.05, 1.30, rng.random())
            melody_shift = int(round(lerp(-2, +1, rng.random())))
        elif section == "chorus":
            density_mul = lerp(1.05, 1.25, rng.random())
            energy_mul = lerp(1.10, 1.40, rng.random())
            sync_mul = lerp(1.00, 1.25, rng.random())
            chord_mul = lerp(1.00, 1.20, rng.random())
            var_mul = lerp(0.95, 1.20, rng.random())
            rep_mul = lerp(0.95, 1.15, rng.random())
            melody_shift = int(round(lerp(+2, +6, rng.random())))
        elif section == "bridge":
            density_mul = lerp(0.85, 1.10, rng.random())
            energy_mul = lerp(0.85, 1.20, rng.random())
            sync_mul = lerp(0.95, 1.20, rng.random())
            chord_mul = lerp(1.00, 1.30, rng.random())
            var_mul = lerp(1.10, 1.45, rng.random())
            rep_mul = lerp(0.75, 1.00, rng.random())
            melody_shift = int(round(lerp(0, +4, rng.random())))
        else:  # outro
            density_mul = lerp(0.70, 0.95, rng.random())
            energy_mul = lerp(0.70, 0.95, rng.random())
            sync_mul = lerp(0.80, 1.05, rng.random())
            chord_mul = lerp(0.90, 1.10, rng.random())
            var_mul = lerp(0.85, 1.10, rng.random())
            rep_mul = lerp(1.05, 1.35, rng.random())
            melody_shift = int(round(lerp(-3, +1, rng.random())))

        density_mul *= motif_density_bias
        if section == "chorus":
            density_mul *= lift_density_bias
            energy_mul *= lift_energy_bias
        elif section in {"intro", "outro"}:
            density_mul *= lerp(1.02, 0.90, level2.form_strictness)
        elif section == "bridge":
            density_mul *= lerp(0.95, 1.08, 1 - level2.form_strictness)

        density_mul = lerp(density_mul, 1.0, level2.form_strictness * 0.25)

        if is_phrase_end and b != length - 1:
            energy_mul *= lerp(1.03, 1.10, clamp01(ctrl.derived.cadence_strength))
            sync_mul *= lerp(1.00, 1.10, clamp01(ctrl.derived.syncopation))
            var_mul *= lerp(1.02, 1.20, clamp01(ctrl.derived.variation))

        density_mul = clamp(density_mul, 0.55, 1.35)
        energy_mul = clamp(energy_mul, 0.55, 1.55)
        sync_mul = clamp(sync_mul, 0.55, 1.55)
        chord_mul = clamp(chord_mul, 0.70, 1.60)
        var_mul = clamp(var_mul, 0.60, 1.70)
        rep_mul = clamp(rep_mul, 0.60, 1.70)

        bar_mods.append(
            BarModifiers(
                section=section,
                density_mul=density_mul,
                energy_mul=energy_mul,
                sync_mul=sync_mul,
                chord_comp_mul=chord_mul,
                variation_mul=var_mul,
                repetition_mul=rep_mul,
                melody_shift_semitones=melody_shift,
                is_phrase_end=is_phrase_end,
                is_section_start=is_section_start,
                is_section_end=is_section_end,
            )
        )

    rhythm = build_rhythm_profile(ctrl, rng)
    contour = build_melody_contour(ctrl, rng)
    templates = choose_section_templates(ctrl, rng)

    return SongPlan(
        sections=sections,
        bar_mods=bar_mods,
        rhythm=rhythm,
        contour=contour,
        templates=templates,
        phrase_len_bars=phrase_len,
    )
