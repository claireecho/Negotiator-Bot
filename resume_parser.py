"""
Resume Parser for Negotiator Bot
Extracts key information from uploaded resumes to enhance negotiation context
"""

import os
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import PyPDF2
from docx import Document
import pandas as pd

@dataclass
class ResumeData:
    """Structured resume data"""
    name: str
    email: str
    phone: str
    years_experience: int
    current_title: str
    current_company: str
    skills: List[str]
    education: List[str]
    experience: List[Dict[str, Any]]
    achievements: List[str]
    certifications: List[str]
    languages: List[str]
    summary: str

class ResumeParser:
    """Parse resumes from various formats (PDF, DOCX, TXT)"""
    
    def __init__(self):
        self.skill_keywords = {
            'programming': ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'php', 'ruby', 'scala'],
            'web_dev': ['react', 'angular', 'vue', 'node.js', 'django', 'flask', 'express', 'spring', 'laravel', 'rails'],
            'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn', 'r', 'sql', 'spark'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb'],
            'mobile': ['ios', 'android', 'react native', 'flutter', 'xamarin', 'swift', 'kotlin'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'git', 'linux', 'bash', 'ansible', 'terraform'],
            'design': ['figma', 'sketch', 'adobe', 'photoshop', 'illustrator', 'ui/ux', 'wireframing'],
            'management': ['project management', 'agile', 'scrum', 'leadership', 'team management', 'product management'],
            'analytics': ['tableau', 'power bi', 'excel', 'sql', 'statistics', 'data analysis', 'business intelligence']
        }
        
        self.experience_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4}|\bpresent\b|\bcurrent\b)',
            r'(\d{4})\s*[-–]\s*(\d{4}|\bpresent\b|\bcurrent\b)',
            r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4}|\bpresent\b|\bcurrent\b)',
        ]
        
        self.title_patterns = [
            r'(software engineer|developer|programmer|architect)',
            r'(data scientist|data analyst|ml engineer)',
            r'(product manager|project manager|scrum master)',
            r'(devops engineer|sre|platform engineer)',
            r'(frontend|backend|full stack)',
            r'(senior|lead|principal|staff)',
            r'(manager|director|vp|cto)'
        ]

    def parse_resume(self, file_path: str, file_type: str) -> ResumeData:
        """Parse resume from file"""
        try:
            if file_type.lower() == 'pdf':
                text = self._extract_pdf_text(file_path)
            elif file_type.lower() in ['docx', 'doc']:
                text = self._extract_docx_text(file_path)
            elif file_type.lower() == 'txt':
                text = self._extract_txt_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            return self._parse_text(text)
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")

    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _parse_text(self, text: str) -> ResumeData:
        """Parse text content to extract resume data"""
        lines = text.split('\n')
        text_lower = text.lower()
        
        # Extract basic information
        name = self._extract_name(lines)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        
        # Extract experience information
        years_experience = self._extract_years_experience(text)
        current_title, current_company = self._extract_current_position(text)
        
        # Extract skills
        skills = self._extract_skills(text_lower)
        
        # Extract education
        education = self._extract_education(text)
        
        # Extract work experience
        experience = self._extract_experience(text)
        
        # Extract achievements
        achievements = self._extract_achievements(text)
        
        # Extract certifications
        certifications = self._extract_certifications(text)
        
        # Extract languages
        languages = self._extract_languages(text)
        
        # Generate summary
        summary = self._generate_summary(name, years_experience, current_title, skills, achievements)
        
        return ResumeData(
            name=name,
            email=email,
            phone=phone,
            years_experience=years_experience,
            current_title=current_title,
            current_company=current_company,
            skills=skills,
            education=education,
            experience=experience,
            achievements=achievements,
            certifications=certifications,
            languages=languages,
            summary=summary
        )

    def _extract_name(self, lines: List[str]) -> str:
        """Extract name from resume (usually first line or first few lines)"""
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 2 and not any(char.isdigit() for char in line):
                # Check if it looks like a name (has spaces, no special chars)
                if ' ' in line and len(line.split()) <= 4:
                    return line
        return "Unknown"

    def _extract_email(self, text: str) -> str:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group() if match else ""

    def _extract_phone(self, text: str) -> str:
        """Extract phone number"""
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+1[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        return ""

    def _extract_years_experience(self, text: str) -> int:
        """Extract years of experience"""
        # Look for patterns like "5 years", "5+ years", "5 years of experience"
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*in\s*(?:software|development|engineering|technology)',
            r'(\d+)\+?\s*years?\s*working\s*(?:with|in)',
            r'(\d+)\+?\s*years?\s*of\s*(?:professional|relevant)\s*experience',
            r'(\d+)\+?\s*years?\s*in\s*(?:the\s*)?(?:tech|software|IT)\s*industry',
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                # Return the highest number found
                years = [int(match) for match in matches]
                return max(years)
        
        # Calculate from work experience dates
        experience_entries = self._extract_experience(text)
        if experience_entries:
            total_years = 0
            for entry in experience_entries:
                duration = entry.get('duration', '')
                years = self._calculate_duration_years(duration)
                total_years += years
            return min(int(total_years), 20)  # Cap at 20 years
        
        return 0

    def _calculate_duration_years(self, duration: str) -> float:
        """Calculate years from duration string"""
        if not duration:
            return 0
        
        # Look for year patterns
        year_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4})',  # 2020 - 2022
            r'(\d{4})\s*[-–]\s*(?:present|current|now)',  # 2020 - present
            r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4})',  # Jan 2020 - Dec 2022
            r'(\w+\s+\d{4})\s*[-–]\s*(?:present|current|now)',  # Jan 2020 - present
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, duration.lower())
            if match:
                start = match.group(1)
                end = match.group(2) if len(match.groups()) > 1 else "present"
                
                # Extract year from start
                start_year = re.search(r'\d{4}', start)
                if start_year:
                    start_year = int(start_year.group())
                else:
                    continue
                
                # Extract year from end
                if end.lower() in ['present', 'current', 'now']:
                    from datetime import datetime
                    end_year = datetime.now().year
                else:
                    end_year_match = re.search(r'\d{4}', end)
                    if end_year_match:
                        end_year = int(end_year_match.group())
                    else:
                        continue
                
                return max(0, end_year - start_year)
        
        return 0

    def _extract_current_position(self, text: str) -> tuple:
        """Extract current job title and company"""
        # Look for current/present positions
        current_patterns = [
            r'(?:current|present).*?(?:title|position|role)[:\s]*([^,\n]+)',
            r'(?:current|present).*?at\s+([^,\n]+)',
            r'([^,\n]+)\s*\(current\)',
            r'([^,\n]+)\s*\(present\)'
        ]
        
        for pattern in current_patterns:
            match = re.search(pattern, text.lower())
            if match:
                position = match.group(1).strip()
                # Try to separate title and company
                if ' at ' in position:
                    parts = position.split(' at ', 1)
                    return parts[0].strip(), parts[1].strip()
                return position, ""
        
        return "Unknown", "Unknown"

    def _extract_skills(self, text_lower: str) -> List[str]:
        """Extract technical skills"""
        skills = []
        
        for category, skill_list in self.skill_keywords.items():
            for skill in skill_list:
                if skill in text_lower:
                    skills.append(skill.title())
        
        # Remove duplicates and return
        return list(set(skills))

    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        education_keywords = ['university', 'college', 'bachelor', 'master', 'phd', 'degree', 'certificate']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                education.append(line.strip())
        
        return education[:5]  # Limit to 5 entries

    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience entries"""
        experience = []
        
        # Split text into sections
        sections = re.split(r'\n\s*\n', text)
        
        for section in sections:
            if any(keyword in section.lower() for keyword in ['experience', 'employment', 'work history']):
                # Look for job entries in this section
                lines = section.split('\n')
                current_job = {}
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Check if this looks like a job title
                    if any(title in line.lower() for title in ['engineer', 'developer', 'manager', 'analyst', 'consultant']):
                        if current_job:
                            experience.append(current_job)
                        current_job = {'title': line, 'company': '', 'duration': ''}
                    elif current_job and not current_job.get('company'):
                        current_job['company'] = line
                    elif current_job and not current_job.get('duration'):
                        # Check if line contains dates
                        if re.search(r'\d{4}', line):
                            current_job['duration'] = line
                
                if current_job:
                    experience.append(current_job)
        
        return experience[:10]  # Limit to 10 entries

    def _extract_achievements(self, text: str) -> List[str]:
        """Extract achievements and accomplishments"""
        achievements = []
        achievement_keywords = ['achieved', 'increased', 'improved', 'reduced', 'led', 'managed', 'delivered', 'implemented']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in achievement_keywords):
                if len(line.strip()) > 10:  # Filter out very short lines
                    achievements.append(line.strip())
        
        return achievements[:10]  # Limit to 10 entries

    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        cert_keywords = ['certified', 'certification', 'certificate', 'aws', 'azure', 'gcp', 'pmp', 'scrum', 'agile']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in cert_keywords):
                certifications.append(line.strip())
        
        return certifications[:5]  # Limit to 5 entries

    def _extract_languages(self, text: str) -> List[str]:
        """Extract programming languages and spoken languages"""
        languages = []
        language_keywords = ['english', 'spanish', 'french', 'german', 'chinese', 'japanese', 'korean']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in language_keywords):
                languages.append(line.strip())
        
        return languages[:5]  # Limit to 5 entries

    def _generate_summary(self, name: str, years_experience: int, current_title: str, skills: List[str], achievements: List[str]) -> str:
        """Generate a professional summary"""
        summary_parts = []
        
        if name != "Unknown":
            summary_parts.append(f"{name} is a")
        else:
            summary_parts.append("This candidate is a")
        
        if years_experience > 0:
            summary_parts.append(f"{years_experience}-year experienced")
        
        if current_title != "Unknown":
            summary_parts.append(current_title)
        else:
            summary_parts.append("professional")
        
        if skills:
            top_skills = skills[:5]
            summary_parts.append(f"with expertise in {', '.join(top_skills)}")
        
        if achievements:
            summary_parts.append("and a proven track record of delivering results")
        
        return " ".join(summary_parts) + "."

    def get_negotiation_context(self, resume_data: ResumeData) -> Dict[str, Any]:
        """Convert resume data to negotiation context format"""
        return {
            "name": resume_data.name,
            "years_experience": resume_data.years_experience,
            "current_title": resume_data.current_title,
            "current_company": resume_data.current_company,
            "primary_skill": resume_data.skills[0] if resume_data.skills else "software development",
            "industry": self._infer_industry(resume_data),
            "key_achievement": resume_data.achievements[0] if resume_data.achievements else "delivering exceptional results",
            "education": resume_data.education[0] if resume_data.education else "Bachelor's degree",
            "certifications": resume_data.certifications,
            "languages": resume_data.languages,
            "summary": resume_data.summary,
            "skills": resume_data.skills,
            "experience": resume_data.experience
        }

    def _infer_industry(self, resume_data: ResumeData) -> str:
        """Infer industry from resume data"""
        text = " ".join(resume_data.skills + [resume_data.current_title] + resume_data.achievements).lower()
        
        if any(keyword in text for keyword in ['fintech', 'banking', 'finance', 'trading', 'investment']):
            return "finance"
        elif any(keyword in text for keyword in ['healthcare', 'medical', 'pharma', 'biotech']):
            return "healthcare"
        elif any(keyword in text for keyword in ['ecommerce', 'retail', 'shopping', 'marketplace']):
            return "retail"
        elif any(keyword in text for keyword in ['media', 'entertainment', 'gaming', 'streaming']):
            return "media"
        elif any(keyword in text for keyword in ['automotive', 'car', 'vehicle', 'transportation']):
            return "automotive"
        elif any(keyword in text for keyword in ['consulting', 'advisory', 'strategy']):
            return "consulting"
        else:
            return "technology"

# Example usage
if __name__ == "__main__":
    parser = ResumeParser()
    
    # Test with sample data
    sample_text = """
    John Smith
    john.smith@email.com
    (555) 123-4567
    
    Software Engineer with 5 years of experience
    Current: Senior Software Engineer at TechCorp
    
    Skills: Python, JavaScript, React, AWS, Docker
    Education: Bachelor's in Computer Science from MIT
    
    Experience:
    - Senior Software Engineer at TechCorp (2020-Present)
    - Software Engineer at StartupXYZ (2018-2020)
    
    Achievements:
    - Led team of 5 developers
    - Increased system performance by 40%
    - Implemented CI/CD pipeline
    """
    
    # This would be used with actual file parsing
    print("Resume parser ready for use!")
