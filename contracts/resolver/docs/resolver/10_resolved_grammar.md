# 10 — ResolvedGrammar (NEW)

## Why this exists
A postdoc will not accept “style” as hand-wavy prose. They will accept a **grammar**:
- vocabulary
- legality sets
- transition rules
- placement rules
- typologies

`ResolvedGrammar` is the explicit, compiled, theory-native artifact that makes “style” real.

---

## ResolvedGrammar shape (conceptual)

```yaml
ResolvedGrammar:
  context:
    styleFamilyId: string
    styleVariantId: string|null
    profileId: string|null
    overrideMode: locked|simple|expert

  harmonyGrammar:
    functionStateMachine:
      states: [T, PD, D]
      transitions: {T:{PD:..,D:..,T:..}, PD:{...}, D:{...}}
    progressionTemplateLibrary:
      templates: [{id, romanNumerals, harmonicRhythmModel, cadenceTags, allowSubstitutions}]
    chordVocabulary:
      allowedQualities: [maj, min, dim, aug, sus2, sus4, dom7, maj7, min7, ...]
      maxExtension: 0|7|9|11|13
      alterationsAllowed: boolean
      modalInterchangeAllowed: boolean
      secondaryDominantsAllowed: boolean
    cadenceTypology:
      allowedCadences: [PAC, IAC, HC, DC, plagal, avoided, modal]
      requiredAtPhraseEnd: boolean
      cadenceWindows: {phraseEnd:{barsFromEnd:int, allowedBeats:[...]}, sectionEnd:{...}}
    chromaticPolicy:
      caps:
        nonChordToneRateMax: 0..1
        nonDiatonicPitchRateMax: 0..1
        approachToneRateMax: 0..1
      allowedNCTTypes: [passing, neighbor, suspension, anticipation, appoggiatura]

  rhythmGrammar:
    meter: "4/4"|...
    gridPolicy:
      base: 1/4|1/8|1/16|1/32
      tupletsAllowed: boolean
      tupletKinds: [triplet,...]|null
    onsetLegality:
      styleMask: [tickPositions]
      forbiddenZones: [tickRanges]|null
    accentGrammar:
      archetypes: [backbeat, clave_2_3, tresillo, straight4, ...]
    grooveTemplates:
      templates: [{id, onsetMask, accentModel, microtimingDefaults}]

  pitchGrammar:
    scaleVocabulary:
      allowedScales: [major, natural_minor, dorian, mixolydian, ...]
      allowedPitchClassesBase: [0..11]
    chordTonePolicy:
      chordToneStrengthRange: {min:0..1, max:0..1}
      tendencyTones:
        leadingToneResolvesTo: tonic
        scaleDegree4ResolvesTo: 3|5 (style dependent)
    voiceLeadingHardRules:
      maxLeapSemitonesMax: int
      parallelPerfectsForbidden: boolean
      spacingRules: {minSemitonesBetweenVoices, maxSpanPerTexture}|null

  formGrammar:
    sectionArchetypes:
      allowed: [intro, verse, prechorus, chorus, bridge, outro]
      typicalLengthsBars: {intro:[2,4,8], verse:[8,16], ...}
    phraseGrammar:
      phraseLengthOptionsBars: [2,4,8]
      groupingOptions: [AAAA, AABA, ABAC, evolving]
    cadencePlacementNorms:
      phraseEndCadenceProbability: 0..1
      sectionEndCadenceStrengthBias: soft|medium|strong

  motifGrammar:
    allowedTransforms: [transpose, invert, augment, diminish, fragment]
    transformMagnitudeCaps: {transposeSemitonesMax:int, augmentFactorMax:float, ...}
    reuseExpectations:
      motifSimilarityTargetsByScheme: {AAAA:0.8..1.0, AABA:0.6..0.9, ...}

  performanceGrammar:
    humanizationBounds:
      timingVarianceMaxMs: float
      velocityAccentBoostMax: int
    articulationNorms:
      legatoBias: 0..1
      staccatoBias: 0..1
```

---

## Relationship to ResolvedControls
- Grammar defines **legal sets and typologies**
- Controls define **which legal choices** to emphasize for this Thought

Example:
- Grammar says “allowedCadences = [PAC,HC]”
- Controls decide “cadencePlan has HC at bar 3 and PAC at bar 7, strength strong”

---

## Minimal viable grammar (MVG)
You do not need the entire shape above to start.
But you MUST have enough grammar to make “style differences” real and testable:
- chord vocabulary + cadence typology + chromatic caps
- onset legality + accent archetype + grid policy
- allowed pitch classes + voice-leading hard caps
- phrase length options + cadence placement requirements
