# Canonical Field Index — Thought Editor (14 Panes)

This index defines the **UI grouping** (panes) and the **canonical field paths** in `ThoughtSpec`.

The same paths are referenced in:
- resolver mapping docs (pane → ResolvedGrammar / ResolvedControls)
- generator decision sites

> Naming convention: `thought.<pane>.<field>...`

---

## Pane 01 — Identity
- `thought.identity.thoughtId`
- `thought.identity.label`
- `thought.identity.enabled`
- `thought.identity.frozen`

## Pane 02 — Style Family & Variant (Grammar selector)
- `thought.style.inheritFromUpstream`
- `thought.style.styleFamilyId`
- `thought.style.styleVariantId`
- `thought.style.allowOverrides` (expert)
- `thought.style.overridePatch` (expert: partial overrides of derived grammar)

## Pane 03 — Profile (Bias selector)
- `thought.profile.inheritFromUpstream`
- `thought.profile.profileId`
- `thought.profile.biasOverrides` (expert)

## Pane 04 — Bars, Meter, Tempo, Type (container)
- `thought.container.bars`
- `thought.container.meterOverride`
- `thought.container.tempoOverrideBpm`
- `thought.container.seed`
- `thought.container.thoughtType` (setup|melody|harmony|bass|beat|texture)

## Pane 05 — Form & Phrasing (phrase/cadence plan)
- `thought.form.phrasePlan.mode` (auto|explicit)
- `thought.form.phrasePlan.barsPerPhrase`
- `thought.form.phrasePlan.peakPosition`
- `thought.form.phrasePlan.contourShape`
- `thought.form.phrasePlan.climaxLift`
- `thought.form.cadencePlan.mode` (auto|explicit)
- `thought.form.cadencePlan.events[]`

## Pane 06 — Role (functional job)
- `thought.role.roleBehavior` (hook|lead_line|counterline|fill|pad|comp|anchor|groove)
- `thought.role.priority` (lead|support|background)
- `thought.role.interaction.followsHarmony`
- `thought.role.interaction.followsRhythm`
- `thought.role.interaction.callResponseGroup`

## Pane 07 — Harmony Language
- `thought.harmony.progressionTemplateId`
- `thought.harmony.functionTransitionsPresetId`
- `thought.harmony.chordQualitiesPresetId`
- `thought.harmony.chromaticCapsPresetId`
- `thought.harmony.cadenceConstraintsPresetId`
- `thought.harmony.harmonicRhythm` (slow|medium|fast)
- `thought.harmony.userChordProgression` (optional explicit chords)

## Pane 08 — Figuration / Patterns
- `thought.figuration.patternFamilyId`
- `thought.figuration.patternVariantId`
- `thought.figuration.intensity` (low|medium|high)
- `thought.figuration.params` (pattern-specific knobs)

## Pane 09 — Pitch / Tonality
- `thought.pitch.tonalCenterPolicy` (inherit|override)
- `thought.pitch.scaleOverride`
- `thought.pitch.chordToneStrength` (low|medium|high)
- `thought.pitch.nonChordToneRateMax`
- `thought.pitch.nonDiatonicRateMax`
- `thought.pitch.cadenceTargets.enabled`
- `thought.pitch.cadenceTargets.targets[]`
- `thought.pitch.cadenceTargets.strength`
- `thought.pitch.cadenceTargets.applyAt`
- `thought.pitch.range.minMidi`
- `thought.pitch.range.maxMidi`
- `thought.pitch.voiceLeading.maxLeap`
- `thought.pitch.voiceLeading.preferStepwise`
- `thought.pitch.voiceLeading.resolveLeadingTone`

## Pane 10 — Rhythm (Placement)
- `thought.rhythm.grid` (1/4|1/8|1/16|1/32)
- `thought.rhythm.density` (low|medium|high)
- `thought.rhythm.syncopation` (low|medium|high)
- `thought.rhythm.swing` (off|light|medium|heavy)
- `thought.rhythm.restPolicy.minRestBeatsPerBar`
- `thought.rhythm.restPolicy.allowAnticipations`
- `thought.rhythm.accent.preferStrongBeats`
- `thought.rhythm.accent.backbeatBias`

## Pane 11 — Register (Tessitura)
- `thought.register.center` (low|mid_low|mid|mid_high|high)
- `thought.register.span` (narrow|medium|wide)
- `thought.register.climaxLift` (none|small|medium|large)
- `thought.register.octaveBias.preferredOctaves[]`
- `thought.register.octaveBias.penalizeOuterOctaves`

## Pane 12 — Contour (Macro Shape)
- `thought.contour.shape` (static|arch|ascending|descending|wave)
- `thought.contour.motion` (static|mostly_stepwise|mixed|leapy)
- `thought.contour.smoothness` (low|medium|high)
- `thought.contour.targets.phraseStart`
- `thought.contour.targets.phraseEnd`
- `thought.contour.targets.peakPosition`

## Pane 13 — Motive & Variation
- `thought.motif.scheme` (AAAA|AABA|ABAC|evolving)
- `thought.motif.variation` (none|small|medium|large)
- `thought.motif.repeatStrength` (high|medium|low)
- `thought.motif.transformAllow[]` (transpose|invert|augment|diminish|fragment)

## Pane 14 — Performance & Rendering
- `thought.performance.microtimingProfile` (tight|pocket|laidback|swingy) — maps to `ResolvedControls.rhythm.microtimingProfile`
- `thought.performance.timingVariance` (none|small|medium|large)
- `thought.performance.velocityCurve` (flat|gentle_arch|crescendo|decrescendo|strong_arch)
- `thought.performance.articulationBias` (legato|mixed|staccato)
- `thought.render.partInstrument` (instrument mapping per role/type)
- `thought.render.mixer` (level/pan optional)
