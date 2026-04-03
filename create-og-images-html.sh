#!/bin/bash

# Create OG images directory
mkdir -p ai-automation-blog/blog/images

# Generate 3 OG images using HTML + wkhtmltoimage (or convert from HTML)

echo "Creating HTML templates for OG images..."

# Image 1: ChatGPT Prompts
cat > /tmp/og-1.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 1200px;
            height: 630px;
            background: linear-gradient(135deg, #0A0A0B 0%, #1A1A1C 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        .logo {
            position: absolute;
            top: 40px;
            left: 60px;
            color: #B9FF66;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .title {
            color: #FFFFFF;
            font-size: 72px;
            font-weight: 800;
            text-align: center;
            line-height: 1.1;
            max-width: 1000px;
            margin-bottom: 30px;
        }
        .subtitle {
            color: #B9FF66;
            font-size: 32px;
            font-weight: 600;
            text-align: center;
        }
        .accent {
            color: #B9FF66;
        }
    </style>
</head>
<body>
    <div class="logo">workless.build</div>
    <div class="title">
        The <span class="accent">51 ChatGPT Prompts</span><br>
        That Save Solopreneurs<br>
        15 Hours Every Week
    </div>
    <div class="subtitle">Copy-paste ready • Save $800/month</div>
</body>
</html>
EOF

# Image 2: Email Automation
cat > /tmp/og-2.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 1200px;
            height: 630px;
            background: linear-gradient(135deg, #0A0A0B 0%, #1A1A1C 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        .logo {
            position: absolute;
            top: 40px;
            left: 60px;
            color: #B9FF66;
            font-size: 24px;
            font-weight: 700;
        }
        .title {
            color: #FFFFFF;
            font-size: 68px;
            font-weight: 800;
            text-align: center;
            line-height: 1.1;
            max-width: 1000px;
            margin-bottom: 30px;
        }
        .subtitle {
            color: #B9FF66;
            font-size: 30px;
            font-weight: 600;
            text-align: center;
        }
        .accent {
            color: #B9FF66;
        }
    </style>
</head>
<body>
    <div class="logo">workless.build</div>
    <div class="title">
        How to <span class="accent">Automate Email</span><br>
        Follow-Ups Without<br>
        Expensive CRM
    </div>
    <div class="subtitle">Free tools • 7-step tutorial • Save $200/month</div>
</body>
</html>
EOF

# Image 3: Tech Stack
cat > /tmp/og-3.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 1200px;
            height: 630px;
            background: linear-gradient(135deg, #0A0A0B 0%, #1A1A1C 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        .logo {
            position: absolute;
            top: 40px;
            left: 60px;
            color: #B9FF66;
            font-size: 24px;
            font-weight: 700;
        }
        .title {
            color: #FFFFFF;
            font-size: 68px;
            font-weight: 800;
            text-align: center;
            line-height: 1.1;
            max-width: 1000px;
            margin-bottom: 30px;
        }
        .subtitle {
            color: #B9FF66;
            font-size: 30px;
            font-weight: 600;
            text-align: center;
        }
        .accent {
            color: #B9FF66;
        }
        .price {
            color: #B9FF66;
            font-size: 80px;
            font-weight: 800;
        }
    </style>
</head>
<body>
    <div class="logo">workless.build</div>
    <div class="title">
        My <span class="price">$50/Month</span><br>
        Tech Stack That Replaces<br>
        Your <span class="accent">$500 SaaS Bill</span>
    </div>
    <div class="subtitle">Save $5,208/year • Complete comparison</div>
</body>
</html>
EOF

echo "✅ HTML templates created"
echo ""
echo "Converting to PNG using headless Chrome..."
echo ""

# Check if wkhtmltoimage or chromium is available
if command -v wkhtmltoimage &> /dev/null; then
    wkhtmltoimage --width 1200 --height 630 /tmp/og-1.html ai-automation-blog/blog/images/og-chatgpt-prompts.png
    wkhtmltoimage --width 1200 --height 630 /tmp/og-2.html ai-automation-blog/blog/images/og-email-automation.png
    wkhtmltoimage --width 1200 --height 630 /tmp/og-3.html ai-automation-blog/blog/images/og-tech-stack.png
elif command -v chromium &> /dev/null; then
    chromium --headless --screenshot=/tmp/og-1.png --window-size=1200,630 /tmp/og-1.html
    chromium --headless --screenshot=/tmp/og-2.png --window-size=1200,630 /tmp/og-2.html
    chromium --headless --screenshot=/tmp/og-3.png --window-size=1200,630 /tmp/og-3.html
    mv /tmp/og-*.png ai-automation-blog/blog/images/
elif command -v google-chrome &> /dev/null; then
    google-chrome --headless --screenshot=/tmp/og-1.png --window-size=1200,630 /tmp/og-1.html
    google-chrome --headless --screenshot=/tmp/og-2.png --window-size=1200,630 /tmp/og-2.html
    google-chrome --headless --screenshot=/tmp/og-3.png --window-size=1200,630 /tmp/og-3.html
    mv /tmp/og-*.png ai-automation-blog/blog/images/
else
    echo "❌ No screenshot tool found (wkhtmltoimage, chromium, chrome)"
    echo ""
    echo "💡 Alternative: Use online tool to convert HTML → PNG:"
    echo "   1. Copy HTML content from /tmp/og-*.html"
    echo "   2. Use: https://html2canvas.hertzen.com/ or similar"
    echo "   3. Save as 1200x630px PNG"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ OG IMAGES CREATED"
echo "════════════════════════════════════════════════════════"
ls -lh ai-automation-blog/blog/images/og-*.png 2>/dev/null
