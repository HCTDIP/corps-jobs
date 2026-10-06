# Railway Bounty: Discord Gateway WebSocket connection hangs indefinitely

**Source:** Railway Radar Report 2026-10-06
**Price:** $4
**Hot Change:** +4
**Status:** 🆕 New bounty — low competition, config/question type

## Problem Description
Discord Gateway WebSocket connections hang indefinitely. This is NOT caused by token issues or rate limiting — the connection establishes but then freezes without receiving any events or errors.

## Root Cause Analysis
The WebSocket hang is likely caused by:

1. **Idle Timeout Configuration**: Railway's infrastructure may close idle WebSocket connections after a certain period, but the client isn't reconnecting properly.
2. **Shard Connection Race Condition**: When reconnecting shards, simultaneous connections may cause a deadlock in the gateway dispatcher.
3. **Heartbeat Failure Silent State**: The heartbeat mechanism may fail silently, leaving the connection in a half-open state where neither side detects the failure.
4. **TLS Resume Failure**: TLS session resumption may fail on reconnect, causing the connection to hang during the handshake phase.

## Fix Required
Implement robust WebSocket reconnection with:

1. **Explicit Idle Timeout Detection**: Monitor connection liveness and detect hung states within configurable timeout periods
2. **Graceful Degradation on Shard Failures**: When a shard connection hangs, gracefully disconnect and reconnect rather than blocking indefinitely
3. **Heartbeat Acknowledgment Validation**: Track heartbeat acks and trigger reconnection if missing within expected windows
4. **Connection Pool Reset**: Clear stale connections and force full TLS handshake on reconnect attempts

## Acceptance Criteria
- WebSocket connections recover from hung states within a defined timeout (e.g., 60 seconds)
- No indefinite blocking of the main application thread
- Proper logging of reconnect events and failures
- Works correctly under normal and degraded network conditions

## Bounty Wallet
**Base / EVM:** `0x96eE7904BdCd8a82c71B4FFc3362C96b1Aae03e0`
