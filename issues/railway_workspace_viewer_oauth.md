# Railway Bounty: workspace:viewer OAuth token: workspace(workspaceId) query returns INTERNAL_SERVER_ERROR

**Source:** Railway Radar Report 2026-10-06
**Price:** $4
**Hot Change:** +4
**Status:** Hot bounty — low competition

## Problem Description
When using a `workspace:viewer` OAuth token, querying `workspace(workspaceId)` returns an `INTERNAL_SERVER_ERROR`. The token should have read-only access to workspace information but currently fails with a server error instead of returning the data or a proper authorization error.

## Root Cause Analysis
1. **Permission Check Bug**: The GraphQL resolver for `workspace` doesn't correctly handle the `workspace:viewer` scope, falling through to an unhandled code path that throws INTERNAL_SERVER_ERROR.
2. **Missing Scope Validation**: The resolver assumes admin-level permissions and doesn't branch for viewer-level access.
3. **Null Coalescing Error**: A null reference occurs when viewer-scoped tokens don't have access to certain workspace fields, and the error isn't caught.

## Fix Required
Fix the `workspace` GraphQL resolver to properly handle `workspace:viewer` scoped tokens:

1. Add explicit permission checks for viewer scope in the workspace resolver
2. Return appropriate data (or a proper 403 Forbidden) instead of INTERNAL_SERVER_ERROR
3. Ensure all workspace fields are accessible at viewer level where intended

## Acceptance Criteria
- `workspace(workspaceId)` query returns valid data for `workspace:viewer` tokens
- Returns a proper 403 or scoped error when the viewer lacks access
- No INTERNAL_SERVER_ERROR is thrown for viewer-scoped queries
- Tests cover viewer, editor, and admin token scenarios

## Bounty Wallet
**Base / EVM:** `0x96eE7904BdCd8a82c71B4FFc3362C96b1Aae03e0`
