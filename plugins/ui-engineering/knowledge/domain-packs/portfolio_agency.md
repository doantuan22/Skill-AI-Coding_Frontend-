# Portfolio & Agency Domain Design Pack

**Pack ID**: `domain.portfolio_agency`  
**Domain**: `portfolio_agency`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `portfolio`, `agency`, `studio`, `creative`, `freelance`, `showcase`  

---

## 1. User Types & Operational Context
- **Primary Users**: Prospective clients, recruiters, hiring managers, creative directors.
- **Key Psychology**: Assessing credibility, technical craft, aesthetic maturity, and quantifiable past outcomes in under 30 seconds.

## 2. Domain Subtopics
- `narrative_structure`: Hero statement, positioning tagline, about the studio/practitioner, philosophy.
- `project_showcase`: Featured project cards, hover reveals, client tags, discipline badges (Design, Engineering, Brand).
- `case_study`: Challenge, solution, architecture diagrams, before/after comparisons, tangible business outcomes (KPIs).
- `services_outcomes`: Service offerings, engagement models, client logos, social proof testimonials.
- `contact_conversion`: Clean inquiry form, project budget selectors, email/calendar booking links.

## 3. Critical Flows
1. **Showcase to Case Study**: Browsing project gallery -> clicking project card -> reading narrative case study -> reviewing metrics.
2. **Client Inquiry / Booking**: Reviewing services and testimonials -> clicking "Start a Project" -> filling inquiry form -> confirmation.

## 4. Information Hierarchy & UX Patterns
- **Outcomes Over Fluff**: Feature tangible results prominently (e.g. `+140% conversion rate`, `Reduced latency by 45%`).
- **Media & Typography Craft**: High-quality project imagery, balanced typographic hierarchy, generous breathing room.
- **Motion Discipline**:
  - Micro-interactions (hover reveals, smooth page transitions) must feel polished and purposeful.
  - Motion must **never** hijack native scrolling (`scrolljacking`) or impair keyboard navigation.
  - Respect `prefers-reduced-motion` strictly.

## 5. Required UI States
- `loading`: Subtle, elegant opacity fade-in or layout skeleton.
- `empty`: Friendly placeholder if project categories currently have no public case studies.
- `interactive_preview`: Interactive video or iframe preview of live project work with a fallback static image.
- `inquiry_success`: Warm confirmation message confirming typical response time ("We reply within 24 hours").

## 6. Responsive & Accessibility Priorities
- **Responsive**: Grid to single-column stacking for case studies; responsive image resolution to ensure fast mobile page loads.
- **Accessibility**:
  - All project images must include descriptive `alt` text explaining the design or interface shown.
  - Interactive carousels must have visible previous/next buttons and pause on hover/focus.
  - High contrast text against background (avoid ultra-pale gray body text).

## 7. Anti-Patterns to Avoid
- **Scrolljacking**: Overriding the user's natural scroll wheel behavior with jarring horizontal or accelerated scrolling.
- **Heavy Unoptimized Assets**: Dumping 15 uncompressed 10MB video files on the home page causing sluggish rendering.
- **Vague Descriptions**: Showing pretty screenshots without explaining the problem, the process, or the outcome.

## 8. Workflow Integration & Precedence
- **Greenfield**: Allows high creative expression, unique layout grids, and brand personality.
- **Existing UI**: Subordinate to existing brand systems and established showcase architecture. Level 6 in precedence hierarchy.
