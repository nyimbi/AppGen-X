# AppGen DSL Tutorial

This tutorial builds a small invoicing app with forms, workflow, roles, and an
agent.

## 1. Name The App

Create `invoice.appgen`:

```appgen
app InvoiceDesk { theme: sage; targets: web, pwa, mobile, desktop }
```

## 2. Add Core Tables

```appgen
table Customer {
  id: int pk
  name: string required search
  email: string unique
}

table Invoice {
  id: int pk
  invoice_number: string required unique search
  customer_id: int required -> Customer.id [many-to-one]
  status: string default "draft" search
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
}

table InvoiceLine {
  id: int pk
  invoice_id: int required -> Invoice.id [many-to-one]
  description: string required
  quantity: decimal default 1
  unit_price: decimal default 0
  line_total: decimal = quantity * unit_price
}
```

## 3. Add Form Layouts

```appgen
view InvoiceForm for Invoice {
  Header: invoice_number, customer_id, status;
  Totals: subtotal, tax, total;
  @ invoice_number TextBox 0 0 4 1;
  @ customer_id Lookup 4 0 4 1;
  @ status Select 8 0 3 1;
}
```

## 4. Add Workflow

```appgen
flow InvoiceLifecycle {
  draft -> approved
  approved -> sent
  sent -> paid
  sent -> void
}
```

## 5. Add Rules

```appgen
rule InvoicePolicy for Invoice {
  invoice_number required "Invoice number is required"
  customer_id required "Customer is required"
  status in draft, approved, sent, paid, void -> review
}
```

## 6. Add Roles

```appgen
role Accountant {
  Customer: read, create, update
  Invoice: read, create, update
  InvoiceLine: read, create, update
}

role Auditor {
  Customer: read
  Invoice: read
  InvoiceLine: read
}
```

## 7. Add An Agent

```appgen
llm LocalAssistant {
  provider: ollama
  mode: local
  model: llama3
}

agent InvoiceReviewer {
  provider: LocalAssistant
  goal: "Review invoices for missing customer, tax, and line totals"
  tools: schema, forms, reports
}
```

## 8. Lint And Generate

```bash
appgen --lint-dsl invoice.appgen
appgen --dsl invoice.appgen --writedir generated/invoice/app
```

After generation, inspect:

- `app/studio.py` for IDE/workbench contracts.
- `app/dsl_reference.py` for generated DSL examples and lint helpers.
- `app/form_designer.py` for Delphi-style component placement.
- `app/platforms.py` and `native/` for web, mobile, and desktop targets.
- `app/agents.py` for local/API LLM readiness and agent plans.

