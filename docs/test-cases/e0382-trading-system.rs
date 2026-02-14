// E0382 test case: Trading system
// Used to test whether AI can perform meta-cognitive traceback

use std::time::SystemTime;

#[derive(Debug)]
struct TransactionRecord {
    id: String,
    amount: f64,  // Note: Financial systems should not use f64; simplified here for demonstration
    timestamp: SystemTime,
    from_account: String,
    to_account: String,
}

fn save_to_database(record: TransactionRecord) {
    println!("Saving to DB: {:?}", record);
}

fn send_notification(record: TransactionRecord) {
    println!("Sending notification for: {:?}", record);
}

fn write_audit_log(record: TransactionRecord) {
    println!("Audit log: {:?}", record);
}

fn process_transaction(record: TransactionRecord) {
    // Save to database
    save_to_database(record);

    // Send notification
    send_notification(record);  // E0382: use of moved value

    // Write audit log
    write_audit_log(record);    // E0382: use of moved value
}

fn main() {
    let tx = TransactionRecord {
        id: "TX-2024-001".to_string(),
        amount: 1000.50,
        timestamp: SystemTime::now(),
        from_account: "ACC-001".to_string(),
        to_account: "ACC-002".to_string(),
    };

    process_transaction(tx);
}
