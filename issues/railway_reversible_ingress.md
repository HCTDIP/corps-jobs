# Railway Bounty: Supported reversible ingress isolation during deployment and rollback

**Source:** Railway Radar Report 2026-10-06
**Price:** $4
**Hot Change:** +4
**Status:** Hot bounty — low competition, config/question type

## Problem Description
Railway needs to support reversible ingress isolation during deployment and rollback operations. Currently, there's no clean way to isolate ingress traffic during deployments to prevent downtime or partial traffic routing.

## Root Cause Analysis
1. **No Native Isolation Mechanism**: Railway's current ingress system doesn't expose a way to temporarily isolate traffic during deployments.
2. **Rollback Triggers Full Re-deploy**: Rollbacks currently re-deploy the entire service rather than isolating and switching traffic.
3. **Missing Staged Rollout Controls**: No built-in support for canary or blue-green deployment patterns at the ingress level.

## Fix Required
Implement reversible ingress isolation by:

1. Adding an `isolate` flag to deployment operations that routes traffic only to the new service instance
2. Supporting `rollback` as a traffic-swap operation rather than a full redeploy
3. Ensuring isolated deployments can be cleanly reversed without service disruption

## Acceptance Criteria
- Deployments can be run with ingress isolation enabled
- Rolled-back deployments restore original traffic routing without full re-deploy
- Isolated state is visible in the Railway dashboard
- No traffic hits the partially-deployed service during isolation

## Bounty Wallet
**Base / EVM:** `0x96eE7904BdCd8a82c71B4FFc3362C96b1Aae03e0`
