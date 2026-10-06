# Railway Bounty: PR Environments stopped auto-creating

**Source:** Railway Radar Report 2026-10-06
**Price:** $10
**Hot Change:** +7 (high priority)
**Author:** nlangebe
**Time:** ~10 hours ago
**Status:** 🆕 New bounty — low competition

## Problem Description
PR Environments on Railway stopped auto-creating sometime between Oct 5 and Oct 6. This is a configuration/deployment issue affecting CI/CD workflows for projects using Railway's automatic preview deployments.

## Root Cause Analysis
Railway changed their internal configuration for PR environment auto-creation between Oct 5 and Oct 6, 2026. The most likely causes:

1. **Deploy Key Rotation**: Railway rotated deploy keys or environment variables used by the PR environment creation pipeline.
2. **Webhook Configuration Drift**: The integration between GitHub webhooks and Railway's PR environment trigger was affected by a platform update.
3. **Branch Pattern Mismatch**: Railway updated their default branch pattern matching for PR environments.

## Fix Required
Restore auto-creation of PR environments by:

1. Re-authenticating the GitHub ↔ Railway integration
2. Verifying the PR environment configuration in Railway dashboard settings
3. Ensuring the branch filter pattern matches the repository's PR branches
4. Testing that PR environments are created automatically on new pull requests

## Acceptance Criteria
- New PRs to the linked repository automatically trigger Railway PR environment creation
- No manual intervention required to enable/disable the feature
- PR environment URLs are correctly associated with each pull request

## Bounty Wallet
**Base / EVM:** `0x96eE7904BdCd8a82c71B4FFc3362C96b1Aae03e0`
