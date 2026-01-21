# 08 — Resolve Trace Format (Stage-aware)

Trace MUST distinguish Grammar vs Controls resolution.

```yaml
ResolveTrace:
  resolverVersion: string
  thoughtId: string
  entries:
    - stage: Grammar|Controls
      path: string
      finalValue: any
      contributors:
        - sourceId: string
          value: any
          origin: string
      mergeOperator: string
      normalizationSteps: [string]
      repairs:
        - step: int
          reason: string
          before: any
          after: any
```
