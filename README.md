# CLNICALC

CLNICALC is a modern web application designed to streamline and simplify nursing informatics calculations. By entering patient data, nurses and healthcare professionals can instantly access accurate, actionable insights for medication dosing, fluid management, lab interpretation, and more. The tool supports over 100+ medical calculations, making it an essential resource for clinical decision-making and patient care.

## Features

- 100+ medical and nursing calculations
- Unit conversions (length, weight, temperature, pressure, area, volume, energy, infusion, concentration)
- Animated, user-friendly interface
- Search and filter calculations by category
- AI-powered explanations for calculation results
- Responsive design for desktop and mobile
- Built with Flask, CSS, Bootstrap, and modern JavaScript

## Try It Out

You can use CLNICALC instantly at:  
👉 [https://clinicalc.onrender.com](https://clinicalc.onrender.com)

---

## Contributing

We welcome contributions!  
**For now, we are only accepting new medical calculation functions.**

### How to Add a New Calculation

1. **Fork this repository** and clone your fork to your machine.

2. **Create a new branch** for your calculation:

   ```sh
   git checkout -b add/my-new-calculation
   ```

3. **Add your calculation function:**

   - Open `calculations/calculations.py`.
   - Use the `@register_calc("Your Calculation Name")` decorator.
   - Write your function using clear, well-documented Python code.
   - Example:
     ```python
     @register_calc("Body Surface Area")
     def body_surface_area(weight: float, height: float) -> float:
         """
         Calculates the body surface area (BSA) using the Mosteller formula.
         Formula: BSA (m^2) = sqrt([height(cm) x weight(kg)]/3600)
         """
         return ((height * weight) / 3600) ** 0.5
     ```

4. **Add an entry to `data/calculations.json`:**

   - Open `data/calculations.json`.
   - **Find the category** that best fits your calculation (e.g., `"Medical Dosage and Administration"`, `"Patient Monitoring"`, `"Nutrition and Fluid Management"`, etc.).
   - If your calculation fits an existing category, add your calculation object to the `"calculations"` array for that category.
   - **If no suitable category exists,** you may add a new category object (ask a maintainer if unsure).
   - **Example entry:**
     ```json
     {
       "name": "Body Surface Area",
       "description": "Calculates the body surface area (BSA) using the Mosteller formula.",
       "formula": "BSA (m^2) = sqrt([height(cm) x weight(kg)]/3600)",
       "result_unit": "m²",
       "parameters": [
         {
           "name": "weight",
           "description": "Patient's weight",
           "unit": "kg",
           "type": "float"
         },
         {
           "name": "height",
           "description": "Patient's height",
           "unit": "cm",
           "type": "float"
         }
       ]
     }
     ```
   - **Place your entry under the most appropriate category** in the `"categories"` array. For example, if your calculation is about body measurements, add it to the `"Body Mechanisms and Growth"` category.
   - **Make sure the `"name"` matches the one you used in the Python decorator.**
   - **Fields required in each calculation entry:**

     - `name`: The calculation name (must match the Python function decorator).
     - `description`: A short description of what the calculation does.
     - `formula`: The formula used (in plain text).
     - `result_unit`: The unit of the result (e.g., `"mg/dL"`, `"m²"`, `"score"`, etc.).
     - `parameters`: An array of parameter objects, each with:
       - `name`: Parameter name (must match the Python function argument).
       - `description`: Short description of the parameter.
       - `unit`: Unit for the parameter.
       - `type`: `"float"`, `"integer"`, or `"string"` (and optionally `enum` or `options` for choices).

   - **Example of adding to an existing category:**

     ```json
     {
       "title": "Body Mechanisms and Growth",
       "slug": "body-mechanisms-growth",
       "description": "...",
       "calculations": [
         ...existing calculations...,
         {
           "name": "Body Surface Area",
           "description": "Calculates the body surface area (BSA) using the Mosteller formula.",
           "formula": "BSA (m^2) = sqrt([height(cm) x weight(kg)]/3600)",
           "result_unit": "m²",
           "parameters": [
             {"name": "weight", "description": "Patient's weight", "unit": "kg", "type": "float"},
             {"name": "height", "description": "Patient's height", "unit": "cm", "type": "float"}
           ]
         }
       ]
     }
     ```

   - **If you are unsure about the best category,** ask in your Pull Request and a maintainer will help you place it correctly.

5. **(Optional but recommended) Add a docstring**

   - Explain the formula and parameters.

6. **Test your calculation:**

   - If you have a test suite, add a test for your function.
   - Otherwise, you can test it by importing and calling it in a Python shell.

7. **Commit your changes:**

   ```sh
   git add calculations/calculations.py data/calculations.json
   git commit -m "Add Body Surface Area calculation"
   git push origin add/my-new-calculation
   ```

8. **Open a Pull Request (PR):**
   - Go to your fork on GitHub and click "Compare & pull request".
   - In your PR description, include:
     - The calculation name
     - A brief explanation of the formula
     - Example input/output if possible

---

**Note:**  
Both the Python function and the JSON entry are required for your calculation to appear and work in the app.

### Advanced Contribution Rules

- **Add calculation functions only in `calculations/calculations.py`.**
- **Add a corresponding entry for your calculation in `data/calculations.json` under the most appropriate category.** If no suitable category exists, you may propose a new one in your PR.
- Use the `@register_calc` decorator with a unique, descriptive name that matches the `"name"` field in your JSON entry.
- Write clear, readable code and include a docstring with the formula, parameter descriptions, and references if possible.
- Ensure your JSON entry includes all required fields (`name`, `description`, `formula`, `result_unit`, and `parameters`), and that parameter names/types match your Python function.
- Do **not** modify other files unless instructed by a maintainer.
- Do **not** add external dependencies.
- If your calculation is similar to an existing one, explain the difference in your PR.
- All code must pass linting and basic tests (if available).
- Be respectful and constructive in code reviews and discussions.

---

### Reporting Issues

- Use [GitHub Issues](https://github.com/niol08/CLINICALC/issues) to report bugs or request features.
- Please provide as much detail as possible (screenshots, error messages, steps to reproduce).

---

## License

This project is not currently licensed for public use, modification, or redistribution.

If you wish to use or contribute to this project beyond submitting calculation functions, please contact the maintainer for permission or clarification.

---

## Contact

- enioladejo1725@gmail.com
- 19-10aq119@students.unilorin.edu.ng
- [GitHub Repo](https://github.com/niol08/CLINICALC)

---

Thank you for helping make CLNICALC better!
