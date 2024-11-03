
# Prompt

### Instruction ###
Convert the following affiliation text into a **structured JSON format** by extracting its components: **country (ISO 3166-1 alpha-2 format), university, institute, department, city, postal code, and email**. Follow these rules:

1. **Standardize country** to the **ISO 3166-1 alpha-2** format.
2. **Format university names** in a complete, formal style (e.g., “Univ.” to “University”).
3. **Extract institutes** (which may be part of the university or independent, e.g., a company).
4. **Extract department** (a part of either the university or the institute).
5. **Ensure postal codes and cities** are extracted clearly and concisely.
6. **Correct abbreviations** (e.g., "Univ.", "Dept.") into full standard forms.
7. **Only return the JSON** output with no additional comments or information.

### Example Input ###
**Affiliation**: "INSERM, U729, Paris, F-75006 France. David.Ouagne@spim.jussieu.fr"

### Example Output (JSON) ###

  "country": "FR",
  "institute": "INSERM",
  "department": "U729",
  "university": null,
  "city": "Paris",
  "postalcode": "75006",
  "email": "David.Ouagne@spim.jussieu.fr"


### Affiliation ###
{Affiliation}
