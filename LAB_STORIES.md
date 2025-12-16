# Lab Stories – Cloud Compliance Readiness Toolkit

Short, interview-ready stories for three key labs, showing how they map
to controls, evidence, and remediation in the toolkit.

## Lab 1 – CloudTrail Validation (Logging & Monitoring)

**What the lab does**  
Validates that AWS CloudTrail is enabled and configured correctly (for
example, multi-region, centralized logging). This helps prove that user
activities and system events are being captured for security and
compliance review.

**Key frameworks and controls**

- **ISO/IEC 27001:2022** – A.12.4.1 Event logging
- **SOC 2** – CC7.x (system operations and monitoring)
- **PCI DSS 4.0** – Req. 10 (logging and monitoring)

**Example evidence in the toolkit**

Recorded via `POST /evidence`:

```json
{
  "project_id": "<project_id>",
  "control_id": "A.12.4.1",
  "lab_id": "lab1_cloudtrail_validation",
  "type": "json_report",
  "location": "s3://grc-demo-evidence/cloudtrail/2025-12-01-validation.json"
}
```

**Example remediation task**

Recorded via `POST /tasks`:

```json
{
  "project_id": "<project_id>",
  "control_id": "A.12.4.1",
  "title": "Harden CloudTrail logging coverage",
  "description": "Use Lab 1 CloudTrail validation to identify regions or accounts without full audit trail coverage and update the baseline.",
  "owner": "Cloud Platform Lead",
  "status": "open"
}
```

**How I would explain this to a client or auditor**

> "This lab validates that CloudTrail is running in all the right
>  places and that logs are centralized. In a readiness engagement, I
>  use the output to prove that user and system activities are being
>  captured consistently. If we find gaps (such as regions or accounts
>  without CloudTrail), they become remediation tasks in the toolkit. By
>  the time we reach the audit, we can show both the historical
>  validation reports and the changes we made, supporting ISO A.12.4.1,
>  SOC 2 CC7, and PCI Req. 10."

---

## Lab 3 – S3 Public-Access Detector (Data Exposure & Access Control)

**What the lab does**  
Scans S3 buckets to detect public access and produces a findings report.
This helps identify accidental data exposure and enforce least-privilege
access.

**Key frameworks and controls**

- **ISO/IEC 27001:2022** – A.9.4.1 Information access restriction
- **SOC 2** – CC6.x (logical access controls)
- **PCI DSS 4.0** – Req. 7/8 (access control & authentication)

**Example evidence in the toolkit**

Recorded via `POST /evidence`:

```json
{
  "project_id": "<project_id>",
  "control_id": "A.9.4.1",
  "lab_id": "lab3_s3_public_check",
  "type": "json_report",
  "location": "s3://grc-demo-evidence/s3-public/2025-12-01-findings.json"
}
```

**Example remediation task**

Recorded via `POST /tasks`:

```json
{
  "project_id": "<project_id>",
  "control_id": "A.9.4.1",
  "title": "Remediate public S3 buckets",
  "description": "Review the S3 public access findings from Lab 3 and either restrict access or document approved exceptions.",
  "owner": "Data Owner",
  "status": "open"
}
```

**How I would explain this to a client or auditor**

> "This lab continuously looks for publicly accessible S3 buckets and
>  generates a clear list of risk areas. During a readiness project, I
>  work with data owners to review each bucket: which ones truly need to
>  be public, which can be restricted, and which require formal
>  exceptions. Every finding is tracked as a remediation task in the
>  toolkit, so we can demonstrate to auditors that we not only detect
>  exposure but also manage and close it, aligning with ISO A.9.4.1,
>  SOC 2 CC6, and PCI 7/8."

---

## Lab 4 – MFA Enforcement Evidence (Identity & Access Management)

**What the lab does**  
Enumerates IAM users and checks whether multi-factor authentication
(MFA) is enforced, producing a report of accounts without MFA.

**Key frameworks and controls**

- **SOC 2** – CC6.1 (logical access – strong authentication)
- **ISO/IEC 27001:2022** – A.9.2.3 Management of privileged access
- **PCI DSS 4.0** – Req. 7/8 (access control & strong authentication)

**Example evidence in the toolkit**

Recorded via `POST /evidence`:

```json
{
  "project_id": "<project_id>",
  "control_id": "CC6.1.2",
  "lab_id": "lab4_mfa_enforcement",
  "type": "csv_report",
  "location": "s3://grc-demo-evidence/iam-mfa/2025-12-01-users-without-mfa.csv"
}
```

**Example remediation task**

Recorded via `POST /tasks`:

```json
{
  "project_id": "<project_id>",
  "control_id": "CC6.1.2",
  "title": "Close MFA gaps for privileged IAM users",
  "description": "Use the Lab 4 MFA enforcement report to require MFA on all privileged IAM users and document the enforcement policy.",
  "owner": "Head of Security",
  "status": "open"
}
```

**How I would explain this to a client or auditor**

> "This lab surfaces which IAM users do and do not have MFA enforced.
>  In practice, I use it with the security and platform teams to clean
>  up privileged accounts before an audit. We take the MFA report,
>  create remediation tasks in the toolkit, and then rerun the lab to
>  prove the gaps have been closed. That gives auditors a clear
>  before-and-after story for SOC 2 CC6.1, ISO A.9.2.3, and PCI 7/8."

---

## Other scenarios I can walk through

- **Continuous monitoring & reporting (Labs 1, 6, 8)** – Combining CloudTrail validation, continuous control checks, and an audit-pack generator to show how findings flow into dashboards and packaged evidence.
- **Access governance & least privilege (Labs 3, 4, 7)** – Using S3 public-access detection, MFA enforcement, and IAM role review to reduce attack surface and prove strong logical access controls.
