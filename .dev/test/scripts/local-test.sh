#!/bin/bash

###############################################################################
# Local CI/CD Testing Script
#
# This script runs parts of the CI/CD workflow locally using Docker.
# It builds the Ansible collection, installs it, and runs sanity tests.
#
# Usage:
#   ./local-test.sh
#
# Configuration:
#   Edit the variables below to specify Python and Ansible versions to test.
###############################################################################

set -euo pipefail

# ============================================================================
# CONFIGURATION - Edit these variables to change test parameters
# ============================================================================

# Python version to use (e.g., "3.11", "3.12")
PYTHON_VERSION="${PYTHON_VERSION:-3.11}"

# Ansible Core version to use (e.g., "2.18", "2.19")
ANSIBLE_VERSION="${ANSIBLE_VERSION:-2.18}"

# ============================================================================
# SCRIPT SETUP
# ============================================================================

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

# Get version from galaxy.yml (try Python first, fallback to grep/sed)
VERSION=$(python3 -c "import yaml; print(yaml.safe_load(open('${PROJECT_ROOT}/galaxy.yml'))['version'])" 2>/dev/null || \
    grep -E "^version:" "${PROJECT_ROOT}/galaxy.yml" | sed -E 's/^version:[[:space:]]*["'\'']?([^"'\'']+)["'\'']?/\1/' | head -1 || \
    echo "unknown")

# Setup directories
TEST_DIR="${PROJECT_ROOT}/.dev/test/results"
RELEASE_DIR="${TEST_DIR}/release-${VERSION}"
LOG_DIR="${RELEASE_DIR}/logs"
RESULTS_DIR="${RELEASE_DIR}/results"
COLLECTION_DIR="${RELEASE_DIR}/collection"

# Create directories
mkdir -p "${LOG_DIR}"
mkdir -p "${RESULTS_DIR}"
mkdir -p "${COLLECTION_DIR}"

# Log file
LOG_FILE="${LOG_DIR}/test-$(date +%Y%m%d-%H%M%S).log"
SUMMARY_FILE="${RESULTS_DIR}/summary.txt"
RESULT_CSV="${RESULTS_DIR}/result.csv"

# Docker image and container names
DOCKER_IMAGE="python:${PYTHON_VERSION}-slim"
CONTAINER_NAME="alpaca-test-${PYTHON_VERSION//./}-ansible-${ANSIBLE_VERSION//./}-$(date +%s)"

# Colors for output (only when attached to a TTY)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    NC=''
fi

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# Function to strip ANSI color codes
strip_colors() {
    sed 's/\x1b\[[0-9;]*m//g'
}

log() {
    local message="[$(date +'%Y-%m-%d %H:%M:%S')] $*"
    echo -e "${BLUE}${message}${NC}"
    echo "${message}" >> "${LOG_FILE}"
}

log_success() {
    local message="[$(date +'%Y-%m-%d %H:%M:%S')] ✓ $*"
    echo -e "${GREEN}${message}${NC}"
    echo "${message}" >> "${LOG_FILE}"
}

log_error() {
    local message="[$(date +'%Y-%m-%d %H:%M:%S')] ✗ $*"
    echo -e "${RED}${message}${NC}"
    echo "${message}" >> "${LOG_FILE}"
}

log_warning() {
    local message="[$(date +'%Y-%m-%d %H:%M:%S')] ⚠ $*"
    echo -e "${YELLOW}${message}${NC}"
    echo "${message}" >> "${LOG_FILE}"
}

cleanup() {
    log "Cleaning up Docker container..."
    docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
}

trap cleanup EXIT

# ============================================================================
# MAIN SCRIPT
# ============================================================================

log "=========================================="
log "Local CI/CD Testing Script"
log "=========================================="
log "Project Root: ${PROJECT_ROOT}"
log "Version: ${VERSION}"
log "Python Version: ${PYTHON_VERSION}"
log "Ansible Version: ${ANSIBLE_VERSION}"
log "Test Directory: ${TEST_DIR}"
log "Release Directory: ${RELEASE_DIR}"
log "=========================================="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed or not in PATH"
    exit 1
fi

log "Step 1: Pulling Docker image ${DOCKER_IMAGE}..."
docker pull "${DOCKER_IMAGE}" 2>&1 | strip_colors >> "${LOG_FILE}" || {
    log_error "Failed to pull Docker image"
    exit 1
}
log_success "Docker image pulled successfully"

log "Step 2: Starting Docker container..."
# Check if Docker socket is available for Docker-in-Docker
DOCKER_SOCKET=""
if [ -S /var/run/docker.sock ]; then
    DOCKER_SOCKET="-v /var/run/docker.sock:/var/run/docker.sock"
    log "Docker socket detected - enabling Docker-in-Docker support"
fi

docker run -d \
    --name "${CONTAINER_NAME}" \
    -v "${PROJECT_ROOT}:/workspace:ro" \
    -v "${RELEASE_DIR}:/output" \
    ${DOCKER_SOCKET} \
    -w /build \
    "${DOCKER_IMAGE}" \
    tail -f /dev/null >> "${LOG_FILE}" 2>&1 || {
    log_error "Failed to start Docker container"
    exit 1
}
log_success "Docker container started: ${CONTAINER_NAME}"

# Create build directory in container and copy workspace files
log "Preparing build environment..."
docker exec "${CONTAINER_NAME}" bash -c "mkdir -p /build && cp -r /workspace/* /build/ 2>/dev/null || true" 2>&1 | strip_colors >> "${LOG_FILE}"

# Function to run commands in container
run_in_container() {
    local output
    output=$(docker exec "${CONTAINER_NAME}" bash -c "$1" 2>&1)
    local exit_code=$?
    # Strip colors from output before writing to log
    echo "${output}" | strip_colors >> "${LOG_FILE}"
    echo "${output}"
    return ${exit_code}
}

log "Step 3: Installing system dependencies..."
# Check if Docker socket was mounted and install Docker if needed
DOCKER_NEEDED=""
if [ -n "${DOCKER_SOCKET}" ]; then
    DOCKER_NEEDED="docker.io"
    log "Docker socket detected - will install Docker in container"
fi

run_in_container "
    apt-get update -qq && \
    apt-get install -y -qq \
        shellcheck \
        git \
        build-essential \
        ${DOCKER_NEEDED} \
        >/dev/null 2>&1
" || {
    log_error "Failed to install system dependencies"
    exit 1
}
log_success "System dependencies installed"

