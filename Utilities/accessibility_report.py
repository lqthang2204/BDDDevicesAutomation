import os
import re


def parse_output_data(output_data, out_file_name):
    # Initialize variables to store data
    total_violations = 0
    critical_count = 0
    serious_count = 0
    moderate_count = 0
    minor_count = 0
    critical_elements = ""
    serious_elements = ""
    moderate_elements = ""
    minor_elements = ""

    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Split the output_data by the 'Rule Violated:' lines
    violations = output_data.strip().split("Rule Violated:\n")

    # Remove the first element as it contains the header
    violations.pop(0)

    # Loop through each violation
    for violation in violations:
        # Split each violation by lines
        lines = violation.strip().split('\n')

        # Extract the impact level
        impact_level = None
        for line in lines:
            if line.strip().startswith("Impact Level:"):
                impact_level = line.split(": ")[1]
                break

        # Extract the elements affected
        elements_affected = []
        affected = False
        affected_element_cnt = 0
        for line in lines:
            if affected and line.strip():
                if 'Target:' in line.strip():
                    clean_line = re.sub(r'\d+\)\s+', '', line, flags=re.MULTILINE)
                    elements_affected.append(f'<b>{clean_line.strip()}</b>')
                    affected_element_cnt += 1
                else:
                    elements_affected.append(f'<i>{line.strip()}<i>')
            if line.strip().startswith("Elements Affected:"):
                affected = True

        # Update counts and elements lists based on impact level
        if impact_level:
            total_violations += 1
            if impact_level == "critical":
                critical_count += affected_element_cnt
                critical_elements += "<li>{}</li>".format("</li><li>".join(elements_affected))
            elif impact_level == "serious":
                serious_count += affected_element_cnt
                serious_elements += "<li>{}</li>".format("</li><li>".join(elements_affected))
            elif impact_level == "moderate":
                moderate_count += affected_element_cnt
                moderate_elements += "<li>{}</li>".format("</li><li>".join(elements_affected))
            elif impact_level == "minor":
                minor_count += affected_element_cnt
                minor_elements += "<li>{}</li>".format("</li><li>".join(elements_affected))

    # Read the HTML template
    template_path = os.path.join(project_folder, "resources", "accessibility", "AXE_Main_Template.html")
    with open(template_path, "r") as file:
        html_template = file.read()

    # Fill in the data into the template
    html_report = html_template.format(
        page_name=out_file_name,
        total_count=int(critical_count + serious_count + moderate_count + minor_count),
        critical_count=int(critical_count),
        serious_count=int(serious_count),
        moderate_count=int(moderate_count),
        minor_count=int(minor_count),
        critical_elements=critical_elements.strip() if critical_elements.strip() else 'Critical: None',
        serious_elements=serious_elements.strip() if serious_elements.strip() else 'Serious: None',
        moderate_elements=moderate_elements.strip() if moderate_elements.strip() else 'Moderate: None',
        minor_elements=minor_elements.strip() if minor_elements.strip() else 'Minor: None'
    )

    # Create the target folder if it doesn't exist
    target_folder = os.path.join(project_folder, "target", "accessibility")
    os.makedirs(target_folder, exist_ok=True)

    # Write the HTML report to a file in the target folder
    output_file_path = os.path.join(target_folder, f'{out_file_name}.html')
    with open(output_file_path, "w") as file:
        file.write(html_report)


