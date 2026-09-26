# Finance & Fintech Domain Design Pack

**Pack ID**: `domain.finance_fintech`  
**Domain**: `finance_fintech`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `fintech`, `finance`, `banking`, `crypto`, `payments`, `investment`, `wallet`  

---

## 1. User Types & Operational Context
- **Primary Users**: Bank customers, investors, financial controllers, payment users.
- **Key Psychology**: Extreme risk aversion, high security consciousness, demanding complete transparency regarding balances, fees, and transaction confirmations.

## 2. Domain Subtopics
- `account_overview`: Total balance cards, multi-currency accounts, quick action buttons (Send, Receive, Add Funds).
- `transaction_history`: Date-grouped transaction feeds, category icons, merchant details, download statement actions.
- `transfer_payment`: Recipient selector, amount input with real-time conversion/fees, payment method selection, memo field.
- `confirmation_audit`: Two-step verification modal, itemized transfer review (Amount, Fee, Total Debited, Recipient Account), irreversible action warnings.
- `risk_security`: Session timeout warnings, biometric authentication cues, 2FA input screens, card freeze/unfreeze toggles.

## 3. Critical Flows
1. **Fund Transfer**: Entering recipient -> typing amount -> inspecting fee breakdown -> reviewing confirmation summary -> submitting with 2FA -> receipt.
2. **Transaction Inspection**: Browsing transaction list -> filtering by date/type -> expanding receipt drawer -> exporting PDF.
3. **Card Management**: Viewing card details (masked by default) -> toggling temporary freeze -> adjusting transaction limits.

## 4. Information Hierarchy & Trust Patterns
- **Numeric Clarity & Prominence**:
  - Currency symbols and decimal amounts must be visually distinct and clearly aligned.
  - Negative values (debits/expenses) clearly distinguished from positive values (credits/income) via clean formatting (`-$45.00` vs `+$250.00`).
- **Confirmation Step Discipline**:
  - Every financial transaction must include an explicit review step before execution.
  - Primary button must state the exact amount: `"Transfer $150.00"` rather than generic `"Submit"` or `"OK"`.
- **Fee Transparency**: Display transfer fees prominently before confirmation. Never conceal charges.

## 5. Strict Financial Scope Boundary
- **NO Financial Advice**: The UI pack guides data visualization, transaction safety, and form clarity. It must NEVER generate algorithmic financial recommendations or automated investment instructions.

## 6. Required UI States
- `loading`: Secure animated shield or skeleton table while querying bank balances.
- `masked`: Sensitive account numbers and balances concealed by default (`$••,•••.••`) with a toggle eye icon.
- `destructive_confirm`: High-friction confirmation for irreversible transfers or account closure.
- `transaction_status`: Explicit tags for `Pending`, `Completed`, `Failed`, and `Reversed`.

## 7. Responsive & Accessibility Priorities
- **Responsive**: Sticky confirmation buttons on mobile transfer screens; responsive keypad for PIN/amount entry.
- **Accessibility**:
  - Currency amounts and numbers must use tabular/monospaced digits (`tabular-nums`) to prevent jitter and misalignment.
  - Screen readers must read full currency names: `aria-label="Negative 45 US Dollars"` for `-$45.00`.
  - Contrast ratios for status tags (`Pending: Amber`, `Failed: Red`, `Success: Green`) must pass WCAG AA.

## 8. Anti-Patterns to Avoid
- **Ambiguous Confirmation CTAs**: Buttons that say "Confirm" without reiterating the monetary amount and recipient.
- **Hidden Fees**: Revealing network or exchange rate fees only after the transaction is executed.
- **Decorative Obscurity**: Gradient text or light gray typography on balance amounts that impairs readability.

## 9. Workflow Integration & Precedence
- **Greenfield**: Informs account dashboards, transaction tables, and two-step transfer modals.
- **Existing UI**: Subordinate to existing brand systems and regulatory UI standards. Level 6 in precedence hierarchy.
