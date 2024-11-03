

remove

"None","No Uni"
"University","No Uni"
"University Hospital","No Uni"

# Prompt
### Instruction ###
You are given a list of university names in DE (ISO 3166 alpha-2 ). Your task is to:
1. Identify and combine similar names of universities into one english English name.
2. Output the result in this format:  
`"[Original University Name]","[Edited University Name]"`
3. If the Original University Name was not the name of a university, put "No Uni" in the answer.
4. If the Original University Name was the name of the center or a part of the university, you should use the original name of the university without additions.

Ensure each pair is listed on a new line.

### Example ###
- `"Universität München","Munich University"`

### University name list ###

Osnabrück University
Osnabrück University of Applied Sciences
Otto-von-Guericke-Universität Magdeburg
Otto-von-Guericke-University Magdeburg
Otto-von-Guericke University Magdeburg
Otto von Guericke University

