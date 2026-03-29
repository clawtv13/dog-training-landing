# How to Regenerate Posts with Real Content

## Prerequisites

You need an OpenRouter API key to generate content with Claude.

### Get API Key

1. Go to https://openrouter.ai/
2. Sign up / log in
3. Go to Keys section
4. Create new key
5. Copy the key (starts with `sk-or-v1-...`)

### Set Environment Variable

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

Or add to your shell profile (`~/.bashrc` or `~/.zshrc`):
```bash
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Regenerate Existing Posts

### Option 1: Manual Regeneration

Delete the old posts first:
```bash
cd /root/.openclaw/workspace/ai-automation-blog
rm blog/posts/2026-03-29-*.html
```

Clear the published state so they regenerate:
```bash
echo '[]' > .state/published-posts.json
```

Run the script:
```bash
python3 scripts/blog-auto-post.py
```

This will:
1. Fetch the same HN items from database
2. Generate NEW content using the improved prompt
3. Add author cards and credibility signals
4. Create posts with real voice and examples

### Option 2: Test Single Post Generation

Want to test before regenerating everything?

```bash
cd /root/.openclaw/workspace/ai-automation-blog

# Modify script to only process 1 post
# Change: POSTS_PER_DAY = 1

python3 scripts/blog-auto-post.py
```

Compare the new post against `blog/posts/test-real-content.html` to verify quality.

## Verify Quality

After regeneration, check each post for:

- [ ] Author card is visible
- [ ] HN score shown in metadata
- [ ] First-person voice ("I tested", "I've seen")
- [ ] Specific examples with numbers/data
- [ ] 2-3 external links (tools, repos, papers)
- [ ] Natural tone (not marketing copy)
- [ ] "Sources & Related" section at end
- [ ] Personal opinion or experience included
- [ ] No "As a..." openings
- [ ] No generic buzzwords

## Example Output

Good post should look like `blog/posts/test-real-content.html`:
- Conversational opening
- Technical depth
- Personal experiments mentioned
- Real tools linked
- Admits limitations
- Sounds like a human wrote it

## Troubleshooting

**"No new content to publish"**
- Clear `.state/published-posts.json` first

**"API error: 401"**
- Check your OPENROUTER_API_KEY is set correctly
- Verify the key is valid on openrouter.ai

**"Generation failed"**
- Check you have credits on OpenRouter
- Claude Sonnet 4 costs ~$3 per million tokens
- Each post generation uses ~4-5k tokens (~$0.01-0.02)

**Posts still feel fake**
- Read the BEFORE-AFTER.md comparison
- Check if prompt was applied correctly
- Verify temperature is set to 0.8
- Make sure author data is being inserted

## Cost Estimate

**Per post:** ~$0.01-0.02
**Daily (2 posts):** ~$0.02-0.04  
**Monthly:** ~$0.60-1.20

Negligible cost for quality improvement.

## Next Steps After Regeneration

1. **Review posts manually** - read through, check quality
2. **Compare to test post** - should feel similar
3. **Update author bio** if needed (in script)
4. **Deploy to GitHub** - script does this automatically
5. **Share one post** - see if anyone notices it's better

---

**Status:** Script ready, just needs API key
**Script:** `/root/.openclaw/workspace/ai-automation-blog/scripts/blog-auto-post.py`
**Example:** `/root/.openclaw/workspace/ai-automation-blog/blog/posts/test-real-content.html`
