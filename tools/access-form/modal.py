modal = {
    "callback_id": "send_command",
    "title": {
        "type": "plain_text",
        "text": "Request for Access"
    },
    "submit": {
        "type": "plain_text",
        "text": "Request"
    },
    "type": "modal",
    "close": {
        "type": "plain_text",
        "text": "Cancel"
    },
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "The following form will request access to the specified resource."
			}
		},
		{
			"type": "divider"
		},
		{
			"block_id": "resource_block",
			"type": "input",
			"element": {
				"action_id": "resource",
				"type": "plain_text_input",
				"placeholder": {
					"type": "plain_text",
					"text": "Type a resource"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "To what resource do you need access?"
			}
		},
		{
			"block_id": "duration_block",
			"optional": True,
			"type": "input",
			"element": {
				"action_id": "duration",
				"type": "plain_text_input",
				"placeholder": {
					"type": "plain_text",
					"text": "Type a duration (e.g., 60m)"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "How long to do you need access?"
			}
		},
		{
			"block_id": "reason_block",
			"optional": True,
			"type": "input",
			"element": {
				"action_id": "reason",
				"type": "plain_text_input",
				"multiline": True,
				"placeholder": {
					"type": "plain_text",
					"text": "Type a reason"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Why do you need access?"
			}
		},
		{
			"block_id": "approver_block",
			"type": "input",
			"element": {
				"action_id": "approver",
				"type": "plain_text_input",
				"placeholder": {
					"type": "plain_text",
					"text": "Type a responsible (e.g., @username)"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Who should approve this request? (peer, engineering lead, manager)"
			}
		},
	]
}
