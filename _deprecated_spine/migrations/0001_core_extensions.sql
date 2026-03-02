-- Migration 0001: Core Extensions and Enums
-- Depends on: None

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Role Enum (Matches RBAC Policy)
CREATE TYPE role_enum AS ENUM (
    'super_admin',
    'admin',
    'user',
    'auditor',
    'system_bot'
);

-- Outcome Enum (Matches Decision Object)
CREATE TYPE outcome_enum AS ENUM (
    'APPROVED',
    'DENIED',
    'NEEDS_MORE_EVIDENCE'
);

-- Surface Criticality Enum (Matches Surface Map)
CREATE TYPE criticality_enum AS ENUM (
    'HIGH',
    'MEDIUM',
    'LOW'
);
