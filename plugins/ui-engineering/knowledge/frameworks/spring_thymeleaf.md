# Spring Boot + Thymeleaf UI Engineering Knowledge Pack

**Pack ID**: `framework.spring_thymeleaf`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Thymeleaf Frontend Templates & Fragments
- **Template Layouts**: Use `th:replace` and `th:insert` with fragments (`th:fragment="header"`) to share shells across pages without duplicate markup.
- **Data Binding**: Use `th:text="${item.name}"`, `th:each="item : ${items}"`, and `th:if="${hasData}"` for deterministic view rendering.
- **Form UI**: Bind form fields with `th:field="*{fieldName}"` and handle error states with `th:if="${#fields.hasErrors('fieldName')}"`.

## 2. Hard Preservation & Architecture Boundary
- **Preserve Controller/Template Contracts**: Do not alter template model variable names expected by Spring MVC controllers.
- **UI Focus Only**: Never rewrite Spring services, repositories, JPA entities, or backend business logic during a UI/UX task.
- **Styling Integration**: Work within the project's existing CSS/Bootstrap pipeline (e.g. `src/main/resources/static/css/`).