log "Step 4: Upgrading pip and installing Python dependencies..."
run_in_container "
    python -m pip install --upgrade pip setuptools wheel --quiet && \
    pip install -r /workspace/requirements.txt --quiet && \
    pip install yamllint flake8 PyYAML --quiet
" || {
    log_warning "Some Python dependencies may have failed to install (continuing...)"
}
log_success "Python dependencies installed"

log "Step 5: Installing Ansible Core ${ANSIBLE_VERSION}..."
if run_in_container "pip install 'ansible-core==${ANSIBLE_VERSION}.*' --quiet"; then
    log_success "Ansible Core ${ANSIBLE_VERSION} installed"
    ANSIBLE_STATUS="tested"
else
    log_error "Failed to install Ansible Core ${ANSIBLE_VERSION}"
    ANSIBLE_STATUS="unsupported"
    echo "unsupported" > "${RESULTS_DIR}/unsupported.flag"
fi

# Get installed Ansible version
INSTALLED_ANSIBLE=$(run_in_container "ansible --version 2>/dev/null | head -n1 | sed 's/ansible \[core //;s/\].*//' || ansible --version 2>/dev/null | grep '^ansible' | awk '{print \$2}' || echo 'unknown'")
log "Installed Ansible version: ${INSTALLED_ANSIBLE}"

