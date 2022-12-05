from slack_sdk.models.blocks import SectionBlock
from typing import List

from elementary.clients.slack.schema import SlackMessageSchema, SlackBlocksType


LONGEST_MARKDOWN_SUFFIX_LEN = 3
CONTINUATION_SYMBOL = "..."
MAX_SLACK_SECTION_SIZE = 2
SHOW_MORE_ATTACHMENTS_MARK = 5


class SlackMessageBuilder:
    def __init__(self) -> None:
        self.slack_message = self._initial_slack_message()

    @classmethod
    def _initial_slack_message(cls) -> dict:
        return {"blocks": [], "attachments": [{"blocks": []}]}

    def _add_blocks_to_blocks_section(self, blocks: SlackBlocksType):
        self.slack_message["blocks"].extend(blocks)

    def _add_blocks_to_attachments_sections(self, blocks: SlackBlocksType):
        self.slack_message["attachments"][0]["blocks"].extend(blocks)

    @staticmethod
    def _format_section_msg(section_msg: str) -> str:
        if len(section_msg) < SectionBlock.text_max_length:
            return section_msg
        return (
            section_msg[
                : SectionBlock.text_max_length
                - len(CONTINUATION_SYMBOL)
                - LONGEST_MARKDOWN_SUFFIX_LEN
            ]
            + CONTINUATION_SYMBOL
            + section_msg[-LONGEST_MARKDOWN_SUFFIX_LEN:]
        )

    @staticmethod
    def create_divider_block() -> dict:
        return {"type": "divider"}

    @staticmethod
    def create_fields_section_block(section_msgs: list) -> dict:
        fields = []
        for section_msg in section_msgs:
            fields.append(
                {
                    "type": "mrkdwn",
                    "text": SlackMessageBuilder._format_section_msg(section_msg),
                }
            )

        return {"type": "section", "fields": fields}

    @staticmethod
    def create_text_section_block(section_msg: str) -> dict:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": SlackMessageBuilder._format_section_msg(section_msg),
            },
        }

    @staticmethod
    def create_empty_section_block() -> dict:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": SlackMessageBuilder._format_section_msg("\t"),
            },
        }

    @staticmethod
    def create_context_block(context_msgs: list) -> dict:
        fields = []
        for context_msg in context_msgs:
            fields.append(
                {
                    "type": "mrkdwn",
                    "text": SlackMessageBuilder._format_section_msg(context_msg),
                }
            )

        return {"type": "context", "elements": fields}

    @staticmethod
    def create_header_block(msg: str) -> dict:
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": msg,
            },
        }

    @staticmethod
    def create_compacted_sections_blocks(section_msgs: list) -> List[dict]:
        # Compacting sections into attachments.
        # Each section can contian _MAX_SLACK_SECTION_SIZE fields.
        attachments = []
        section_fields = []

        for section_msg in section_msgs:
            section_field = {
                "type": "mrkdwn",
                "text": SlackMessageBuilder._format_section_msg(section_msg),
            }
            if len(section_fields) < MAX_SLACK_SECTION_SIZE:
                section_fields.append(section_field)
            else:
                attachment = {"type": "section", "fields": section_fields}
                attachments.append(attachment)
                section_fields = [section_field]

        attachment = {"type": "section", "fields": section_fields}
        attachments.append(attachment)
        return attachments

    @staticmethod
    def get_slack_status_icon(status: str) -> str:
        icon = ":small_red_triangle:"
        if status == "warn":
            icon = ":warning:"
        elif status == "error":
            icon = ":x:"
        return icon

    def get_slack_message(self) -> SlackMessageSchema:
        return SlackMessageSchema(**self.slack_message)
