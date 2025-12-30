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
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
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
            
            if link_lower.startswith('http') and 'github' not in link_lower and 'linkedin' not in link_lower:
                if 'portfolio_links' not in contact:
                    contact['portfolio_links'] = []
                contact['portfolio_links'].append(link)
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails and 'email' not in contact:
            contact['email'] = emails[0]
        
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact['phone'] = phones[0]
        
        if 'github' not in contact:
            github_pattern = r'github\.com/([\w-]+)'
            github_matches = re.findall(github_pattern, text, re.IGNORECASE)
            if github_matches:
                contact['github'] = github_matches[0]
                contact['github_url'] = f'https://github.com/{github_matches[0]}'
        
        if 'linkedin' not in contact:
            linkedin_pattern = r'linkedin\.com/in/([\w-]+)'
            linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
            if linkedin_matches:
                contact['linkedin'] = linkedin_matches[0]
                contact['linkedin_url'] = f'https://linkedin.com/in/{linkedin_matches[0]}'
        
        return contact
