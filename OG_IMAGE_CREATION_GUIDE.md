# Open Graph Image Creation Guide for Shorty

## Requirements

- **Resolution:** 1200x630 pixels (minimum: 600x315, recommended: 1200x630)
- **Format:** PNG (recommended), JPG, or WebP
- **File size:** Under 8MB (ideal: under 500KB)
- **Aspect ratio:** 1.91:1 (1200x630)
- **Location:** `/app/static/icons/og-image.png`

## Design Specifications

### Color Scheme (Based on Shorty's existing design)
- **Primary Blue:** `#2563eb` (Tailwind blue-600)
- **Primary Purple:** `#9333ea` (Tailwind purple-600)
- **Background:** White `#ffffff` or light gray gradient
- **Text:** Dark gray/black `#1f2937` for contrast

### Layout Structure

```
+--------------------------------------------------+
|                                                  |
|  [LOGO]   Shorty                              |
|              URL Shortener &                       |
|              QR Code Generator                      |
|                                                  |
|  [QR Code Icon]  [Link Icon]                    |
|                                                  |
|  Shorten URLs instantly                          |
|  Free • Fast • Secure                           |
|                                                  |
+--------------------------------------------------+
```

### Content Elements

1. **Logo/Brand** (Left side, 120x120px)
   - "Shorty" text in bold
   - Font: Inter, Roboto, or system-ui
   - Color: `#2563eb`

2. **Tagline** (Below logo)
   - "URL Shortener & QR Code Generator"
   - Font size: 32px
   - Color: `#6b7280` (gray-500)

3. **Visual Elements** (Center-right)
   - QR Code icon (100x100px)
   - Link/chain icon (100x100px)
   - Both in gradient blue-to-purple
   - Use SVG icons for crisp quality

4. **Features Badges** (Bottom)
   - "Free" • "Fast" • "Secure"
   - Pill-shaped badges
   - Background: Light gray `#f3f4f6`
   - Text: Dark gray `#4b5563`

### Typography

- **Primary Font:** Sans-serif (Inter, SF Pro, Segoe UI, system-ui)
- **Weight:** Bold (700) for "Shorty", Medium (500) for tagline
- **Colors:**
  - Brand name: `#2563eb`
  - Tagline: `#1f2937`
  - Features: `#4b5563`

### Accessibility

- **Color Contrast:** Minimum 4.5:1 ratio
- **Text Size:** Minimum 16px (use 32px for headline)
- **Clear Icons:** High contrast, no low-opacity overlays

## Tools to Create

### Option 1: Canva (Free)
1. Create new design: 1200x630
2. Use gradient background (light gray to white)
3. Add "Shorty" text (left-aligned, large)
4. Add tagline below
5. Add QR and link icons
6. Add feature badges at bottom
7. Download as PNG (600KB or less)

### Option 2: Figma (Free)
1. Create frame: 1200x630
2. Use gradients: Linear from `#f9fafb` to `#ffffff`
3. Add text layers
4. Add icon layers (SVG format)
5. Export: PNG @ 1x, quality 90%
6. Optimize: TinyPNG or Squoosh

### Option 3: HTML/CSS Preview (Quick Test)
Create a temporary file `og-preview.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #e5e7eb;
        }
        .og-preview {
            width: 1200px;
            height: 630px;
            background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 60px;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .brand {
            font-size: 72px;
            font-weight: 700;
            color: #2563eb;
            margin-bottom: 20px;
        }
        .tagline {
            font-size: 32px;
            font-weight: 500;
            color: #1f2937;
            margin-bottom: 60px;
        }
        .features {
            display: flex;
            gap: 40px;
        }
        .badge {
            background: #f3f4f6;
            color: #4b5563;
            padding: 12px 32px;
            border-radius: 50px;
            font-size: 24px;
            font-weight: 600;
        }
        .icons {
            display: flex;
            gap: 30px;
            margin-bottom: 60px;
        }
        .icon {
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #2563eb 0%, #9333ea 100%);
            border-radius: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .icon svg {
            width: 60px;
            height: 60px;
            fill: white;
        }
    </style>
</head>
<body>
    <div class="og-preview">
        <div class="brand">Shorty</div>
        <div class="tagline">URL Shortener & QR Code Generator</div>
        <div class="icons">
            <div class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M3 11h2v2H3v-2zm0 4h2v2H3v-2zm0-8h2v2H3V7zm0 4h2v2H3v-2zm12 0h2v2h-2v-2zm0 4h2v2h-2v-2zm0-8h2v2h-2V7zm0 4h2v2h-2v-2zm2-6h2v2h-2V5zm-2 4h2v2h-2v-2zm-2 4h2v2h-2v-2zm-2 4h2v2h-2v-2z"/>
                </svg>
            </div>
            <div class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M10 13a5 5 0 0 0 7.54 10.39l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A5 5 0 0 0 10 13zm0-2a3 3 0 0 1 4.52 6.23l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A3 3 0 0 1 10 11zm0-2a1 1 0 0 1 1.51.62l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A1 1 0 0 1 10 9zm0-2a1 1 0 0 1 1.51.62l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A1 1 0 0 1 10 7zm0-2a1 1 0 0 1 1.51.62l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A1 1 0 0 1 10 5zm0-2a1 1 0 0 1 1.51.62l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A1 1 0 0 1 10 3zm0-2a1 1 0 0 1 1.51.62l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A1 1 0 0 1 10 1zm0-2a1 1 0 0 1 1.51.62l-3.76 2.27a1 1 0 0 0 0 1.78l3.76-2.27A1 1 0 0 1 10 1zm10 18h2v2h-2v-2zm0 4h2v2h-2v-2zm0-8h2v2h-2V7zm0 4h2v2h-2v-2zm0 4h2v2h-2v-2zm2-6h2v2h-2V5zm-2 4h2v2h-2v-2zm-2 4h2v2h-2v-2zm-2 4h2v2h-2v-2z"/>
                </svg>
            </div>
        </div>
        <div class="features">
            <div class="badge">Free</div>
            <div class="badge">Fast</div>
            <div class="badge">Secure</div>
        </div>
    </div>
</body>
</html>
```

