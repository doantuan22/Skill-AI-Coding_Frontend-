# Hospitality & Travel Domain Design Pack

**Pack ID**: `domain.hospitality_travel`  
**Domain**: `hospitality_travel`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `travel`, `hotel`, `booking`, `hospitality`, `resort`, `tourism`, `vacation`  

---

## 1. User Types & Operational Context
- **Primary Users**: Vacationers, business travelers, family trip planners.
- **Key Psychology**: Anticipation and excitement paired with anxiety over dates, pricing transparency, cancellation terms, and location accuracy.

## 2. Domain Subtopics
- `search`: Sticky horizontal or prominent hero search bar (Destination, Check-in/Check-out dates, Guests/Rooms counter).
- `date_guest`: Dual-month interactive calendar date range picker, adult/child/infant room occupancy selectors.
- `property_detail`: High-res photo gallery with category filters, amenities list (Wi-Fi, pool, parking), neighborhood map, guest reviews.
- `room_selection`: Room cards displaying bed types, maximum occupancy, cancellation policy badge, nightly rate vs total stay rate.
- `booking`: Guest contact info, special requests, arrival time estimates, payment details, price breakdown itemization.
- `confirmation`: Printable booking voucher, check-in instructions, host/hotel contact info, trip modification/cancellation entry point.

## 3. Critical Flows
1. **Search & Availability Check**: Entering destination and dates -> viewing filtered property cards -> checking availability.
2. **Room Comparison & Selection**: Comparing room types (Standard vs Deluxe) -> selecting rate tier (Non-refundable vs Free cancellation).
3. **Reservation & Confirmation**: Reviewing stay dates and price breakdown -> submitting booking -> receiving confirmation with cancellation policy.

## 4. Information Hierarchy & UX Patterns
- **Persistent Date & Guest Context**: When navigating from search to property page, the selected dates and guest count must remain visible and easily editable.
- **Total Price Transparency**: Always display both the nightly price and the calculated total price for the selected stay duration, including estimated taxes and fees.
- **Cancellation Policy Prominence**: Clearly label free cancellation dates in green or neutral status tags (e.g., "Free cancellation before Oct 15").

## 5. Required UI States
- `loading`: Map and property card skeletons while querying live availability.
- `unavailable`: Clear feedback when dates have no availability, suggesting flexible +/- 3 days alternatives.
- `booking_summary`: Live updating price breakdown drawer as room options or add-ons (breakfast, airport shuttle) are toggled.
- `confirmed`: Dedicated confirmation view with Google/Apple calendar integration links.

## 6. Responsive & Accessibility Priorities
- **Responsive**: Compact search bar on mobile that opens a full-screen search modal with clean touch-friendly date selection.
- **Accessibility**:
  - Calendar date pickers must have complete keyboard navigation (arrow keys across days, `PageUp`/`PageDown` for months).
  - Guest counter buttons (`+` and `-`) must have descriptive `aria-label="Add adult"` / `aria-label="Remove adult"`.

## 7. Anti-Patterns to Avoid
- **Hidden Fees & Taxes**: Disclosing resort fees or cleaning charges only on the final payment page.
- **Ambiguous Date Context**: Displaying "Oct 12 - Oct 15" without clearly indicating the number of nights or the check-out year.
- **Fake Urgency Slop**: Displaying misleading or fabricated countdown timers and "Only 1 room left!" banners that erode user trust.
- **Airbnb / Booking.com Cloning**: Copying proprietary visual brand assets or layouts directly.

## 8. Workflow Integration & Precedence
- **Greenfield**: Guides booking search bars, room cards, and itemized reservation flows.
- **Existing UI**: Subordinate to existing brand colors and design systems. Never recolor an existing boutique hotel site to generic travel blue.
