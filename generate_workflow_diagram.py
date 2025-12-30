"""
Generate a colorful Context Graph workflow diagram for the demo video.
Run this once: python generate_workflow_diagram.py
Output: workflow_diagram.png (for use in video)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#F5F5F5')  # Grey background

# Color palette - Black, White, Red scheme (Streamlit style)
color_input = '#EF553B'         # Red (Primary)
color_process = '#2C3E50'       # Dark grey/black
color_decision = '#2C3E50'      # Dark grey/black
color_database = '#EF553B'      # Red (Accent)
color_output = '#FFFFFF'        # White
color_flow = '#000000'          # Black

def draw_box(ax, x, y, width, height, text, color, fontsize=11, fontweight='normal', border_color='black'):
    """Draw a rounded rectangle box with text."""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.1", 
                          edgecolor=border_color, facecolor=color, linewidth=2.5, alpha=0.95)
    ax.add_patch(box)
    text_color = 'black' if color == '#FFFFFF' else 'white'
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, 
            fontweight=fontweight, color=text_color, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, label='', color='#34495E', width=2.5):
    """Draw an arrow with optional label."""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=30, 
                           linewidth=width, color=color, alpha=0.7)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 0.3, mid_y + 0.2, label, fontsize=9, 
                style='italic', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Title
ax.text(5, 9.5, 'Context Graph: System of Record for Decisions', 
        ha='center', fontsize=22, fontweight='bold')
ax.text(5, 9.1, 'How Tribal Knowledge Becomes Queryable Data', 
        ha='center', fontsize=14, style='italic', color='#555')

# --- LAYER 1: INPUT ---
draw_box(ax, 5, 8.2, 3, 0.6, 'REQUEST: "30% discount for Tier-1 customer"', color_input, fontsize=11, fontweight='bold')

# Arrows down
draw_arrow(ax, 5, 7.9, 5, 7.3, color=color_flow)

# --- LAYER 2: ORCHESTRATION LAYER (Parallel Processing) ---
draw_box(ax, 2, 6.5, 2.2, 0.8, 'Extract Intent\n(Tags, Categories)', color_process)
draw_box(ax, 5, 6.5, 2.2, 0.8, 'Query Policies\n(10% cap policy)', color_process)
draw_box(ax, 8, 6.5, 2.2, 0.8, 'Find Customer Data\n(ARR, Tickets)', color_process)

# Arrows from input to orchestration
draw_arrow(ax, 4, 7.9, 2.2, 6.9, color=color_flow)
draw_arrow(ax, 5, 7.9, 5, 6.9, color=color_flow)
draw_arrow(ax, 6, 7.9, 7.8, 6.9, color=color_flow)

# Arrows down from orchestration
draw_arrow(ax, 2, 6.1, 3.5, 5.4, color=color_flow)
draw_arrow(ax, 5, 6.1, 5, 5.4, color=color_flow)
draw_arrow(ax, 8, 6.1, 6.5, 5.4, color=color_flow)

# --- LAYER 3: CRITICAL STEP - NEO4J PRECEDENT SEARCH ---
draw_box(ax, 5, 4.8, 5, 1.1, 
         '🔍 PRECEDENT SEARCH IN NEO4J\n' +
         '6 months ago: VP approved 30% discount → Service outage → Customer retained\n' +
         'Similarity: 92% | Outcome: SUCCESS ✓',
         color_database, fontsize=10, fontweight='bold')

# Arrow down
draw_arrow(ax, 5, 4.25, 5, 3.6, label='With Context', color=color_flow)

# --- LAYER 4: LLM SYNTHESIS ---
draw_box(ax, 5, 3, 4.5, 1, 
         'LLM REASONING ENGINE\n' +
         'Policy vs. Precedent: "Rule says 10%, but precedent + context say approve"',
         color_decision, fontsize=10, fontweight='bold')

# Arrow down
draw_arrow(ax, 5, 2.5, 5, 1.9, color=color_flow)

# --- LAYER 5: OUTPUT + RECORDING (Sequential) ---
draw_box(ax, 3.5, 1.2, 2.2, 0.8, 
         'DECISION\nAPPROVE 30%\nConfidence: 89%',
         color_output, fontsize=11, fontweight='bold', border_color='#EF553B')

draw_box(ax, 6.5, 1.2, 2.2, 0.8, 
         'RECORD IN NEO4J\n(Permanent Trace)',
         color_database, fontsize=11, fontweight='bold')

# Arrows from LLM to outputs (sequential flow)
draw_arrow(ax, 5, 2.5, 3.5, 1.6, color=color_flow)
draw_arrow(ax, 4.6, 1.2, 5.4, 1.2, label='Then', color=color_flow)



# --- LEGEND ---
legend_y = 9.5
legend_x = 0.5
ax.text(legend_x, legend_y, '● Input Layer', fontsize=10, color='#EF553B', fontweight='bold')
ax.text(legend_x, legend_y - 0.35, '● Orchestration', fontsize=10, color='#2C3E50', fontweight='bold')
ax.text(legend_x, legend_y - 0.70, '● Neo4j (Context Graph)', fontsize=10, color='#EF553B', fontweight='bold')
ax.text(legend_x, legend_y - 1.05, '● LLM Decision', fontsize=10, color='#2C3E50', fontweight='bold')
ax.text(legend_x, legend_y - 1.40, '● Output (Traceable)', fontsize=10, color='#000000', fontweight='bold')

# Save
plt.tight_layout()
plt.savefig('workflow_diagram.png', dpi=300, bbox_inches='tight', facecolor='#F5F5F5', edgecolor='none')
print("✓ Workflow diagram saved as: workflow_diagram.png")
print("✓ Color scheme: Black, White, Red on Grey (Streamlit style)")
print("✓ Resolution: 300 DPI (perfect for video)")
print("✓ You can now use this in your demo video!")

plt.show()
