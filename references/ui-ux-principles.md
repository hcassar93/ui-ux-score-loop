# UI/UX Principle Notes

Compact scoring guidance distilled from the user's UI/UX playbook. Use this file when scoring views and choosing improvements. Do not quote or load the source book; apply these ideas to the user's product context.

## Visual Hierarchy

Visual hierarchy is the ordering of attention. A strong view makes the most important information and action obvious first, then lets supporting details recede. Size, position, color, contrast, font weight, spacing, and imagery should all help the user understand what matters and what to do next. If everything is equally loud, the user has to decide the hierarchy for themselves.

Look for misplaced emphasis: primary and secondary actions styled the same, metadata louder than the value it describes, decorative images overpowering task content, or labels that dominate actual data. Improve by ranking the visible elements by user importance, then increasing emphasis only where it helps the next action or key understanding.

Useful fixes include making the primary action more visually distinct, demoting destructive or secondary actions, strengthening the main value or heading, and reducing the salience of repeated metadata. Prefer one clear focal path over several competing "important" elements.

## Proximity

Proximity tells users what belongs together. Related labels, fields, helper text, actions, and content should be close enough to read as a unit, while unrelated groups need enough space to feel separate. Good proximity reduces interpretation work because the layout itself explains relationships.

Look for labels floating between fields, helper text that could apply to multiple controls, buttons detached from the object they affect, or dense content where every gap feels the same. Improve by tightening related pairs, increasing gaps between groups, and using consistent spacing rules so relationships are predictable across the flow.

Useful fixes include moving helper text directly under the relevant input, placing row actions inside or beside the row they affect, grouping related filters with their results, and using larger section gaps than item gaps. Proximity should make the user's interpretation feel automatic.

## Clarity

Clarity is the user's ability to understand where they are, what each element means, and what to do next. A clear UI uses plain labels, readable text, familiar patterns, visible state, and enough context to prevent guessing. It should make sense to a human who cannot read logs, infer implementation, or patiently reverse-engineer the page.

Look for ambiguous copy, unexplained icons, hidden next steps, raw errors, misleading instructions, or screens that become understandable only after trial and error. Improve by making state and intent explicit, replacing technical language with user-facing language, labeling unfamiliar controls, and preserving enough context to support confident action.

Useful fixes include rewriting button labels as concrete actions, adding short helper text only where uncertainty appears, showing validation next to the field it concerns, and translating backend or provider errors into human recovery steps. Clarity should reduce "what just happened?" moments.

## Alignment

Alignment creates order. Text, controls, cards, images, and data should follow consistent axes so the screen feels intentional and easy to scan. Left alignment usually supports reading, right alignment helps compare numbers, and center alignment works best for short titles or focused moments rather than long text.

Look for drifting edges, inconsistent baselines, mixed alignment rules in similar components, or centered paragraphs that make reading harder. Improve with grids, repeated column rules, consistent control placement, and alignment choices that match the content type. The goal is a calm visual path, not mathematical neatness for its own sake.

Useful fixes include aligning repeated cards to shared edges, lining up form fields and labels consistently, right-aligning comparable numeric values, and avoiding mixed center/left alignment inside the same content group. Alignment should make scanning feel steady.

## Contrast

Contrast separates things so users can read, compare, and act. It can come from color, size, weight, outlines, borders, shadows, background treatment, or motion. Strong contrast helps important text, actions, states, and regions stand out while preserving accessibility.

Look for low-contrast text, disabled states that look enabled, active states that are too subtle, and important controls that blend into their surroundings. Also watch for excessive contrast that creates false hierarchy. Improve by strengthening readability, adding borders or outlines when colors are too close, and testing text over real/dynamic content rather than ideal samples.

Useful fixes include darkening body copy enough for comfortable reading, adding an outline to pale controls, increasing selected/active state contrast, and adding overlays behind text on images. Contrast should help the user notice meaning, not merely create visual punch.

## Simplicity

Simplicity means keeping the interface focused on what the user needs to accomplish now. A simple view removes irrelevant details, redundant controls, noisy imagery, and competing information so the task feels approachable. It lowers cognitive effort and makes the next step easier to find.

Look for information that is true but irrelevant to the current decision, repeated actions, overly detailed cards, and controls that exist because the system can expose them rather than because the user needs them now. Improve by removing, grouping, or demoting low-value elements while keeping context that supports trust, decision-making, and recovery.

Useful fixes include shortening secondary descriptions, hiding advanced options behind progressive disclosure, merging duplicate controls, and moving nonessential facts below the main task. Simplicity should make the screen easier to use without making it feel under-explained.

## Whitespace

Whitespace is the empty space that gives information room to breathe. It improves readability, focus, grouping, and perceived quality. It is not wasted space; it is one of the main ways the UI tells users what belongs together and what deserves attention.

Look for cramped sidebars, forms where labels and fields are hard to pair, cards with uneven padding, or interfaces that feel busy even with modest content. Improve by starting with more space than feels necessary, then tightening carefully. Use a spacing scale such as multiples of 4 or 8 so the rhythm feels intentional rather than random.

Useful fixes include increasing card padding, adding section breaks, separating groups more than items, and standardizing vertical rhythm between labels, fields, helper text, and actions. Whitespace should reveal structure while preserving enough density for the task.

## Layout

Layout is the structure that joins usability and visual presentation. A good layout reflects what matters to the user, puts information in the order a human needs it, and makes the intended path easy to follow. It should support the psychology of the task, not just arrange boxes neatly.

