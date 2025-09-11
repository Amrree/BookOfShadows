"""
Safety and ethics management for Book of Shadows - The Crone
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)

class SafetyLevel(Enum):
    """Safety levels for content."""
    SAFE = "safe"
    WARNING = "warning"
    DANGEROUS = "dangerous"
    PROHIBITED = "prohibited"

class ContentType(Enum):
    """Types of content being checked."""
    COMMAND = "command"
    TEXT = "text"
    RITUAL = "ritual"
    INGREDIENT = "ingredient"
    CITATION = "citation"

class SafetyManager:
    """Manages safety checks and ethics validation."""
    
    def __init__(self):
        """Initialize safety manager."""
        self.prohibited_keywords = [
            "poison", "poisonous", "toxic", "lethal", "deadly",
            "explosive", "bomb", "detonate", "incendiary",
            "weapon", "knife", "gun", "blade", "sharp",
            "self-harm", "suicide", "kill", "murder", "violence",
            "illegal", "drug", "narcotic", "controlled substance",
            "biological weapon", "chemical weapon", "radioactive"
        ]
        
        self.cultural_sensitive_terms = [
            "sacred", "secret", "restricted", "initiation",
            "ceremony", "ritual", "tradition", "ancestral"
        ]
        
        self.medical_terms = [
            "diagnosis", "treatment", "medicine", "cure",
            "therapy", "medical", "clinical", "prescription"
        ]
    
    async def initialize(self):
        """Initialize safety manager."""
        logger.info("Initializing safety manager")
        # Load any additional safety rules or patterns
        pass
    
    async def check_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Check if a command is safe to execute."""
        logger.debug(f"Safety checking command: {command}")
        
        # Check for prohibited keywords
        prohibited_found = self._check_prohibited_keywords(command)
        if prohibited_found:
            return {
                'safe': False,
                'level': SafetyLevel.PROHIBITED,
                'reason': f"Command contains prohibited content: {prohibited_found}",
                'suggestion': "Please rephrase your request without dangerous content"
            }
        
        # Check for cultural sensitivity
        cultural_issues = self._check_cultural_sensitivity(command)
        if cultural_issues:
            return {
                'safe': True,
                'level': SafetyLevel.WARNING,
                'reason': f"Cultural sensitivity concerns: {cultural_issues}",
                'suggestion': "Consider consulting with community representatives"
            }
        
        return {
            'safe': True,
            'level': SafetyLevel.SAFE,
            'reason': "Command appears safe"
        }
    
    async def check_text(self, text: str, content_type: ContentType = ContentType.TEXT) -> Dict[str, Any]:
        """Check if text content is safe."""
        logger.debug(f"Safety checking text of type: {content_type}")
        
        # Check for prohibited keywords
        prohibited_found = self._check_prohibited_keywords(text)
        if prohibited_found:
            return {
                'safe': False,
                'level': SafetyLevel.PROHIBITED,
                'reason': f"Text contains prohibited content: {prohibited_found}",
                'flagged_content': prohibited_found
            }
        
        # Check for medical claims
        medical_claims = self._check_medical_claims(text)
        if medical_claims:
            return {
                'safe': False,
                'level': SafetyLevel.DANGEROUS,
                'reason': f"Text contains medical claims: {medical_claims}",
                'suggestion': "Medical advice should be provided by licensed professionals"
            }
        
        # Check for cultural sensitivity
        cultural_issues = self._check_cultural_sensitivity(text)
        if cultural_issues:
            return {
                'safe': True,
                'level': SafetyLevel.WARNING,
                'reason': f"Cultural sensitivity concerns: {cultural_issues}",
                'suggestion': "Consider cultural context and permissions"
            }
        
        return {
            'safe': True,
            'level': SafetyLevel.SAFE,
            'reason': "Text appears safe"
        }
    
    async def check_ritual(self, ritual_text: str) -> Dict[str, Any]:
        """Check if ritual content is safe."""
        logger.debug("Safety checking ritual content")
        
        # Check for dangerous ingredients or procedures
        dangerous_procedures = self._check_dangerous_procedures(ritual_text)
        if dangerous_procedures:
            return {
                'safe': False,
                'level': SafetyLevel.DANGEROUS,
                'reason': f"Ritual contains dangerous procedures: {dangerous_procedures}",
                'suggestion': "Consider symbolic alternatives or historical context only"
            }
        
        # Check for efficacy claims
        efficacy_claims = self._check_efficacy_claims(ritual_text)
        if efficacy_claims:
            return {
                'safe': True,
                'level': SafetyLevel.WARNING,
                'reason': f"Ritual contains efficacy claims: {efficacy_claims}",
                'suggestion': "Ensure claims are marked as UNVERIFIABLE_SUPERNATURAL"
            }
        
        # General text check
        return await self.check_text(ritual_text, ContentType.RITUAL)
    
    async def check_ingredient(self, ingredient: str) -> Dict[str, Any]:
        """Check if ingredient is safe to include."""
        logger.debug(f"Safety checking ingredient: {ingredient}")
        
        # Check for hazardous substances
        hazardous = self._check_hazardous_substances(ingredient)
        if hazardous:
            return {
                'safe': False,
                'level': SafetyLevel.DANGEROUS,
                'reason': f"Ingredient is hazardous: {hazardous}",
                'suggestion': "Provide historical context only, no operational details"
            }
        
        # Check for legal restrictions
        legal_issues = self._check_legal_restrictions(ingredient)
        if legal_issues:
            return {
                'safe': True,
                'level': SafetyLevel.WARNING,
                'reason': f"Ingredient has legal restrictions: {legal_issues}",
                'suggestion': "Include legal warnings and sourcing disclaimers"
            }
        
        return {
            'safe': True,
            'level': SafetyLevel.SAFE,
            'reason': "Ingredient appears safe"
        }
    
    def _check_prohibited_keywords(self, text: str) -> List[str]:
        """Check for prohibited keywords in text."""
        found = []
        text_lower = text.lower()
        
        for keyword in self.prohibited_keywords:
            if keyword in text_lower:
                found.append(keyword)
        
        return found
    
    def _check_cultural_sensitivity(self, text: str) -> List[str]:
        """Check for cultural sensitivity issues."""
        found = []
        text_lower = text.lower()
        
        for term in self.cultural_sensitive_terms:
            if term in text_lower:
                found.append(term)
        
        return found
    
    def _check_medical_claims(self, text: str) -> List[str]:
        """Check for medical claims."""
        found = []
        text_lower = text.lower()
        
        for term in self.medical_terms:
            if term in text_lower:
                found.append(term)
        
        return found
    
    def _check_dangerous_procedures(self, text: str) -> List[str]:
        """Check for dangerous procedures in rituals."""
        dangerous_patterns = [
            r"ingest\s+\w+",  # ingestion instructions
            r"inject\s+\w+",  # injection instructions
            r"burn\s+\w+",    # burning instructions
            r"mix\s+\w+\s+with\s+\w+",  # mixing instructions
        ]
        
        found = []
        for pattern in dangerous_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                found.extend(matches)
        
        return found
    
    def _check_efficacy_claims(self, text: str) -> List[str]:
        """Check for efficacy claims."""
        efficacy_patterns = [
            r"will\s+\w+",     # "will cause"
            r"guaranteed\s+\w+",  # "guaranteed to"
            r"certain\s+\w+",  # "certain to"
            r"proven\s+\w+",   # "proven to"
        ]
        
        found = []
        for pattern in efficacy_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                found.extend(matches)
        
        return found
    
    def _check_hazardous_substances(self, ingredient: str) -> List[str]:
        """Check for hazardous substances."""
        hazardous_substances = [
            "mercury", "lead", "arsenic", "cyanide", "strychnine",
            "chlorine", "ammonia", "bleach", "acid", "alkali",
            "radioactive", "toxic", "poisonous", "corrosive"
        ]
        
        found = []
        ingredient_lower = ingredient.lower()
        
        for substance in hazardous_substances:
            if substance in ingredient_lower:
                found.append(substance)
        
        return found
    
    def _check_legal_restrictions(self, ingredient: str) -> List[str]:
        """Check for legal restrictions."""
        restricted_substances = [
            "controlled substance", "schedule", "prescription",
            "illegal", "prohibited", "restricted"
        ]
        
        found = []
        ingredient_lower = ingredient.lower()
        
        for substance in restricted_substances:
            if substance in ingredient_lower:
                found.append(substance)
        
        return found
    
    async def cleanup(self):
        """Clean up safety manager resources."""
        logger.info("Cleaning up safety manager")