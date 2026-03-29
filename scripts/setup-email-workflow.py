#!/usr/bin/env python3
"""
Setup n8n Email Capture Workflow for CleverDogMethod
Creates complete workflow: Webhook → Google Sheets → Telegram
"""

import json
import sys

# n8n workflow definition
workflow = {
    "name": "CleverDog Email Capture",
    "active": True,
    "nodes": [
        {
            "parameters": {
                "httpMethod": "POST",
                "path": "cleverdogmethod-email",
                "responseMode": "onReceived",
                "responseData": "allEntries",
                "options": {}
            },
            "id": "webhook-node",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [240, 300]
        },
        {
            "parameters": {
                "values": {
                    "string": [
                        {
                            "name": "email",
                            "value": "={{ $json.body.email }}"
                        },
                        {
                            "name": "resource",
                            "value": "={{ $json.body.resource }}"
                        },
                        {
                            "name": "page",
                            "value": "={{ $json.body.page }}"
                        },
                        {
                            "name": "source",
                            "value": "={{ $json.body.source }}"
                        },
                        {
                            "name": "timestamp",
                            "value": "={{ $now.toISO() }}"
                        }
                    ]
                }
            },
            "id": "set-data",
            "name": "Format Data",
            "type": "n8n-nodes-base.set",
            "typeVersion": 1,
            "position": [460, 300]
        },
        {
            "parameters": {
                "operation": "appendOrUpdate",
                "documentId": "REPLACE_WITH_SHEET_ID",
                "sheetName": "Sheet1",
                "columnToMatchOn": "email",
                "valueToMatchOn": "={{ $json.email }}",
                "dataToSend": "autoMapInputData",
                "options": {}
            },
            "id": "sheets-node",
            "name": "Save to Google Sheets",
            "type": "n8n-nodes-base.googleSheets",
            "typeVersion": 4,
            "position": [680, 300],
            "credentials": {
                "googleSheetsOAuth2Api": {
                    "id": "REPLACE_WITH_CREDENTIALS_ID",
                    "name": "Google Sheets"
                }
            }
        },
        {
            "parameters": {
                "chatId": "8116230130",
                "text": "=🎉 New email signup!\n\n📧 {{ $json.email }}\n📁 Resource: {{ $json.resource }}\n📍 Page: {{ $json.page }}\n🕒 {{ $json.timestamp }}\n\nTotal captured: Check Google Sheets",
                "additionalFields": {}
            },
            "id": "telegram-node",
            "name": "Notify Telegram",
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1,
            "position": [900, 300],
            "credentials": {
                "telegramApi": {
                    "id": "REPLACE_WITH_TELEGRAM_CRED_ID",
                    "name": "Telegram"
                }
            }
        }
    ],
    "connections": {
        "Webhook": {
            "main": [
                [
                    {
                        "node": "Format Data",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Format Data": {
            "main": [
                [
                    {
                        "node": "Save to Google Sheets",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Save to Google Sheets": {
            "main": [
                [
                    {
                        "node": "Notify Telegram",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    },
    "settings": {
        "executionOrder": "v1"
    }
}

# Print workflow JSON
print(json.dumps(workflow, indent=2))
print("\n" + "="*60)
print("✅ Workflow definition created")
print("\nTO IMPORT INTO N8N:")
print("1. Open: https://writing-majority-drink-brad.trycloudflare.com")
print("2. Click: Workflows → Import from File")
print("3. Paste this JSON")
print("4. Configure credentials for:")
print("   - Google Sheets OAuth")
print("   - Telegram Bot (token: 8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU)")
print("5. Create Google Sheet: 'CleverDogMethod Emails'")
print("6. Activate workflow")
print("="*60)
