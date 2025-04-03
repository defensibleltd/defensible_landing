# CSS Styles for IP Fabric Reports

This directory contains the CSS styles used to customize the appearance of IP Fabric reports. You can switch between different color themes by modifying the import statements in the `default_style.css` file.

## How to Use CSS Themes

To apply a specific theme to your reports, follow these steps:

1. **Open the `default_style.css` file**: This file serves as the main stylesheet for your reports.

2. **Uncomment the desired theme import**: At the top of the `default_style.css` file, you will find import statements for different themes. Uncomment the import statement for the theme you want to use.

   ```css
   /* Uncomment the desired theme to apply */
   /* @import url('themes/theme_light.css'); */
   /* @import url('themes/theme_dark.css'); */
   @import url('themes/default_colors.css');
   ```

3. **Save the file**: After uncommenting the desired theme, save the changes to the `default_style.css` file.

4. **Generate your report**: Run the report generation command as usual. The selected theme will be applied to the report.

## Available Themes

- **Default Colors**: A neutral color palette that serves as the base style.
- **Light Theme**: A bright and clean appearance suitable for well-lit environments.
- **Dark Theme**: A dark and modern look that is easy on the eyes in low-light conditions.

## Chart Colors Configuration

The `chart_colors.json` file in this directory defines the color palette used for pie charts in the IP Fabric Reports. The colors are specified in hexadecimal format and are used to ensure consistent styling across all reports.

### How to Update Chart Colors

1. **Locate the `chart_colors.json` file**: This file is located in the `themes` directory.
2. **Edit the Colors**: Open the file and modify the values in the `"chart_colors"` array to update the colors.
3. **Save the Changes**: After editing, save the file to apply the new color scheme to your reports.

This setup allows for easy customization of chart colors without altering the Python or CSS code directly.

## Notes

- Ensure that only one theme import is uncommented at a time to avoid conflicts.
- You can customize the themes further by editing the respective CSS files in the `themes` directory.
