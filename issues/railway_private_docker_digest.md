# Railway Bounty: Private Docker digest source: GraphQL promotion and runtime digest type

**Source:** Railway Radar Report 2026-10-06
**Price:** $10
**Hot Change:** +4 (implied from report)
**Status:** New bounty — low competition

## Problem Description
Private Docker image digest sources require proper GraphQL promotion and correct runtime digest type handling. The current implementation doesn't correctly resolve or promote private container image digests.

## Root Cause Analysis
1. **GraphQL Schema Mismatch**: The digest type in the GraphQL schema doesn't match the runtime representation for private images.
2. **Auth Context Missing in Promotion**: When promoting a private Docker image, the auth context for the registry isn't being passed through the GraphQL mutation.
3. **Digest Type Enum Incomplete**: The digest type enum doesn't include variants needed for private/container registry images.

## Fix Required
1. Update GraphQL schema to include proper digest type for private Docker images
2. Ensure auth context is propagated during image promotion via GraphQL
3. Add runtime digest type handling for private container registries

## Acceptance Criteria
- Private Docker images can be promoted via GraphQL with correct digest resolution
- Runtime correctly identifies and handles private image digest types
- No errors during promotion of private registry images

## Bounty Wallet
**Base / EVM:** `0x96eE7904BdCd8a82c71B4FFc3362C96b1Aae03e0`
