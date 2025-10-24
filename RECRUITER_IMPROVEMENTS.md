# Recruiter Bot Accuracy Improvements

## Overview

Made the recruiter bot significantly more realistic and less lenient to provide a more authentic negotiation experience.

## Key Changes Made

### 1. 🎯 Increased Negotiation Difficulty

**Before:**

- Tech Giants: Easy (0.3)
- Startups: Very Easy (0.2)
- Finance: Hard (0.7)
- Consulting: Medium-Hard (0.6)

**After:**

- Tech Giants: Medium-Hard (0.6) ⬆️
- Startups: Medium (0.4) ⬆️
- Finance: Very Hard (0.8) ⬆️
- Consulting: Hard (0.7) ⬆️
- Healthcare: Very Hard (0.9) ⬆️
- Automotive: Hard (0.7) ⬆️
- Retail: Extremely Hard (0.95) ⬆️
- Media: Medium-Hard (0.6) ⬆️

### 2. 💰 Much More Conservative Salary Progression

**Streamlit Version:**

- **Easy Companies**: 0 → 0 → 1K → 2K → 3K → 4K → 5K (max)
- **Medium Companies**: 0 → 0 → 0 → 1K → 1.5K → 2.5K → 3K (max)
- **Hard Companies**: 0 → 0 → 0 → 0 → 500 → 1K → 1.5K (max)

**Flask Version:**

- **Old**: 85K → 87K → 90K → 95K → 100K
- **New**: 85K → 85K → 85K → 87K → 90K → 92K → 95K

### 3. 🚫 More Resistant Response Patterns

**New Recruiter Responses:**

- "I understand your perspective, but $85,000 is our standard rate for this level. We have many qualified candidates interested in this position."
- "I appreciate your enthusiasm, but our budget is fixed for this role. We can offer additional benefits like flexible hours or professional development opportunities."
- "We value your skills, but we need to maintain consistency across our team. Perhaps we can discuss a performance review after 6 months?"
- "Thank you for your patience. After reviewing your case, we can offer $90,000 with the same benefits package. This is our final offer."

### 4. 🛡️ Added Resistance Mechanisms

**Dynamic Resistance Based on:**

- **Company Type**: Hard companies show more resistance
- **Negotiation Round**: Later rounds get more pushback
- **Difficulty Level**: Higher difficulty = more resistance

**Resistance Phrases Added:**

- "I need to be clear - this is pushing our budget limits."
- "We have very strict compensation guidelines we must follow."
- "I'm not sure we can justify this increase to leadership."
- "This is significantly above our typical range for this role."
- "We need to maintain equity across our team members."

### 5. 📊 Realistic Company Behavior

**Large Companies (Harder to Negotiate):**

- More rigid salary structures
- Stricter budget constraints
- Multiple approval layers
- Equity considerations across teams

**Small Companies (Easier to Negotiate):**

- More flexible decision-making
- Direct access to decision makers
- Faster approval processes
- More creative compensation options

### 6. 🎭 Enhanced Negotiation Psychology

**Progressive Stricter Evaluation:**

- **Round 1-2**: Moderately lenient for reasonable arguments
- **Round 3-4**: More strict, requires compelling evidence
- **Round 5+**: Very strict, only exceptional cases get improvements
- **Round 8+**: Often results in offer withdrawal

**Withdrawal Criteria:**

- Unprofessional language
- Demanding attitude
- Unrealistic demands
- Repeated pressure after "no"
- Threats or ultimatums

## Results

### Before (Too Lenient):

- Easy 10-15K salary increases
- Generous responses to basic requests
- Quick agreement to most demands
- Unrealistic negotiation outcomes

### After (More Realistic):

- Conservative 1-5K salary increases
- Firm resistance to unreasonable requests
- Professional but strict responses
- Realistic negotiation outcomes

## Testing

**Difficulty Distribution:**

- **Easy**: 12.5% (Startups only)
- **Medium**: 25% (Tech Giants, Media)
- **Hard**: 62.5% (Finance, Consulting, Healthcare, Automotive, Retail)

**Salary Progression Examples:**

- **Google Software Engineer**: $150K → $150K → $151K → $152K → $153K (max)
- **Goldman Sachs Data Scientist**: $200K → $200K → $200K → $200.5K → $201K (max)
- **Walmart Product Manager**: $80K → $80K → $80K → $80K → $80.5K (max)

## Impact

✅ **More Realistic Negotiations**: Recruiters now behave like real HR professionals
✅ **Challenging Experience**: Requires genuine negotiation skills to succeed
✅ **Educational Value**: Teaches realistic salary negotiation expectations
✅ **Company-Specific Behavior**: Different companies have different negotiation styles
✅ **Progressive Difficulty**: Gets harder as negotiations continue

The recruiter bot now provides a much more authentic and challenging negotiation experience that better reflects real-world salary discussions! 🎯
