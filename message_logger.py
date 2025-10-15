import os
import json
from datetime import datetime
from typing import Any, Dict, List
import logging

class SQLMessageLogger:
    def __init__(self, log_dir: str = "logs/sql_agent"):
        # Disable all logging - no files will be created
        self.log_dir = None
        self.log_file = None
        self.conversation = []
        self.llm_call_count = 0
        self.tool_call_count = 0
        self.logger = logging.getLogger(__name__)
    
    def log_llm_interaction(self, input_messages: List[Dict], output: str) -> None:
        """Log an LLM interaction with input and output."""
        self.llm_call_count += 1
        self.logger.debug(f"LLM Call #{self.llm_call_count}")
        
        message = {
            "role": "system",
            "content": [
                {
                    "type": "llm_interaction",
                    "id": f"llm_call_{self.llm_call_count}",
                    "input_messages": input_messages,
                    "output": output,
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        self.conversation.append(message)
        self._write_to_file()
    
    def log_user_message(self, text: str) -> None:
        """Log a user message."""
        self.logger.debug(f"User Message: {text[:100]}...")
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }
        self.conversation.append(message)
        self._write_to_file()

    def log_assistant_message(self, text: str = None, tool_use: Dict = None) -> None:
        """Log an assistant message with optional tool use."""
        content = []
        
        if text:
            self.logger.debug(f"Assistant Message: {text[:100]}...")
            content.append({
                "type": "text",
                "text": text
            })
            
        if tool_use:
            self.tool_call_count += 1
            self.logger.debug(f"Tool Call #{self.tool_call_count}: {tool_use.get('name', 'unknown')}")
            content.append({
                "type": "tool_use",
                "id": tool_use.get("id", f"tool_call_{self.tool_call_count}"),
                "name": tool_use.get("name", ""),
                "input": tool_use.get("input", {}),
                "timestamp": datetime.now().isoformat()
            })
            
        message = {
            "role": "assistant",
            "content": content
        }
        self.conversation.append(message)
        self._write_to_file()

    def log_tool_result(self, tool_use_id: str, result: str) -> None:
        """Log a tool result."""
        self.logger.debug(f"Tool Result for {tool_use_id}: {result[:100]}...")
        message = {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": result,
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        self.conversation.append(message)
        self._write_to_file()
    
    def _write_to_file(self) -> None:
        """Write conversation to the log file."""
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "conversation": self.conversation,
                "statistics": {
                    "llm_calls": self.llm_call_count,
                    "tool_calls": self.tool_call_count
                }
            }
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error writing to log file: {e}")

    def get_conversation(self) -> List[Dict[str, Any]]:
        """Retrieve the entire conversation."""
        return self.conversation
        
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about LLM and tool usage."""
        return {
            "llm_calls": self.llm_call_count,
            "tool_calls": self.tool_call_count
        } 