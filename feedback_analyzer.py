import json
import csv
import re
import os

# Beginner friendly ticket analyzer proof of concept
# Using standard Python libraries without heavy external dependencies

def check_if_ticket_qualifies(ticket_text):
    # Convert text to lower case for simple matching
    clean_text = ticket_text.lower().strip()

    # Rule 1: Check if message is empty or too short
    word_list = clean_text.split()
    total_words = len(word_list)
    if total_words <= 1:
        return False, "Single-word greeting or too short"

    # Rule 2: Check if text is just a polite fluff message without any actual request
    polite_fluff_phrases = [
        "hope you are having a nice day",
        "hope you have a great day",
        "have a nice day",
        "just saying hi",
        "hey there",
        "good morning team"
    ]
    
    for phrase in polite_fluff_phrases:
        if phrase in clean_text:
            # Check if there is any actual issue or feature mentioned
            action_keywords = ["issue", "bug", "crash", "error", "broken", "help", "feature", "add", "bill", "refund", "invoice"]
            found_action = False
            for act in action_keywords:
                if act in clean_text:
                    found_action = True
                    break
            if found_action == False:
                return False, "Non-actionable polite greeting"

    # Rule 3: Check for promotional spam messages
    spam_keywords = [
        "win big",
        "cash prize",
        "claim your reward",
        "buy 1 get 1",
        "promotional discount",
        "http://spam",
        "free prize"
    ]
    for spam in spam_keywords:
        if spam in clean_text:
            return False, "Promotional broadcast or spam"

    # If it passes all rules, ticket is valid
    return True, "Valid"


def find_ticket_catagory(ticket_text):
    clean_text = ticket_text.lower()

    # Check for bug reports first
    bug_keywords = [
        "crash", "crashes", "crashed", "error", "broken", "freeze", "freezing",
        "glitch", "bug", "not working", "unresponsive", "failed", "vulnerability",
        "code 500", "flaw", "downtime"
    ]
    for word in bug_keywords:
        if word in clean_text:
            return "Bug Report"

    # Check for billing issues
    billing_keywords = [
        "charged", "charge", "billing", "invoice", "payment", "refund",
        "credit card", "subscription", "declined", "receipt", "overcharged",
        "cancel my subscription"
    ]
    for word in billing_keywords:
        if word in clean_text:
            return "Billing Issue"

    # Check for feature requests (using regex word boundaries to avoid partial word matches like address)
    feature_patterns = [
        r"\badd\b", r"\bfeature\b", r"\bdark mode\b", r"\bwould be awesome\b",
        r"\bintegration\b", r"\boption to\b", r"\bsupport for\b",
        r"\bmulti-language\b", r"\bwould love\b", r"\bcan we please\b"
    ]
    for pat in feature_patterns:
        if re.search(pat, clean_text):
            return "Feature Request"

    # Check for general inquiries
    inquiry_keywords = [
        "how do i", "how can i", "where can i", "is there", "question",
        "documentation", "api documentation", "inquiry"
    ]
    for phrase in inquiry_keywords:
        if phrase in clean_text:
            return "General Inquiry"

    # Default category if none matched
    return "General Feedback"


def find_ticket_prioity(ticket_text, catagory):
    clean_text = ticket_text.lower()

    # High urgency keywords
    urgent_keywords = [
        "asap", "urgent", "immediately", "emergency", "critical",
        "cannot access", "crashes", "crash", "vulnerability", "downtime"
    ]
    for word in urgent_keywords:
        if word in clean_text:
            return "Urgent"

    # High priority keywords
    high_keywords = [
        "broken", "freeze", "freezing", "charged twice", "declined",
        "unresponsive", "failed", "cancel", "error", "code 500"
    ]
    for word in high_keywords:
        if word in clean_text:
            return "High"

    # Medium priority keywords or categories
    if catagory == "Feature Request":
        return "Medium"
    
    if catagory == "Billing Issue":
        return "Medium"

    medium_keywords = ["option to", "integration", "update", "invoice", "report"]
    for word in medium_keywords:
        if word in clean_text:
            return "Medium"

    # Default low priority
    return "Low"


def find_ticket_sentimant(ticket_text):
    clean_text = ticket_text.lower()

    # Negative words list
    negative_words = [
        "crash", "crashes", "crashed", "broken", "freeze", "freezing",
        "error", "unresponsive", "failed", "asap", "angry", "annoyed",
        "worst", "terrible", "vulnerability", "flaw", "downtime", "declined"
    ]
    for word in negative_words:
        if word in clean_text:
            return "Negative"

    # Positive words list
    positive_words = [
        "awesome", "great", "love", "super fast", "amazing",
        "thank you", "thanks", "excellent", "wonderful", "good", "helpful"
    ]
    for word in positive_words:
        if word in clean_text:
            return "Positive"

    # Default neutral sentiment
    return "Neutral"


