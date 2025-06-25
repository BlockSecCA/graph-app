# Node Importance Ranking Plugin

Rank and highlight nodes by importance using multiple criteria with rich color-coding and visual tiers.

## Overview

This plugin provides comprehensive node importance analysis with beautiful visual highlighting. Unlike simple centrality analysis, it focuses on **visual storytelling** through color schemes, tiers, and rich highlighting to make important nodes immediately apparent.

Perfect for:
- **Executive presentations** - Clear visual hierarchy
- **Network monitoring** - Quick identification of critical nodes  
- **Educational purposes** - Understanding network structure at a glance
- **Decision making** - Prioritizing nodes for attention/resources

## Ranking Methods

### Composite Score (Default)
Combines multiple centrality measures for balanced importance assessment:
- **30% Degree Centrality** (connections)
- **30% Betweenness Centrality** (bottlenecks)  
- **20% Closeness Centrality** (reach)
- **20% PageRank** (authority)

### Individual Measures
- **Degree:** Count of direct connections
- **Betweenness:** Control over information flow
- **Closeness:** Average distance to other nodes
- **PageRank:** Authority based on incoming connections
- **Clustering:** Local network density

## Visual Features

### Color Schemes

#### Heat (Default)
- **Red:** Highest importance (critical)
- **Orange:** High importance  
- **Yellow:** Moderate importance
- **Green:** Lower importance
- Perfect for highlighting critical nodes

#### Cool  
- **Dark Blue:** Highest importance
- **Light Blue:** High importance
- **Cyan:** Moderate importance  
- **Green:** Lower importance
- Calming, professional appearance

#### Traffic Light
- **Red:** Critical/urgent attention needed
- **Yellow:** Caution/moderate importance
- **Green:** Safe/stable nodes
- Intuitive for operational dashboards

#### Rainbow
- **Full spectrum** from red to violet
- Maximum visual distinction between tiers
- Great for presentations and education

#### Monochrome
- **Blue shades** only
- Professional, print-friendly
- Good for formal reports

### Importance Tiers
- **Tier 1:** Most critical nodes
- **Tier 2:** High importance  
- **Tier 3:** Moderate importance
- **Tier 4+:** Lower importance

Visual features:
- **Larger nodes** for higher tiers
- **Distinct colors** per tier
- **Optional score labels** on nodes

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Ranking Method** | How to calculate importance | Composite |
| **Importance Tiers** | Number of visual tiers (2-8) | 4 |
| **Top Percent to Highlight** | % of nodes to include in ranking | 50% |
| **Color Scheme** | Visual style for highlighting | Heat |
| **Show Importance Labels** | Display scores on nodes | True |
| **Size by Importance** | Scale node size by tier | True |

## Example Results

```json
{
  "importance_ranking": {
    "CEO": 0.847,
    "Manager": 0.623,
    "Lead Dev": 0.445,
    "Sales Rep": 0.234
  },
  "tier_summary": [
    {
      "tier": 1,
      "count": 2,
      "avg_score": 0.735,
      "color": "#d73027"
    },
    {
      "tier": 2, 
      "count": 3,
      "avg_score": 0.445,
      "color": "#f46d43"
    }
  ]
}
```

## Use Cases

### Organizational Analysis
- **Executive dashboards:** Visual hierarchy of key personnel
- **Succession planning:** Identify critical knowledge holders
- **Team restructuring:** Understand informal influence networks

### Network Operations
- **Infrastructure monitoring:** Critical server/router identification
- **Capacity planning:** Prioritize upgrades for important nodes
- **Incident response:** Focus on high-impact systems first

### Social Network Analysis  
- **Influencer identification:** Find key opinion leaders
- **Community management:** Identify important community members
- **Marketing targeting:** Prioritize outreach efforts

### Research & Education
- **Citation networks:** Important papers/authors
- **Collaboration networks:** Key researchers
- **Knowledge graphs:** Central concepts

### Business Intelligence
- **Supply chain:** Critical suppliers/distributors
- **Customer networks:** High-value customer identification
- **Process analysis:** Bottleneck identification

## Interpretation Guide

### Tier 1 (Highest Importance)
- **Red/Dark colors** in most schemes
- **Largest node sizes**
- **Critical for network function**
- **High priority for protection/attention**

### Tier 2-3 (Moderate-High Importance)  
- **Orange/Medium colors**
- **Medium node sizes**
- **Important but not critical**
- **Good candidates for development/monitoring**

### Tier 4+ (Lower Importance)
- **Yellow/Light colors or gray**
- **Smaller node sizes**  
- **Supporting roles**
- **Lower priority for immediate attention**

### Score Interpretation
- **>0.8:** Extremely important, single point of failure
- **0.5-0.8:** Very important, high impact  
- **0.2-0.5:** Moderately important, some impact
- **<0.2:** Lower importance, minimal individual impact

## Best Practices

### Choosing Ranking Methods
- **Composite:** Best for general analysis and presentations
- **Betweenness:** Focus on bottlenecks and control points
- **Degree:** Simple hub identification
- **PageRank:** Authority and influence (good for directed graphs)
- **Closeness:** Information spread and reach

### Visual Settings
- **Heat scheme:** Best for highlighting problems/critical nodes
- **Cool scheme:** Professional, calming for operational dashboards
- **Traffic light:** Intuitive for status/alert systems  
- **4 tiers:** Good balance between detail and simplicity
- **Show labels:** Great for analysis, disable for clean presentations

### Parameter Tuning
- **50% highlighting:** Shows clear importance hierarchy
- **25% highlighting:** Focus only on truly critical nodes
- **75% highlighting:** Include broader importance spectrum
- **More tiers (6-8):** Fine-grained importance levels
- **Fewer tiers (2-3):** Simple high/medium/low classification

## Tips

- **Start with composite scoring** for balanced results
- **Use heat colors** for immediate visual impact
- **Adjust tier count** based on network size (2-4 for small, 4-8 for large)
- **Enable size scaling** to reinforce visual hierarchy  
- **Show labels during analysis**, hide for final presentations
- **Try different methods** to validate important nodes
- **Consider domain context** when interpreting scores

## Technical Notes

- Handles both directed and undirected graphs
- Automatically normalizes scores across different centrality measures
- Falls back gracefully for disconnected graphs
- Supports weighted and unweighted networks
- Creates visually distinct colors even with many tiers
- Optimized for clear visual communication