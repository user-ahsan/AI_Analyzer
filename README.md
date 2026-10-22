# AI-Powered Customer Feedback & Support Ticket Analyzer (PoC)

A lightweight, automated Proof of Concept (PoC) system designed to process customer feedback and support tickets. The system filters out non-actionable noise, extracts structured parameters (intent, priority, sentiment, and product features) using rule-based AI pattern logic, generates tailored auto-replies, and exports structured results to a spreadsheet-ready CSV file.

---

## 1. Project Overview & Architecture

The analyzer processes incoming messages through four sequential stages:

1. **Data Ingestion**: Reads structured customer feedback and ticket messages from a local JSON dataset (`customer_tickets_data.json`).
2. **Filtering & Validation**: Evaluates each message against quality rules. Automatically ignores spam, single-word greetings (e.g., "hi", "hey"), and polite fluff without actionable requests.
3. **AI Feature Extraction**:
   - **Category / Intent**: Identifies `Bug Report`, `Feature Request`, `Billing Issue`, or `General Inquiry`.
   - **Priority Level**: Assesses urgency (`Urgent`, `High`, `Medium`, `Low`) based on critical operational keywords.
   - **Sentiment Analysis**: Evaluates customer emotion as `Positive`, `Neutral`, or `Negative`.
   - **Product / Feature Mention**: Uses regex pattern detection to extract mentioned components (e.g., `Checkout / Payment Page`, `Dark Mode`, `Mobile App`, `Database System`).
   - **Suggested Auto-Reply**: Dynamically drafts a polite, context-aware auto-response.
4. **Structured Storage & Output**: Exports all evaluated records with status and classification details to `analyzed_customer_tickets.csv`.

---

## 2. Project File Structure

```text
AI_Analyzer/
│
├── customer_tickets_data.json     # Mock input dataset containing 25 realistic support tickets
├── feedback_analyzer.py           # Main Python PoC script
├── analyzed_customer_tickets.csv  # Output CSV file containing structured results
├── README.md                      # Project documentation and setup guide
└── .gitignore                     # Git ignore file
```

---

## 3. Getting Started & Running the PoC

### Prerequisites
- Python 3.8 or newer installed on your machine.
- No external packages or pip installations required (built entirely using Python's standard library: `json`, `csv`, `re`, `os`).

### Step-by-Step Execution (VS Code)

1. **Open the project folder** in Visual Studio Code:
   ```text
   File -> Open Folder -> Select AI_Analyzer directory
   ```

2. **Open the Integrated Terminal** in VS Code:
   - Use shortcut: `` Ctrl + ` `` (Backtick) or go to `Terminal -> New Terminal`.

3. **Verify Python is installed**:
   ```powershell
   python --version
   ```

4. **Run the analyzer script**:
   ```powershell
   python feedback_analyzer.py
   ```
   *(On macOS / Linux, you can also run `python3 feedback_analyzer.py`)*

5. **Review the Output**:
   - Live terminal feedback displays each ticket being evaluated (`[PROCESSED]` vs `[IGNORED]`).
   - The final spreadsheet is saved to `analyzed_customer_tickets.csv` in the root workspace.

---

## 4. Test Scenarios & Verification

The included test dataset contains 25 realistic customer tickets, specifically validating the required benchmark scenarios:

| Ticket ID | Message Snippet | Expected Result | Actual System Output |
| :--- | :--- | :--- | :--- |
| **TCK-1001** | *"The payment page crashes every time I click 'Checkout' on Chrome..."* | Category: `Bug Report`<br>Priority: `Urgent`<br>Sentiment: `Negative` | **Category:** Bug Report<br>**Priority:** Urgent<br>**Sentiment:** Negative<br>**Feature:** Checkout / Payment Page |
| **TCK-1002** | *"Hi team, it would be awesome if you could add a dark mode to the mobile app."* | Category: `Feature Request`<br>Priority: `Medium`<br>Sentiment: `Positive` | **Category:** Feature Request<br>**Priority:** Medium<br>**Sentiment:** Positive<br>**Feature:** Dark Mode |
| **TCK-1003** | *"Hello, hope you are having a nice day!"* | Ignored / Non-Qualifying | **Status:** NON-QUALIFYING<br>**Reason:** Non-actionable polite greeting |

---

## 5. Sample Output Format (`analyzed_customer_tickets.csv`)

The exported CSV contains the following columns:

- `ticket_id`: Unique identifier for the support ticket.
- `customer_name`: Name of the sender.
- `message`: Original customer submission.
- `status`: Validation outcome (`QUALIFIED` or `NON-QUALIFYING`).
- `rejection_reason`: Explains why a non-qualifying ticket was filtered out (e.g., spam, single-word greeting).
- `category`: Detected customer intent (`Bug Report`, `Feature Request`, `Billing Issue`, etc.).
- `priority`: Urgency level (`Urgent`, `High`, `Medium`, `Low`).
- `sentiment`: Customer sentiment (`Positive`, `Neutral`, `Negative`).
- `product_feature`: Detected system component or feature.
- `suggested_reply`: Drafted customer auto-reply ready for dispatch.
