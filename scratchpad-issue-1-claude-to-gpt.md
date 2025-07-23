# Issue #1: Claude to GPT Conversion

**GitHub Issue**: https://github.com/tl375/testWebsite/issues/1
**Status**: In Progress
**Description**: Convert the chatbot to a GPT API chatbot

## Current Implementation Analysis

The current chatbot implementation uses:
- **Backend**: Anthropic's Claude API (claude-3-5-sonnet-20241022)
- **Library**: anthropic==0.40.0
- **API Key**: ANTHROPIC_API_KEY environment variable
- **Frontend**: Displays "CLAUDE" branding throughout UI
- **Error Handling**: Claude-specific error messages and handling

## Required Changes

### Phase 1: Backend Changes
1. **Dependencies (requirements.txt)**:
   - Remove: `anthropic==0.40.0`
   - Add: `openai` (latest version)

2. **API Integration (main/views.py)**:
   - Change import: `from anthropic import Anthropic` → `from openai import OpenAI`
   - Update client initialization: `Anthropic(api_key=api_key)` → `OpenAI(api_key=api_key)`
   - Change API call: `client.messages.create()` → `client.chat.completions.create()`
   - Update model: `claude-3-5-sonnet-20241022` → `gpt-3.5-turbo`
   - Update message format:
     ```python
     # Current Claude format
     messages=[{"role": "user", "content": f"System prompt\n\nUser: {user_message}"}]
     response_message = response.content[0].text.strip()
     
     # New OpenAI format  
     messages=[
         {"role": "system", "content": "System prompt"},
         {"role": "user", "content": user_message}
     ]
     response_message = response.choices[0].message.content.strip()
     ```

3. **Environment Variables**:
   - Change: `ANTHROPIC_API_KEY` → `OPENAI_API_KEY`
   - Optional: Add `GPT_MODEL` (default: "gpt-3.5-turbo")

4. **Error Handling**:
   - Remove Claude-specific error checks
   - Add OpenAI-specific error handling (InvalidAPIKey, RateLimitError, etc.)
   - Update error messages to reference OpenAI platform

### Phase 2: Frontend Changes

1. **JavaScript (main/static/main/js/script.js)**:
   - Change avatar text: `'CLAUDE'` → `'GPT'` or `'ChatGPT'`
   - Update console messages referencing Claude

2. **HTML Templates (main/templates/main/homepage.html)**:
   - Update page title: "Claude Chat" → "GPT Chat"
   - Change bot greeting: "Hello! I'm Claude..." → "Hello! I'm ChatGPT..."
   - Update footer: "Powered by Anthropic Claude" → "Powered by OpenAI"

### Phase 3: Documentation Updates

1. **README.md**:
   - Replace all "Claude" references with "GPT" or "ChatGPT"
   - Update API configuration section for OpenAI
   - Change setup instructions to reference OpenAI platform
   - Update links from Anthropic console to OpenAI platform

2. **CLAUDE.md** (if needed):
   - Consider if this file needs updating for the new implementation

### Phase 4: Testing & Validation

1. **Manual Testing with Puppeteer**:
   - Test chat interface functionality
   - Verify error handling with invalid API keys
   - Check UI branding updates
   - Test successful message exchanges

2. **Unit Tests** (Django tests, not rspec):
   - Write tests for `chat_api` view
   - Mock OpenAI API responses
   - Test error scenarios
   - Test message processing

3. **Full Test Suite**:
   - Run Django test suite
   - Fix any failing tests
   - Ensure all functionality works

## Implementation Steps

1. **Create new branch**: `feature/issue-1-claude-to-gpt`
2. **Backend changes**: Update dependencies and API integration
3. **Frontend changes**: Update UI branding and references
4. **Documentation**: Update README and other docs
5. **Testing**: Manual and automated testing
6. **PR Creation**: Open pull request for review

## Potential Considerations

- **Cost differences**: OpenAI pricing vs Claude pricing
- **Rate limiting**: Different behavior between providers
- **Model capabilities**: GPT-3.5-turbo vs Claude 3.5 Sonnet differences
- **Content policies**: OpenAI vs Anthropic content guidelines
- **Response times**: Performance differences between APIs

## Next Steps

1. Create the feature branch
2. Start with backend API integration changes
3. Test each component as it's implemented
4. Update frontend and documentation
5. Comprehensive testing before PR

---
*Created: 2025-07-23*
*Issue Link: https://github.com/tl375/testWebsite/issues/1*