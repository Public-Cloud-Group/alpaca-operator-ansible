#!/bin/bash

###############################################################################
# Test Matrix Script
#
# Runs local tests for multiple Python/Ansible version combinations.
# This is useful for testing compatibility across different versions.
#
# Usage:
#   ./local-test-matrix.sh
#
# Configuration:
#   Edit the TEST_MATRIX array below to specify which combinations to test.
###############################################################################

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

# Test matrix: array of "PYTHON_VERSION:ANSIBLE_VERSION" pairs
# By default, this script derives the matrix from the GitHub Actions workflow
# in `.github/workflows/ci-cd.yml` (job `test`, strategy.matrix.include).
# To override it manually, add entries to TEST_MATRIX below. If TEST_MATRIX is
# empty, the CI/CD matrix will be used.
declare -a TEST_MATRIX
TEST_MATRIX=(
    # Example manual override entries:
    # "3.11:2.18"
    # "3.12:2.18"
)

# If no manual matrix is defined, derive it from the CI/CD workflow
if [ ${#TEST_MATRIX[@]} -eq 0 ]; then
    CI_WORKFLOW_FILE="${PROJECT_ROOT}/.github/workflows/ci-cd.yml"
    if [ -f "${CI_WORKFLOW_FILE}" ]; then
        CI_MATRIX=$(
            awk '
                /^  test:/ { in_test=1; next }
                /^  [a-zA-Z0-9_-]+:/ && in_test && $1 != "test:" { in_test=0 }
                in_test && /strategy:/ { in_strategy=1; next }
                in_strategy && /matrix:/ { in_matrix=1; next }
                in_matrix && /include:/ { in_include=1; next }

                in_include && /^ {10}- ansible-version:/ {
                    gsub(/"/, "", $3); ansible=$3; next
                }

                in_include && /^ {12}python-version:/ {
                    gsub(/"/, "", $2); python=$2;
                    if (ansible != "" && python != "") {
                        print python ":" ansible;
                        ansible=""; python="";
                    }
                }
            ' "${CI_WORKFLOW_FILE}"
        )

        # Fill TEST_MATRIX array from CI_MATRIX (one "py:ansible" per line)
        TEST_MATRIX=()
        if [ -n "${CI_MATRIX}" ]; then
            while IFS= read -r line; do
                [ -n "${line}" ] && TEST_MATRIX+=("${line}")
            done <<EOF
${CI_MATRIX}
EOF
        fi
    fi
fi

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Running Test Matrix${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

RESULTS_DIR="${PROJECT_ROOT}/.dev/test/results"
MATRIX_RESULTS="${RESULTS_DIR}/matrix-results.csv"

# Ensure results directory exists and is clean
rm -rf "${RESULTS_DIR}"
mkdir -p "${RESULTS_DIR}"

# Create results file with header
echo "python_version;ansible_version;status" > "${MATRIX_RESULTS}"

PASSED=0
FAILED=0
UNSUPPORTED=0
TOTAL=${#TEST_MATRIX[@]}

for combination in "${TEST_MATRIX[@]}"; do
    IFS=':' read -r PYTHON_VERSION ANSIBLE_VERSION <<< "${combination}"

    echo -e "${BLUE}------------------------------------------${NC}"
    echo -e "${BLUE}Testing: Python ${PYTHON_VERSION} / Ansible ${ANSIBLE_VERSION}${NC}"
    echo -e "${BLUE}------------------------------------------${NC}"

    # Simple spinner animation while the test for this combination runs
    PYTHON_VERSION="${PYTHON_VERSION}" ANSIBLE_VERSION="${ANSIBLE_VERSION}" \
        "${SCRIPT_DIR}/local-test.sh" >> "${RESULTS_DIR}/matrix.log" 2>&1 &
    TEST_PID=$!

    SPINNER_FRAMES='|/-\'
    FRAME_INDEX=0
    while kill -0 "${TEST_PID}" 2>/dev/null; do
        FRAME_CHAR=${SPINNER_FRAMES:FRAME_INDEX:1}
        printf "\r[%s] " "${FRAME_CHAR}"
        FRAME_INDEX=$(( (FRAME_INDEX + 1) % ${#SPINNER_FRAMES} ))
        sleep 0.1
    done
    printf "\r    \r"

    if wait "${TEST_PID}"; then

        # Read result from the generated CSV (find any result file from recent test)
        # The local-test.sh script creates result.csv in release-*/results/
        RESULT_FILE=$(find "${RESULTS_DIR}" -path "*/release-*/results/result.csv" -type f 2>/dev/null | head -1)

        if [ -n "${RESULT_FILE}" ] && [ -f "${RESULT_FILE}" ]; then
            RESULT=$(tail -n1 "${RESULT_FILE}")
            echo "${RESULT}" >> "${MATRIX_RESULTS}"

            STATUS=$(echo "${RESULT}" | cut -d';' -f3)
            case "${STATUS}" in
                tested)
                    echo -e "${GREEN}✓ Passed${NC}"
                    ((PASSED++))
                    ;;
                unsupported)
                    echo -e "${YELLOW}⚠ Unsupported${NC}"
                    ((UNSUPPORTED++))
                    ;;
                *)
                    echo -e "${RED}✗ Failed${NC}"
                    ((FAILED++))
                    ;;
            esac
        else
            # Fallback: try to determine status from flags
            if find "${RESULTS_DIR}" -name "failed.flag" -type f | grep -q .; then
                echo -e "${RED}✗ Failed${NC}"
                ((FAILED++))
                echo "${PYTHON_VERSION};${ANSIBLE_VERSION};failed" >> "${MATRIX_RESULTS}"
            elif find "${RESULTS_DIR}" -name "unsupported.flag" -type f | grep -q .; then
                echo -e "${YELLOW}⚠ Unsupported${NC}"
                ((UNSUPPORTED++))
                echo "${PYTHON_VERSION};${ANSIBLE_VERSION};unsupported" >> "${MATRIX_RESULTS}"
            else
                echo -e "${GREEN}✓ Passed${NC}"
                ((PASSED++))
                echo "${PYTHON_VERSION};${ANSIBLE_VERSION};tested" >> "${MATRIX_RESULTS}"
            fi
        fi
    else
        echo -e "${RED}✗ Failed${NC}"
        ((FAILED++))
        echo "${PYTHON_VERSION};${ANSIBLE_VERSION};failed" >> "${MATRIX_RESULTS}"
    fi

    echo ""
done

# Summary
echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Test Matrix Summary${NC}"
echo -e "${BLUE}==========================================${NC}"
echo "Total: ${TOTAL}"
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"
echo -e "${YELLOW}Unsupported: ${UNSUPPORTED}${NC}"
echo -e "${CYAN}Results saved to: ${MATRIX_RESULTS}${NC}"
if [ "${FAILED}" -gt 0 ]; then
    exit 1
fi

exit 0
