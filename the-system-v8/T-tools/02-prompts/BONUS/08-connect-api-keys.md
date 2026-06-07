# Prompt: Connect API Keys & External Services

Use this to set up API keys and connect external services to your AI team.

Copy and paste this into your chat (fill in your service first):

---

```
I want to connect a new external service to my AI team. Here's what I need:

---
Service name: [e.g., "Google Gemini", "OpenAI DALL-E", "ElevenLabs", "Replicate"]
What it does: [e.g., "Generate images", "Text-to-speech", "Video generation"]
API key location: [Where did you get the key? e.g., "Google AI Studio", "OpenAI dashboard"]
---

Please help me:

1. First, explain what this service will allow my agents to do

2. Guide me through the setup process:
   - Where to add the API key in Claude Code settings
   - What MCP (Model Context Protocol) server I need to install (if any)
   - The exact commands to run in terminal

3. Create a test to verify the connection works

4. Update C-core/api-keys-registry.md:
   - Add an entry for this service
   - Document the service name, what it does, when it was connected
   - Note any usage limits or pricing info
   - Do NOT store the actual API key in this file (keep it in Claude Code settings only)

5. Update M-memory/learning-log.md:
   - Document what service was connected
   - Note the date and what capabilities it adds
   - Add any usage notes or limitations

6. If relevant, suggest which agents could use this new capability

Show me the step-by-step setup and confirm when it's working.
```

---

## Common API Services You Might Want to Connect

| Service | What It Does | Where to Get API Key |
|---------|--------------|---------------------|
| **Google Gemini** | Image generation, vision | [Google AI Studio](https://aistudio.google.com/) |
| **OpenAI** | DALL-E images, GPT models | [OpenAI Platform](https://platform.openai.com/) |
| **ElevenLabs** | Text-to-speech, voice cloning | [ElevenLabs](https://elevenlabs.io/) |
| **Replicate** | Various AI models | [Replicate](https://replicate.com/) |
| **Stability AI** | Stable Diffusion images | [Stability AI](https://stability.ai/) |
| **Perplexity** | Web search with AI | [Perplexity API](https://docs.perplexity.ai/) |

---

## Example: Connecting Google Gemini for Image Generation

```
I want to connect a new external service to my AI team. Here's what I need:

---
Service name: Google Gemini
What it does: Generate images from text prompts
API key location: Google AI Studio (https://aistudio.google.com/)
---

Please help me set this up...
```

---

## Security Tips

- **Never share your API keys** in public channels or files
- **Set spending limits** on your API accounts
- **Monitor usage** regularly to avoid surprise charges
- **Rotate keys** if you suspect they've been exposed

---

## After Connecting

Once connected, you can update your agents to use the new capability:

1. Add instructions to relevant agent files (e.g., update copywriter to request images)
2. Create a new skill file if the capability needs specific guidance
3. Document the workflow in M-memory for future reference

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
