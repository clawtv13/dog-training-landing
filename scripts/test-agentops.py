#!/usr/bin/env python3
"""
Test AgentOps integration - v4 API
"""
import os
import agentops
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Initialize AgentOps
api_key = os.getenv("AGENTOPS_API_KEY")
print(f"✅ AgentOps API Key loaded: {api_key[:8]}...")

# Init with @trace decorator approach (v4)
agentops.init(api_key=api_key, default_tags=["openclaw", "test"])

print("✅ AgentOps initialized")
print("\n📊 Check your dashboard: https://app.agentops.ai/")
print("\nAgentOps will now automatically track:")
print("  - LLM calls")
print("  - Agent actions")
print("  - Costs")
print("\nIntegrate into your scripts with @agentops.trace decorator")
