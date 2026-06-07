"""
question_bank_generator.py — Generate layered question bank per JD + archetype.

Usage:
  python3 question_bank_generator.py --archetype ai_enterprise_pm
  python3 question_bank_generator.py --archetype founding_pm --jd-text '<JD text>' --stage startup
  python3 question_bank_generator.py --archetype growth_pm --format json
"""

import argparse
import json
import re

UNIVERSAL_QUESTIONS = [
    {"q": "Tell me about yourself.", "story_type": None, "layer": 1},
    {"q": "Why this company? Why this role?", "story_type": None, "layer": 1},
    {"q": "Tell me about your biggest product failure and what you learned.", "story_type": "failure_learning", "layer": 1},
    {"q": "How do you prioritize competing requests when everything feels urgent?", "story_type": "vision_prioritization", "layer": 1},
    {"q": "Tell me about a time an engineer pushed back on your spec. How did you handle it?", "story_type": "stakeholder_conflict", "layer": 1},
    {"q": "Walk me through a data-driven decision you made. What data, what choice, what outcome?", "story_type": "data_driven_decision", "layer": 1},
    {"q": "How do you know when a product is successful?", "story_type": None, "layer": 1},
    {"q": "Tell me about a time you led a cross-functional initiative without formal authority.", "story_type": "cross_functional_leadership", "layer": 1},
    {"q": "What's the biggest cross-functional challenge you've faced and how did you navigate it?", "story_type": "stakeholder_conflict", "layer": 1},
    {"q": "Where do you see yourself in 3 years?", "story_type": None, "layer": 1},
    {"q": "Tell me about a time user insight fundamentally changed your direction.", "story_type": "customer_obsession", "layer": 1},
    {"q": "Walk me through a complex system or problem you had to reason through from scratch.", "story_type": "systems_thinking", "layer": 1},
]

ARCHETYPE_QUESTIONS = {
    "ai_enterprise_pm": [
        {"q": "How do you decide when to use AI vs traditional software for a product problem?", "story_type": "data_driven_decision"},
        {"q": "Tell me about a time you had to build trust in an AI-powered feature with skeptical users.", "story_type": "customer_obsession"},
        {"q": "How do you evaluate a model for production use? What's your decision framework?", "story_type": "systems_thinking"},
        {"q": "Walk me through how you've designed prompts or AI workflows for a product.", "story_type": "systems_thinking"},
        {"q": "Tell me about navigating enterprise procurement or security review for an AI feature.", "story_type": "cross_functional_leadership"},
    ],
    "founding_pm": [
        {"q": "Tell me about building something from zero — no process, no team, no clear spec.", "story_type": "ambiguity_handling"},
        {"q": "When have you had to pivot? How did you know it was time?", "story_type": "vision_prioritization"},
        {"q": "How do you prioritize when you have no data, no users, and no money?", "story_type": "vision_prioritization"},
        {"q": "Tell me about a bet you made that didn't pay off. What would you do differently?", "story_type": "failure_learning"},
        {"q": "What's the hardest call you've made with incomplete information?", "story_type": "ambiguity_handling"},
    ],
    "growth_pm": [
        {"q": "Walk me through designing an A/B test end-to-end — hypothesis to decision.", "story_type": "data_driven_decision"},
        {"q": "Tell me about a growth experiment that surprised you — result went opposite to your hypothesis.", "story_type": "failure_learning"},
        {"q": "How do you resolve a conflict between short-term growth metrics and long-term retention?", "story_type": "vision_prioritization"},
        {"q": "Describe a growth loop you designed or optimized. What was the lever?", "story_type": "systems_thinking"},
        {"q": "How do you attribute results when multiple channels are running simultaneously?", "story_type": "data_driven_decision"},
    ],
    "analytics_pm": [
        {"q": "Walk me through how you'd define the North Star metric for a new product.", "story_type": "data_driven_decision"},
        {"q": "Tell me about a time you had conflicting data signals. How did you decide what to trust?", "story_type": "data_driven_decision"},
        {"q": "Describe a dashboard or reporting system you built or designed. What drove the design?", "story_type": "systems_thinking"},
        {"q": "How do you communicate data insights to non-technical stakeholders who are skeptical?", "story_type": "cross_functional_leadership"},
    ],
    "csm_implementation": [
        {"q": "Tell me about onboarding a complex enterprise client. What made it hard?", "story_type": "cross_functional_leadership"},
        {"q": "Walk me through how you've managed scope creep on an implementation project.", "story_type": "stakeholder_conflict"},
        {"q": "Tell me about a customer escalation. How did you handle it?", "story_type": "stakeholder_conflict"},
        {"q": "How do you manage timelines when the customer's team is slow to deliver their part?", "story_type": "ambiguity_handling"},
        {"q": "Tell me about driving product adoption post-implementation. What worked, what didn't?", "story_type": "customer_obsession"},
    ],
    "consumer_pm": [
        {"q": "Walk me through a user research study you designed and what you did with the findings.", "story_type": "customer_obsession"},
        {"q": "Tell me about a decision where user feedback contradicted your intuition. Who won?", "story_type": "customer_obsession"},
        {"q": "Describe a retention problem you diagnosed and solved.", "story_type": "data_driven_decision"},
        {"q": "How do you design for habit formation? Walk me through an example.", "story_type": "systems_thinking"},
    ],
    "general_pm": [
        {"q": "Tell me about a time you had to push back on a request from leadership.", "story_type": "stakeholder_conflict"},
        {"q": "How do you decide what to cut from a roadmap when something urgent comes up?", "story_type": "vision_prioritization"},
    ],
}

