import PyPDF2
import re
from typing import Dict, List, Any

class ResumeParser:
    def __init__(self):
        self.section_patterns = {
            'education': r'(?i)(education|academic|qualification)',
            'experience': r'(?i)(experience|employment|work history)',
            'skills': r'(?i)(skills|technical skills|competencies)',
            'projects': r'(?i)(projects|portfolio)',
            'certifications': r'(?i)(certifications|certificates|licenses)'
        }

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except:
            return ""
        return text

    def extract_hyperlinks(self, pdf_path: str) -> List[str]:
        hyperlinks = []
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    if '/Annots' in page:
                        annotations = page['/Annots']
                        for annotation in annotations:
                            obj = annotation.get_object()
                            if obj.get('/Subtype') == '/Link':
                                if '/A' in obj:
                                    action = obj['/A']
                                    if '/URI' in action:
                                        uri = action['/URI']
                                        hyperlinks.append(str(uri))
        except Exception as e:
            pass
        return hyperlinks

    def parse_resume(self, pdf_path: str) -> Dict[str, Any]:
        text = self.extract_text_from_pdf(pdf_path)
        hyperlinks = self.extract_hyperlinks(pdf_path)

        sections = self._identify_sections(text)
        contact_info = self._extract_contact_info(text, hyperlinks)

        return {
            'raw_text': text,
            'sections': sections,
            'contact_info': contact_info,
            'hyperlinks': hyperlinks
        }

    def _identify_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        lines = text.split('\n')
        current_section = 'summary'
        section_content = []

        for line in lines:
            matched = False
            for section_name, pattern in self.section_patterns.items():
                if re.search(pattern, line):
                    if section_content:
                        sections[current_section] = '\n'.join(section_content)
                    current_section = section_name
                    section_content = []
                    matched = True
                    break

            if not matched:
                section_content.append(line)

        if section_content:
            sections[current_section] = '\n'.join(section_content)

        return sections

    def _extract_contact_info(self, text: str, hyperlinks: List[str] = None) -> Dict[str, str]:
        contact = {}
        hyperlinks = hyperlinks or []

        for link in hyperlinks:
            link_lower = link.lower()

            if 'github.com/' in link_lower:
                github_match = re.search(r'github\.com/([\w-]+)', link, re.IGNORECASE)
                if github_match:
                    contact['github'] = github_match.group(1)
                    contact['github_url'] = link

            if 'linkedin.com/in/' in link_lower:
                linkedin_match = re.search(r'linkedin\.com/in/([\w-]+)', link, re.IGNORECASE)
                if linkedin_match:
                    contact['linkedin'] = linkedin_match.group(1)
                    contact['linkedin_url'] = link

            if 'mailto:' in link_lower:
                email = link.replace('mailto:', '')
                contact['email'] = email

        return contact
