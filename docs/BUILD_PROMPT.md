# Complete ConsentGate build prompt

Use this prompt to rebuild or extend the project. It describes the intended product, security boundary, implementation, tests, demo, and deployment. The repository's README describes what the current prototype actually implements.

---

You are a senior product engineer and security engineer. Build a complete, runnable application named **ConsentGate** for the BUILD 2036 Digital Infrastructure track. Work in the existing repository. Inspect its files and instructions first. Deliver a polished app, tests, documentation, a reproducible demo, and a Render deployment configuration. Do not stop at a mockup or two isolated features.

## Product intent

ConsentGate is a purpose-bound data access layer for AI customer-support agents. A company must be able to use an agent to answer a customer question without giving that agent the entire customer profile. Start with one complete workflow: “Where is my order?” A trusted application issues a short-lived task grant for one tenant, customer, order, and purpose. The gateway checks that grant and the current synthetic consent state on every read. A controlled connector selects only the permitted fields before data reaches the agent.

The user roles are: (1) customer whose data is involved, (2) support operator using the agent, and (3) privacy/security reviewer inspecting decisions. The demo data is synthetic. The app must not imply a real Consent Manager, government, or CRM integration.

## Complete application

Build an operator console with an overview, live simulator, consent center, decision log, evaluation page, and useful empty/error/loading states. Build an API with typed inputs, clear errors, health check, documented routes, and a local synthetic database containing at least two customers and two tenants. Provide an offline deterministic agent so the demo works without external services. Add an optional Groq-backed agent that makes a real tool-call round trip and answers using the tool result. Keep the Groq API key only in server-side environment settings. Never expose it in frontend code, logs, screenshots, or Git.

Use a maintainable stack already present in the repository. Keep the policy engine independent of prompts and models. Design the UI so a judge can understand the access boundary and outcomes in under three minutes.

## Standout feature 1: live privacy counterfactual

Run the same synthetic order-status request through two clearly labeled lanes. The baseline lane is an intentionally broad tool-level configuration; the protected lane is ConsentGate. Show each lane's answer, number and names of fields that reached the agent, the access decision, and a hostile note planted in the baseline record. The protected connector must not send that note or any contact/marketing field to its agent. The baseline is an implemented comparison, not a statement about all commercial gateways. If the real Groq model varies, display the observed run honestly and preserve the deterministic fallback.

## Standout feature 2: mid-run consent change

Issue a task and allow its first read. Pause. Let the customer withdraw synthetic consent. Resume the same task and deny its next read because the current consent version no longer matches the grant. Show a chronological receipt of the allowed first read, consent change, and denied second read. State plainly that prior copies outside controlled systems are not erased. If time permits, support narrowing fields as well as full withdrawal; do not trade away a reliable revoke demonstration for this extension.

## Enforcement design

Treat agent prompts, tool arguments, model output, and retrieved notes as untrusted. The agent must not mint or change its own purpose. The trusted application issues a signed grant containing issuer, audience, tenant, customer, order, fixed purpose ID, expiry, unique ID, consent version, and policy version. Verify signature, issuer, audience, expiry, current consent version, resource ownership, operation, and policy version on each access. Use a maintained cryptographic library or standard primitives; never invent a cryptographic scheme. Fail closed when required state is missing.

For `ORDER_STATUS`, permit `get_order_status` on the grant's order and return only `status` and `delivery_window`. Deny `get_customer_profile`, cross-customer or cross-tenant reads, expired or modified grants, and reads after withdrawal. Select fields in the controlled connector before forming the tool result. Do not use an LLM as the allow/deny authority. An optional semantic detector may flag suspicious context for review but cannot substitute for the deterministic boundary.

## Audit

Record decision metadata: time, operation, target reference, rule, allow/deny, permitted field names, task ID or digest, and policy/consent version. Do not log personal field values. A hash chain may detect local edits; test that it does. Do not claim it resists a party able to replace the entire chain unless independently anchored. Make this limitation visible in docs.

## Evaluation

Write tests before implementation for each important behavior. Include allowed status lookup, extra-field denial, wrong customer, wrong tenant, modified token, wrong audience, expiry, revocation during a run, benign requests, hostile retrieved note, and audit tampering. Run a fixed synthetic scenario suite and report actual pass/fail counts. Compare field exposure for the baseline and protected paths. Measure local latency only if the benchmark controls and sample count are documented. Do not invent incident reduction, real-user outcomes, or model accuracy.

## Deployment and documentation

Provide `requirements.txt` or equivalent, an ignored `.env`, `.env.example`, health endpoint, and `render.yaml`. Secrets must be configured in Render, never committed. README must explain setup, architecture, API, threat model, policy, three-minute demo, tests, Groq configuration, Render deployment, prior art, limitations, and pilot path. Explicitly label the public hosted version as a synthetic, unauthenticated demo. Do not connect it to real customer records.

Prior art to acknowledge: Permit MCP Gateway has consent, authorization, and audit; an open-source consent gateway has an MCP proxy and hash-chained receipts; MCP has authorization guidance. Do not claim “first,” “unique,” “DPDP-compliant,” “zero leakage,” “instant global deletion,” or “production ready.” A defensible claim is that this prototype **demonstrates task-bound, customer-bound, field-level minimization and mid-run revocation in an AI support workflow**, compared with a clearly defined broad tool-permission baseline.

## Finish criteria

The app starts from a clean checkout, its tests pass, the two demo moments work in the browser, the offline path works without credentials, the Groq path uses only synthetic data, the Render blueprint is valid, and the README contains exact reproduction commands. Report any unverified deployment or external integration honestly. Do not claim success without running the relevant checks.