# Example Usage:
if __name__ == '__main__':
    data = '''Found 8 accessibility violations:

Rule Violated:
color-contrast - Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds
	URL: https://dequeuniversity.com/rules/axe/3.1/color-contrast?application=axeAPI
	Impact Level: serious
	Tags: cat.color wcag2aa wcag143
	Elements Affected:
	1) Target: #Inpatient\ Ward
		Element has insufficient color contrast of 3.83 (foreground color: #007fff, background color: #ffffff, font size: 9.6pt, font weight: normal). Expected contrast ratio of 4.5:1
	2) Target: #Isolation\ Ward
		Element has insufficient color contrast of 3.83 (foreground color: #007fff, background color: #ffffff, font size: 9.6pt, font weight: normal). Expected contrast ratio of 4.5:1
	3) Target: #Laboratory
		Element has insufficient color contrast of 3.83 (foreground color: #007fff, background color: #ffffff, font size: 9.6pt, font weight: normal). Expected contrast ratio of 4.5:1
	4) Target: #Outpatient\ Clinic
		Element has insufficient color contrast of 3.83 (foreground color: #007fff, background color: #ffffff, font size: 9.6pt, font weight: normal). Expected contrast ratio of 4.5:1
	5) Target: #Pharmacy
		Element has insufficient color contrast of 3.83 (foreground color: #007fff, background color: #ffffff, font size: 9.6pt, font weight: normal). Expected contrast ratio of 4.5:1
	6) Target: #Registration\ Desk
		Element has insufficient color contrast of 3.83 (foreground color: #007fff, background color: #ffffff, font size: 9.6pt, font weight: normal). Expected contrast ratio of 4.5:1
	7) Target: #cantLogin
		Element has insufficient color contrast of 3.83 (foreground color: #007fff, background color: #ffffff, font size: 12.0pt, font weight: normal). Expected contrast ratio of 4.5:1

Rule Violated:
duplicate-id - Ensures every id attribute value is unique
	URL: https://dequeuniversity.com/rules/axe/3.1/duplicate-id?application=axeAPI
	Impact Level: minor
	Tags: cat.parsing wcag2a wcag411
	Elements Affected:
	1) Target: .container-fluid
		Document has multiple static elements with the same id attribute

Rule Violated:
html-has-lang - Ensures every HTML document has a lang attribute
	URL: https://dequeuniversity.com/rules/axe/3.1/html-has-lang?application=axeAPI
	Impact Level: serious
	Tags: cat.language wcag2a wcag311
	Elements Affected:
	1) Target: html
		The <html> element does not have a lang attribute

Rule Violated:
image-alt - Ensures <img> elements have alternate text or a role of none or presentation
	URL: https://dequeuniversity.com/rules/axe/3.1/image-alt?application=axeAPI
	Impact Level: critical
	Tags: cat.text-alternatives wcag2a wcag111 section508 section508.22.a
	Elements Affected:
	1) Target: img
		Element does not have an alt attribute
		aria-label attribute does not exist or is empty
		aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		Element has no title attribute or the title attribute is empty
		Element's default semantics were not overridden with role="presentation"
		Element's default semantics were not overridden with role="none"

Rule Violated:
landmark-one-main - Ensures the page has only one main landmark and each iframe in the page has at most one main landmark
	URL: https://dequeuniversity.com/rules/axe/3.1/landmark-one-main?application=axeAPI
	Impact Level: moderate
	Tags: cat.semantics best-practice
	Elements Affected:
	1) Target: html
		Page does not have a main landmark

Rule Violated:
link-name - Ensures links have discernible text
	URL: https://dequeuniversity.com/rules/axe/3.1/link-name?application=axeAPI
	Impact Level: serious
	Tags: cat.name-role-value wcag2a wcag412 wcag244 section508 section508.22.a
	Elements Affected:
	1) Target: .logo > a
		Element does not have text that is visible to screen readers
		aria-label attribute does not exist or is empty
		aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		Element's default semantics were not overridden with role="presentation"
		Element's default semantics were not overridden with role="none"
		Element is in tab order and does not have accessible text

Rule Violated:
page-has-heading-one - Ensure that the page, or at least one of its frames contains a level-one heading
	URL: https://dequeuniversity.com/rules/axe/3.1/page-has-heading-one?application=axeAPI
	Impact Level: moderate
	Tags: cat.semantics best-practice
	Elements Affected:
	1) Target: html
		Page must have a level-one heading

Rule Violated:
region - Ensures all page content is contained by landmarks
	URL: https://dequeuniversity.com/rules/axe/3.1/region?application=axeAPI
	Impact Level: moderate
	Tags: cat.keyboard best-practice
	Elements Affected:
	1) Target: html
		Some page content is not contained by landmarks'''

    parse_output_data(output_data=data, out_file_name="adfadf")
