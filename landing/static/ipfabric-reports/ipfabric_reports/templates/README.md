# IP Fabric Report Templates

This directory contains the HTML templates used for generating IP Fabric reports. The templates use Jinja2 templating engine and follow a hierarchical structure to maintain consistency across all reports.

## Template Structure

- **`base_template.html`**: The foundation template that defines the common structure for all reports.
- **`_macros.html`**: Contains reusable components and macros for report elements.
- **Report-specific templates**: Each report type has its own template file (e.g., `overview_template.html`, `cve_template.html`).

## Base Template

The `base_template.html` provides a consistent structure for all reports, including:
- HTML document structure
- Header with logo and report title
- Footer with timestamp and page information
- Content block for report-specific content

## Using Templates

### Extending the Base Template

All report templates should extend the base template:

```html
{% extends 'base_template.html' %}
{% import "_macros.html" as macros %}

{% block content %}
    <!-- Report-specific content goes here -->
{% endblock %}
```

### Available Blocks

The base template provides the following blocks that can be overridden:

- **`title`**: For setting the document title
- **`head`**: For adding additional head elements
- **`content`**: For the main report content

### Using Macros

Common report elements are available as macros:

```html
{{ macros.header(report_details.name, site_filter) }}
{{ macros.footer(report_details.name, current_time) }}
{{ macros.network_summary(network_summary) }}
{{ macros.report_introduction(report_details) }}
```

## Best Practices

1. **Always extend the base template** for new report types.
2. **Use macros for repeated elements** to maintain consistency.
3. **Keep templates focused on presentation** - logic should be handled in Python code.
4. **Test reports with various data sets** to ensure templates handle edge cases.
5. **Maintain consistent styling** by using the CSS classes defined in the style sheets.

## Common Variables

Most templates have access to these variables:

- `report_details`: Contains report metadata including name and introduction
- `site_filter`: The site filter applied to the report (if any)
- `current_time`: The timestamp when the report was generated
- `network_summary`: Summary statistics about the network
