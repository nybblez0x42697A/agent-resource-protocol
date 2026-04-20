# Deprecation and Sunset Policy

## Status

This document defines the baseline deprecation and sunset policy for protocol artifacts.

It builds on:

- `spec/versioning/versioning-and-evolution-policy.md`
- `spec/discovery/capability-discovery-and-negotiation.md`
- `spec/extensions/extension-and-profile-model.md`

## Scope

This document is normative for:

- baseline deprecation states and obligations
- sunset notice expectations
- post-sunset behavior for retired artifacts

It is not normative for:

- organization-specific support contracts
- release calendar cadence
- tooling for announcement distribution

## Purpose

Deprecation provides advance notice that an artifact should no longer be adopted for new integrations.

Sunset marks the point at which continued support is no longer required under the baseline policy.

The purpose of this policy is to make retirement predictable and observable without creating silent interoperability loss.

## Artifact Scope

This policy applies to protocol artifacts such as:

- bindings
- profiles
- extensions
- capability identifiers

It may also guide deprecation of normative documents where appropriate, but its primary focus is the artifacts implementations advertise and negotiate.

## Baseline Deprecation States

The baseline retirement states are:

- `active`
- `deprecated`
- `sunset`

`active` means the artifact is available for normal use.

`deprecated` means the artifact remains recognized for compatibility, but new adoption is discouraged and a replacement or migration target should be identified.

`sunset` means the artifact is retired and baseline support is no longer expected.

## Deprecation Obligations

When an artifact becomes `deprecated`, the publisher should provide:

- the deprecated artifact identifier
- the deprecation effective date
- the recommended replacement when one exists
- the planned sunset date when known
- compatibility notes for existing users

During deprecation, the publisher should continue to describe the artifact accurately in discovery or documentation so that existing clients can make informed compatibility decisions.

## Sunset Obligations

When an artifact reaches `sunset`, the publisher should provide:

- the sunset effective date
- the identifier of the retired artifact
- the replacement or migration path when one exists
- the expected post-sunset behavior

After sunset, baseline policy no longer requires the artifact to remain negotiable or supported.

## Notice Expectations

Deprecation notice should be given before sunset wherever practical.

The baseline policy does not mandate a fixed minimum duration, but it does require that notice be explicit enough for interoperating parties to understand:

- what is being retired
- when it is expected to retire
- what to use instead when applicable

If no replacement exists, the notice should say so explicitly.

## Compatibility During Deprecation

During deprecation:

- the artifact may still be advertised
- the artifact may still be negotiated
- the artifact should be clearly marked as deprecated in discovery or documentation

Deprecation does not by itself make an artifact incompatible.

If an artifact remains supported during deprecation, its semantics must remain stable enough for existing compatible integrations.

## Post-Sunset Behavior

After sunset:

- the artifact should no longer be advertised as supported unless retained under an explicit compatibility exception
- negotiation should fail clearly if the artifact is required and no longer supported
- discovery should not imply continued support when support has ended

If a publisher retains the artifact beyond sunset for compatibility reasons, that retention should be described as an implementation-specific exception rather than baseline expectation.

## Discovery Interaction

Capability discovery should expose retirement state clearly enough that a client can distinguish:

- active support
- deprecated but still supported capability
- sunset or unavailable capability

Negotiation should treat a deprecated artifact as selectable only when the implementation still supports it.

Negotiation must not treat a sunset artifact as available unless the implementation explicitly declares a compatibility exception.

## Replacement Guidance

When possible, a deprecation notice should identify:

- the replacement artifact identifier
- the compatibility relationship between old and new artifacts
- any migration actions required

If migration requires a breaking change, the notice should say so explicitly rather than implying transparent compatibility.

## Conformance Notes

A baseline-conformant implementation must not:

- silently stop supporting an advertised artifact without updating discovery or documentation
- advertise a sunset artifact as active
- imply that a retired artifact is baseline-required after sunset

An implementation may:

- continue supporting a deprecated artifact during the notice window
- retain support after sunset as an implementation-specific compatibility choice

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a deprecation notice
- a completed sunset transition

They do not define a mandatory publication or announcement format.
