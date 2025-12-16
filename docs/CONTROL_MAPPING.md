# Control Mapping Overview

The detailed control catalog lives in `control_catalog_skeleton.yaml` at
the portfolio project root.

This document explains how it is used by the Cloud Compliance Readiness
Toolkit.

## Catalog Dimensions

Each catalog entry can be thought of as:

- **Framework:** SOC 2, ISO/IEC 27001:2022, PCI DSS v4.0 (subset)
- **Control:** e.g., `CC7.2`, `A.12.4.1`, `Req.10`
- **Labs:** AWS GRC labs such as `lab1_cloudtrail_validation`,
  `lab3_s3_public_check`, `lab8_audit_pack_generator`,
  `lab9_control_dashboard`
- **Evidence types:** CSV/JSON reports, Security Hub findings,
  dashboards, screenshots

## How the API Will Use the Catalog

- Seed `Framework`, `Control`, and `Lab` tables from the YAML file.
- Power `/frameworks`, `/controls`, and `/labs` read-only endpoints.
- Provide a backbone for project-specific evidence and remediation
  planning in `/projects`, `/evidence`, and `/tasks`.