def extract_prodcut_name(ticket_text):
    # Using regex search patterns to detect specific features or products
    patterns = [
        (r"\b(checkout|payment page)\b", "Checkout / Payment Page"),
        (r"\b(dark mode)\b", "Dark Mode"),
        (r"\b(mobile app|ios|android)\b", "Mobile App"),
        (r"\b(login|sign in|safari)\b", "Login / Authentication"),
        (r"\b(search bar|search)\b", "Search Bar"),
        (r"\b(export|excel|csv|analytics reports)\b", "Analytics / Export"),
        (r"\b(database sync|database)\b", "Database System"),
        (r"\b(user settings|profile|profile picture|email address)\b", "User Profile / Settings"),
        (r"\b(subscription|invoice|credit card|billing)\b", "Billing & Subscription"),
        (r"\b(api documentation|api|webhook|webhooks)\b", "API & Webhooks"),
        (r"\b(password reset|password)\b", "Password Security"),
        (r"\b(multi-language|french|spanish)\b", "Multi-Language Support"),
        (r"\b(slack|discord)\b", "Third-Party Integrations")
    ]

    for regex_pattern, feature_label in patterns:
        match = re.search(regex_pattern, ticket_text, re.IGNORECASE)
        if match:
            return feature_label

    return "General Platform"


def make_auto_responce(catagory, prioity, prodcut_name, sentimant):
    # Create simple, polite AI suggested auto reply based on category
    if catagory == "Bug Report":
        return f"Hello! We apologize for the issue you experienced with {prodcut_name}. Our technical team has been notified with {prioity} priority and is actively investigating it. Thank you for reporting this."
    
    elif catagory == "Feature Request":
        return f"Hi there! Thank you for reaching out and suggesting an improvement for {prodcut_name}. We have logged your request with our product team for review in our roadmap."
    
    elif catagory == "Billing Issue":
        return f"Hello! Thank you for contacting our support team regarding {prodcut_name}. Our billing department has received your request and is reviewing your account to resolve this promptly."
    
    elif catagory == "General Inquiry":
        return f"Hello! Thank you for contacting customer support. We are happy to assist you with {prodcut_name}. A representative will follow up with detailed instructions shortly."
    
    else:
        if sentimant == "Positive":
            return f"Hello! Thank you so much for your kind words and feedback regarding {prodcut_name}. We truly appreciate your support!"
        else:
            return f"Hello! Thank you for sharing your feedback with us. We value your input and our team will review it carefully."


def run_analyzer():
    # File paths
    input_filepah = "customer_tickets_data.json"
    output_filepah = "analyzed_customer_tickets.csv"

    print("=========================================================")
    print("AI Customer Feedback & Support Ticket Analyzer PoC")
    print("=========================================================")

    # Check if input file exists
    if not os.path.exists(input_filepah):
        print(f"Error: Input file '{input_filepah}' was not found in directory!")
        return

    # Load JSON customer tickets
    try:
        with open(input_filepah, "r", encoding="utf-8") as f:
            custumer_tickets = json.load(f)
        print(f"Loaded {len(custumer_tickets)} customer tickets successfully.\n")
    except Exception as error_msg:
        print("Failed to read input JSON file:", error_msg)
        return

    processed_results = []
    qualified_count = 0
    ignored_count = 0

    # Process each ticket one by one
    for ticket in custumer_tickets:
        ticket_id = ticket.get("ticket_id", "N/A")
        custumer_name = ticket.get("customer_name", "Anonymous")
        message_body = ticket.get("message", "")

        is_qualifying, filter_reason = check_if_ticket_qualifies(message_body)

        if is_qualifying:
            qualified_count = qualified_count + 1

            # Extract features and structured parameters
            catagory = find_ticket_catagory(message_body)
            prioity = find_ticket_prioity(message_body, catagory)
            sentimant = find_ticket_sentimant(message_body)
            prodcut_name = extract_prodcut_name(message_body)
            auto_responce = make_auto_responce(catagory, prioity, prodcut_name, sentimant)

            result_row = {
                "ticket_id": ticket_id,
                "customer_name": custumer_name,
                "message": message_body,
                "status": "QUALIFIED",
                "rejection_reason": "None",
                "category": catagory,
                "priority": prioity,
                "sentiment": sentimant,
                "product_feature": prodcut_name,
                "suggested_reply": auto_responce
            }
            processed_results.append(result_row)

            print(f"[PROCESSED] {ticket_id} | Category: {catagory} | Priority: {prioity} | Sentiment: {sentimant} | Feature: {prodcut_name}")
        else:
            ignored_count = ignored_count + 1

            result_row = {
                "ticket_id": ticket_id,
                "customer_name": custumer_name,
                "message": message_body,
                "status": "NON-QUALIFYING",
                "rejection_reason": filter_reason,
                "category": "N/A",
                "priority": "N/A",
                "sentiment": "N/A",
                "product_feature": "N/A",
                "suggested_reply": "N/A"
            }
            processed_results.append(result_row)

            print(f"[IGNORED]   {ticket_id} | Reason: {filter_reason}")

    # Write structured output to CSV file
    try:
        fieldnames = [
            "ticket_id",
            "customer_name",
            "message",
            "status",
            "rejection_reason",
            "category",
            "priority",
            "sentiment",
            "product_feature",
            "suggested_reply"
        ]
        with open(output_filepah, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in processed_results:
                writer.writerow(row)

        print("\n=========================================================")
        print(f"Summary: {qualified_count} tickets qualified, {ignored_count} tickets ignored.")
        print(f"Results successfully saved to CSV file: {output_filepah}")
        print("=========================================================")

    except Exception as error_msg:
        print("Error saving results to CSV:", error_msg)


if __name__ == "__main__":
    run_analyzer()
