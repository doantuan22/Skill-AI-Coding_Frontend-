# Healthcare Domain Design Pack

**Pack ID**: `domain.healthcare`  
**Domain**: `healthcare`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `health`, `medical`, `clinic`, `patient`, `telehealth`, `doctor`, `hospital`  

---

## 1. User Types & Operational Context
- **Primary Users**: Patients, doctors, nurses, clinic administrators, elderly individuals, vulnerable populations.
- **Key Psychology**: Stress or anxiety, need for absolute clarity and reassurance, zero tolerance for ambiguity, high accessibility demands.

## 2. Domain Subtopics
- `patient_practitioner`: Profiles, credentials, specialties, hospital affiliations, patient demographic records.
- `appointments`: Real-time slot booking, consultation mode (in-person vs video call), appointment reminders.
- `medical_records`: Lab results, prescription lists, immunization records, clinical notes history.
- `structured_data`: Health metric cards (blood pressure, glucose, heart rate), standard reference ranges, vital signs charts.
- `status_actions`: Prescription refill requests, emergency contact prompts, visit preparation checklists.

## 3. Critical Flows
1. **Practitioner Search & Booking**: Searching by specialty/condition -> selecting practitioner -> picking available time slot -> intake form.
2. **Lab Result Inspection**: Viewing test list -> opening detailed panel -> observing value against normal reference range -> doctor note.
3. **Prescription Refill Request**: Viewing active medications -> selecting dosage -> confirming pharmacy -> receiving submission confirmation.

## 4. Information Hierarchy & Safe UX Patterns
- **Extreme Clarity Over Decoration**: Clean typography, high contrast, uncluttered layouts. Decorative elements must never distract from medical facts.
- **Reference Ranges for Metrics**: When showing medical metrics (e.g. `128/82 mmHg`), always show the standard normal range and clear text status ("Normal", "Elevated", "Low").
- **Clear Distinction Between Observation, Status, and Action**:
  - Observation: `Blood Glucose: 110 mg/dL`
  - Status: `Within normal range (Fasting)`
  - Action: `Schedule follow-up appointment`

## 5. Strict Medical Safety & Scope Boundary
- **NO Medical Diagnosis**: The UI engineering pack guides presentation and accessibility only. It must NEVER generate medical diagnoses, clinical treatment plans, or arbitrary medication recommendations.

## 6. Required UI States
- `loading`: Calm, non-intrusive loading spinners with reassurance ("Securely loading your health records...").
- `empty`: Friendly empty states encouraging preventive checkups or clear instructions for newly registered patients.
- `abnormal_flag`: Unambiguous, high-contrast badges for out-of-range lab results (combining color with icons and text labels).
- `emergency_notice`: Prominent persistent banner on patient portals ("If you are experiencing a medical emergency, call 911 / 115 immediately").

## 7. Responsive & Accessibility Priorities
- **Accessibility (Critical Priority)**:
  - Strict compliance with WCAG AAA contrast where feasible (minimum WCAG AA 4.5:1 text, 3:1 graphical objects).
  - Minimum font size of 16px for body text; avoid light font weights (use 400+ regular or 500 medium).
  - All form controls must have explicit `<label>` tags and descriptive error feedback.
  - Large touch targets (minimum 48x48px on mobile).

## 8. Anti-Patterns to Avoid
- **Color-Only Status Indicators**: Indicating normal/abnormal using only green/red dots without supporting text labels or icons (violates a11y for colorblind users).
- **Ambiguous Dosages**: Displaying numbers without units (`10` instead of `10 mg`).
- **Hidden Emergency Resources**: Burying critical clinical contact numbers in footers or behind multiple clicks.

## 9. Workflow Integration & Precedence
- **Greenfield**: Establishes clean accessible layouts, high-contrast text hierarchies, and patient portal navigation.
- **Existing UI**: Subordinate to existing brand systems. If an existing healthcare client uses a dark or monochrome palette, retain it while enforcing WCAG contrast standards. Never force arbitrary "medical blue" onto an existing brand.
