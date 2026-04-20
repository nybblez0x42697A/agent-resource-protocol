# Capability Discovery and Negotiation

## Status

This document defines the baseline capability discovery and negotiation model.

It builds on:

- `spec/conformance/baseline-conformance.md`
- `spec/bindings/http-json-binding.md`
- `spec/extensions/extension-and-profile-model.md`
- `spec/security/security-and-policy-model.md`

## Scope

This document is normative for:

- baseline capability advertisement content
- baseline compatibility and negotiation rules
- fallback behavior when compatible capabilities cannot be selected

It is not normative for:

- a mandatory discovery transport
- registry deployment or service topology
- dynamic session management

## Purpose

Capability discovery allows an implementation to describe what it supports before an operation is attempted.

Capability negotiation allows two parties to select a mutually compatible set of capabilities from what has been advertised.

Neither discovery nor negotiation may redefine the meaning of a baseline operation or artifact.

## Capability Advertisement Model

A baseline capability advertisement should identify:

- implementation identifier
- supported conformance level
- supported transport bindings
- supported profiles
- supported extensions
- supported baseline operations

An advertisement may also identify:

- supported resource kinds
- supported lifecycle state extensions
- implementation notes or limits

## Baseline Advertisement Rules

An implementation claiming baseline support must advertise baseline conformance truthfully.

If an implementation advertises:

- a binding
- a profile
- an extension
- an additional resource kind

then it must either support that capability or reject use of it explicitly at runtime.

An implementation must not advertise a stricter profile unless it also satisfies baseline conformance.

## Capability Categories

The baseline capability categories are:

- `conformance`
- `binding`
- `profile`
- `extension`
- `operation`
- `resourceKind`

These categories are descriptive only. They do not create a mandatory wire format.

## Negotiation Inputs

A negotiation decision may consider:

- requested conformance level
- requested binding
- requested profiles
- requested extensions
- required baseline operations

The requesting party should declare only the capabilities it actually requires.

## Negotiation Rules

The baseline negotiation rules are:

1. baseline conformance is the minimum compatible floor
2. a selected profile is valid only if both parties support it and baseline conformance remains preserved
3. a selected extension is valid only if both parties support it or if the requesting party can proceed without it
4. a selected binding is valid only if both parties support it
5. a required operation must be available without semantic redefinition

Negotiation selects from already-declared capabilities. It must not infer undeclared support.

## Selection Outcomes

A negotiation attempt has three baseline outcomes:

- `compatible`: the required capability set can be satisfied
- `compatible_with_fallback`: the required baseline set is satisfied, but optional capabilities were not selected
- `incompatible`: the required capability set cannot be satisfied

If the result is `compatible_with_fallback`, the selected capability set must remain semantically correct under baseline rules.

## Fallback Rules

Fallback is permitted only when:

- the dropped capability was optional to the requester
- dropping the capability does not change required baseline semantics

Fallback is not permitted when:

- a required profile is unavailable
- a required extension is unavailable and no baseline-safe alternative exists
- the requested binding is mandatory for the interaction and no shared binding exists

## Incompatibility Handling

When negotiation fails, the implementation should report:

- which required category was incompatible
- which required identifier could not be satisfied
- whether a baseline-safe fallback exists

The exact error encoding is transport-specific, but the explanation should be specific enough for implementers to diagnose compatibility failure.

## Relationship To Baseline Operations

Discovery and negotiation do not create new meanings for baseline operations.

They help select:

- which binding to use
- which optional extensions may be used
- which stricter profile may govern the interaction

After selection, the resulting interaction must still preserve baseline operation semantics.

## Relationship To Security

An implementation may expose capability advertisements publicly or under access control.

If discovery is protected, authorization and policy evaluation must still preserve the denial rules defined in `spec/security/security-and-policy-model.md`.

Negotiation results must not claim unsupported secure behavior or bypass required authorization and policy gates.

## Declaration Guidance

A capability advertisement should declare:

- stable identifiers for bindings, profiles, and extensions
- which capabilities are mandatory versus optional for that implementation
- any important limits affecting interoperability

A negotiation result should declare:

- selected binding
- selected profiles
- selected extensions
- fallback notes when optional capabilities were dropped

## Conformance Notes

A baseline-conformant implementation must:

- advertise baseline support truthfully when it advertises capabilities at all
- avoid claiming undeclared support during negotiation
- preserve baseline semantics after capability selection
- fail clearly when required compatibility cannot be established