Look for layouts that put low-value details before decision-making content, force scanning in awkward directions, hide comparisons in lists, or make forms feel disconnected from the outcome they create. Improve by matching structure to intent: show visual products visually, make choices comparable, group form fields around the user's mental model, and place actions where the decision naturally happens.

Useful fixes include moving the most decision-relevant content higher, turning hard-to-compare options into cards or columns, placing CTAs after the information needed to choose, and structuring creation forms around the final object. Layout should mirror the user's thinking sequence.

## Balance And Harmony

Balance and harmony describe how the whole screen feels when all elements work together. A balanced UI gives every element appropriate prominence without letting one image, button, color, or panel overpower the rest. The result should feel coherent, calm, and easy to understand as a whole.

Look for one oversized element stealing attention, a palette dominated by one loud color, mismatched component sizes, or sections that feel unrelated despite being on the same page. Improve by tuning proportion, scale, color distribution, spacing, and typographic relationships. Add less; rebalance what already exists first.

Useful fixes include reducing an image or CTA that overwhelms the rest, varying a one-note palette with neutrals, normalizing component sizes, and checking whether each region feels like part of the same system. Harmony is often a matter of restraint.

## Consistency

Consistency lets users learn once and apply that knowledge everywhere. Buttons, inputs, cards, icons, states, spacing, typography, and interaction patterns should behave and look predictably across screens and repeated items. This reduces cognitive load and builds trust.

Look for mixed icon styles, inconsistent corner radii, uneven card heights, changing button colors, different labels for the same action, or repeated components with accidental visual differences. Improve by standardizing repeated patterns while allowing meaningful variation for content, state, or hierarchy. Different should mean different.

Useful fixes include reusing one button system, keeping input states consistent, normalizing repeated cards, choosing one icon family, and aligning component copy conventions. Consistency should help the user predict behavior before interacting.

## Visual Cues

Visual cues help users understand faster than text alone. Icons, images, avatars, logos, progress indicators, state markers, color chips, and thumbnails can clarify identity, status, affordance, direction, and grouping. Good cues reduce reading and make the interface more memorable.

Look for decorative icons that do not add comprehension, missing progress indicators, generic placeholders where identity matters, or cues whose style changes without meaning. Improve by using cues to answer practical questions: who is this, where am I, what changed, what can I click, what happens next, and how far through the flow am I?

Useful fixes include adding icons to clarify status, replacing generic initials with recognizable avatars/logos when identity matters, using progress indicators for multi-step flows, and showing clear selected/current states. Cues should speed recognition, not add ornament.

## Depth And Texture

Depth and texture create layers, affordance, and focus. Shadows, outlines, elevation, background shifts, blur, and subtle material effects can make floating elements, clickable regions, modals, dropdowns, and selected states easier to understand. Depth should clarify structure and interaction.

Look for flat interfaces where dropdowns blend into the page, floating controls vanish on complex backgrounds, harsh shadows that feel unpolished, or fashionable effects that hurt readability. Improve with a restrained elevation system: subtle depth for ordinary surfaces, stronger depth for overlays, and background-aware shadows or outlines when content sits over variable imagery.

Useful fixes include adding subtle elevation to popovers, giving modals clear separation, using tinted shadows on colored backgrounds, and replacing trendy translucent effects when they reduce legibility. Depth should explain layering and interaction priority.

## Color Theory

Color sets mood, expresses brand, and guides interaction. Strong color use is selective: primary colors highlight important actions or links, neutral backgrounds let content breathe, and status colors follow familiar conventions. Light and dark modes should each preserve readability, hierarchy, and brand feel.

Look for primary color used everywhere, too many competing colors, vibrant backgrounds fighting the content, status colors used unconventionally, or errors/success states communicated by color alone. Improve by reducing color noise, reserving saturated color for action or state, pairing color with text/icons/shape, and checking both light and dark modes with real content.

Useful fixes include moving brand color from decoration to key interactions, using neutral backgrounds for dense work surfaces, preserving red/green/yellow conventions for status, and adding labels or icons to state color. Color should guide behavior and emotion without carrying meaning alone.

## Typography

Typography carries both meaning and tone. A strong typographic system uses readable fonts, limited font families, clear heading/body relationships, comfortable line length, adequate line height, and suitable weights. It should make scanning and reading feel effortless.

Look for too many fonts, extra-light body text, tiny sizes, pure black or pure white text everywhere, low contrast, centered long paragraphs, oversized line lengths, dense paragraphs, or headings that do not stand apart. Improve with one versatile family or a disciplined pair, clear type scale, darker/stronger headings, readable body copy, short paragraphs, subheadings, and left alignment for longer text.

Useful fixes include limiting line length, increasing paragraph line height, breaking long text into scannable chunks, strengthening heading weight or size, and softening pure black/white text to more comfortable neutrals. Typography should make reading feel easy before it feels stylish.

## Interaction Cost

Interaction cost is the mental, physical, and time effort required to complete the goal. It includes reading, searching, scrolling, clicking, typing, waiting, remembering, correcting mistakes, and recovering from errors. A strong UI lets users recognize options, make decisions, act with few steps, and understand progress without uncertainty.

Look for hidden choices, distant related actions, small click targets, too many options, repeated inputs, unnecessary steps, silent loading, unclear recovery, or flows that require recall instead of recognition. Improve by keeping related actions close, exposing important options, chunking information, reducing distractions, streamlining steps, supporting autofill/defaults, and making progress and recovery visible.

Useful fixes include replacing hidden dropdown choices with visible swatches or segmented options when the set is small, moving the submit action near the final decision, adding loading/progress states, reducing required typing, and turning errors into clear next steps. Interaction cost includes every moment of effort.
