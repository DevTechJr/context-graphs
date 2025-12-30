"""
Visual Logging Utilities

Provides colored, structured terminal output for tracing decision flows.
Shows exactly what's happening at each step with visual indicators.
"""

from typing import List, Dict, Any
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    GRAY = '\033[90m'


def print_header(text: str):
    """Print a major section header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.END}\n")


def print_subheader(text: str):
    """Print a subsection header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─' * 80}{Colors.END}")


def print_step(step_num: int, total_steps: int, description: str):
    """Print a step in the process."""
    progress = f"[{step_num}/{total_steps}]"
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{progress} {description}{Colors.END}")


def print_success(text: str, indent: int = 2):
    """Print a success message."""
    prefix = " " * indent
    print(f"{prefix}{Colors.GREEN}✓{Colors.END} {text}")


def print_info(text: str, indent: int = 2):
    """Print an info message."""
    prefix = " " * indent
    print(f"{prefix}{Colors.CYAN}ℹ{Colors.END} {text}")


def print_warning(text: str, indent: int = 2):
    """Print a warning message."""
    prefix = " " * indent
    print(f"{prefix}{Colors.YELLOW}⚠{Colors.END} {text}")


def print_error(text: str, indent: int = 2):
    """Print an error message."""
    prefix = " " * indent
    print(f"{prefix}{Colors.RED}✗{Colors.END} {text}")


def print_metric(label: str, value: Any, indent: int = 2):
    """Print a labeled metric."""
    prefix = " " * indent
    print(f"{prefix}{Colors.GRAY}{label}:{Colors.END} {Colors.BOLD}{value}{Colors.END}")


def print_separator(char: str = "─", length: int = 80):
    """Print a separator line."""
    print(f"{Colors.GRAY}{char * length}{Colors.END}")


def print_policies(policies: List[Dict[str, Any]], max_display: int = 5):
    """Print formatted policy list."""
    total = len(policies)
    display = policies[:max_display]
    
    for i, policy in enumerate(display, 1):
        name = policy.get('name', 'Unknown Policy')
        severity = policy.get('severity', 'N/A')
        
        # Color-code by severity
        if severity == 'strict':
            severity_color = Colors.RED
        elif severity == 'moderate':
            severity_color = Colors.YELLOW
        else:
            severity_color = Colors.GREEN
        
        print(f"    {Colors.GRAY}{i}.{Colors.END} {name}")
        print(f"       {Colors.GRAY}Severity:{Colors.END} {severity_color}{severity}{Colors.END}")
        
        if policy.get('description'):
            desc = policy['description'][:80] + "..." if len(policy.get('description', '')) > 80 else policy.get('description')
            print(f"       {Colors.GRAY}{desc}{Colors.END}")
    
    if total > max_display:
        print(f"    {Colors.GRAY}... and {total - max_display} more{Colors.END}")


def print_precedents(precedents: List[Dict[str, Any]], max_display: int = 3):
    """Print formatted precedent list."""
    total = len(precedents)
    display = precedents[:max_display]
    
    for i, prec in enumerate(display, 1):
        decision = prec["decision"]
        similarity = prec["similarity"]
        
        # Color-code by similarity
        if similarity > 0.8:
            sim_color = Colors.GREEN
        elif similarity > 0.6:
            sim_color = Colors.YELLOW
        else:
            sim_color = Colors.GRAY
        
        print(f"    {Colors.GRAY}{i}.{Colors.END} {sim_color}Similarity: {similarity:.3f}{Colors.END}")
        print(f"       {Colors.GRAY}ID:{Colors.END} {decision.get('id')}")
        
        prompt = decision.get('prompt', 'N/A')
        if len(prompt) > 60:
            prompt = prompt[:60] + "..."
        print(f"       {Colors.GRAY}Prompt:{Colors.END} {prompt}")
        print(f"       {Colors.GRAY}Response:{Colors.END} {decision.get('response', 'N/A')}")
    
    if total > max_display:
        print(f"    {Colors.GRAY}... and {total - max_display} more{Colors.END}")


def print_decision_box(decision: str, confidence: float, reasoning: str):
    """Print the final decision in a highlighted box."""
    print(f"\n{Colors.BOLD}{'┌' + '─' * 78 + '┐'}{Colors.END}")
    print(f"{Colors.BOLD}│{Colors.END} {Colors.BOLD}{Colors.GREEN}DECISION{Colors.END}".ljust(90) + f"{Colors.BOLD}│{Colors.END}")
    print(f"{Colors.BOLD}├{'─' * 78}┤{Colors.END}")
    
    # Color-code decision
    if decision in ["APPROVE", "APPROVED"]:
        dec_color = Colors.GREEN
    elif decision in ["DENY", "DENIED"]:
        dec_color = Colors.RED
    else:
        dec_color = Colors.YELLOW
    
    print(f"{Colors.BOLD}│{Colors.END}   {Colors.GRAY}Result:{Colors.END} {dec_color}{Colors.BOLD}{decision}{Colors.END}".ljust(90) + f"{Colors.BOLD}│{Colors.END}")
    
    # Color-code confidence
    if confidence > 0.8:
        conf_color = Colors.GREEN
    elif confidence > 0.5:
        conf_color = Colors.YELLOW
    else:
        conf_color = Colors.RED
    
    print(f"{Colors.BOLD}│{Colors.END}   {Colors.GRAY}Confidence:{Colors.END} {conf_color}{confidence:.2f}{Colors.END}".ljust(90) + f"{Colors.BOLD}│{Colors.END}")
    print(f"{Colors.BOLD}├{'─' * 78}┤{Colors.END}")
    
    # Wrap reasoning
    max_width = 74
    words = reasoning.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    
    print(f"{Colors.BOLD}│{Colors.END}   {Colors.GRAY}Reasoning:{Colors.END}".ljust(90) + f"{Colors.BOLD}│{Colors.END}")
    for line in lines[:5]:  # Max 5 lines
        print(f"{Colors.BOLD}│{Colors.END}   {line}".ljust(86) + f"{Colors.BOLD}│{Colors.END}")
    
    print(f"{Colors.BOLD}└{'─' * 78}┘{Colors.END}\n")


def print_trace_summary(
    decision_id: str,
    policies_count: int,
    precedents_count: int,
    used_precedents: bool,
    timestamp: str = None
):
    """Print a summary of the decision trace."""
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{Colors.GRAY}{'─' * 80}{Colors.END}")
    print(f"{Colors.BOLD}Decision Trace Summary{Colors.END}")
    print(f"{Colors.GRAY}{'─' * 80}{Colors.END}")
    print(f"  {Colors.GRAY}ID:{Colors.END} {decision_id}")
    print(f"  {Colors.GRAY}Timestamp:{Colors.END} {timestamp}")
    print(f"  {Colors.GRAY}Policies Considered:{Colors.END} {policies_count}")
    print(f"  {Colors.GRAY}Precedents Found:{Colors.END} {precedents_count}")
    
    prec_indicator = f"{Colors.GREEN}Yes{Colors.END}" if used_precedents else f"{Colors.GRAY}No{Colors.END}"
    print(f"  {Colors.GRAY}Used Precedents:{Colors.END} {prec_indicator}")
    print(f"{Colors.GRAY}{'─' * 80}{Colors.END}\n")
