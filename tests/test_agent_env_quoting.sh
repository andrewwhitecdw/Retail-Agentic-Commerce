#!/usr/bin/env bash
set -euo pipefail

# Unit test for the AGENT_ENV_ARGS pattern used in install.sh.
# Ensures environment values containing spaces are passed as a single
# argument and not split by word splitting.

NVIDIA_API_KEY="nvapi-test-key"
TEST_SPACE_VAR="value with spaces"

NAT_ENV_VARS=(
    NVIDIA_API_KEY
    TEST_SPACE_VAR
)

AGENT_ENV_ARGS=()
for var in "${NAT_ENV_VARS[@]}"; do
    val="${!var:-}"
    if [ -n "$val" ]; then
        AGENT_ENV_ARGS+=("$var=$val")
    fi
done

result=$(env "${AGENT_ENV_ARGS[@]}" bash -c 'echo "$TEST_SPACE_VAR"')

if [ "$result" = "value with spaces" ]; then
    echo "PASS: space-containing env value preserved"
else
    echo "FAIL: expected 'value with spaces', got '$result'"
