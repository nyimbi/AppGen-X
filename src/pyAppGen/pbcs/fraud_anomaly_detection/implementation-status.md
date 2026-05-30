# Implementation Status for `fraud_anomaly_detection`

## Improve1 fraud control implementation

- Added `fraud_control.py` as the executable control contract for all 50 fraud and anomaly detection capabilities.
- Each capability maps to owned fraud signal, score, rule, case, identity graph, device, network, velocity, explanation, loss, queue, configuration, and AppGen-X runtime surfaces.
- Runtime, UI, and release evidence expose fraud controls without stream-engine picker leakage and keep ordinary datastore backends limited to PostgreSQL/MySQL/MariaDB.
- Domain behavior tests cover positive execution for all 50 capabilities plus negative guards for canonicalization, signal quality, rule lifecycle, simulation side effects, policy approval, explanation leakage, tenant isolation, privacy, fairness, agent confirmation, cross-PBC boundaries, replay safety, evidence packs, and workbench coverage.