STAGE_QUESTIONS = {
    "startup": [
        {"q": "How do you build conviction on a priority when you have no data?", "story_type": "ambiguity_handling"},
        {"q": "Tell me about a time you shipped fast and had to fix things after. Was it the right call?", "story_type": "execution"},
        {"q": "How do you work when the process is undefined and the team is small?", "story_type": "ambiguity_handling"},
    ],
    "enterprise": [
        {"q": "How do you drive change in a complex org with many stakeholders?", "story_type": "cross_functional_leadership"},
        {"q": "Tell me about managing stakeholder politics when two powerful teams wanted opposite things.", "story_type": "stakeholder_conflict"},
        {"q": "How do you get executive sponsorship for a product bet?", "story_type": "cross_functional_leadership"},
    ],
}


def extract_jd_questions(jd_text: str) -> list[dict]:
    """Generate likely behavioral questions from JD keyword patterns."""
    questions = []
    jd_lower = jd_text.lower()

    patterns = [
        (r"lead(?:ing)?\s+(?:across\s+)?\d+\+?\s+teams?", "Tell me about a time you aligned multiple teams on a shared priority with no formal authority.", "cross_functional_leadership"),
        (r"ambigu(?:ity|ous)", "Tell me about a time you had to define scope from scratch with no clear direction.", "ambiguity_handling"),
        (r"0[\s-]to[\s-]1|zero\s+to\s+one|from\s+scratch|greenfield", "Walk me through building something completely new. What was hardest?", "ambiguity_handling"),
        (r"data[\s-]driven|data[\s-]informed|analytics", "Tell me about a decision you made purely based on data. What data, what decision, what outcome?", "data_driven_decision"),
        (r"stakeholder|alignment|executive\s+(?:buy[\s-]in|sponsor)", "How do you get executive alignment on a product bet they're initially skeptical of?", "stakeholder_conflict"),
        (r"launch|ship|go[\s-]to[\s-]market|gtm", "Tell me about a product launch you owned. What did you control, what went wrong, what'd you fix?", "cross_functional_leadership"),
        (r"ai|ml|machine\s+learning|llm|generative", "How do you evaluate whether to use AI vs traditional software for a user problem?", "systems_thinking"),
        (r"customer\s+success|implementation|onboard", "Walk me through onboarding a complex customer. What made it hard?", "cross_functional_leadership"),
        (r"growth|retention|acquisition|conversion", "Tell me about a growth initiative you owned — hypothesis, experiment, result.", "data_driven_decision"),
        (r"fail(?:ure|ed)|pivot|didn.t\s+work|miss(?:ed)?", "Tell me about a product that didn't land. What happened and what did you learn?", "failure_learning"),
    ]

    seen = set()
    for pattern, question, story_type in patterns:
        if re.search(pattern, jd_lower) and question not in seen:
            questions.append({"q": question, "story_type": story_type, "layer": 3, "jd_derived": True})
            seen.add(question)

    return questions


def generate_bank(archetype: str, jd_text: str = "", stage: str = "") -> list[dict]:
    bank = []

    for q in UNIVERSAL_QUESTIONS:
        bank.append({**q, "layer": 1})

    for q in ARCHETYPE_QUESTIONS.get(archetype, []):
        bank.append({**q, "layer": 2})

    if jd_text:
        for q in extract_jd_questions(jd_text):
            bank.append(q)

    if stage in STAGE_QUESTIONS:
        for q in STAGE_QUESTIONS[stage]:
            bank.append({**q, "layer": 4})

    # Deduplicate by question text
    seen = set()
    deduped = []
    for item in bank:
        if item["q"] not in seen:
            seen.add(item["q"])
            deduped.append(item)

    return deduped


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--archetype", required=True)
    p.add_argument("--jd-text", default="")
    p.add_argument("--stage", default="", choices=["", "startup", "enterprise"])
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    bank = generate_bank(args.archetype, args.jd_text, args.stage)

    if args.format == "json":
        print(json.dumps(bank, indent=2))
        return

    layer_labels = {1: "UNIVERSAL PM", 2: f"ARCHETYPE: {args.archetype.upper()}", 3: "JD-DERIVED", 4: f"STAGE: {args.stage.upper()}"}
    current_layer = None

    print(f"\nQUESTION BANK — {args.archetype}  ({len(bank)} questions)\n")
    for item in bank:
        if item["layer"] != current_layer:
            current_layer = item["layer"]
            print(f"\n--- {layer_labels.get(current_layer, f'LAYER {current_layer}')} ---")
        story_hint = f"  [→ {item['story_type']}]" if item.get("story_type") else ""
        print(f"  • {item['q']}{story_hint}")


if __name__ == "__main__":
    main()
