# Donor Grant Fundraising Implementation Plan

## Objective

Make `donor_grant_fundraising` usable as a standalone AppGen-X application when selected as the only PBC. The package must support fundraising and grant teams with owned records, command services, forms, wizards, controls, workbench queues, assistant document intake, release evidence, and package-local tests.

## Domain Scope

The PBC owns donor profiles, campaign hierarchies, pledges, gifts, restriction rules, grant applications, stewardship touchpoints, relationship maps, proposal workspaces, acknowledgements, briefing packets, opportunity scores, review chains, budget validations, governance records, and AppGen-X event tables.

Cross-PBC information is handled as future API/event projections. The PBC does not share datastore tables with customer, finance, document, or workflow packages.

## Implementation Slices

1. Standalone app runtime
   - Add an executable in-package fundraising app state and command surface.
   - Preserve PostgreSQL, MySQL, and MariaDB as the only ordinary backend choices.
   - Emit AppGen-X events through the package outbox contract.

2. Core fundraising flows
   - Register governed donor profiles for individuals, households, corporations, and foundations.
   - Enforce prospect pipeline stage progression and qualification evidence.
   - Model campaign hierarchy and goal progress.
   - Create pledge commitments with installment discipline and remaining balance.
   - Post gifts against pledges, campaigns, appeals, and restrictions.
   - Enforce restriction purpose matching.

3. Grant and stewardship flows
   - Manage grant opportunities, proposal completion, internal review, submission, award setup, and post-award obligations.
   - Record stewardship touchpoints, acknowledgements, cadence gaps, and next ask readiness.
   - Surface grant deadline risk, acknowledgement backlog, stewardship gaps, pledge exposure, and campaign performance.

4. Single-PBC UI and assistant
   - Expose forms for donors, prospects, campaigns, pledges, gifts, restrictions, grants, and stewardship.
   - Expose guided wizards for donor conversion, major gifts, restriction setup, grant submission, post-award setup, and first-run launch.
   - Expose blocking controls for prospect stages, pledge installments, gift matching, restriction rules, grant review, acknowledgements, and assistant mutations.
   - Route donor letters, gift documents, pledge instructions, restrictions, campaign appeals, stewardship notes, and grant guidelines into confirmed mutation plans with stable document hashes.

5. Verification
   - Add package-local tests for the executable flow, controls, assistant routing, service state, release evidence, and AppGen-X PBC audits.
   - Keep all edits inside `src/pyAppGen/pbcs/donor_grant_fundraising`.

## Acceptance Checks

- Package-local tests pass.
- Runtime smoke includes the fundraising app smoke.
- Release evidence includes schema, services, APIs, events, handlers, UI, forms, wizards, controls, assistant, governance, and the single-PBC app.
- A one-PBC generated app has enough forms, wizards, controls, service methods, workbench queues, and assistant guidance to operate the fundraising and grants domain.
