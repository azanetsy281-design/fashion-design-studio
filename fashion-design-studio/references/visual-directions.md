# Consistent garment previews

Use the user's requested visual style. For an unspecified style on an image-capable
host, prefer a realistic garment-only concept on a neutral background. For a vector
request, create an illustrated fashion flat instead.

## Image prompt contract

Describe these facts explicitly in one prompt:

1. The garment and intended wearer category, without unverified sizing claims.
2. One identical proposed garment shown from front and back, at the same scale.
3. Exact silhouette, neckline, sleeves, hem length and key details in both views.
4. Fabric appearance, base/accent colours, print scale and plausible drape.
5. Front/back-specific closures, seams and pockets.
6. A clean layout with unobstructed views, no unintended model, props, logos or text.

Example to adapt, not reuse unchanged:

> Create a realistic garment design concept of a relaxed sage cotton women's top.
> Show the same proposed top twice: front on the left, back on the right, equally
> sized on a warm neutral background. Use a soft square front neckline, a higher
> rounded back neckline, short sleeves, a straight regular-length hem and no
> pockets. Keep fabric colour, sleeve shape, proportions and finish consistent
> across both views. No model, accessories, branding, measurements or text.

Choose original details for the actual brief. When using a reference, state what
to retain and what to change, and provide the reference through the host's real
image-input mechanism. Do not invent a local reference path.

## Visual checks

Check shoulder/sleeve continuity, matching hem length, fabric and colour, plausible
openings, pocket location and counts, and compatible front/back views. Treat hidden
construction as a proposal, not recovered facts. Check that a request for a dress
did not become a top and that a modest neckline revision did not change the whole
garment.

For a revision, preserve the previous composition and unaffected details. Request
only the intended change. Do not keep regenerating after the result meets the brief.