if [ "${ANSIBLE_STATUS}" != "unsupported" ]; then
    log "Step 6: Building Ansible Collection..."
    if run_in_container "cd /build && ansible-galaxy collection build"; then
        log_success "Collection built successfully"

        # Copy built collection to output directory
        run_in_container "
            COLLECTION_FILE=\$(ls -1 /build/pcg-alpaca_operator-*.tar.gz | head -n1) && \
            cp \${COLLECTION_FILE} /output/collection/ && \
            ls -lh /output/collection/
        "
        log_success "Collection artifact saved to ${COLLECTION_DIR}/"
    else
        log_error "Failed to build collection"
        ANSIBLE_STATUS="failed"
        exit 1
    fi

    log "Step 7: Installing Ansible Collection..."
    if run_in_container "
        COLLECTION_FILE=\$(ls -1 /build/pcg-alpaca_operator-*.tar.gz | head -n1) && \
        ansible-galaxy collection install \${COLLECTION_FILE} --force --collections-path /root/.ansible/collections
    "; then
        log_success "Collection installed successfully"
    else
        log_error "Failed to install collection"
        ANSIBLE_STATUS="failed"
        exit 1
    fi

    log "Step 8: Running ansible-test sanity..."
    COLLECTION_PATH="/root/.ansible/collections/ansible_collections/pcg/alpaca_operator"

    # Check if Docker is available in container for ansible-test
    DOCKER_AVAILABLE=$(run_in_container "command -v docker >/dev/null 2>&1 && echo 'yes' || echo 'no'")

    if [ "${DOCKER_AVAILABLE}" = "yes" ]; then
        log "Docker available in container - using Docker mode for ansible-test"
        ANSIBLE_TEST_CMD="ansible-test sanity --python ${PYTHON_VERSION} --color --docker"
    else
        log_warning "Docker not available in container - running ansible-test without Docker"
        ANSIBLE_TEST_CMD="ansible-test sanity --python ${PYTHON_VERSION} --color"
    fi

    # Run ansible-test and capture output
    TEST_OUTPUT=$(run_in_container "
        cd ${COLLECTION_PATH} && \
        ${ANSIBLE_TEST_CMD} 2>&1
    ")
    TEST_EXIT_CODE=$?

    # Save test output to file
    echo "${TEST_OUTPUT}" > "${LOG_DIR}/test-output.log"

    if [ ${TEST_EXIT_CODE} -eq 0 ]; then
        log_success "Sanity tests passed"
        ANSIBLE_STATUS="tested"
    else
        log_error "Sanity tests failed (exit code: ${TEST_EXIT_CODE})"
        ANSIBLE_STATUS="failed"
        echo "failed" > "${RESULTS_DIR}/failed.flag"
        log "Test output saved to: ${LOG_DIR}/test-output.log"
    fi

    # Copy any test results from the container
    run_in_container "
        if [ -d ${COLLECTION_PATH}/tests/output ]; then
            cp -r ${COLLECTION_PATH}/tests/output/* /output/results/ 2>/dev/null || true
        fi
    " || true
fi

# ============================================================================
# GENERATE SUMMARY
# ============================================================================

log "Step 9: Generating test summary..."

{
    echo "=========================================="
    echo "Test Summary"
    echo "=========================================="
    echo "Date: $(date)"
    echo "Version: ${VERSION}"
    echo "Python Version: ${PYTHON_VERSION}"
    echo "Ansible Version: ${ANSIBLE_VERSION}"
    echo "Installed Ansible: ${INSTALLED_ANSIBLE:-N/A}"
    echo "Status: ${ANSIBLE_STATUS}"
    echo "=========================================="
    echo ""
    echo "Test Results:"
    echo "  - Collection Build: $([ -f "${COLLECTION_DIR}"/*.tar.gz ] && echo "✓ Success" || echo "✗ Failed")"
    echo "  - Collection Install: $([ "${ANSIBLE_STATUS}" != "unsupported" ] && echo "✓ Success" || echo "✗ Failed")"
    echo "  - Sanity Tests: $([ "${ANSIBLE_STATUS}" == "tested" ] && echo "✓ Passed" || echo "✗ Failed/Unsupported")"
    echo ""
    echo "Files:"
    echo "  - Collection: ${COLLECTION_DIR}/"
    echo "  - Logs: ${LOG_DIR}/"
    echo "  - Results: ${RESULTS_DIR}/"
    echo "=========================================="
} > "${SUMMARY_FILE}"

# Write CSV result
echo "${PYTHON_VERSION};${ANSIBLE_VERSION};${ANSIBLE_STATUS}" > "${RESULT_CSV}"

# Display summary
cat "${SUMMARY_FILE}"

log "=========================================="
if [ "${ANSIBLE_STATUS}" == "tested" ]; then
    log_success "All tests completed successfully!"
    echo ""
    log "Results are available in: ${RELEASE_DIR}"
    exit 0
elif [ "${ANSIBLE_STATUS}" == "unsupported" ]; then
    log_warning "Ansible version ${ANSIBLE_VERSION} is not supported with Python ${PYTHON_VERSION}"
    echo ""
    log "Results are available in: ${RELEASE_DIR}"
    exit 0
else
    log_error "Tests failed. Check logs for details."
    echo ""
    log "Results are available in: ${RELEASE_DIR}"
    exit 1
fi