### Option 4: Use AI Image Generator

**Prompts for DALL-E, Midjourney, or Stable Diffusion:**

```
"Modern minimal app icon design for 'Shorty' URL shortener. 1200x630 pixels. Gradient light blue background. Large bold text 'Shorty' in blue. Subtitle 'URL Shortener & QR Code Generator'. Include QR code icon and link icon. Clean, professional, tech startup style. Blue and purple color scheme. High contrast, readable text."
```

## Optimization

After creating the image:

1. **Compress:**
   - TinyPNG: https://tinypng.com/
   - Squoosh: https://squoosh.app/

2. **Check size:**
   - Must be under 8MB
   - Ideal: under 500KB

3. **Validate:**
   - Test at: https://www.opengraph.xyz/
   - Upload image and check preview

4. **Save to:**
   - `/app/static/icons/og-image.png`
   - Or `/app/static/icons/og-image.jpg`

## Alternative: SVG Placeholder

If you need a quick placeholder, save this as `og-image.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f9fafb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ffffff;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg-grad)"/>
  <text x="60" y="200" font-family="system-ui, sans-serif" font-size="72" font-weight="700" fill="#2563eb">Shorty</text>
  <text x="60" y="270" font-family="system-ui, sans-serif" font-size="32" font-weight="500" fill="#1f2937">URL Shortener & QR Code Generator</text>
  <rect x="400" y="350" width="120" height="120" rx="20" fill="#2563eb"/>
  <rect x="550" y="350" width="120" height="120" rx="20" fill="#9333ea"/>
  <rect x="60" y="500" width="100" height="40" rx="20" fill="#f3f4f6"/>
  <text x="110" y="528" font-family="system-ui, sans-serif" font-size="20" font-weight="600" fill="#4b5563" text-anchor="middle">Free</text>
  <rect x="180" y="500" width="100" height="40" rx="20" fill="#f3f4f6"/>
  <text x="230" y="528" font-family="system-ui, sans-serif" font-size="20" font-weight="600" fill="#4b5563" text-anchor="middle">Fast</text>
  <rect x="300" y="500" width="100" height="40" rx="20" fill="#f3f4f6"/>
  <text x="350" y="528" font-family="system-ui, sans-serif" font-size="20" font-weight="600" fill="#4b5563" text-anchor="middle">Secure</text>
</svg>
```

**Note:** SVG is not ideal for OG images (many platforms prefer PNG/JPG), but works as a fallback.

## Final Checklist

- [ ] Resolution: 1200x630 pixels
- [ ] Format: PNG (preferred)
- [ ] File size: Under 500KB
- [ ] Brand name visible: "Shorty"
- [ ] Tagline included
- [ ] Color scheme: Blue/purple
- [ ] High contrast for accessibility
- [ ] Saved to: `/app/static/icons/og-image.png`
- [ ] Tested at https://www.opengraph.xyz/

## After Creating

1. Update `.env` file with correct URL:
   ```
   OG_IMAGE_URL=/static/icons/og-image.png
   ```

2. Restart the application

3. Test sharing on:
   - Facebook Debugger: https://developers.facebook.com/tools/debug/
   - Twitter Card Validator: https://cards-dev.twitter.com/validator
   - LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/

4. Verify cache clears (24 hours max)
