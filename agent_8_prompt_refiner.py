"""
AGENT 8: PROMPT REFINER & VALIDATOR
Video Generation Quality Assurance System
Deployment: Google Cloud / Vertex AI
Stand: 12. November 2025
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ValidationScores:
    """Holds all validation layer scores"""
    structural: float
    genre_compliance: float
    artifact_risk: float
    consistency: float
    performance_optimization: float

    @property
    def overall_quality_score(self) -> float:
        """Calculate weighted overall score"""
        return (
            self.structural * 0.25 +
            self.genre_compliance * 0.25 +
            self.artifact_risk * 0.30 +
            self.consistency * 0.15 +
            self.performance_optimization * 0.05
        )

@dataclass
class Issue:
    """Represents a validation issue"""
    severity: str  # critical, warning, info
    layer: str     # structural, genre, artifact, consistency
    message: str
    original: str
    suggestion: str

@dataclass
class FixApplied:
    """Represents an auto-fix that was applied"""
    fix_type: str
    original: str
    fixed_to: str
    reason: str
    confidence: float

@dataclass
class ValidationReport:
    """Complete validation report"""
    prompt_type: str  # veo_3.1, runway_gen4
    genre_detected: str
    original_prompt: str
    refined_prompt: str
    validation_scores: ValidationScores
    issues_found: List[Issue]
    auto_fixes_applied: List[FixApplied]
    recommendations: List[str]
    ready_for_generation: bool
    generation_mode_recommendation: str
    estimated_quality_rating: float
    timestamp: str

    def to_json(self) -> str:
        """Convert to JSON output"""
        return json.dumps({
            "prompt_type": self.prompt_type,
            "genre_detected": self.genre_detected,
            "original_prompt": self.original_prompt,
            "refined_prompt": self.refined_prompt,
            "validation_scores": {
                "structural": self.validation_scores.structural,
                "genre_compliance": self.validation_scores.genre_compliance,
                "artifact_risk": self.validation_scores.artifact_risk,
                "consistency": self.validation_scores.consistency,
                "performance_optimization": self.validation_scores.performance_optimization,
                "overall_quality_score": self.validation_scores.overall_quality_score
            },
            "issues_found": [
                {
                    "severity": i.severity,
                    "layer": i.layer,
                    "message": i.message,
                    "original": i.original,
                    "suggestion": i.suggestion
                }
                for i in self.issues_found
            ],
            "auto_fixes_applied": [
                {
                    "fix_type": f.fix_type,
                    "original": f.original,
                    "fixed_to": f.fixed_to,
                    "reason": f.reason,
                    "confidence": f.confidence
                }
                for f in self.auto_fixes_applied
            ],
            "recommendations": self.recommendations,
            "ready_for_generation": self.ready_for_generation,
            "generation_mode_recommendation": self.generation_mode_recommendation,
            "estimated_quality_rating": self.estimated_quality_rating,
            "timestamp": self.timestamp
        }, indent=2, ensure_ascii=False)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN AGENT CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Agent8PromptRefiner:
    """Agent 8: Prompt Refiner & Validator"""

    def __init__(self, config_path: str = "config_agent8.json"):
        """Initialize with config file"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # Build genre lookup
        self.genres_by_id = {g["id"]: g for g in self.config["genres"]}
        self.genres_by_alias = {}
        for g in self.config["genres"]:
            for alias in g["aliases"]:
                self.genres_by_alias[alias.lower()] = g

    def validate_and_refine(self, prompt: str, prompt_type: str, genre: str = None) -> ValidationReport:
        """Main validation and refinement process"""

        # Step 1: Detect genre if not provided
        if not genre:
            genre = self.detect_genre(prompt)

        genre_config = self.genres_by_id.get(genre) or self.genres_by_alias.get(genre.lower())
        if not genre_config:
            genre_config = self.genres_by_id["pop"]  # Fallback

        # Step 2: Structural validation
        structural_score = self.validate_structure(prompt, prompt_type)

        # Step 3: Genre compliance
        genre_score = self.validate_genre_compliance(prompt, genre_config, prompt_type)

        # Step 4: Artifact detection
        artifacts_score, artifact_issues = self.detect_artifacts(prompt, prompt_type, genre_config)

        # Step 5: Consistency check
        consistency_score = self.validate_consistency(prompt)

        # Step 6: Performance optimization
        performance_score = self.validate_performance(prompt, prompt_type)

        # Step 7: Auto-fix
        refined_prompt, fixes_applied = self.apply_auto_fixes(
            prompt, prompt_type, genre_config, artifact_issues
        )

        # Step 8: Calculate overall score
        scores = ValidationScores(
            structural=structural_score,
            genre_compliance=genre_score,
            artifact_risk=artifacts_score,
            consistency=consistency_score,
            performance_optimization=performance_score
        )

        # Step 9: Determine readiness
        ready = (scores.overall_quality_score > 0.75 and
                 not any(i.severity == "critical" for i in artifact_issues))

        # Step 10: Mode recommendation
        mode_rec = self.recommend_generation_mode(scores, prompt_type, genre_config)

        # Step 11: Generate recommendations
        recommendations = self.generate_recommendations(artifact_issues, scores)

        # Create report
        report = ValidationReport(
            prompt_type=prompt_type,
            genre_detected=genre_config["id"],
            original_prompt=prompt,
            refined_prompt=refined_prompt,
            validation_scores=scores,
            issues_found=artifact_issues,
            auto_fixes_applied=fixes_applied,
            recommendations=recommendations,
            ready_for_generation=ready,
            generation_mode_recommendation=mode_rec,
            estimated_quality_rating=min(5.0, scores.overall_quality_score * 5),
            timestamp=datetime.now().isoformat()
        )

        return report

    def detect_genre(self, prompt: str) -> str:
        """Auto-detect genre from prompt content"""
        prompt_lower = prompt.lower()

        for genre in self.config["genres"]:
            for alias in genre["aliases"]:
                if alias.lower() in prompt_lower:
                    return genre["id"]

        return "pop"  # Fallback

    def validate_structure(self, prompt: str, prompt_type: str) -> float:
        """Layer 1: Structural validation"""
        score = 1.0

        if prompt_type == "veo_3.1":
            # Check for 6 layers
            layers = ["IDENTITY", "CINEMATOGRAPHY", "ENVIRONMENT", "PERFORMANCE", "AUDIO", "NEGATIVES"]
            found_layers = sum(1 for layer in layers if layer in prompt.upper())
            score *= (found_layers / 6.0)

            # Check word count (75-150)
            word_count = len(prompt.split())
            if 75 <= word_count <= 150:
                score *= 1.0
            elif 50 <= word_count <= 200:
                score *= 0.9
            else:
                score *= 0.7

        elif prompt_type == "runway_gen4":
            # Check motion focus (no excessive visual description)
            visual_words = len(re.findall(r'\b(color|texture|style|aesthetic|looks)\b', prompt, re.I))
            motion_words = len(re.findall(r'\b(moves|walks|pans|tracks|dolly|zoom)\b', prompt, re.I))

            if motion_words > visual_words:
                score *= 1.0
            else:
                score *= 0.8

            # Check word count (50-100)
            word_count = len(prompt.split())
            if 50 <= word_count <= 100:
                score *= 1.0
            elif 40 <= word_count <= 120:
                score *= 0.9
            else:
                score *= 0.7

        return max(0.0, min(1.0, score))

    def validate_genre_compliance(self, prompt: str, genre_config: Dict, prompt_type: str) -> float:
        """Layer 2: Genre-specific parameter validation"""
        score = 0.7  # Base score

        # Check for genre-specific keywords
        genre_id = genre_config["id"]
        prompt_lower = prompt.lower()

        # This is simplified; in production would check more thoroughly
        if any(alias in prompt_lower for alias in genre_config["aliases"]):
            score += 0.2

        # Check for genre-appropriate language
        if genre_id == "reggaeton":
            warm_keywords = ["warm", "golden", "amber", "tropical"]
            if any(k in prompt_lower for k in warm_keywords):
                score += 0.1

        elif genre_id == "edm":
            energy_keywords = ["neon", "bright", "dynamic", "energetic", "electric"]
            if any(k in prompt_lower for k in energy_keywords):
                score += 0.1

        return max(0.0, min(1.0, score))

    def detect_artifacts(self, prompt: str, prompt_type: str, genre_config: Dict) -> Tuple[float, List[Issue]]:
        """Layer 3: Artifact detection (most critical)"""
        issues = []
        score = 1.0

        if prompt_type == "veo_3.1":
            # Check dialog length
            dialogue_lines = re.findall(r'Dialogue:\s*"([^"]+)"', prompt, re.I)
            for line in dialogue_lines:
                word_count = len(line.split())
                if word_count > genre_config.get("dialog_max_words", 7):
                    issues.append(Issue(
                        severity="critical",
                        layer="artifact",
                        message=f"Dialog exceeds {genre_config.get('dialog_max_words')} words",
                        original=line,
                        suggestion=f"Reduce to max {genre_config.get('dialog_max_words')} words"
                    ))
                    score -= 0.15

            # Check for conflicting lighting
            if re.search(r'\b(sunlight|daylight|bright)\b', prompt, re.I) and \
               re.search(r'\b(night|dark|shadow)\b', prompt, re.I):
                issues.append(Issue(
                    severity="critical",
                    layer="artifact",
                    message="Conflicting lighting (day and night)",
                    original="prompt has both daylight and night references",
                    suggestion="Choose either golden hour OR night lighting, not both"
                ))
                score -= 0.2

            # Check for too many negatives (should have some!)
            if "NEGATIVES" not in prompt or len(re.findall(r',\s*no\s+', prompt, re.I)) < 3:
                issues.append(Issue(
                    severity="warning",
                    layer="artifact",
                    message="Missing or insufficient negative prompts",
                    original="No/few negative prompts",
                    suggestion="Add at least 3 negative prompts (warping, floating limbs, etc)"
                ))
                score -= 0.1

        elif prompt_type == "runway_gen4":
            # Check for artsy language
            artsy_terms = ["ethereal", "dreamlike", "whimsical", "mystical", "surreal"]
            found_artsy = [t for t in artsy_terms if t in prompt.lower()]
            if found_artsy:
                issues.append(Issue(
                    severity="warning",
                    layer="artifact",
                    message=f"Artsy language detected: {', '.join(found_artsy)}",
                    original=f"prompt contains: {found_artsy}",
                    suggestion="Replace with concrete terms (soft-focused, blurred, etc)"
                ))
                score -= 0.1

            # Check for prompt length with clear image
            word_count = len(prompt.split())
            if word_count > 100:
                issues.append(Issue(
                    severity="info",
                    layer="artifact",
                    message="Prompt longer than 100 words (when image is clear)",
                    original=f"{word_count} words",
                    suggestion="Trim to 50-80 words (image provides visuals)"
                ))
                score -= 0.05

        return max(0.0, min(1.0, score)), issues

    def validate_consistency(self, prompt: str) -> float:
        """Layer 4: Consistency checks"""
        score = 0.8  # Default good

        # Check for repeated character descriptions
        if prompt.count("woman") + prompt.count("man") + prompt.count("character") > 1:
            score += 0.15  # Good sign of consistency

        # Check for "continues" keywords (multi-shot continuity)
        if "continues" in prompt.lower():
            score += 0.05

        return min(1.0, score)

    def validate_performance(self, prompt: str, prompt_type: str) -> float:
        """Layer 5: Performance optimization"""
        score = 0.8

        # Check for reference image mentions
        if "reference" in prompt.lower() or "image" in prompt.lower():
            score += 0.1

        # Check for explicit duration
        if re.search(r'\b(4|6|8|5|10)\s*second', prompt, re.I):
            score += 0.1

        return min(1.0, score)

    def apply_auto_fixes(self, prompt: str, prompt_type: str, genre_config: Dict, issues: List[Issue]) -> Tuple[str, List[FixApplied]]:
        """Step 7: Apply automatic fixes"""
        refined = prompt
        fixes = []

        for issue in issues:
            if prompt_type == "veo_3.1":
                if issue.message.startswith("Dialog exceeds"):
                    # Fix: Trim dialog
                    old = refined
                    refined = re.sub(
                        r'Dialogue:\s*"([^"]+)"',
                        lambda m: f'Dialogue: "{" ".join(m.group(1).split()[:genre_config["dialog_max_words"]])"',
                        refined
                    )
                    if old != refined:
                        fixes.append(FixApplied(
                            fix_type="too_long_dialog",
                            original=issue.original,
                            fixed_to=refined,
                            reason="VEO 3.1 Lip-sync requirement",
                            confidence=0.95
                        ))

                elif "Missing" in issue.message and "negative" in issue.message:
                    # Fix: Add base negatives + genre-specific
                    if "[NEGATIVES]" not in refined and "NEGATIVES" not in refined:
                        negatives_section = f"\n\n[NEGATIVES]\n{', '.join(genre_config['auto_negatives'])}"
                        refined += negatives_section
                        fixes.append(FixApplied(
                            fix_type="missing_negatives",
                            original="(missing)",
                            fixed_to=negatives_section,
                            reason=f"Added genre-specific negatives for {genre_config['id']}",
                            confidence=0.95
                        ))

            elif prompt_type == "runway_gen4":
                if "Artsy language detected" in issue.message:
                    # Fix: Replace artsy terms
                    replacements = {
                        "ethereal": "soft-focused",
                        "dreamlike": "blurred, hazy",
                        "whimsical": "playful, animated",
                        "mystical": "atmospheric, moody"
                    }
                    for artsy, concrete in replacements.items():
                        old = refined
                        refined = re.sub(rf'\b{artsy}\b', concrete, refined, flags=re.I)
                        if old != refined:
                            fixes.append(FixApplied(
                                fix_type="artsy_language_replacement",
                                original=artsy,
                                fixed_to=concrete,
                                reason="Replace abstract with concrete terms to prevent artifacts",
                                confidence=0.90
                            ))

        return refined, fixes

    def recommend_generation_mode(self, scores: ValidationScores, prompt_type: str, genre_config: Dict) -> str:
        """Recommend optimal generation mode"""

        if prompt_type == "veo_3.1":
            if scores.overall_quality_score < 0.75:
                return "veo_standard"
            else:
                return genre_config.get("veo_preferred_mode", "standard")

        elif prompt_type == "runway_gen4":
            if scores.overall_quality_score < 0.75:
                return "runway_standard"
            else:
                return genre_config.get("runway_preferred_mode", "standard")

        return "standard"

    def generate_recommendations(self, issues: List[Issue], scores: ValidationScores) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        for issue in issues:
            if issue.severity == "critical":
                recommendations.append(f"⚠️ CRITICAL: {issue.message}")
            elif issue.severity == "warning":
                recommendations.append(f"⚠️ {issue.suggestion}")

        if scores.consistency < 0.7:
            recommendations.append("Consider adding reference images for character consistency")

        if scores.overall_quality_score < 0.8:
            recommendations.append("Option: Refine prompt through interactive feedback loop")

        return recommendations

# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE CLOUD FUNCTION ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def validate_prompt(request):
    """Cloud Function entry point for HTTP trigger"""
    import flask

    # Parse request
    request_json = request.get_json(silent=True)

    if not request_json or 'prompt' not in request_json or 'prompt_type' not in request_json:
        return flask.jsonify({
            "error": "Missing required fields: 'prompt' and 'prompt_type'"
        }), 400

    # Initialize agent
    agent = Agent8PromptRefiner("config_agent8.json")

    # Validate and refine
    report = agent.validate_and_refine(
        prompt=request_json['prompt'],
        prompt_type=request_json['prompt_type'],
        genre=request_json.get('genre')
    )

    # Return JSON response
    return flask.Response(
        report.to_json(),
        mimetype='application/json',
        status=200
    )

# ─────────────────────────────────────────────────────────────────────────────
# LOCAL TESTING & USAGE EXAMPLE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize Agent 8
    agent = Agent8PromptRefiner("config_agent8.json")

    # Example VEO 3.1 prompt
    veo_prompt = """
    [IDENTITY]
    Woman, 30s, dark hair, warm expression

    [CINEMATOGRAPHY]
    Dolly-in over 6 seconds, eye-level camera

    [ENVIRONMENT]
    Modern apartment, golden hour, warm amber palette

    [PERFORMANCE]
    Woman walks to window, pauses, smiles

    [AUDIO]
    Dialogue: "I have been thinking about this for a very long time"
    Ambience: Subtle wind outside

    [NEGATIVES]
    No watermark, no floating limbs
    """

    # Validate and refine
    print("=" * 80)
    print("AGENT 8: PROMPT REFINER & VALIDATOR - TEST RUN")
    print("=" * 80)

    report = agent.validate_and_refine(veo_prompt, "veo_3.1", "reggaeton")

    # Output JSON report
    print(report.to_json())

    # Check readiness
    print("\n" + "=" * 80)
    if report.ready_for_generation:
        print(f"✓ Ready for generation in {report.generation_mode_recommendation}")
        print(f"Quality Score: {report.validation_scores.overall_quality_score:.2f}")
        print(f"Estimated Rating: {report.estimated_quality_rating:.1f}/5.0 stars")
    else:
        print(f"✗ Not ready - Score: {report.validation_scores.overall_quality_score:.2f}")
        print("\nRecommendations:")
        for rec in report.recommendations:
            print(f"  - {rec}")
    print("=" * 80)
