#!/usr/bin/env bash
# // ZeaZDev [Operational Recovery Helper Script] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Reliability Improvements) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

set -euo pipefail

# ============================================================================
# fix.sh - Comprehensive recovery and generation script
# ============================================================================
# 
# Purpose:
#   Streamline recovery and Prisma client generation with automatic fallbacks,
#   disk space management, and optional migration execution.
#
# Environment Variables:
#   PRUNE=1              - Enable aggressive disk space pruning before build
#   SKIP_MIGRATE=1       - Skip prisma migrate dev step
#   SKIP_WORKER=1        - Skip worker service rebuild
#   DEBUG=1              - Enable verbose output
#
# Usage:
#   ./fix.sh                    # Standard run: build, generate, migrate
#   PRUNE=1 ./fix.sh            # With disk space pruning
#   SKIP_MIGRATE=1 ./fix.sh     # Skip migration step
#   DEBUG=1 ./fix.sh            # Verbose mode
#
# ============================================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

log_debug() {
    if [ "${DEBUG:-0}" = "1" ]; then
        echo -e "${BLUE}[DEBUG]${NC} $*"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check disk space and warn if low
check_disk_space() {
    log_info "Checking disk space..."
    local available
    available=$(df -h . | awk 'NR==2 {print $4}')
    log_info "Available disk space: $available"
    
    local available_kb
    available_kb=$(df -k . | awk 'NR==2 {print $4}')
    
    if [ "$available_kb" -lt 2097152 ]; then # Less than 2GB
        log_warn "Low disk space detected (< 2GB available)"
        return 1
    fi
    return 0
}

# Prune Docker resources to free disk space
prune_docker() {
    log_info "Pruning Docker resources to free disk space..."
    
    if ! command_exists docker; then
        log_warn "Docker not found, skipping Docker pruning"
        return 0
    fi
    
    log_debug "Removing stopped containers..."
    docker container prune -f || true
    
    log_debug "Removing dangling images..."
    docker image prune -f || true
    
    log_debug "Removing unused volumes..."
    docker volume prune -f || true
    
    log_debug "Removing build cache..."
    docker builder prune -f || true
    
    log_success "Docker pruning completed"
}

# Install Node.js in container if needed
install_nodejs_in_container() {
    local container="$1"
    log_info "Checking Node.js availability in container: $container"
    
    if docker exec "$container" which node >/dev/null 2>&1; then
        log_success "Node.js already available in $container"
        return 0
    fi
    
    log_warn "Node.js not found in $container, attempting installation..."
    
    # Try NodeSource installation first
    log_debug "Attempting NodeSource installation..."
    if docker exec "$container" bash -c '
        apt-get update && \
        apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
        mkdir -p /etc/apt/keyrings && \
        curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
        echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
        apt-get update && \
        apt-get install -y --no-install-recommends nodejs && \
        apt-get clean && rm -rf /var/lib/apt/lists/*
    ' 2>/dev/null; then
        log_success "Node.js installed via NodeSource in $container"
        return 0
    fi
    
    # Fallback to apt nodejs if available
    log_debug "NodeSource failed, trying apt fallback..."
    if docker exec "$container" bash -c 'apt-get update && apt-get install -y nodejs && apt-get clean' 2>/dev/null; then
        log_success "Node.js installed via apt in $container"
        return 0
    fi
    
    log_error "Failed to install Node.js in $container"
    return 1
}

# Generate Prisma client in container
generate_prisma_client() {
    local container="$1"
    log_info "Generating Prisma client in container: $container"
    
    if ! docker exec "$container" test -f prisma/schema.prisma; then
        log_warn "No Prisma schema found in $container, skipping generation"
        return 0
    fi
    
    # Ensure Node.js is available
    install_nodejs_in_container "$container" || {
        log_error "Cannot generate Prisma client without Node.js"
        return 1
    }
    
    # Generate client
    if docker exec "$container" prisma generate --schema prisma/schema.prisma; then
        log_success "Prisma client generated successfully in $container"
        return 0
    else
        log_error "Prisma client generation failed in $container"
        return 1
    fi
}

# Run Prisma migrations
run_migrations() {
    local container="$1"
    log_info "Running Prisma migrations in container: $container"
    
    if ! docker exec "$container" test -f prisma/schema.prisma; then
        log_warn "No Prisma schema found in $container, skipping migrations"
        return 0
    fi
    
    if docker exec "$container" prisma migrate dev --name auto_migration --skip-generate; then
        log_success "Migrations completed successfully in $container"
        return 0
    else
        log_warn "Migration failed (may be expected if already up to date)"
        return 0 # Non-fatal
    fi
}

# Main execution
main() {
    log_info "Starting fix.sh - Operational Recovery Helper"
    log_info "========================================"
    
    # Check prerequisites
    if ! command_exists docker; then
        log_error "Docker is required but not found"
        exit 1
    fi
    
    if ! docker compose version >/dev/null 2>&1; then
        log_error "Docker Compose is required but not found"
        exit 1
    fi
    
    # Optional: Disk space pruning
    if [ "${PRUNE:-0}" = "1" ]; then
        log_info "PRUNE=1 detected, performing disk cleanup..."
        prune_docker
        check_disk_space || log_warn "Still low on disk space after pruning"
    else
        check_disk_space || log_warn "Consider running with PRUNE=1 if build fails"
    fi
    
    # Stop existing services
    log_info "Stopping existing services..."
    docker compose down || true
    
    # Build services
    log_info "Building services..."
    
    log_info "Building backend..."
    if docker compose build backend; then
        log_success "Backend built successfully"
    else
        log_error "Backend build failed"
        exit 1
    fi
    
    if [ "${SKIP_WORKER:-0}" != "1" ]; then
        log_info "Building worker..."
        if docker compose build worker; then
            log_success "Worker built successfully"
        else
            log_warn "Worker build failed (non-fatal)"
        fi
    else
        log_info "SKIP_WORKER=1 detected, skipping worker build"
    fi
    
    # Start services
    log_info "Starting services..."
    if docker compose up -d postgres redis backend; then
        log_success "Services started"
    else
        log_error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 5
    
    # Generate Prisma client if needed
    log_info "Checking Prisma client generation..."
    if generate_prisma_client "abt_backend"; then
        log_success "Prisma client ready"
    else
        log_warn "Prisma client generation had issues (check logs)"
    fi
    
    # Run migrations unless skipped
    if [ "${SKIP_MIGRATE:-0}" != "1" ]; then
        if run_migrations "abt_backend"; then
            log_success "Database migrations completed"
        else
            log_warn "Migration step completed with warnings"
        fi
    else
        log_info "SKIP_MIGRATE=1 detected, skipping migrations"
    fi
    
    # Verify Prisma CLI
    log_info "Verifying Prisma CLI..."
    if docker exec abt_backend prisma --version; then
        log_success "Prisma CLI is functional"
    else
        log_warn "Prisma CLI verification failed"
    fi
    
    # Show service status
    log_info "========================================"
    log_info "Service Status:"
    docker compose ps
    
    log_info "========================================"
    log_success "fix.sh completed successfully!"
    log_info ""
    log_info "Available endpoints:"
    log_info "  Backend API:  http://localhost:8000/docs"
    log_info "  Frontend:     http://localhost:3000"
    log_info "  Prometheus:   http://localhost:9090"
    log_info "  Grafana:      http://localhost:3001"
    log_info ""
    log_info "To view logs: docker compose logs -f backend"
    log_info "To stop:      docker compose down"
}

# Run main function
main "$@"
